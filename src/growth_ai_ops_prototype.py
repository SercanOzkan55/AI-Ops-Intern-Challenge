from __future__ import annotations

import argparse
import csv
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
WORKFLOW_DIR = ROOT / "workflows"


COMPANY_PROFILES = {
    "Trendyol": {
        "sector": "E-commerce / Marketplace",
        "size": "5000+",
        "english_intensity": 88,
        "growth_signal": "hızlı ölçeklenen ekipler ve uluslararası operasyon",
    },
    "Getir": {
        "sector": "Quick commerce / Delivery",
        "size": "5000+",
        "english_intensity": 82,
        "growth_signal": "çok lokasyonlu operasyon ve saha ekipleri",
    },
    "Hepsiburada": {
        "sector": "E-commerce / Retail tech",
        "size": "1000-5000",
        "english_intensity": 80,
        "growth_signal": "müşteri deneyimi ve teknoloji ekipleri",
    },
    "Yemeksepeti": {
        "sector": "Food delivery / Tech",
        "size": "1000-5000",
        "english_intensity": 76,
        "growth_signal": "operasyon, satış ve teknoloji ekipleri",
    },
    "Peak Games": {
        "sector": "Gaming / Technology",
        "size": "250-1000",
        "english_intensity": 91,
        "growth_signal": "global ürün ve çok uluslu çalışma ritmi",
    },
    "Dream Games": {
        "sector": "Gaming / Technology",
        "size": "250-1000",
        "english_intensity": 92,
        "growth_signal": "global ürün ekipleri ve hızlı işe alım",
    },
    "Turkcell": {
        "sector": "Telecommunications",
        "size": "5000+",
        "english_intensity": 84,
        "growth_signal": "kurumsal dönüşüm ve teknoloji yetkinlikleri",
    },
    "Vodafone Turkey": {
        "sector": "Telecommunications",
        "size": "5000+",
        "english_intensity": 90,
        "growth_signal": "global ekiplerle yoğun iş birliği",
    },
    "Garanti BBVA": {
        "sector": "Banking / Finance",
        "size": "5000+",
        "english_intensity": 86,
        "growth_signal": "global bankacılık standartları ve dijitalleşme",
    },
    "Akbank": {
        "sector": "Banking / Finance",
        "size": "5000+",
        "english_intensity": 83,
        "growth_signal": "dijital bankacılık ve yetenek dönüşümü",
    },
    "Yapi Kredi": {
        "sector": "Banking / Finance",
        "size": "5000+",
        "english_intensity": 82,
        "growth_signal": "şube, merkez ve teknoloji ekiplerinin karma yapısı",
    },
    "Isbank": {
        "sector": "Banking / Finance",
        "size": "5000+",
        "english_intensity": 81,
        "growth_signal": "kurumsal ölçekte eğitim standardizasyonu",
    },
    "Ford Otosan": {
        "sector": "Automotive / Manufacturing",
        "size": "5000+",
        "english_intensity": 78,
        "growth_signal": "üretim, mühendislik ve global tedarik zinciri",
    },
    "Tofas": {
        "sector": "Automotive / Manufacturing",
        "size": "5000+",
        "english_intensity": 77,
        "growth_signal": "mavi yaka, beyaz yaka ve global partner dengesi",
    },
    "Arcelik": {
        "sector": "Consumer durables / Manufacturing",
        "size": "5000+",
        "english_intensity": 87,
        "growth_signal": "global marka ve çok ülkeli ekip yapısı",
    },
    "Vestel": {
        "sector": "Electronics / Manufacturing",
        "size": "5000+",
        "english_intensity": 79,
        "growth_signal": "ihracat ağı ve teknik ekiplerin İngilizce ihtiyacı",
    },
    "LC Waikiki": {
        "sector": "Retail / Fashion",
        "size": "5000+",
        "english_intensity": 73,
        "growth_signal": "mağaza, merkez ve yurt dışı perakende operasyonları",
    },
    "Mavi": {
        "sector": "Retail / Fashion",
        "size": "1000-5000",
        "english_intensity": 70,
        "growth_signal": "perakende ekipleri ve marka iş birlikleri",
    },
    "Eczacibasi": {
        "sector": "Conglomerate / Healthcare / Industry",
        "size": "5000+",
        "english_intensity": 84,
        "growth_signal": "çok sektörlü yetenek gelişimi",
    },
    "Koc Holding": {
        "sector": "Conglomerate",
        "size": "5000+",
        "english_intensity": 89,
        "growth_signal": "grup şirketleri arası ortak gelişim programları",
    },
    "Sabanci Holding": {
        "sector": "Conglomerate",
        "size": "5000+",
        "english_intensity": 88,
        "growth_signal": "globalleşme ve liderlik gelişimi",
    },
    "Logo Yazilim": {
        "sector": "B2B SaaS / Software",
        "size": "1000-5000",
        "english_intensity": 85,
        "growth_signal": "teknoloji yetenekleri ve müşteri odaklı ekipler",
    },
    "Insider": {
        "sector": "B2B SaaS / MarTech",
        "size": "1000-5000",
        "english_intensity": 94,
        "growth_signal": "global SaaS satış, müşteri başarısı ve ürün ekipleri",
    },
    "Papara": {
        "sector": "Fintech",
        "size": "250-1000",
        "english_intensity": 87,
        "growth_signal": "fintech büyümesi ve regülasyonla uyumlu ekipler",
    },
    "Colendi": {
        "sector": "Fintech",
        "size": "250-1000",
        "english_intensity": 89,
        "growth_signal": "uluslararası fintech ürünleşmesi",
    },
}


