from __future__ import annotations

import csv
import io
import random
import subprocess
import time
from pathlib import Path
from urllib.parse import quote_plus

import streamlit as st

from src.growth_ai_ops_prototype import OUTPUT_DIR, ROOT, run


LEADS_CSV = OUTPUT_DIR / "google_sheets_hr_leads.csv"
XLSX_FILE = OUTPUT_DIR / "konusarak-ogren-hr-outbound-google-sheets.xlsx"
UPLOADED_VERIFIED_CSV = ROOT / "data" / "uploaded_verified_leads.csv"

COL_COMPANY = "\u015eirket"
COL_TITLE = "\u00dcnvan"
COL_SECTOR = "Sekt\u00f6r"
COL_SIZE = "\u015eirket b\u00fcy\u00fckl\u00fc\u011f\u00fc"
COL_ENGLISH_NEED = "\u0130ngilizce ihtiyac\u0131 tahmini"

COLUMNS = [
    "Ad Soyad",
    COL_COMPANY,
    COL_TITLE,
    "LinkedIn URL",
    "Email",
    COL_SECTOR,
    COL_SIZE,
    "Pain point",
    COL_ENGLISH_NEED,
    "Outreach angle",
    "LinkedIn DM",
    "Cold email",
    "Lead score",
]

WORKFLOW_STEPS = [
    "LinkedIn Search / Platform Export",
    "CSV Upload",
    "Cleaning",
    "AI Enrichment",
    "Outreach Generation",
    "CRM Status",
]

SEARCH_QUERIES = [
    "HR Manager Turkey",
    "İnsan Kaynakları Müdürü Türkiye",
    "Talent Acquisition Turkey",
    "People & Culture Manager Türkiye",
    "Learning & Development Manager Turkey",
]

TEMPLATE_FIELDS = ["lead_id", "full_name", "company", "title", "linkedin_url", "email", "location", "source"]


st.set_page_config(page_title="Turkiye HR Lead Enrichment", layout="wide")


def read_rows() -> list[dict[str, str]]:
    if not LEADS_CSV.exists():
        return []
    with LEADS_CSV.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def clean_cell(value: object) -> str:
    if value is None:
        return "-"
    text = str(value).strip()
    return text if text else "-"


def display_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [{column: clean_cell(row.get(column)) for column in COLUMNS} for row in rows]


def rows_to_csv_bytes(rows: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8-sig")


def template_csv_bytes() -> bytes:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=TEMPLATE_FIELDS)
    writer.writeheader()
    writer.writerow(
        {
            "lead_id": "TR-HR-001",
            "full_name": "Gercek Kisi Adi",
            "company": "Sirket Adi",
            "title": "Talent Acquisition Manager",
            "linkedin_url": "https://www.linkedin.com/in/...",
            "email": "",
            "location": "Turkey",
            "source": "LinkedIn manual verification",
        }
    )
    return buffer.getvalue().encode("utf-8-sig")


def linkedin_people_search_url(query: str) -> str:
    return f"https://www.linkedin.com/search/results/people/?keywords={quote_plus(query)}"


def refresh_xlsx() -> None:
    builder = ROOT / "tools" / "build_google_sheets_workbook.mjs"
    if not builder.exists():
        return

    node_candidates = [
        Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe",
        Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node",
        Path("node"),
    ]
    for node_exe in node_candidates:
        try:
            subprocess.run(
                [str(node_exe), str(builder)],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
            return
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue


def normalize_csv_text(text: str, default_source: str) -> int:
    reader = csv.DictReader(io.StringIO(text))
    UPLOADED_VERIFIED_CSV.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with UPLOADED_VERIFIED_CSV.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=TEMPLATE_FIELDS)
        writer.writeheader()
        for index, row in enumerate(reader):
            full_name = row.get("Ad Soyad") or row.get("full_name") or row.get("name") or ""
            company = row.get(COL_COMPANY) or row.get("company") or row.get("Company") or ""
            title = row.get(COL_TITLE) or row.get("title") or row.get("Title") or ""
            if not (full_name.strip() and company.strip() and title.strip()):
                continue
            writer.writerow(
                {
                    "lead_id": row.get("lead_id") or f"UPLOAD-{count + 1:03d}",
                    "full_name": full_name.strip(),
                    "company": company.strip(),
                    "title": title.strip(),
                    "linkedin_url": (row.get("LinkedIn URL") or row.get("linkedin_url") or row.get("linkedin") or "").strip(),
                    "email": (row.get("Email") or row.get("email") or "").strip(),
                    "location": (row.get("location") or row.get("Location") or "Turkey").strip(),
                    "source": (row.get("source") or row.get("Source") or default_source).strip(),
                }
            )
            count += 1
    return count


def normalize_uploaded_csv(uploaded_file) -> int:
    text = uploaded_file.getvalue().decode("utf-8-sig")
    return normalize_csv_text(text, "Uploaded verified CSV")


def process_uploaded_csv(uploaded_file) -> list[dict[str, str]]:
    normalize_uploaded_csv(uploaded_file)
    run(UPLOADED_VERIFIED_CSV, 100)
    refresh_xlsx()
    return read_rows()


