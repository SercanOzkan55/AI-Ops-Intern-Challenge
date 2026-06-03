from __future__ import annotations

import csv
import json
import subprocess
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

from growth_ai_ops_prototype import OUTPUT_DIR, ROOT, run


HOST = "127.0.0.1"
PORT = 8765
LEADS_CSV = OUTPUT_DIR / "google_sheets_hr_leads.csv"
XLSX_FILE = OUTPUT_DIR / "konusarak-ogren-hr-outbound-google-sheets.xlsx"
NODE_EXE = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe"


HTML = """<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>HR Lead Generator</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f7f9;
      --panel: #ffffff;
      --ink: #1d2433;
      --muted: #667085;
      --line: #d9dee8;
      --accent: #0f766e;
      --accent-dark: #0b5d57;
      --soft: #e8f3f1;
      --warn: #fff5dd;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 14px/1.45 Arial, Helvetica, sans-serif;
    }
    header {
      background: var(--panel);
      border-bottom: 1px solid var(--line);
      padding: 20px 28px 16px;
      position: sticky;
      top: 0;
      z-index: 3;
    }
    h1 {
      margin: 0 0 4px;
      font-size: 22px;
      letter-spacing: 0;
    }
    .sub { color: var(--muted); margin: 0; }
    main { padding: 18px 28px 28px; }
    .toolbar {
      display: grid;
      grid-template-columns: 1.4fr 110px 170px 170px;
      gap: 10px;
      align-items: end;
      margin-bottom: 14px;
    }
    label {
      display: grid;
      gap: 6px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
    }
    input, select {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px 11px;
      color: var(--ink);
      background: #fff;
      font: inherit;
      min-height: 40px;
    }
    button, .button {
      border: 0;
      border-radius: 6px;
      padding: 10px 12px;
      background: var(--accent);
      color: #fff;
      font-weight: 700;
      min-height: 40px;
      cursor: pointer;
      text-decoration: none;
      text-align: center;
    }
    button:hover, .button:hover { background: var(--accent-dark); }
    button.secondary, .button.secondary {
      background: #283449;
    }
    .stats {
      display: grid;
      grid-template-columns: repeat(4, minmax(140px, 1fr));
      gap: 10px;
      margin: 0 0 14px;
    }
    .stat {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px 14px;
    }
    .stat span {
      display: block;
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 3px;
    }
    .stat strong { font-size: 22px; }
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
    }
    .panel-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
    }
    .actions { display: flex; gap: 8px; flex-wrap: wrap; }
    .status {
      color: var(--muted);
      font-size: 13px;
    }
    .table-wrap {
      overflow: auto;
      max-height: calc(100vh - 300px);
    }
    table {
      border-collapse: separate;
      border-spacing: 0;
      width: 100%;
      min-width: 1900px;
    }
    th, td {
      border-bottom: 1px solid var(--line);
      border-right: 1px solid #edf0f5;
      padding: 8px 10px;
      vertical-align: top;
      background: #fff;
    }
    th {
      position: sticky;
      top: 0;
      z-index: 2;
      background: #eef4f3;
      color: #25313f;
      text-align: left;
      font-size: 12px;
      white-space: nowrap;
    }
    td {
      max-width: 310px;
      min-width: 90px;
      word-break: break-word;
    }
    td.score {
      text-align: center;
      font-weight: 700;
      background: var(--soft);
      min-width: 78px;
    }
    .workflow {
      display: grid;
      grid-template-columns: repeat(6, minmax(120px, 1fr));
      gap: 8px;
      margin: 14px 0;
    }
    .step {
      background: var(--warn);
      border: 1px solid #efd99f;
      border-radius: 8px;
      padding: 10px;
      font-weight: 700;
      text-align: center;
    }
    @media (max-width: 980px) {
      .toolbar, .stats, .workflow { grid-template-columns: 1fr; }
      header, main { padding-left: 16px; padding-right: 16px; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Türkiye HR Lead Generator</h1>
    <p class="sub">Türkiye odaklı 100 HR lead üretir, enrichment/outreach tablolarını günceller ve mevcut çıktılara erişim verir.</p>
  </header>
  <main>
    <section class="toolbar">
      <label>Arama niyeti
        <input id="query" value="İnsan kaynakları, HR Manager Turkey, Talent Acquisition Turkey">
      </label>
      <label>Lead sayısı
        <input id="count" type="number" min="1" max="500" value="100">
      </label>
      <button id="generate">Yeni 100 Lead Üret</button>
      <button class="secondary" id="refresh">Mevcut Çıktıyı Aç</button>
    </section>

    <section class="workflow" aria-label="Workflow">
      <div class="step">LinkedIn Search</div>
      <div class="step">Google Sheets</div>
      <div class="step">Cleaning</div>
      <div class="step">AI Enrichment</div>
      <div class="step">Outreach Generation</div>
      <div class="step">CRM Status</div>
    </section>

    <section class="stats">
      <div class="stat"><span>Toplam lead</span><strong id="total">0</strong></div>
      <div class="stat"><span>Ortalama skor</span><strong id="avg">0</strong></div>
      <div class="stat"><span>Priority outreach</span><strong id="priority">0</strong></div>
      <div class="stat"><span>Son güncelleme</span><strong id="updated">-</strong></div>
    </section>

    <section class="panel">
      <div class="panel-head">
        <div>
          <strong>HR Leads</strong>
          <div class="status" id="status">Hazır.</div>
        </div>
        <div class="actions">
          <a class="button secondary" href="/download/google_sheets_hr_leads.csv">CSV indir</a>
          <a class="button secondary" href="/download/konusarak-ogren-hr-outbound-google-sheets.xlsx">XLSX indir</a>
        </div>
      </div>
      <div class="table-wrap">
        <table>
          <thead id="thead"></thead>
          <tbody id="tbody"></tbody>
        </table>
      </div>
    </section>
  </main>

  <script>
    const columns = [
      "Ad Soyad", "Şirket", "Ünvan", "LinkedIn URL", "Email", "Sektör",
      "Şirket büyüklüğü", "Pain point", "İngilizce ihtiyacı tahmini",
      "Outreach angle", "LinkedIn DM", "Cold email", "Lead score"
    ];

    function setStatus(text) {
      document.getElementById("status").textContent = text;
    }

    function render(rows, meta) {
      document.getElementById("thead").innerHTML = "<tr>" + columns.map(c => `<th>${c}</th>`).join("") + "</tr>";
      document.getElementById("tbody").innerHTML = rows.map(row => {
        return "<tr>" + columns.map(col => {
          const value = row[col] ?? "";
          const cls = col === "Lead score" ? " class='score'" : "";
          return `<td${cls}>${String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;")}</td>`;
        }).join("") + "</tr>";
      }).join("");
      document.getElementById("total").textContent = meta.total ?? rows.length;
      document.getElementById("avg").textContent = meta.average_score ?? "0";
      document.getElementById("priority").textContent = meta.priority_count ?? "0";
      document.getElementById("updated").textContent = meta.updated_at ?? "-";
    }

    async function loadLeads() {
      setStatus("Tablo yükleniyor...");
      const res = await fetch("/api/leads");
      const data = await res.json();
      render(data.rows, data.meta);
      setStatus(data.message);
    }

    async function generate() {
      const count = Number(document.getElementById("count").value || 100);
      const query = document.getElementById("query").value;
      setStatus("Yeni Türkiye HR lead seti üretiliyor...");
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ count, query })
      });
      const data = await res.json();
      render(data.rows, data.meta);
      setStatus(data.message);
    }

    document.getElementById("generate").addEventListener("click", generate);
    document.getElementById("refresh").addEventListener("click", loadLeads);
    loadLeads();
  </script>
</body>
</html>
"""


