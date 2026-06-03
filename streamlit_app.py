from __future__ import annotations

import csv
import io
import random
import subprocess
import time
from pathlib import Path

import streamlit as st

from src.growth_ai_ops_prototype import OUTPUT_DIR, ROOT, run


LEADS_CSV = OUTPUT_DIR / "google_sheets_hr_leads.csv"
XLSX_FILE = OUTPUT_DIR / "konusarak-ogren-hr-outbound-google-sheets.xlsx"

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
    "LinkedIn Search",
    "Google Sheets",
    "Cleaning",
    "AI Enrichment",
    "Outreach Generation",
    "CRM Status",
]

DEMO_EMAIL_DOMAINS = {
    "Trendyol": "trendyol.example",
    "Getir": "getir.example",
    "Hepsiburada": "hepsiburada.example",
    "Yemeksepeti": "yemeksepeti.example",
    "Peak Games": "peakgames.example",
    "Dream Games": "dreamgames.example",
    "Turkcell": "turkcell.example",
    "Vodafone Turkey": "vodafone.example",
    "Garanti BBVA": "garantibbva.example",
    "Akbank": "akbank.example",
    "Yapi Kredi": "yapikredi.example",
    "Isbank": "isbank.example",
    "Ford Otosan": "fordotosan.example",
    "Tofas": "tofas.example",
    "Arcelik": "arcelik.example",
    "Vestel": "vestel.example",
    "LC Waikiki": "lcwaikiki.example",
    "Mavi": "mavi.example",
    "Eczacibasi": "eczacibasi.example",
    "Koc Holding": "kocholding.example",
    "Sabanci Holding": "sabanci.example",
    "Logo Yazilim": "logoyazilim.example",
    "Insider": "insider.example",
    "Papara": "papara.example",
    "Colendi": "colendi.example",
}


st.set_page_config(
    page_title="Turkiye HR Lead Generator",
    layout="wide",
)


def read_rows() -> list[dict[str, str]]:
    if not LEADS_CSV.exists():
        run(None, 100, seed=random.randint(1, 1_000_000))

    with LEADS_CSV.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def clean_cell(value: object) -> str:
    if value is None:
        return "-"
    text = str(value).strip()
    return text if text else "-"


def display_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [{column: clean_cell(row.get(column)) for column in COLUMNS} for row in rows]


def email_name_slug(full_name: str) -> str:
    replacements = {
        "ı": "i",
        "ğ": "g",
        "ü": "u",
        "ş": "s",
        "ö": "o",
        "ç": "c",
    }
    normalized = full_name.lower()
    for source, target in replacements.items():
        normalized = normalized.replace(source, target)
    return ".".join(part for part in normalized.split() if part)