FIRST_NAMES = [
    "Ayse",
    "Mehmet",
    "Elif",
    "Can",
    "Zeynep",
    "Mert",
    "Derya",
    "Burak",
    "Selin",
    "Emre",
    "Ece",
    "Kerem",
    "Ceren",
    "Onur",
    "Deniz",
    "Gizem",
    "Berk",
    "Asli",
    "Tolga",
    "Irem",
]

LAST_NAMES = [
    "Yilmaz",
    "Kaya",
    "Demir",
    "Sahin",
    "Celik",
    "Arslan",
    "Aydin",
    "Ozturk",
    "Koc",
    "Yildiz",
    "Ozdemir",
    "Kilic",
    "Aslan",
    "Cetin",
    "Kara",
    "Acar",
    "Bulut",
    "Polat",
    "Erdem",
    "Kaplan",
]

TITLES = [
    "Human Resources Director",
    "HR Business Partner",
    "Talent Acquisition Manager",
    "Learning and Development Manager",
    "People and Culture Manager",
    "Employee Experience Lead",
    "Talent Management Specialist",
    "Organizational Development Manager",
]


@dataclass
class Lead:
    lead_id: str
    full_name: str
    company: str
    title: str
    linkedin_url: str
    email: str
    location: str
    source: str


def ensure_dirs() -> None:
    for directory in (DATA_DIR, OUTPUT_DIR, WORKFLOW_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def build_demo_leads(limit: int = 100, seed: int | None = None) -> list[Lead]:
    companies = list(COMPANY_PROFILES)
    leads: list[Lead] = []
    rng = random.Random(seed)
    seen: set[tuple[str, str, str]] = set()

    for index in range(limit):
        for _ in range(100):
            first_name = rng.choice(FIRST_NAMES)
            last_name = rng.choice(LAST_NAMES)
            company = rng.choice(companies)
            title = rng.choice(TITLES)
            unique_key = (f"{first_name} {last_name}", company, title)
            if unique_key not in seen:
                seen.add(unique_key)
                break
        search_query = f"{first_name} {last_name} {company} {title}".replace(" ", "%20")

        leads.append(
            Lead(
                lead_id=f"TR-HR-{index + 1:03d}",
                full_name=f"{first_name} {last_name}",
                company=company,
                title=title,
                linkedin_url="",
                email="",
                location="Turkey",
                source=f"Demo seed. Verify via LinkedIn search: https://www.linkedin.com/search/results/people/?keywords={search_query}",
            )
        )

    return leads


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_leads(path: Path) -> list[Lead]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        leads = []
        for row in reader:
            leads.append(
                Lead(
                    lead_id=row.get("lead_id") or f"LEAD-{len(leads) + 1:03d}",
                    full_name=row["full_name"],
                    company=row["company"],
                    title=row["title"],
                    linkedin_url=row.get("linkedin_url", ""),
                    email=row.get("email", ""),
                    location=row.get("location", "Turkey"),
                    source=row.get("source", "Imported CSV"),
                )
            )
    return leads


def seniority(title: str) -> str:
    normalized = title.lower()
    if "director" in normalized:
        return "Director"
    if "manager" in normalized:
        return "Manager"
    if "lead" in normalized:
        return "Lead"
    if "partner" in normalized:
        return "Partner"
    return "Specialist"


def persona(title: str) -> str:
    normalized = title.lower()
    if "talent acquisition" in normalized:
        return "recruitment_growth"
    if "learning" in normalized or "development" in normalized:
        return "learning_owner"
    if "employee experience" in normalized or "people" in normalized:
        return "employee_experience"
    if "business partner" in normalized:
        return "business_partner"
    return "hr_leadership"


def infer_pain_point(lead: Lead, profile: dict[str, object]) -> str:
    p = persona(lead.title)
    if p == "recruitment_growth":
        return "Aday deneyiminde İngilizce değerlendirme ve global rol iletişimini standardize etmek"
    if p == "learning_owner":
        return "Çalışanlara ölçülebilir, ölçeklenebilir ve yoğun programa uyumlu İngilizce gelişim yolu kurmak"
    if p == "employee_experience":
        return "Çalışan bağlılığını artıran, kişiye özel gelişim benefit'i sunmak"
    if p == "business_partner":
        return "Farklı ekiplerin İngilizce ihtiyacını tek modelde önceliklendirmek"
    return f"{profile['growth_signal']} nedeniyle İngilizce gelişim programını ölçeklemek"


def infer_outreach_angle(lead: Lead, profile: dict[str, object]) -> str:
    p = persona(lead.title)
    if p == "recruitment_growth":
        return "Global aday ve ekip iletişimi için konuşma odaklı İngilizce gelişimi"
    if p == "learning_owner":
        return "L&D programlarına ölçülebilir konuşma pratiği katmanı"
    if p == "employee_experience":
        return "Çalışan deneyimi benefit'i olarak esnek İngilizce gelişimi"
    if p == "business_partner":
        return "Departman bazlı İngilizce ihtiyacını HRBP perspektifiyle haritalama"
    return "Kurumsal İngilizce gelişimini hızlı pilotla test etme"


def sentence_start(text: str) -> str:
    return text[:1].upper() + text[1:] if text else text


def score_lead(lead: Lead, profile: dict[str, object]) -> int:
    base = int(profile["english_intensity"])
    title_bonus = {
        "Director": 8,
        "Manager": 6,
        "Lead": 5,
        "Partner": 4,
        "Specialist": 2,
    }[seniority(lead.title)]
    sector_bonus = 5 if any(token in profile["sector"].lower() for token in ["saas", "fintech", "gaming", "telecommunications"]) else 2
    size_bonus = 4 if profile["size"] == "5000+" else 3
    return min(100, base + title_bonus + sector_bonus + size_bonus - 8)


def crm_stage(score: int) -> str:
    if score >= 90:
        return "Priority outreach"
    if score >= 82:
        return "Warm nurture"
    if score >= 74:
        return "Test sequence"
    return "Low-touch nurture"


def generate_linkedin_dm(lead: Lead, profile: dict[str, object], pain_point: str, angle: str) -> str:
    first_name = lead.full_name.split()[0]
    pain_point = sentence_start(pain_point)
    return (
        f"Merhaba {first_name}, {lead.company} için {lead.title} rolünüzü gördüm. "
        f"{profile['sector']} tarafında {profile['growth_signal']} nedeniyle İngilizce iletişim kritik hale geliyor. "
        f"Konuşarak Öğren'de '{angle}' başlığıyla 2 haftalık küçük bir pilot kurguluyoruz. "
        f"Eğer '{pain_point}' gündeminizdeyse 15 dk fikir alışverişi yapmak isterim."
    )


def generate_email(lead: Lead, profile: dict[str, object], pain_point: str, angle: str) -> tuple[str, str]:
    first_name = lead.full_name.split()[0]
    pain_point = sentence_start(pain_point)
    subject = f"{lead.company} ekipleri için konuşma odaklı İngilizce pilotu"
    body = (
        f"Merhaba {first_name},\n\n"
        f"{lead.company} ekibinin {profile['sector']} ölçeğinde {profile['growth_signal']} odağı olduğunu görüyorum. "
        f"Bu yapıdaki HR ekiplerinde sık gördüğümüz konu: {pain_point}.\n\n"
        f"Konuşarak Öğren ile '{angle}' üzerine düşük eforlu bir pilot tasarlayabiliriz: "
        f"seviye tespiti, hedef grup seçimi, konuşma pratiği ve kısa gelişim raporu.\n\n"
        f"Uygunsa bu hafta 15 dakikalık bir görüşmede {lead.company} için mantıklı pilot segmentini birlikte çıkaralım.\n\n"
        f"Sevgiler,\n"
        f"Growth Automation Ekibi"
    )
    return subject, body


def enrich_lead(lead: Lead) -> dict[str, object]:
    profile = COMPANY_PROFILES.get(
        lead.company,
        {
            "sector": "Unknown",
            "size": "Unknown",
            "english_intensity": 65,
            "growth_signal": "büyüyen ekip yapısı",
        },
    )
    pain_point = infer_pain_point(lead, profile)
    angle = infer_outreach_angle(lead, profile)
    score = score_lead(lead, profile)
    subject, email_body = generate_email(lead, profile, pain_point, angle)

    return {
        "lead_id": lead.lead_id,
        "full_name": lead.full_name,
        "company": lead.company,
        "title": lead.title,
        "linkedin_url": lead.linkedin_url,
        "email": lead.email,
        "location": lead.location,
        "source": lead.source,
        "company_sector": profile["sector"],
        "company_size": profile["size"],
        "seniority": seniority(lead.title),
        "persona": persona(lead.title),
        "estimated_english_need_score": profile["english_intensity"],
        "likely_pain_point": pain_point,
        "outreach_angle": angle,
        "lead_score": score,
        "crm_stage": crm_stage(score),
        "linkedin_dm": generate_linkedin_dm(lead, profile, pain_point, angle),
        "email_subject": subject,
        "email_body": email_body,
    }


def write_workflow_blueprint(path: Path) -> None:
    workflow = {
        "name": "Growth Automation & AI Ops HR Outbound Prototype",
        "version": "1.0",
        "nodes": [
            {
                "id": "lead_source",
                "type": "manual_or_export",
                "description": "LinkedIn Sales Navigator, Apollo, Clay, Google Sheets, or manually verified CSV export.",
                "output": "data/raw_hr_leads_sample.csv",
            },
            {
                "id": "cleaning",
                "type": "python",
                "description": "Normalize names, companies, titles, duplicate keys, empty email/linkedin fields.",
                "input": "raw leads CSV",
            },
            {
                "id": "enrichment",
                "type": "python + AI prompt layer",
                "description": "Infer sector, company size, persona, English need, pain point, and outreach angle.",
                "input": "clean leads",
            },
            {
                "id": "lead_scoring",
                "type": "rules",
                "description": "Score by sector intensity, company size, seniority, and role relevance.",
                "input": "enriched leads",
            },
            {
                "id": "outreach_generation",
                "type": "AI copy generation",
                "description": "Generate short LinkedIn DM and cold email using lead-level context.",
                "input": "scored enriched leads",
            },
            {
                "id": "crm_pipeline",
                "type": "csv_or_airtable",
                "description": "Route leads into Priority outreach, Warm nurture, Test sequence, or Low-touch nurture.",
                "output": "output/crm_pipeline.csv",
            },
            {
                "id": "reply_classification_bonus",
                "type": "AI classifier",
                "description": "Classify replies as interested, objection, timing, wrong person, unsubscribe, or bounced.",
                "status": "bonus blueprint",
            },
        ],
        "edges": [
            ["lead_source", "cleaning"],
            ["cleaning", "enrichment"],
            ["enrichment", "lead_scoring"],
            ["lead_scoring", "outreach_generation"],
            ["outreach_generation", "crm_pipeline"],
            ["crm_pipeline", "reply_classification_bonus"],
        ],
    }
    path.write_text(json.dumps(workflow, indent=2, ensure_ascii=False), encoding="utf-8")


def run(input_csv: Path | None, limit: int, seed: int | None = None) -> None:
    ensure_dirs()
    leads = read_leads(input_csv) if input_csv else build_demo_leads(limit, seed=seed)
    raw_rows = [lead.__dict__ for lead in leads]
    enriched_rows = [enrich_lead(lead) for lead in leads]

    write_csv(
        DATA_DIR / "raw_hr_leads_sample.csv",
        raw_rows,
        ["lead_id", "full_name", "company", "title", "linkedin_url", "email", "location", "source"],
    )
    write_csv(
        OUTPUT_DIR / "enriched_hr_leads.csv",
        enriched_rows,
        list(enriched_rows[0].keys()),
    )
    write_csv(
        OUTPUT_DIR / "outreach_messages.csv",
        [
            {
                "lead_id": row["lead_id"],
                "full_name": row["full_name"],
                "company": row["company"],
                "linkedin_dm": row["linkedin_dm"],
                "email_subject": row["email_subject"],
                "email_body": row["email_body"],
            }
            for row in enriched_rows
        ],
        ["lead_id", "full_name", "company", "linkedin_dm", "email_subject", "email_body"],
    )
    write_csv(
        OUTPUT_DIR / "crm_pipeline.csv",
        [
            {
                "lead_id": row["lead_id"],
                "full_name": row["full_name"],
                "company": row["company"],
                "title": row["title"],
                "lead_score": row["lead_score"],
                "crm_stage": row["crm_stage"],
                "next_action": "LinkedIn connect + DM" if row["crm_stage"] == "Priority outreach" else "Email sequence / nurture",
            }
            for row in enriched_rows
        ],
        ["lead_id", "full_name", "company", "title", "lead_score", "crm_stage", "next_action"],
    )
    write_csv(
        OUTPUT_DIR / "google_sheets_hr_leads.csv",
        [
            {
                "Ad Soyad": row["full_name"],
                "Şirket": row["company"],
                "Ünvan": row["title"],
                "LinkedIn URL": row["linkedin_url"],
                "Email": row["email"],
                "Sektör": row["company_sector"],
                "Şirket büyüklüğü": row["company_size"],
                "Pain point": row["likely_pain_point"],
                "İngilizce ihtiyacı tahmini": row["estimated_english_need_score"],
                "Outreach angle": row["outreach_angle"],
                "LinkedIn DM": row["linkedin_dm"],
                "Cold email": f"Subject: {row['email_subject']}\n\n{row['email_body']}",
                "Lead score": row["lead_score"],
            }
            for row in enriched_rows
        ],
        [
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
        ],
    )
    write_csv(
        OUTPUT_DIR / "workflow_steps.csv",
        [
            {"Step": "1", "Workflow": "LinkedIn Search", "Description": "HR Manager Turkey, İnsan Kaynakları Müdürü, Talent Acquisition Turkey, People & Culture Manager Türkiye, Learning & Development Manager Turkey aramalarıyla lead havuzu oluştur."},
            {"Step": "2", "Workflow": "Google Sheets", "Description": "Ad Soyad, Şirket, Ünvan, LinkedIn URL, Email ve source bilgilerini tek tabloda topla. Email yoksa boş bırak."},
            {"Step": "3", "Workflow": "Cleaning", "Description": "Duplicate kayıtları, ünvan varyasyonlarını, şirket adlarını ve boş alanları normalize et."},
            {"Step": "4", "Workflow": "AI Enrichment", "Description": "Şirket, ünvan ve sektör üzerinden pain point, İngilizce ihtiyacı tahmini ve outreach angle üret."},
            {"Step": "5", "Workflow": "Outreach Generation", "Description": "Her lead için şirket + ünvan + ihtiyaç bağlamıyla kısa LinkedIn DM ve cold email üret."},
            {"Step": "6", "Workflow": "CRM Status", "Description": "Lead score'a göre Priority outreach, Warm nurture, Test sequence veya Low-touch nurture stage'ine ata."},
        ],
        ["Step", "Workflow", "Description"],
    )
    write_workflow_blueprint(WORKFLOW_DIR / "workflow_blueprint.json")

    print(f"Generated {len(leads)} raw leads")
    print(f"Wrote {DATA_DIR / 'raw_hr_leads_sample.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'enriched_hr_leads.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'outreach_messages.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'crm_pipeline.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'google_sheets_hr_leads.csv'}")
    print(f"Wrote {OUTPUT_DIR / 'workflow_steps.csv'}")
    print(f"Wrote {WORKFLOW_DIR / 'workflow_blueprint.json'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Growth Automation & AI Ops HR outbound prototype")
    parser.add_argument("--input-csv", type=Path, help="Optional raw lead CSV to process instead of demo seed data.")
    parser.add_argument("--limit", type=int, default=100, help="Number of demo leads to generate when no input CSV is provided.")
    parser.add_argument("--seed", type=int, help="Optional random seed for reproducible Turkish HR demo leads.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.input_csv, args.limit, seed=args.seed)
