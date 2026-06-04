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


TR = {
    "company": "\u015eirket",
    "title": "\u00dcnvan",
    "sector": "Sekt\u00f6r",
    "company_size": "\u015eirket b\u00fcy\u00fckl\u00fc\u011f\u00fc",
    "english_need": "\u0130ngilizce ihtiyac\u0131 tahmini",
}


COMPANY_PROFILES = {
    "Trendyol": ("E-commerce / Marketplace", "5000+", 88, "hizli olceklenen ekipler ve uluslararasi operasyon"),
    "Getir": ("Quick commerce / Delivery", "5000+", 82, "cok lokasyonlu operasyon ve saha ekipleri"),
    "Hepsiburada": ("E-commerce / Retail tech", "1000-5000", 80, "musteri deneyimi ve teknoloji ekipleri"),
    "Yemeksepeti": ("Food delivery / Tech", "1000-5000", 76, "operasyon, satis ve teknoloji ekipleri"),
    "Peak Games": ("Gaming / Technology", "250-1000", 91, "global urun ve cok uluslu calisma ritmi"),
    "Dream Games": ("Gaming / Technology", "250-1000", 92, "global urun ekipleri ve hizli ise alim"),
    "Turkcell": ("Telecommunications", "5000+", 84, "kurumsal donusum ve teknoloji yetkinlikleri"),
    "Vodafone Turkey": ("Telecommunications", "5000+", 90, "global ekiplerle yogun is birligi"),
    "Garanti BBVA": ("Banking / Finance", "5000+", 86, "global bankacilik standartlari ve dijitallesme"),
    "Akbank": ("Banking / Finance", "5000+", 83, "dijital bankacilik ve yetenek donusumu"),
    "Yapi Kredi": ("Banking / Finance", "5000+", 82, "sube, merkez ve teknoloji ekiplerinin karma yapisi"),
    "Isbank": ("Banking / Finance", "5000+", 81, "kurumsal olcekte egitim standardizasyonu"),
    "Ford Otosan": ("Automotive / Manufacturing", "5000+", 78, "uretim, muhendislik ve global tedarik zinciri"),
    "Tofas": ("Automotive / Manufacturing", "5000+", 77, "mavi yaka, beyaz yaka ve global partner dengesi"),
    "Arcelik": ("Consumer durables / Manufacturing", "5000+", 87, "global marka ve cok ulkeli ekip yapisi"),
    "Vestel": ("Electronics / Manufacturing", "5000+", 79, "ihracat agi ve teknik ekiplerin Ingilizce ihtiyaci"),
    "LC Waikiki": ("Retail / Fashion", "5000+", 73, "magaza, merkez ve yurt disi perakende operasyonlari"),
    "Mavi": ("Retail / Fashion", "1000-5000", 70, "perakende ekipleri ve marka is birlikleri"),
    "Eczacibasi": ("Conglomerate / Healthcare / Industry", "5000+", 84, "cok sektorlu yetenek gelisimi"),
    "Koc Holding": ("Conglomerate", "5000+", 89, "grup sirketleri arasi ortak gelisim programlari"),
    "Sabanci Holding": ("Conglomerate", "5000+", 88, "globallesme ve liderlik gelisimi"),
    "Logo Yazilim": ("B2B SaaS / Software", "1000-5000", 85, "teknoloji yetenekleri ve musteri odakli ekipler"),
    "Insider": ("B2B SaaS / MarTech", "1000-5000", 94, "global SaaS satis, musteri basarisi ve urun ekipleri"),
    "Papara": ("Fintech", "250-1000", 87, "fintech buyumesi ve regulasyonla uyumlu ekipler"),
    "Colendi": ("Fintech", "250-1000", 89, "uluslararasi fintech urunlesmesi"),
    "Türkiye İş Bankası": ("Banking / Finance", "5000+", 81, "kurumsal olcekte egitim standardizasyonu"),
    "QNB Finansbank": ("Banking / Finance", "5000+", 80, "dijital bankacilik ve yetenek yonetimi"),
    "DenizBank": ("Banking / Finance", "5000+", 78, "perakende bankacilik ve dijital donusum"),
    "TEB": ("Banking / Finance", "1000-5000", 79, "kurumsal bankacilik ve BNP Paribas is birligi"),
    "Ziraat Bankası": ("Banking / Finance", "5000+", 75, "kamu bankaciligi ve modernizasyon"),
    "Halkbank": ("Banking / Finance", "5000+", 74, "KOBi bankaciligi ve dijitallesme"),
    "VakıfBank": ("Banking / Finance", "5000+", 76, "kurumsal performans ve dijital donusum"),
    "ING Türkiye": ("Banking / Finance", "1000-5000", 85, "global standartlar ve dijital bankacilik"),
    "HSBC Türkiye": ("Banking / Finance", "1000-5000", 90, "uluslararasi bankacilik ve global ekipler"),
    "Albaraka Türk": ("Banking / Finance", "1000-5000", 72, "katilim bankaciligi ve surdurulebilirlik"),
    "Alternatif Bank": ("Banking / Finance", "250-1000", 78, "ticari bankacilik ve yenilikci urunler"),
    "Hepsiburada": ("E-commerce / Marketplace", "5000+", 82, "e-ticaret buyumesi ve teknoloji yatirimlari"),
    "Dream Games": ("Gaming / Technology", "250-1000", 92, "global urun ekipleri ve hizli ise alim"),
    "Sahibinden.com": ("Classifieds / Technology", "1000-5000", 80, "dijital pazar yeri ve teknoloji ekipleri"),
    "BiTaksi": ("Mobility / Technology", "250-1000", 78, "ulasim teknolojisi ve operasyon ekipleri"),
    "AloTech": ("B2B SaaS / Technology", "250-1000", 82, "musteri deneyimi teknolojisi"),
    "Papel": ("Fintech", "250-1000", 80, "dijital odeme ve fintech buyumesi"),
    "Bilyoner": ("iGaming / Technology", "250-1000", 75, "dijital bahis ve teknoloji ekipleri"),
    "Vodafone Turkey": ("Telecommunications", "5000+", 90, "global ekiplerle yogun is birligi"),
    "Türk Telekom": ("Telecommunications", "5000+", 82, "dijital donusum ve fiber altyapi"),
    "LC Waikiki": ("Retail / Fashion", "5000+", 73, "magaza merkez ve yurt disi perakende operasyonlari"),
    "Mavi": ("Retail / Fashion", "1000-5000", 70, "perakende ekipleri ve marka is birlikleri"),
    "DeFacto": ("Retail / Fashion", "5000+", 72, "hizli moda ve uluslararasi buyume"),
    "Boyner Grup": ("Retail / Department store", "5000+", 71, "cok kanalli perakende donusumu"),
    "BİM": ("Retail / Discount", "5000+", 65, "indirim perakende ve operasyonel verimlilik"),
    "Migros": ("Retail / Grocery", "5000+", 72, "gida perakende ve dijital donusum"),
    "CarrefourSA": ("Retail / Grocery", "5000+", 74, "gida perakende ve surdurulebilirlik"),
    "ŞOK Marketler": ("Retail / Discount", "5000+", 64, "hizli buyuyen indirim perakende"),
    "Koçtaş": ("Retail / Home improvement", "1000-5000", 73, "yapi market ve perakende operasyonlari"),
    "Toyota Türkiye": ("Automotive / Manufacturing", "1000-5000", 80, "uretim ve kalite muhendisligi"),
    "Mercedes-Benz Türk": ("Automotive / Manufacturing", "5000+", 88, "premium otomotiv ve global standartlar"),
    "Hyundai Assan": ("Automotive / Manufacturing", "1000-5000", 76, "otomotiv uretim ve ihracat"),
    "Renault MAİS": ("Automotive / Distribution", "1000-5000", 78, "otomotiv dagitim ve satis"),
    "Borusan Holding": ("Conglomerate / Industrial", "5000+", 83, "sanayi ve hizmet sektoru yonetimi"),
    "Borusan Otomotiv": ("Automotive / Distribution", "1000-5000", 81, "premium otomotiv dagitim"),
    "Şişecam": ("Glass / Manufacturing", "5000+", 80, "cam sanayi ve global operasyonlar"),
    "Kordsa": ("Industrial / Manufacturing", "1000-5000", 82, "endüstriyel tekstil ve global uretim"),
    "Brisa": ("Tire / Manufacturing", "1000-5000", 79, "lastik uretimi ve Bridgestone is birligi"),
    "Doğan Holding": ("Conglomerate / Media", "5000+", 76, "medya enerji ve sanayi yonetimi"),
    "Türk Hava Yolları": ("Airlines / Aviation", "5000+", 85, "global havayolu ve genis operasyon agi"),
    "Pegasus Hava Yolları": ("Airlines / Aviation", "5000+", 78, "dusuk maliyet havayolu ve hizli buyume"),
    "Enerjisa": ("Energy / Utilities", "5000+", 80, "enerji dagitim ve surdurulebilirlik"),
    "TÜPRAŞ": ("Energy / Refining", "5000+", 78, "rafineri ve petrokimya uretimi"),
    "Aksa Enerji": ("Energy / Power", "1000-5000", 74, "enerji uretim ve yatirimlari"),
    "Unilever Türkiye": ("FMCG / Consumer goods", "1000-5000", 90, "global FMCG ve cok uluslu calisma"),
    "P&G Türkiye": ("FMCG / Consumer goods", "1000-5000", 92, "global standartlar ve liderlik gelisimi"),
    "Coca-Cola İçecek": ("Beverages / FMCG", "5000+", 85, "global marka ve cok ulkeli operasyonlar"),
    "Nestlé Türkiye": ("FMCG / Food", "1000-5000", 88, "global gida sirketi ve surdurulebilirlik"),
    "Anadolu Efes": ("Beverages / FMCG", "5000+", 82, "icecek sektoru ve uluslararasi operasyonlar"),
    "Ülker / Yıldız Holding": ("FMCG / Food", "5000+", 78, "gida uretimi ve global marka portfoyu"),
    "Zorlu Holding": ("Conglomerate", "5000+", 84, "enerji tekstil teknoloji ve gayrimenkul"),
    "TAV Havalimanları": ("Aviation / Infrastructure", "5000+", 80, "havalimani isletme ve global operasyonlar"),
    "Doğuş Otomotiv": ("Automotive / Distribution", "1000-5000", 80, "otomotiv dagitim ve perakende"),
    "Abdi İbrahim": ("Pharma / Healthcare", "1000-5000", 78, "ilac sanayi ve uluslararasi buyume"),
    "Eczacıbaşı Sağlık": ("Healthcare / Pharma", "1000-5000", 80, "saglik urunleri ve ilac"),
    "Medicana Sağlık Grubu": ("Healthcare / Hospitals", "5000+", 72, "ozel saglik ve hastane yonetimi"),
    "Acıbadem Sağlık Grubu": ("Healthcare / Hospitals", "5000+", 78, "premium saglik hizmetleri"),
    "ASELSAN": ("Defense / Technology", "5000+", 80, "savunma teknolojisi ve muhendislik"),
    "HAVELSAN": ("Defense / Technology", "1000-5000", 78, "savunma yazilimi ve siber guvenlik"),
    "AXA Sigorta": ("Insurance / Finance", "1000-5000", 82, "global sigorta ve risk yonetimi"),
    "Aras Kargo": ("Logistics / Delivery", "5000+", 70, "kargo dagitim ve lojistik"),
    "Yurtiçi Kargo": ("Logistics / Delivery", "5000+", 68, "kargo ve lojistik operasyonlari"),
    "Teknosa": ("Retail / Electronics", "1000-5000", 74, "teknoloji perakende ve dijital donusum"),
    "MediaMarkt Türkiye": ("Retail / Electronics", "1000-5000", 78, "teknoloji perakende ve MediaSaturn is birligi"),
    "Koton": ("Retail / Fashion", "5000+", 70, "hizli moda ve uluslararasi buyume"),
    "FLO Mağazacılık": ("Retail / Footwear", "5000+", 68, "ayakkabi perakende ve marka portfoyu"),
    "Otokoç Otomotiv": ("Automotive / Rental", "1000-5000", 80, "otomotiv dagitim ve filo yonetimi"),
    "Penti": ("Retail / Fashion", "1000-5000", 70, "ic giyim perakende ve uluslararasi buyume"),
    "Şekerbank": ("Banking / Finance", "1000-5000", 72, "KOBi bankaciligi ve tarim bankaciligi"),
    "Danone Türkiye": ("FMCG / Food", "1000-5000", 86, "global gida sirketi ve beslenme odakli buyume"),
    "Türk Traktör": ("Agricultural machinery / Manufacturing", "1000-5000", 76, "tarim makineleri ve muhendislik"),
}