def enrich_demo_emails(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    enriched: list[dict[str, str]] = []
    for row in rows:
        next_row = dict(row)
        if not next_row.get("Email"):
            domain = DEMO_EMAIL_DOMAINS.get(next_row.get(COL_COMPANY, ""))
            name = email_name_slug(next_row.get("Ad Soyad", ""))
            if domain and name:
                next_row["Email"] = f"{name}@{domain}"
        enriched.append(next_row)
    return enriched


def rows_to_csv_bytes(rows: list[dict[str, str]]) -> bytes:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8-sig")


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


def generate_new_leads(count: int, progress_slot, log_slot) -> list[dict[str, str]]:
    progress = progress_slot.progress(0)
    messages = [
        "LinkedIn arama niyeti hazirlaniyor...",
        "Turkiye HR lead havuzu olusturuluyor...",
        "Cleaning ve duplicate kontrolu yapiliyor...",
        "AI enrichment sinyalleri uretiliyor...",
        "Outreach mesajlari ve lead score hesaplaniyor...",
        "CSV/XLSX ciktilari guncelleniyor...",
    ]

    for index, message in enumerate(messages, start=1):
        log_slot.caption(message)
        progress.progress(index / (len(messages) + 1))
        time.sleep(0.08)
        if index == 3:
            run(None, count, seed=random.randint(1, 1_000_000))

    refresh_xlsx()
    progress.progress(1.0)
    log_slot.caption("Tamamlandi. Yeni tablo hazir.")
    return read_rows()


def score_summary(rows: list[dict[str, str]]) -> dict[str, float | int]:
    lead_scores = [int(row.get("Lead score") or 0) for row in rows]
    english_scores = [int(row.get(COL_ENGLISH_NEED) or 0) for row in rows]
    email_count = sum(1 for row in rows if row.get("Email"))
    return {
        "total": len(rows),
        "average_lead_score": round(sum(lead_scores) / len(lead_scores), 1) if lead_scores else 0,
        "priority_count": sum(1 for score in lead_scores if score >= 90),
        "email_count": email_count,
        "average_english_need": round(sum(english_scores) / len(english_scores), 1) if english_scores else 0,
    }


def unique_values(rows: list[dict[str, str]], column: str) -> list[str]:
    return sorted({row.get(column, "") for row in rows if row.get(column, "")})


def filter_rows(
    rows: list[dict[str, str]],
    sectors: list[str],
    sizes: list[str],
    min_score: int,
) -> list[dict[str, str]]:
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
    st.session_state.rows = read_rows()

st.title("Türkiye HR Lead Generator")
st.caption(
    "Konuşarak Öğren için Türkiye odaklı HR lead enrichment, AI outreach, lead scoring ve CRM pipeline prototipi."
)

with st.sidebar:
    st.header("Kontrol Paneli")
    search_intent = st.text_area(
        "Arama niyeti",
        value="HR Manager Turkey\nİnsan Kaynakları Müdürü\nTalent Acquisition Turkey\nPeople & Culture Manager Türkiye\nLearning & Development Manager Turkey",
        height=130,
    )
    lead_count = st.number_input("Lead sayısı", min_value=10, max_value=500, value=100, step=10)

    st.divider()
    st.subheader("Filtreler")
    sector_filter = st.multiselect("Sektör", unique_values(st.session_state.rows, COL_SECTOR))
    size_filter = st.multiselect("Şirket büyüklüğü", unique_values(st.session_state.rows, COL_SIZE))
    min_score_filter = st.slider("Minimum lead score", min_value=0, max_value=100, value=0, step=5)

    st.divider()
    demo_email_enabled = st.checkbox(
        "Demo email enrichment göster",
        value=False,
        help="Gerçek email bulmaz. Sadece .example domainli, gönderilemez demo adres formatı üretir.",
    )
    generate_clicked = st.button("Yeni 100 Lead Üret", type="primary", use_container_width=True)
    st.caption("Demo veri üretir. Gerçek kullanımda Apollo, Clay veya Sales Navigator CSV export bağlanabilir.")

if generate_clicked:
    progress_slot = st.empty()
    log_slot = st.empty()
    with st.spinner("AI lead enrichment ve outreach üretimi çalışıyor, lütfen bekleyin..."):
        st.session_state.rows = generate_new_leads(int(lead_count), progress_slot, log_slot)
    st.success(f"Türkiye odaklı {len(st.session_state.rows)} HR lead üretildi ve tablolar güncellendi.")

rows = enrich_demo_emails(st.session_state.rows) if demo_email_enabled else st.session_state.rows
filtered_rows = filter_rows(rows, sector_filter, size_filter, min_score_filter)
summary = score_summary(rows)

if demo_email_enabled:
    st.warning(
        "Demo email enrichment açık: Email alanları .example domainiyle gösterilir ve gerçek gönderim adresi değildir."
    )

metric_cols = st.columns(5)
metric_cols[0].metric("Toplam lead", summary["total"])
metric_cols[1].metric("Bulunan e-posta", summary["email_count"])
metric_cols[2].metric("Ort. İngilizce ihtiyacı", summary["average_english_need"])
metric_cols[3].metric("Ort. lead score", summary["average_lead_score"])
metric_cols[4].metric("Priority outreach", summary["priority_count"])

st.subheader("Workflow")
workflow_cols = st.columns(len(WORKFLOW_STEPS))
for column, label in zip(workflow_cols, WORKFLOW_STEPS):
    column.info(label)

st.subheader("HR Leads")
st.caption(f"{len(filtered_rows)} lead gösteriliyor. Boş LinkedIn URL ve Email alanları arayüzde '-' olarak gösterilir.")

summary_columns = ["Ad Soyad", COL_COMPANY, COL_TITLE, COL_SECTOR, COL_SIZE, COL_ENGLISH_NEED, "Lead score"]
st.dataframe(
    display_rows(filtered_rows),
    use_container_width=True,
    height=520,
    column_order=COLUMNS,
)

with st.expander("Hızlı özet tablo", expanded=False):
    st.dataframe(
        [{column: clean_cell(row.get(column)) for column in summary_columns} for row in filtered_rows],
        use_container_width=True,
        hide_index=True,
    )

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

download_cols = st.columns(3)
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

if XLSX_FILE.exists():
    download_cols[2].download_button(
        "XLSX indir",
        data=XLSX_FILE.read_bytes(),
        file_name="konusarak-ogren-hr-outbound-google-sheets.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
else:
    download_cols[2].button("XLSX hazırlanmadı", disabled=True, use_container_width=True)

with st.expander("Sistem notu"):
    st.markdown(
        f"""
        **Arama niyeti**

        ```text
        {search_intent}
        ```

        Bu public demo doğrudan LinkedIn scraping yapmaz ve kişisel email uydurmaz.
        Kod içinde hardcoded API key yoktur; production kullanımında API anahtarları
        `st.secrets` veya güvenli environment variable üzerinden yönetilmelidir.
        Email varsa eklenir, yoksa export dosyasında boş bırakılır.
        """
    )
