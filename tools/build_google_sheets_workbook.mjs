import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = path.resolve(".");
const leadsCsv = await fs.readFile(path.join(root, "output", "google_sheets_hr_leads.csv"), "utf8");
const workbook = await Workbook.fromCSV(leadsCsv, { sheetName: "HR Leads" });

const workflowSheet = workbook.worksheets.add("Workflow");
workflowSheet.getRange("A1:C1").values = [["Step", "Workflow", "Description"]];
workflowSheet.getRange("A2:C7").values = [
  ["1", "LinkedIn Search", "HR Manager Turkey, İnsan Kaynakları Müdürü, Talent Acquisition Turkey, People & Culture Manager Türkiye, Learning & Development Manager Turkey aramalarıyla lead havuzu oluştur."],
  ["2", "Google Sheets", "Ad Soyad, Şirket, Ünvan, LinkedIn URL, Email ve source bilgilerini tek tabloda topla. Email yoksa boş bırak."],
  ["3", "Cleaning", "Duplicate kayıtları, ünvan varyasyonlarını, şirket adlarını ve boş alanları normalize et."],
  ["4", "AI Enrichment", "Şirket, ünvan ve sektör üzerinden pain point, İngilizce ihtiyacı tahmini ve outreach angle üret."],
  ["5", "Outreach Generation", "Her lead için şirket + ünvan + ihtiyaç bağlamıyla kısa LinkedIn DM ve cold email üret."],
  ["6", "CRM Status", "Lead score'a göre Priority outreach, Warm nurture, Test sequence veya Low-touch nurture stage'ine ata."],
];

const outputDir = path.join(root, "output");
await fs.mkdir(outputDir, { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
const outputPath = path.join(outputDir, "konusarak-ogren-hr-outbound-google-sheets.xlsx");
await output.save(outputPath);

console.log(outputPath);