FIRST_NAMES = [
    "Ayse", "Mehmet", "Elif", "Can", "Zeynep", "Mert", "Derya", "Burak", "Selin", "Emre",
    "Ece", "Kerem", "Ceren", "Onur", "Deniz", "Gizem", "Berk", "Asli", "Tolga", "Irem",
]

LAST_NAMES = [
    "Yilmaz", "Kaya", "Demir", "Sahin", "Celik", "Arslan", "Aydin", "Ozturk", "Koc", "Yildiz",
    "Ozdemir", "Kilic", "Aslan", "Cetin", "Kara", "Acar", "Bulut", "Polat", "Erdem", "Kaplan",
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
    "Insan Kaynaklari Muduru",
    "Insan Kaynaklari Uzmani",
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


def profile_for(company: str) -> dict[str, object]:
    sector, size, english_intensity, growth_signal = COMPANY_PROFILES.get(
        company, ("Unknown", "Unknown", 65, "buyuyen ekip yapisi")
    )
    return {
        "sector": sector,
        "size": size,
        "english_intensity": english_intensity,
        "growth_signal": growth_signal,
    }


def build_demo_leads(limit: int = 100, seed: int | None = None) -> list[Lead]:
    rng = random.Random(seed)
    companies = list(COMPANY_PROFILES)
    leads: list[Lead] = []
    seen: set[tuple[str, str, str]] = set()

    while len(leads) < limit:
        first_name = rng.choice(FIRST_NAMES)
        last_name = rng.choice(LAST_NAMES)
        company = rng.choice(companies)
        title = rng.choice(TITLES)
        key = (f"{first_name} {last_name}", company, title)
        if key in seen:
            continue
        seen.add(key)
        search_query = f"{first_name} {last_name} {company} {title}".replace(" ", "%20")
        index = len(leads) + 1
        leads.append(
            Lead(
                lead_id=f"TR-HR-{index:03d}",
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


def build_real_leads() -> list[Lead]:
    from real_hr_leads import generate_real_leads
    real = generate_real_leads()
    return [
        Lead(
            lead_id=r.lead_id,
            full_name=r.full_name,
            company=r.company,
            title=r.title,
            linkedin_url=r.linkedin_url,
            email=r.email,
            location=r.location,
            source=r.source,
        )
        for r in real
    ]


def read_leads(path: Path) -> list[Lead]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = csv.DictReader(handle)
        return [
            Lead(
                lead_id=row.get("lead_id") or f"LEAD-{index + 1:03d}",
                full_name=row["full_name"],
                company=row["company"],
                title=row["title"],
                linkedin_url=row.get("linkedin_url", ""),
                email=row.get("email", ""),
                location=row.get("location", "Turkey"),
                source=row.get("source", "Imported CSV"),
            )
            for index, row in enumerate(rows)
        ]


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def seniority(title: str) -> str:
    normalized = title.lower()
    if "director" in normalized or "muduru" in normalized:
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
    lead_persona = persona(lead.title)
    if lead_persona == "recruitment_growth":
        return "Aday deneyiminde Ingilizce degerlendirme ve global rol iletisimini standardize etmek"
    if lead_persona == "learning_owner":
        return "Calisanlara olculebilir, olceklenebilir ve yogun programa uyumlu Ingilizce gelisim yolu kurmak"
    if lead_persona == "employee_experience":
        return "Calisan bagliligini artiran, kisiye ozel gelisim benefit'i sunmak"
    if lead_persona == "business_partner":
        return "Farkli ekiplerin Ingilizce ihtiyacini tek modelde onceliklendirmek"
    return f"{profile['growth_signal']} nedeniyle Ingilizce gelisim programini olceklendirmek"


def infer_outreach_angle(lead: Lead) -> str:
    lead_persona = persona(lead.title)
    if lead_persona == "recruitment_growth":
        return "Global aday ve ekip iletisimi icin konusma odakli Ingilizce gelisimi"
    if lead_persona == "learning_owner":
        return "L&D programlarina olculebilir konusma pratigi katmani"
    if lead_persona == "employee_experience":
        return "Calisan deneyimi benefit'i olarak esnek Ingilizce gelisimi"
    if lead_persona == "business_partner":
        return "Departman bazli Ingilizce ihtiyacini HRBP perspektifiyle haritalama"
    return "Kurumsal Ingilizce gelisimini hizli pilotla test etme"


def score_lead(lead: Lead, profile: dict[str, object]) -> int:
    base = int(profile["english_intensity"])
    title_bonus = {"Director": 8, "Manager": 6, "Lead": 5, "Partner": 4, "Specialist": 2}[seniority(lead.title)]
    sector_bonus = 5 if any(token in str(profile["sector"]).lower() for token in ["saas", "fintech", "gaming", "telecommunications"]) else 2
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
    return (
        f"Merhaba {first_name}, {lead.company} icin {lead.title} rolunuzu gordum. "
        f"{profile['sector']} tarafinda {profile['growth_signal']} nedeniyle Ingilizce iletisim kritik hale geliyor. "
        f"Konusarak Ogren'de '{angle}' basligiyla 2 haftalik kucuk bir pilot kurguluyoruz. "
        f"Eger '{pain_point}' gundeminizdeyse 15 dk fikir alisverisi yapmak isterim."
    )


def generate_email(lead: Lead, profile: dict[str, object], pain_point: str, angle: str) -> tuple[str, str]:
    first_name = lead.full_name.split()[0]
    subject = f"{lead.company} ekipleri icin konusma odakli Ingilizce pilotu"
    body = (
        f"Merhaba {first_name},\n\n"
        f"{lead.company} ekibinin {profile['sector']} olceginde {profile['growth_signal']} odagi oldugunu goruyorum. "
        f"Bu yapidaki HR ekiplerinde sik gordugumuz konu: {pain_point}.\n\n"
        f"Konusarak Ogren ile '{angle}' uzerine dusuk eforlu bir pilot tasarlayabiliriz: "
        f"seviye tespiti, hedef grup secimi, konusma pratigi ve kisa gelisim raporu.\n\n"
        f"Uygunsa bu hafta 15 dakikalik bir gorusmede {lead.company} icin mantikli pilot segmentini birlikte cikaralim.\n\n"
        f"Sevgiler,\nGrowth Automation Ekibi"
    )
    return subject, body


def enrich_lead(lead: Lead) -> dict[str, object]:
    profile = profile_for(lead.company)
    pain_point = infer_pain_point(lead, profile)
    angle = infer_outreach_angle(lead)
    score = score_lead(lead, profile)
    subject, body = generate_email(lead, profile, pain_point, angle)
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
        "email_body": body,
    }


def write_workflow_blueprint(path: Path) -> None:
    workflow = {
        "name": "Growth Automation & AI Ops HR Outbound Prototype",
        "version": "1.0",
        "nodes": [
            {"id": "lead_source", "type": "manual_or_export", "description": "LinkedIn Sales Navigator, Apollo, Clay, Google Sheets, or manually verified CSV export."},
            {"id": "cleaning", "type": "python", "description": "Normalize names, companies, titles, duplicate keys, and empty fields."},
            {"id": "enrichment", "type": "python + AI prompt layer", "description": "Infer sector, company size, persona, English need, pain point, and outreach angle."},
            {"id": "lead_scoring", "type": "rules", "description": "Score by sector intensity, company size, seniority, and role relevance."},
            {"id": "outreach_generation", "type": "AI copy generation", "description": "Generate short LinkedIn DM and cold email using lead-level context."},
            {"id": "crm_pipeline", "type": "csv_or_airtable", "description": "Route leads into Priority outreach, Warm nurture, Test sequence, or Low-touch nurture."},
        ],
        "edges": [
            ["lead_source", "cleaning"],
            ["cleaning", "enrichment"],
            ["enrichment", "lead_scoring"],
            ["lead_scoring", "outreach_generation"],
            ["outreach_generation", "crm_pipeline"],
        ],
    }
    path.write_text(json.dumps(workflow, indent=2, ensure_ascii=False), encoding="utf-8")


def run(input_csv: Path | None, limit: int, seed: int | None = None, demo: bool = False, real: bool = False) -> None:
    ensure_dirs()
    if input_csv:
        leads = read_leads(input_csv)
    elif real:
        leads = build_real_leads()
    elif demo:
        leads = build_demo_leads(limit, seed=seed)
    else:
        raise ValueError("Verified CSV gerekli. Demo data icin explicit olarak --demo kullan.")
    if not leads:
        raise ValueError("Input CSV en az bir valid lead satiri icermeli.")
    raw_rows = [lead.__dict__ for lead in leads]
    enriched_rows = [enrich_lead(lead) for lead in leads]

    write_csv(DATA_DIR / "raw_hr_leads_sample.csv", raw_rows, ["lead_id", "full_name", "company", "title", "linkedin_url", "email", "location", "source"])
    write_csv(OUTPUT_DIR / "enriched_hr_leads.csv", enriched_rows, list(enriched_rows[0].keys()))
    write_csv(
        OUTPUT_DIR / "outreach_messages.csv",
        [{"lead_id": row["lead_id"], "full_name": row["full_name"], "company": row["company"], "linkedin_dm": row["linkedin_dm"], "email_subject": row["email_subject"], "email_body": row["email_body"]} for row in enriched_rows],
        ["lead_id", "full_name", "company", "linkedin_dm", "email_subject", "email_body"],
    )
    write_csv(
        OUTPUT_DIR / "crm_pipeline.csv",
        [{"lead_id": row["lead_id"], "full_name": row["full_name"], "company": row["company"], "title": row["title"], "lead_score": row["lead_score"], "crm_stage": row["crm_stage"], "next_action": "LinkedIn connect + DM" if row["crm_stage"] == "Priority outreach" else "Email sequence / nurture"} for row in enriched_rows],
        ["lead_id", "full_name", "company", "title", "lead_score", "crm_stage", "next_action"],
    )

    sheet_rows = [
        {
            "Ad Soyad": row["full_name"],
            TR["company"]: row["company"],
            TR["title"]: row["title"],
            "LinkedIn URL": row["linkedin_url"],
            "Email": row["email"],
            TR["sector"]: row["company_sector"],
            TR["company_size"]: row["company_size"],
            "Pain point": row["likely_pain_point"],
            TR["english_need"]: row["estimated_english_need_score"],
            "Outreach angle": row["outreach_angle"],
            "LinkedIn DM": row["linkedin_dm"],
            "Cold email": f"Subject: {row['email_subject']}\n\n{row['email_body']}",
            "Lead score": row["lead_score"],
        }
        for row in enriched_rows
    ]
    sheet_fields = ["Ad Soyad", TR["company"], TR["title"], "LinkedIn URL", "Email", TR["sector"], TR["company_size"], "Pain point", TR["english_need"], "Outreach angle", "LinkedIn DM", "Cold email", "Lead score"]
    write_csv(OUTPUT_DIR / "google_sheets_hr_leads.csv", sheet_rows, sheet_fields)

    write_csv(
        OUTPUT_DIR / "workflow_steps.csv",
        [
            {"Step": "1", "Workflow": "LinkedIn Search", "Description": "HR Manager Turkey, Insan Kaynaklari Muduru, Talent Acquisition Turkey, People & Culture Manager Turkiye, Learning & Development Manager Turkey aramalariyla lead havuzu olustur."},
            {"Step": "2", "Workflow": "Google Sheets", "Description": "Ad Soyad, Sirket, Unvan, LinkedIn URL ve Email alanlarini tek tabloda topla. Email yoksa bos birak."},
            {"Step": "3", "Workflow": "Cleaning", "Description": "Duplicate kayitlari, unvan varyasyonlarini, sirket adlarini ve bos alanlari normalize et."},
            {"Step": "4", "Workflow": "AI Enrichment", "Description": "Sirket, unvan ve sektor uzerinden pain point, Ingilizce ihtiyaci tahmini ve outreach angle uret."},
            {"Step": "5", "Workflow": "Outreach Generation", "Description": "Her lead icin sirket + unvan + ihtiyac baglamiyla kisa LinkedIn DM ve cold email uret."},
            {"Step": "6", "Workflow": "CRM Status", "Description": "Lead score'a gore Priority outreach, Warm nurture, Test sequence veya Low-touch nurture stage'ine ata."},
        ],
        ["Step", "Workflow", "Description"],
    )
    write_workflow_blueprint(WORKFLOW_DIR / "workflow_blueprint.json")

    print(f"Generated {len(leads)} raw leads")
    print(f"Wrote {OUTPUT_DIR / 'google_sheets_hr_leads.csv'}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Growth Automation & AI Ops HR outbound prototype")
    parser.add_argument("--input-csv", type=Path, help="Verified raw lead CSV to process.")
    parser.add_argument("--demo", action="store_true", help="Generate demo seed data explicitly for local testing.")
    parser.add_argument("--real", action="store_true", help="Generate 100 real verified HR leads from public data.")
    parser.add_argument("--limit", type=int, default=100, help="Number of demo leads to generate with --demo.")
    parser.add_argument("--seed", type=int, help="Optional random seed for reproducible Turkish HR demo leads.")
    args = parser.parse_args()
    if not args.input_csv and not args.demo and not args.real:
        parser.error("Gercek/verifiye veri icin --input-csv data/verified_leads.csv kullan. Demo test icin --demo, gercek lead icin --real ekle.")
    if args.input_csv and not args.input_csv.exists():
        parser.error(f"Input CSV bulunamadi: {args.input_csv}")
    return args


if __name__ == "__main__":
    args = parse_args()
    run(args.input_csv, args.limit, seed=args.seed, demo=args.demo, real=getattr(args, 'real', False))
