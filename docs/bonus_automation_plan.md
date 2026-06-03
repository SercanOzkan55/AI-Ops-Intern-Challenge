# Bonus Automation Plan

## 1. LinkedIn Account Warming

Amaç, outbound başlamadan önce hesabın doğal ve güvenilir görünmesini sağlamak.

Plan:

- İlk 7 gün sadece profil optimizasyonu, içerik etkileşimi ve düşük hacimli connection.
- Günlük 5-10 hedef ICP profil ziyareti.
- Günlük 3-5 anlamlı yorum veya tepki.
- İlk hafta satış mesajı yok.
- İkinci hafta connection request başlar, DM hacmi kademeli artar.

Örnek connection note:

```text
Merhaba {first_name}, HR ve çalışan gelişimi tarafındaki paylaşımlarınızı gördüm.
Türkiye'de kurumsal İngilizce gelişimi üzerine çalışıyoruz, bağlantıda kalmak isterim.
```

## 2. Multi-Step Outreach Sequence

| Gün | Kanal | Mesaj |
|---:|---|---|
| 0 | LinkedIn | Profil ziyareti + connection request |
| 1 | Email | Kısa kişiselleştirilmiş problem/çözüm email'i |
| 3 | LinkedIn | Kabul ettiyse 300 karakterlik DM |
| 6 | Email | Mini case/pilot önerisi |
| 10 | Email | Breakup email: "Doğru kişi siz misiniz?" |
| 20 | Nurture | Faydalı içerik veya HR benchmark notu |

## 3. Inbox Automation

Reply classification sınıfları:

- `interested`: toplantı veya detay istiyor
- `objection_price`: fiyat/öncelik itirazı
- `not_now`: zamanlama uygun değil
- `wrong_person`: başka kişiye yönlendiriyor
- `unsubscribe`: iletişim istemiyor
- `bounce`: email ulaşmadı

AI classifier prompt:

```text
You are classifying B2B outbound replies for an HR-focused English learning product.
Return only JSON with: category, confidence, recommended_next_action, short_reason.

Reply:
{{reply_text}}
```

## 4. Lead Scoring

Skor sinyalleri:

- Sektör İngilizce yoğunluğu
- Şirket büyüklüğü
- Global operasyon sinyali
- HR karar verici seniority
- L&D / Talent / HRBP rol uyumu
- Email veya LinkedIn doğrulanmışlığı
- Önceki engagement

Örnek:

| Signal | Puan |
|---|---:|
| Global/SaaS/fintech/gaming sektörü | +10 |
| 1000+ çalışan | +8 |
| Director/Head/Manager | +8 |
| L&D veya HRBP rolü | +6 |
| Doğrulanmış business email | +5 |
| LinkedIn accepted connection | +7 |

## 5. Deliverability Mantığı

Email tarafı:

- Tek domain ile yüksek hacim yapılmaz.
- SPF, DKIM, DMARC kurulu olmalı.
- İlk hafta düşük hacim, sonra kademeli artış.
- Bounce rate yakından izlenir.
- Unsubscribe talepleri otomatik bastırılır.
- Generic bulk copy yerine segment bazlı mesaj yazılır.

LinkedIn tarafı:

- Connection ve DM hacmi kademeli artırılır.
- Aynı mesaj 100 kişiye birebir kopyalanmaz.
- Önce profil ziyareti ve hafif etkileşim yapılır.
- Kabul etmeyen kişiye agresif takip yapılmaz.

## 6. CRM Pipeline

Pipeline stage'leri:

| Stage | Açıklama |
|---|---|
| New lead | Yeni eklendi |
| Enriched | AI enrichment tamamlandı |
| Priority outreach | İlk temas öncelikli |
| Contacted | İlk mesaj gönderildi |
| Replied | Yanıt geldi |
| Meeting booked | Toplantı alındı |
| Nurture | Şimdilik sıcak değil |
| Closed lost | Uygun değil |

## 7. AI Agent Workflow

Agent görevleri:

1. Yeni lead CSV'ini kontrol et.
2. Eksik şirket bilgisini enrich et.
3. Persona ve pain point üret.
4. Mesajı üret.
5. CRM'e kaydet.
6. Yanıt geldiğinde sınıflandır.
7. Pozitif yanıtı Slack/Email ile sales owner'a bildir.

Bu yapı n8n veya Make üzerinde node'lara bölünebilir; Python script'i ise enrichment ve copy generation motoru olarak kullanılabilir.
