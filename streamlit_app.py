from __future__ import annotations

import csv
import io
import random
import subprocess
from pathlib import Path

import streamlit as st

from src.growth_ai_ops_prototype import OUTPUT_DIR, ROOT, run


LEADS_CSV = OUTPUT_DIR / "google_sheets_hr_leads.csv"
XLSX_FILE = OUTPUT_DIR / "konusarak-ogren-hr-outbound-google-sheets.xlsx"
COLUMNS = [
    "Ad Soyad",
    "Şirket",
    "Ünvan",
    "LinkedIn URL",
    "Email",
    "Sektör",
    "Şirket büyüklüğü",
    "Pain point",
    "İngilizce ihtiyacı tahmini",
    "Outreach angle",
    "LinkedIn DM",
    "Cold email",
    "Lead score",
]


st.set_page_config(
    page_title="Türkiye HR Lead Generator",
    page_icon="📊",
    layout="wide",
)


def read_rows() -> list[dict[str, str]]:
    if not LEADS_CSV.exists():
        run(None, 100, seed=random.randint(1, 1_000_000))

    with LEADS_CSV.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


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


def generate_new_leads(count: int) -> list[dict[str, str]]:
    run(None, count, seed=random.randint(1, 1_000_000))
    refresh_xlsx()
    return read_rows()


def score_summary(rows: list[dict[str, str]]) -> tuple[int, float, int]:
    scores = [int(row.get("Lead score") or 0) for row in rows]
    total = len(rows)
    average = round(sum(scores) / total, 1) if total else 0
    priority = sum(1 for score in scores if score >= 90)
    return total, average, priority


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
    generate_clicked = st.button("Yeni 100 Lead Üret", type="primary", use_container_width=True)
    st.caption("Not: Demo veri üretir; gerçek kullanımda Apollo/Clay/Sales Navigator CSV export bağlanabilir.")

if generate_clicked:
    rows = generate_new_leads(int(lead_count))
    st.success(f"Türkiye odaklı {len(rows)} HR lead üretildi ve tablolar güncellendi.")
else:
    rows = read_rows()

total, average_score, priority_count = score_summary(rows)

metric_cols = st.columns(4)
metric_cols[0].metric("Toplam lead", total)
metric_cols[1].metric("Ortalama lead score", average_score)
metric_cols[2].metric("Priority outreach", priority_count)
metric_cols[3].metric("Kolon", len(COLUMNS))

st.subheader("Workflow")
workflow_cols = st.columns(6)
for column, label in zip(
    workflow_cols,
    ["LinkedIn Search", "Google Sheets", "Cleaning", "AI Enrichment", "Outreach Generation", "CRM Status"],
):
    column.info(label)

st.subheader("HR Leads")
st.dataframe(rows, use_container_width=True, height=520, column_order=COLUMNS)

download_cols = st.columns(3)
download_cols[0].download_button(
    "CSV indir",
    data=rows_to_csv_bytes(rows),
    file_name="google_sheets_hr_leads.csv",
    mime="text/csv",
    use_container_width=True,
)

if XLSX_FILE.exists():
    download_cols[1].download_button(
        "XLSX indir",
        data=XLSX_FILE.read_bytes(),
        file_name="konusarak-ogren-hr-outbound-google-sheets.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
else:
    download_cols[1].button("XLSX hazırlanmadı", disabled=True, use_container_width=True)

with st.expander("Sistem notu"):
    st.markdown(
        f"""
        **Arama niyeti**

        ```text
        {search_intent}
        ```

        Bu public demo doğrudan LinkedIn scraping yapmaz ve kişisel email uydurmaz.
        Gerçek kullanımda doğrulanmış CSV/API kaynağı bağlanır; email varsa eklenir, yoksa boş bırakılır.
        """
    )