def read_rows() -> list[dict[str, str]]:
    if not LEADS_CSV.exists():
        run(None, 100)
    with LEADS_CSV.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def build_meta(rows: list[dict[str, str]]) -> dict[str, object]:
    scores = [int(row.get("Lead score") or 0) for row in rows]
    priority = sum(1 for score in scores if score >= 90)
    updated = time.strftime("%H:%M:%S")
    return {
        "total": len(rows),
        "average_score": round(sum(scores) / len(scores), 1) if scores else 0,
        "priority_count": priority,
        "updated_at": updated,
    }


def refresh_xlsx() -> None:
    builder = ROOT / "tools" / "build_google_sheets_workbook.mjs"
    if NODE_EXE.exists() and builder.exists():
        try:
            subprocess.run(
                [str(NODE_EXE), str(builder)],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
                timeout=15,
            )
        except subprocess.TimeoutExpired:
            return


class GuiHandler(BaseHTTPRequestHandler):
    def _send(self, body: bytes, content_type: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, payload: dict[str, object]) -> None:
        self._send(json.dumps(payload, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self) -> None:
        if self.path == "/":
            self._send(HTML.encode("utf-8"), "text/html; charset=utf-8")
            return

        if self.path == "/api/leads":
            rows = read_rows()
            self._send_json({"rows": rows, "meta": build_meta(rows), "message": "Mevcut çıktı yüklendi."})
            return

        if self.path.startswith("/download/"):
            filename = unquote(self.path.removeprefix("/download/"))
            safe_files = {
                "google_sheets_hr_leads.csv": LEADS_CSV,
                "konusarak-ogren-hr-outbound-google-sheets.xlsx": XLSX_FILE,
            }
            file_path = safe_files.get(filename)
            if not file_path or not file_path.exists():
                self._send(b"File not found", "text/plain", HTTPStatus.NOT_FOUND)
                return
            content_type = "text/csv; charset=utf-8" if file_path.suffix == ".csv" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            self._send(file_path.read_bytes(), content_type)
            return

        self._send(b"Not found", "text/plain", HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        if self.path != "/api/generate":
            self._send(b"Not found", "text/plain", HTTPStatus.NOT_FOUND)
            return

        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        count = max(1, min(int(payload.get("count", 100)), 500))
        run(None, count)
        refresh_xlsx()
        rows = read_rows()
        self._send_json(
            {
                "rows": rows,
                "meta": build_meta(rows),
                "message": f"Türkiye odaklı {len(rows)} HR lead üretildi ve tablolar güncellendi.",
            }
        )

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((HOST, PORT), GuiHandler)
    print(f"GUI running at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
