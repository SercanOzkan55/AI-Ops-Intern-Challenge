# Growth Automation & AI Ops Intern Challenge

Bu repo, Konuşarak Öğren için Türkiye'deki insan kaynakları profesyonellerine yönelik minimum çalışan bir outbound growth automation prototipidir.

Amaç: 100 lead'lik örnek HR listesi oluşturmak, lead'leri zenginleştirmek, kişiselleştirilmiş LinkedIn DM / cold email üretmek, lead scoring yapmak ve süreci CRM mantığıyla yönetilebilir hale getirmek.

## Demo

- Lokal GUI: `python src/gui_app.py`
- Lokal adres: `http://127.0.0.1:8765`
- GitHub Pages: Repo Settings > Pages veya Actions tamamlandıktan sonra yayınlanır.

## Teslim Özeti

| Dosya | Açıklama |
|---|---|
| `src/growth_ai_ops_prototype.py` | Lead üretimi, enrichment, outreach generation ve CRM pipeline motoru |
| `src/gui_app.py` | Lokal web arayüzü |
| `data/raw_hr_leads_sample.csv` | 100 kişilik Türkiye HR lead sample listesi |
| `output/google_sheets_hr_leads.csv` | Google Sheets kolonlarıyla ana teslim tablosu |
| `output/konusarak-ogren-hr-outbound-google-sheets.xlsx` | Google Sheets/Excel'e import edilebilir workbook |
| `output/enriched_hr_leads.csv` | Detaylı enrichment çıktısı |
| `output/outreach_messages.csv` | LinkedIn DM ve cold email çıktıları |
| `output/crm_pipeline.csv` | Lead score ve CRM stage çıktısı |
| `workflows/workflow_blueprint.json` | n8n/Make mantığına çevrilebilir workflow blueprint |
| `docs/index.html` | GitHub Pages statik demo sayfası |
| `docs/bonus_automation_plan.md` | Bonus otomasyon yaklaşımı |

## Nasıl Çalışır?

Sistem şu akışı takip eder:

```text
LinkedIn Search
→ Google Sheets
→ Cleaning
→ AI Enrichment
→ Outreach Generation
→ CRM Status
```

Bu prototip doğrudan LinkedIn scraping yapmaz ve kişisel email uydurmaz. Challenge metnindeki "varsa email" beklentisine uygun şekilde email bulunmuyorsa boş bırakılır. Gerçek kullanımda LinkedIn Sales Navigator, Apollo, Clay veya manuel doğrulanmış CSV export sisteme input olarak verilebilir.

## Google Sheets Kolonları

Ana çıktı şu kolonlarla üretilir:

```text
Ad Soyad | Şirket | Ünvan | LinkedIn URL | Email | Sektör | Şirket büyüklüğü | Pain point | İngilizce ihtiyacı tahmini | Outreach angle | LinkedIn DM | Cold email | Lead score
```

## Çalıştırma

Python dışında zorunlu dependency yok.

```bash
python src/growth_ai_ops_prototype.py
```

Bu komut şu dosyaları günceller:

- `data/raw_hr_leads_sample.csv`
- `output/google_sheets_hr_leads.csv`
- `output/enriched_hr_leads.csv`
- `output/outreach_messages.csv`
- `output/crm_pipeline.csv`
- `output/workflow_steps.csv`

Lokal GUI için:

```bash
python src/gui_app.py
```

Sonra tarayıcıda aç:

```text
http://127.0.0.1:8765
```

GUI içinde:

- Mevcut 100 lead tablosu görüntülenir.
- `Yeni 100 Lead Üret` butonu Türkiye odaklı yeni random HR lead seti üretir.
- CSV ve XLSX çıktıları indirilebilir.
- Workflow adımları görünür.

## Kendi CSV'ini İşleme

Gerçek veriyle çalışmak için:

```bash
python src/growth_ai_ops_prototype.py --input-csv data/verified_leads.csv
```

Beklenen kolonlar:

```text
lead_id,full_name,company,title,linkedin_url,email,location,source
```

## Lead Zenginleştirme

Her lead için şu sinyaller üretilir:

| Alan | Açıklama |
|---|---|
| `Sektör` | Şirketin ana faaliyet alanı |
| `Şirket büyüklüğü` | Tahmini çalışan ölçeği |
| `Pain point` | Ünvan + şirket bağlamından olası HR problemi |
| `İngilizce ihtiyacı tahmini` | 0-100 arası ihtiyaç yoğunluğu |
| `Outreach angle` | Kişiselleştirilmiş satış yaklaşımı |
| `Lead score` | Önceliklendirme skoru |

## AI Outreach Sistemi

Sistem her kişi için iki kısa mesaj üretir:

- LinkedIn DM
- Cold email

Mesajlar generic değildir; şirket, sektör, ünvan, pain point ve outreach angle sinyallerini kullanır.

Örnek:

```text
Merhaba Ayse, Trendyol için Human Resources Director rolünüzü gördüm.
E-commerce / Marketplace tarafında hızlı ölçeklenen ekipler ve uluslararası operasyon nedeniyle İngilizce iletişim kritik hale geliyor.
Konuşarak Öğren'de 'Kurumsal İngilizce gelişimini hızlı pilotla test etme' başlığıyla 2 haftalık küçük bir pilot kurguluyoruz.
Eğer 'Hızlı ölçeklenen ekipler ve uluslararası operasyon nedeniyle İngilizce gelişim programını ölçeklemek' gündeminizdeyse 15 dk fikir alışverişi yapmak isterim.
```

## CRM Pipeline

Lead score'a göre stage atanır:

| Lead score | Stage | Aksiyon |
|---:|---|---|
| 90+ | Priority outreach | LinkedIn connect + kısa DM |
| 82-89 | Warm nurture | Email + LinkedIn follow-up |
| 74-81 | Test sequence | Düşük frekanslı sequence |
| <74 | Low-touch nurture | İleri tarihli nurture |

## Bonus Kapsamı

`docs/bonus_automation_plan.md` içinde şu başlıklar yer alır:

- LinkedIn account warming yaklaşımı
- AdsPower / anti-detect setup notları
- Inbox automation
- AI agent workflow
- Auto-reply classification
- Lead scoring
- CRM pipeline
- Deliverability mantığı
- Multi-step outreach kurgusu

Aktif çalışan kısım: lead generation, enrichment, outreach generation, lead scoring, CRM stage ve lokal GUI.

## GitHub Pages

`docs/index.html` statik demo sayfasıdır. GitHub Actions workflow'u `docs` klasörünü Pages'e deploy edecek şekilde eklendi:

```text
.github/workflows/pages.yml
```

Workflow çalışınca repo için Pages linki GitHub tarafından üretilecektir.

## Not

Bu çalışma challenge için MVP/prototip mantığında hazırlanmıştır. Gerçek production kullanımında veri kaynağı izinli export/API olmalı, email deliverability kuralları uygulanmalı ve LinkedIn otomasyonunda platform kurallarına uyulmalıdır.