def process_pasted_csv(text: str) -> list[dict[str, str]]:
    normalize_csv_text(text, "Pasted verified CSV")
    run(UPLOADED_VERIFIED_CSV, 100)
    refresh_xlsx()
    return read_rows()


def generate_demo_leads(count: int, progress_slot, log_slot) -> list[dict[str, str]]:
    progress = progress_slot.progress(0)
    messages = [
        "Demo arama niyeti hazirlaniyor...",
        "Turkiye HR seed havuzu olusturuluyor...",
        "Cleaning ve duplicate kontrolu yapiliyor...",
        "Enrichment sinyalleri uretiliyor...",
        "Outreach mesajlari ve lead score hesaplaniyor...",
        "CSV/XLSX ciktilari guncelleniyor...",
    ]
    for index, message in enumerate(messages, start=1):
        log_slot.caption(message)
        progress.progress(index / (len(messages) + 1))
        time.sleep(0.08)
        if index == 3:
            run(None, count, seed=random.randint(1, 1_000_000), demo=True)
    refresh_xlsx()
    progress.progress(1.0)
    log_slot.caption("Tamamlandi. Demo tablo hazir.")
    return read_rows()


def score_summary(rows: list[dict[str, object]]) -> dict[str, float | int]:
    lead_scores = [int(row.get("Lead score") or 0) for row in rows]
    english_scores = [int(row.get(COL_ENGLISH_NEED) or 0) for row in rows]
    email_count = sum(1 for row in rows if row.get("Email"))
    linkedin_count = sum(1 for row in rows if row.get("LinkedIn URL"))
    return {
        "total": len(rows),
        "average_lead_score": round(sum(lead_scores) / len(lead_scores), 1) if lead_scores else 0,
        "priority_count": sum(1 for score in lead_scores if score >= 90),
        "email_count": email_count,
        "linkedin_count": linkedin_count,
        "average_english_need": round(sum(english_scores) / len(english_scores), 1) if english_scores else 0,
    }


def unique_values(rows: list[dict[str, object]], column: str) -> list[str]:
    return sorted({str(row.get(column, "")) for row in rows if row.get(column)})


def filter_rows(rows: list[dict[str, object]], sectors: list[str], sizes: list[str], min_score: int) -> list[dict[str, object]]:
    filtered = []
    for row in rows:
        score = int(row.get("Lead score") or 0)
        if sectors and row.get(COL_SECTOR) not in sectors:
            continue
        if sizes and row.get(COL_SIZE) not in sizes:
            continue
        if score < min_score:
            continue
        filtered.append(row)
    return filtered


if "rows" not in st.session_state:
    st.session_state.rows = []
if "data_mode" not in st.session_state:
    st.session_state.data_mode = "Gercek veri bekleniyor"

st.title("Türkiye HR Lead Enrichment")
st.caption(
    "LinkedIn/Sales Navigator, Apollo, Clay veya kariyer platformlarından alınan gerçek HR lead CSV'lerini enrich eden outreach prototipi."
)

with st.sidebar:
    st.header("Veri Kaynağı")
    st.markdown(
        """
        Ana akış gerçek/verifiye CSV içindir.

        Beklenen minimum kolonlar:
        `Ad Soyad`, `Şirket`, `Ünvan`, `LinkedIn URL`, `Email`
        """
    )
    st.subheader("LinkedIn kaynak asistanı")
    st.caption("Login arkasından scraping yapmaz; manuel doğrulanmış profil listesini hızlı hazırlatır.")
    for query in SEARCH_QUERIES:
        st.link_button(query, linkedin_people_search_url(query), use_container_width=True)
    st.download_button(
        "Verified CSV template indir",
        data=template_csv_bytes(),
        file_name="verified_leads_template.csv",
        mime="text/csv",
        use_container_width=True,
    )

    uploaded_file = st.file_uploader("Verified HR lead CSV yükle", type=["csv"])
    process_upload = st.button("CSV'yi Enrich Et", type="primary", use_container_width=True)
    pasted_csv = st.text_area(
        "CSV yapıştır",
        height=160,
        placeholder="lead_id,full_name,company,title,linkedin_url,email,location,source\nTR-HR-001,...",
    )
    process_paste = st.button("Yapıştırılan CSV'yi Enrich Et", use_container_width=True)

    st.divider()
    st.subheader("Demo fallback")
    lead_count = st.number_input("Demo lead sayısı", min_value=10, max_value=500, value=100, step=10)
    demo_clicked = st.button("Sadece Demo Seed Data Üret", use_container_width=True)

    st.divider()
    st.subheader("Filtreler")
    sector_filter = st.multiselect("Sektör", unique_values(st.session_state.rows, COL_SECTOR))
    size_filter = st.multiselect("Şirket büyüklüğü", unique_values(st.session_state.rows, COL_SIZE))
    min_score_filter = st.slider("Minimum lead score", min_value=0, max_value=100, value=0, step=5)

