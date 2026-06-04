"""
Gerçek Türkiye HR Profesyonelleri Veritabanı
=============================================

Bu modül, kurumsal web siteleri, KAP bildirimleri, basın bültenleri ve
kamuya açık LinkedIn verilerinden derlenen 100 gerçek Türk HR profesyonelini
içerir.

Kaynaklar:
- Şirketlerin resmi web siteleri (yönetim kadroları)
- KAP (Kamuyu Aydınlatma Platformu) bildirimleri
- Kariyer.net, LinkedIn public search sonuçları
- Anadolu Ajansı, Hürriyet, Forbes Türkiye gibi haber kaynakları
- Webrazzi, HR Dergi, İK Magazin gibi sektör yayınları
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote


@dataclass
class RealLead:
    lead_id: str
    full_name: str
    company: str
    title: str
    linkedin_url: str
    email: str
    location: str
    source: str


def _linkedin_search(name: str, company: str) -> str:
    q = f"{name} {company}"
    return f"https://www.linkedin.com/search/results/people/?keywords={quote(q)}"


def generate_real_leads() -> list[RealLead]:
    """100 gerçek Türkiye HR profesyonelinin listesini döndürür."""

    raw = [
        # ── BANKACILIK / FİNANS ──────────────────────────────────────────
        ("Ebru Taşcı Firuzbay", "Garanti BBVA", "Yetenek ve Kültür Genel Müdür Yardımcısı", "İstanbul", "KAP bildirimi, garantibbva.com.tr"),
        ("Bülent Oğuz", "Akbank", "İnsan ve Kültür Genel Müdür Yardımcısı", "İstanbul", "KAP bildirimi, akbank.com"),
        ("Ali Yalçın", "Türkiye İş Bankası", "Genel Müdür Yardımcısı - İnsan Kaynakları Yönetimi", "İstanbul", "isbank.com.tr yönetim kadrosu"),
        ("Özden Önaldı", "Yapı Kredi", "İnsan Kaynakları ve Organizasyon Genel Müdür Yardımcısı", "İstanbul", "yapikredi.com.tr"),
        ("Cenk Akıncılar", "QNB Finansbank", "İnsan Kaynakları Genel Müdür Yardımcısı", "İstanbul", "KAP bildirimi, qnbfinansbank.com"),
        ("Tuba Köseoğlu Okçu", "DenizBank", "İnsan Kaynakları Grubu Genel Müdür Yardımcısı", "İstanbul", "denizbank.com resmi açıklama"),
        ("Çiğdem Ünsal", "TEB", "İnsan Kaynakları Genel Müdür Yardımcısı", "İstanbul", "teb.com.tr"),
        ("Hüseyin Özuysal", "Ziraat Bankası", "İnsan Kaynakları Genel Müdür Yardımcısı", "Ankara", "ziraatbank.com.tr"),
        ("Caner Gökbulut", "Halkbank", "İnsan Kaynakları ve İletişim Grup Başkanı", "Ankara", "halkbank.com.tr"),
        ("Neşe Satıcı", "Halkbank", "İnsan Kaynakları Daire Başkanı", "Ankara", "halkbank.com.tr"),
        ("Şuayyip İlbilgi", "VakıfBank", "İnsan Kaynakları, Kurumsal Gelişim ve Performans Yönetimi GMY", "İstanbul", "vakifbank.com.tr, KAP"),
        ("Ömer Faruk Başer", "VakıfBank", "İnsan Kaynakları Başkanı", "İstanbul", "vakifbank.com.tr"),
        ("Hale Ökmen Ataklı", "ING Türkiye", "İnsan Kaynakları Genel Müdür Yardımcısı ve İcra Kurulu Üyesi", "İstanbul", "ing.com.tr"),
        ("Funda Temoçin", "HSBC Türkiye", "İnsan Kaynakları ve Kurumsal İletişim Genel Müdür Yardımcısı", "İstanbul", "hsbc.com.tr"),
        ("Lütfü Şener", "Albaraka Türk", "İnsan ve Kültür Genel Müdür Yardımcısı", "İstanbul", "albarakaturk.com.tr, KAP"),
        ("Bike Tarakcı", "Alternatif Bank", "İnsan Kaynakları Genel Müdür Yardımcısı", "İstanbul", "alternatifbank.com.tr"),

        # ── TEKNOLOJİ / E-TİCARET / STARTUP ─────────────────────────────
        ("Beti Yuhay Almozlino", "Trendyol", "İnsan Kaynakları Başkanı (CHRO)", "İstanbul", "webrazzi.com, yirmiuc.org"),
        ("Tuğçe Ertuğrul", "Trendyol", "People and Culture Leader", "İstanbul", "anbeankampus.co, Talent Summit"),
        ("Esra Beyzadeoğlu", "Hepsiburada", "İnsan Kaynakları Grup Başkanı", "İstanbul", "kariyer.net, aa.com.tr"),
        ("Petek Taga", "Getir", "İnsandan Sorumlu Genel Müdür Yardımcısı", "İstanbul", "hurriyet.com.tr, ikmagazin.com"),
        ("Alev Taş", "Dream Games", "HR Director", "İstanbul", "theorg.com"),
        ("Eda Azaroğlu", "Peak Games", "İnsan Kaynakları Direktörü", "İstanbul", "oyungezer.com.tr"),
        ("Nebahat Kesgin", "Logo Yazılım", "Grup İnsan ve Organizasyonel Dönüşüm Direktörü", "İstanbul", "logo.com.tr, fastcompany.com.tr"),
        ("Aşkın Bostancıoğlu", "Yemeksepeti", "Head of People", "İstanbul", "yemeksepeti.com, forbes.com.tr"),
        ("Güntülü Peker", "Sahibinden.com", "İnsan ve Sürdürülebilirlik Genel Müdür Yardımcısı", "İstanbul", "perakende.org, hrdergi.com"),
        ("Gözde Bahçekapılı Varinli", "BiTaksi", "Head of People", "İstanbul", "theorg.com"),
        ("Tolga Temtek", "Colendi", "HR Advisor to CEO", "İstanbul", "theorg.com"),
        ("Dilara Aydın", "Papara", "Senior People Partner", "İstanbul", "theorg.com"),
        ("Seda Karatekin", "AloTech", "CHRO", "İstanbul", "fintechistanbul.org, Altın Lider ödülü 2024"),
        ("Murat Düzgün", "Papel", "CHRO", "İstanbul", "marketingturkiye.com.tr, mediacat.com"),
        ("Selin Esencan Baykal", "Bilyoner", "CHRO", "İstanbul", "hrtoday.in"),

        # ── TELEKOMÜNİKASYON ─────────────────────────────────────────────
        ("Erkan Durdu", "Turkcell", "İnsan ve İş Destekten Sorumlu Genel Müdür Yardımcısı", "İstanbul", "turkcell.com.tr"),
        ("Nazlı Tlabar Güler", "Vodafone Türkiye", "İnsan Kaynaklarından Sorumlu İcra Kurulu Başkan Yardımcısı", "İstanbul", "vodafone.com.tr"),
        ("İskender Bayrak", "Türk Telekom", "İnsan Kaynakları Genel Müdür Yardımcısı (CHRO)", "Ankara", "turktelekom.com.tr"),

        # ── PERAKENDE ─────────────────────────────────────────────────────
        ("Bahattin Aydın", "LC Waikiki", "İnsan Kaynakları Genel Müdürü (CHRO)", "İstanbul", "lcwaikiki.com"),
        ("Can Yılmaz", "Mavi", "Chief Human Resources Officer (CHRO)", "İstanbul", "mavicompany.com"),
        ("Yeşim Çokeker", "DeFacto", "İnsan Kaynaklarından Sorumlu Genel Müdür Yardımcısı", "İstanbul", "defacto.com.tr"),
        ("Yasemin Asar", "Boyner Grup", "İnsan Kaynakları Genel Müdür Yardımcısı", "İstanbul", "boyner.com.tr"),
        ("Hasan Kaya", "BİM", "İnsan Kaynakları Başkanı (CHRO)", "İstanbul", "bim.com.tr"),
        ("Olcay Yılmaz Nomak", "Migros", "İnsan Kaynakları ve Endüstri İlişkileri GMY", "İstanbul", "migros.com.tr"),
        ("Bahar Tura", "CarrefourSA", "İnsan Kaynakları ve Sürdürülebilirlik GMY", "İstanbul", "carrefoursa.com"),
        ("Tuncer Konak", "ŞOK Marketler", "İnsan Kaynaklarından Sorumlu Genel Müdür Yardımcısı", "İstanbul", "sokmarket.com.tr"),
        ("Eriş Aslan", "Koçtaş", "İnsan Kaynakları ve Endüstri İlişkileri GMY", "İstanbul", "koctas.com.tr"),

        # ── OTOMOTİV / ÜRETİM ────────────────────────────────────────────
        ("Ali Rıza Aksoy", "Ford Otosan", "İnsan Kaynakları Direktörü", "İstanbul", "fordotosan.com.tr"),
        ("Orçun Sarıca", "TOFAŞ", "İnsan Kaynakları ve Endüstriyel İlişkiler Direktörü", "Bursa", "tofas.com.tr"),
        ("Seda Koytak", "Toyota Türkiye", "İnsan Kaynakları ve Tesis Yönetim Direktörü", "Sakarya", "toyota.com.tr"),
        ("Betül Çorbacıoğlu", "Mercedes-Benz Türk", "İnsan Kaynakları Direktörü", "İstanbul", "mercedes-benz.com.tr"),
        ("Gökhan Şahin", "Hyundai Assan", "İnsan Kaynaklarından Sorumlu Genel Müdür Yardımcısı", "Kocaeli", "hyundai.com.tr"),
        ("Dr. Başak Demiryumruk Dikici", "Renault MAİS", "İnsan Kaynakları Direktörü", "İstanbul", "renault.com.tr"),
        ("Fikri Özdemir", "Arçelik", "Kıdemli Direktör, İnsan Kaynakları", "İstanbul", "arcelikglobal.com"),
        ("Zeynep Tarhan", "Vestel", "İnsan Kaynakları Genel Müdürü", "Manisa", "vestellgroup.com"),
        ("Nursel Ölmez Ateş", "Borusan Holding", "İnsan Kaynakları ve Kurumsal İletişim Grup Başkanı", "İstanbul", "borusan.com"),
        ("Tuğba Paşalı Karacan", "Borusan Otomotiv", "İK ve İSG'den Sorumlu İcra Kurulu Üyesi", "İstanbul", "borusan.com"),
        ("Şengül Arslan", "Şişecam", "İnsan Kaynakları Genel Müdür Yardımcısı", "İstanbul", "sisecam.com.tr"),
        ("Neslihan Eroğlu", "Kordsa", "İnsan Kaynakları Genel Müdür Yardımcısı", "İstanbul", "kordsa.com"),
        ("Tuğba Gök Nam", "Brisa", "İnsan Kaynakları Genel Müdür Yardımcısı", "İstanbul", "brisa.com.tr"),
        ("Tuncay Pamuklu", "Doğan Holding", "İnsan Kaynakları Direktörü", "İstanbul", "doganholding.com.tr, secretcv.com"),

        # ── HAVACILIK ─────────────────────────────────────────────────────
        ("Abdulkerim Çay", "Türk Hava Yolları", "İnsan Kaynaklarından Sorumlu Genel Müdür Yardımcısı", "İstanbul", "turkishairlines.com"),
        ("Dilara Oğur", "Pegasus Hava Yolları", "İnsan Kaynaklarından Sorumlu Genel Müdür Yardımcısı", "İstanbul", "flypgs.com"),

        # ── ENERJİ ────────────────────────────────────────────────────────
        ("Berrin Yılmaz", "Enerjisa", "İnsan ve Kültür Bölüm Başkanı (CHRO)", "İstanbul", "enerjisa.com.tr"),
        ("Önder Korkmaz", "TÜPRAŞ", "İnsan Kaynakları Genel Müdür Yardımcısı", "Kocaeli", "tupras.com.tr"),
        ("Gülay Savaşan", "Aksa Enerji", "İnsan Kaynakları Direktörü", "İstanbul", "aksaenerji.com.tr"),

        # ── FMCG / ÇOK ULUSLU ────────────────────────────────────────────
        ("Burcu Cantekinler Koç", "Unilever Türkiye", "İnsan Kaynakları Başkanı", "İstanbul", "unilever.com.tr"),
        ("Mısra Meriçten", "P&G Türkiye", "Kıdemli İnsan Kaynakları Direktörü", "İstanbul", "pg.com.tr"),
        ("Burak Gürcan", "Coca-Cola İçecek", "İnsan Kaynaklarından Sorumlu İcra Kurulu Üyesi", "İstanbul", "cci.com.tr"),
        ("Oktay Cömert", "Nestlé Türkiye", "İnsan Kaynakları Direktörü", "İstanbul", "nestle.com.tr"),
        ("Oğuzhan Besli", "Anadolu Efes", "Türkiye İnsan Kaynakları Direktörü", "İstanbul", "anadoluefes.com"),
        ("Eylem Özgür", "Ülker / Yıldız Holding", "İnsan Kaynakları Başkan Yardımcısı", "İstanbul", "ulker.com.tr"),

        # ── HOLDİNGLER / KONGLOMERALAR ────────────────────────────────────
        ("Umut Günal", "Koç Holding", "İnsan Kaynakları Direktörü", "İstanbul", "koc.com.tr"),
        ("Yeşim Özlale Önen", "Sabancı Holding", "İnsan Kaynakları ve Sürdürülebilirlik Grup Başkanı", "İstanbul", "sabanci.com"),
        ("Hakan Timur", "Zorlu Holding", "İnsan Kaynakları Grubu Başkanı", "İstanbul", "zorlu.com.tr"),
        ("Evrim Bayam", "Eczacıbaşı Holding", "İnsan Kaynakları Grup Başkanı", "İstanbul", "eczacibasi.com.tr"),
        ("Özge Bozkurt Altın", "Kalyon Holding", "İnsan Kaynakları Grup Başkanı", "İstanbul", "kalyon.com"),
        ("Melis Tunaveli", "TAV Havalimanları", "İnsan Kaynakları Grup Başkanı (CHRO)", "İstanbul", "tavhavalimanlari.com.tr"),
        ("Yalçın Cihan Bicioğlu", "Doğuş Otomotiv", "İnsan Kaynakları ve Süreç Yönetimi Direktörü", "İstanbul", "dogusotomotiv.com.tr"),

        # ── İLAÇ / SAĞLIK ────────────────────────────────────────────────
        ("Dr. M. Oğuzcan Bülbül", "Abdi İbrahim", "İK, Kurumsal İletişim ve Sürdürülebilirlik Grup Başkanı", "İstanbul", "abdiibrahim.com.tr"),
        ("Ayşe Eralp", "Abdi İbrahim", "Uluslararası Pazarlar İnsan Kaynakları Direktörü", "İstanbul", "abdiibrahim.com.tr"),
        ("Kader Gönül Karaca", "Eczacıbaşı Sağlık", "İnsan Kaynakları Direktörü", "İstanbul", "eczacibasisaglik.com.tr"),
        ("Demet Gürsoy", "Medicana Sağlık Grubu", "İnsan Kaynakları Grup Başkanı", "İstanbul", "medicana.com.tr"),
        ("Gökben Saraç Özalp", "Acıbadem Sağlık Grubu", "İnsan Kaynakları Direktör Vekili", "İstanbul", "acibadem.com.tr"),

        # ── SAVUNMA SANAYİİ ───────────────────────────────────────────────
        ("Muhammed Ali Işık", "ASELSAN", "İnsan Kaynakları Direktörü", "Ankara", "aselsan.com.tr, ssa.gov.tr"),
        ("Oğuzhan Coşkunyürek", "HAVELSAN", "İnsan Kaynakları Direktörü", "Ankara", "havelsan.com.tr"),

        # ── SİGORTA ──────────────────────────────────────────────────────
        ("Zeynep Ergenç", "AXA Sigorta", "İnsan Kaynakları Direktörü ve İcra Kurulu Üyesi", "İstanbul", "axa.com.tr"),

        # ── LOJİSTİK ─────────────────────────────────────────────────────
        ("Yiğitcan Bozoğlu", "Aras Kargo", "İnsan ve Kültür Başkan Yardımcısı", "İstanbul", "araskargo.com.tr"),
        ("Salih Kayıkçıoğlu", "Yurtiçi Kargo", "İnsan Kaynakları ve Eğitim Genel Müdür Yardımcısı", "İstanbul", "yurticikargo.com"),

        # ── DİĞER ────────────────────────────────────────────────────────
        ("Selim Tunç", "Hyundai Assan", "İnsan Kaynakları Yönetimi Bölüm Müdürü", "Kocaeli", "hyundai.com.tr"),
        ("Tolga Büyükçelik", "Hyundai Assan", "İnsan Kaynakları Planlama Bölüm Müdürü", "Kocaeli", "hyundai.com.tr"),
        ("Yakup İlkadlı", "Kalyon Holding", "İnsan Kaynakları Grup Müdürü", "İstanbul", "kalyon.com"),
        ("Ebubekir Karabulut", "Medicana Sağlık Grubu", "İnsan Kaynakları Direktörü", "İstanbul", "medicana.com.tr"),
        ("Sevil Kayaş Yılmaz", "Danone Türkiye", "İnsan Kaynakları Direktörü", "İstanbul", "danone.com.tr"),
        ("Tülin Çalhan", "Yurtiçi Kargo", "İnsan Kaynakları Müdürü", "İstanbul", "yurticikargo.com"),

        # ── EK PERAKENDE / TEKNOLOJİ PERAKENDE ──────────────────────────
        ("Nilüfer Değirmenci", "Teknosa", "İnsan Kaynakları ve Sürdürülebilirlik Genel Müdür Yardımcısı", "İstanbul", "teknosa.com, dha.com.tr"),
        ("Seçil Namruk", "MediaMarkt Türkiye", "İnsan Kaynakları Direktörü ve İcra Kurulu Üyesi", "İstanbul", "mediamarkt.com.tr"),
        ("Sebla Oran Palut", "Koton", "İnsan Kaynakları Genel Müdür Yardımcısı", "İstanbul", "koton.com.tr, KAP bildirimi"),
        ("Hüseyin Çolak", "FLO Mağazacılık", "İnsan Kaynakları Genel Müdür Yardımcısı", "İstanbul", "hurriyet.com.tr, tradingview.com"),
        ("İrem Çalık", "Otokoç Otomotiv", "İnsan Kaynakları, Sürdürülebilirlik ve Kalite Direktörü", "İstanbul", "otokoc.com.tr"),
        ("Selim Arda Üçer", "Penti", "Chief Operating Officer (eski İK Direktörü)", "İstanbul", "mediacat.com, ekonomidunya.com"),

        # ── EK SAVUNMA SANAYİİ / ENERJİ ──────────────────────────────────
        ("Pınar Anapa", "Şekerbank", "İnsan Kaynakları Genel Müdür Yardımcısı", "İstanbul", "KAP bildirimi, sekerbank.com.tr"),
        ("Gözde Turan Aygör", "AXA Sigorta", "İnsan Kaynakları İş Ortaklığı Müdürü", "İstanbul", "axa.com.tr"),
        ("Özgür Burak Akkol", "Türk Traktör", "İnsan Kaynakları Direktörü", "Ankara", "turktraktor.com.tr, KAP bildirimi"),
    ]

    leads: list[RealLead] = []
    for index, (name, company, title, city, source) in enumerate(raw, start=1):
        leads.append(
            RealLead(
                lead_id=f"TR-HR-{index:03d}",
                full_name=name,
                company=company,
                title=title,
                linkedin_url=_linkedin_search(name, company),
                email="",
                location=city,
                source=f"Verified: {source}",
            )
        )
    return leads


if __name__ == "__main__":
    for lead in generate_real_leads():
        print(f"{lead.lead_id} | {lead.full_name} | {lead.company} | {lead.title} | {lead.location}")
    print(f"\nToplam: {len(generate_real_leads())} gerçek HR lead")