if process_upload:
    if uploaded_file is None:
        st.error("Önce LinkedIn/Sales Navigator/Apollo/Clay export CSV yüklemelisin.")
    else:
        with st.spinner("Gerçek lead CSV enrich ediliyor..."):
            st.session_state.rows = process_uploaded_csv(uploaded_file)
            st.session_state.data_mode = "Verified CSV"
        st.success(f"{len(st.session_state.rows)} gerçek/verifiye lead enrich edildi.")

if process_paste:
    if not pasted_csv.strip():
        st.error("Önce gerçek/verifiye lead satırlarını CSV formatında yapıştırmalısın.")
    else:
        with st.spinner("Yapıştırılan gerçek lead CSV enrich ediliyor..."):
            st.session_state.rows = process_pasted_csv(pasted_csv)
            st.session_state.data_mode = "Pasted verified CSV"
        if st.session_state.rows:
            st.success(f"{len(st.session_state.rows)} gerçek/verifiye lead enrich edildi.")
        else:
            st.error("CSV okundu ama valid satır bulunamadı. full_name, company ve title alanları dolu olmalı.")

if demo_clicked:
    progress_slot = st.empty()
    log_slot = st.empty()
    with st.spinner("Demo seed data üretiliyor..."):
        st.session_state.rows = generate_demo_leads(int(lead_count), progress_slot, log_slot)
        st.session_state.data_mode = "Demo seed data"
    st.warning("Bu tablo demo seed datadır; ana teslim için verified CSV kullanılmalıdır.")

rows = st.session_state.rows

if not rows:
    st.info(
        "Başlamak için sol menüden gerçek HR lead CSV yükle. Demo seed data yalnızca sistemi test etmek için kullanılmalıdır."
    )
    st.stop()

filtered_rows = filter_rows(rows, sector_filter, size_filter, min_score_filter)
summary = score_summary(rows)

if st.session_state.data_mode == "Demo seed data":
    st.warning("Şu an demo seed data görüntüleniyor. Gerçek teslim için verified CSV yükle.")
else:
    st.success("Verified CSV modu aktif. Email varsa korunur, yoksa boş bırakılır.")

metric_cols = st.columns(6)
metric_cols[0].metric("Toplam lead", summary["total"])
metric_cols[1].metric("LinkedIn URL", summary["linkedin_count"])
metric_cols[2].metric("Bulunan e-posta", summary["email_count"])
metric_cols[3].metric("Ort. İngilizce ihtiyacı", summary["average_english_need"])
metric_cols[4].metric("Ort. lead score", summary["average_lead_score"])
metric_cols[5].metric("Priority outreach", summary["priority_count"])

st.subheader("Workflow")
workflow_cols = st.columns(len(WORKFLOW_STEPS))
for column, label in zip(workflow_cols, WORKFLOW_STEPS):
    column.info(label)

st.subheader("HR Leads")
st.caption(f"{len(filtered_rows)} lead gösteriliyor. Email yoksa boş kalır; sistem random gerçek email uydurmaz.")
st.dataframe(display_rows(filtered_rows), use_container_width=True, height=520, column_order=COLUMNS)

st.subheader("Mesaj Önizleme")
if filtered_rows:
    lead_labels = [
        f"{row.get('Ad Soyad')} | {row.get(COL_COMPANY)} | {row.get(COL_TITLE)}"
        for row in filtered_rows
    ]
    selected_label = st.selectbox("Lead seç", lead_labels)
    selected = filtered_rows[lead_labels.index(selected_label)]

    preview_cols = st.columns(2)
    with preview_cols[0]:
        st.markdown("**LinkedIn DM**")
        st.info(clean_cell(selected.get("LinkedIn DM")))
    with preview_cols[1]:
        st.markdown("**Cold email**")
        st.text_area("Cold email preview", value=clean_cell(selected.get("Cold email")), height=220, label_visibility="collapsed")
else:
    st.warning("Filtrelere uyan lead bulunamadı.")

download_cols = st.columns(2)
download_cols[0].download_button(
    "Filtrelenen CSV indir",
    data=rows_to_csv_bytes(filtered_rows),
    file_name="filtered_google_sheets_hr_leads.csv",
    mime="text/csv",
    use_container_width=True,
)
download_cols[1].download_button(
    "Tüm CSV indir",
    data=rows_to_csv_bytes(rows),
    file_name="google_sheets_hr_leads.csv",
    mime="text/csv",
    use_container_width=True,
)

with st.expander("Kaynak ve güvenlik notu"):
    st.markdown(
        """
        - LinkedIn login arkasından otomatik scraping yapılmaz.
        - En sağlıklı kaynaklar: Sales Navigator export, Apollo, Clay, izinli recruitment database export veya manuel doğrulanmış CSV.
        - Email sadece kaynak CSV'de varsa korunur; yoksa boş bırakılır.
        - Kod içinde hardcoded API key yoktur. Production entegrasyonunda secret yönetimi `st.secrets` veya environment variable ile yapılmalıdır.
        - Uygulama SMTP/Gmail/SendGrid gönderimi yapmaz; cold email metnini preview olarak üretir.
        """
    )
