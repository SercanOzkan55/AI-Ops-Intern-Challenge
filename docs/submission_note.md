# Challenge Submission Note

## 1. Ne yaptım?

Konuşarak Öğren'in Türkiye'deki HR profesyonellerine outbound büyüme yapabilmesi için minimum çalışan bir growth automation prototipi kurdum.

Sistem şu çıktıları üretiyor:

- 100 kişilik HR lead sample listesi
- Şirket sektörü ve büyüklüğü
- Kişinin HR rolüne göre persona
- Olası pain point
- İngilizce ihtiyacı tahmini
- Outreach angle
- Lead score
- Kişiselleştirilmiş LinkedIn DM
- Kişiselleştirilmiş cold email
- CRM stage ve next action

## 2. Nasıl çalışıyor?

Önce lead listesi alınır. Demo'da bu liste script tarafından üretilir; gerçek kullanımda LinkedIn Sales Navigator, Apollo, Clay veya manuel doğrulanmış CSV kullanılabilir.

Sonra Python script'i lead'leri zenginleştirir. Şirket profili, sektör, büyüklük, rol ve persona sinyallerinden olası İngilizce ihtiyacı çıkarır. Bu sinyallerle outreach mesajı oluşturur ve lead'i CRM stage'e atar.

## 3. Neden böyle kurdum?

Bu challenge'da önemli olan sadece data toplamak değil, tekrar edilebilir bir sistem mantığı göstermekti. Bu yüzden tek bir CSV hazırlamak yerine:

- Data ingestion
- Cleaning
- Enrichment
- Outreach generation
- Lead scoring
- CRM routing

akışını ayrı parçalar olarak tasarladım.

## 4. Demo nasıl test edilir?

```bash
python src/growth_ai_ops_prototype.py
```

Çalıştırınca şu dosyalar oluşur:

- `data/raw_hr_leads_sample.csv`
- `output/enriched_hr_leads.csv`
- `output/outreach_messages.csv`
- `output/crm_pipeline.csv`
- `workflows/workflow_blueprint.json`

## 5. AI nerede kullanılıyor?

Bu prototipte AI mantığı şu alanlarda modellenmiştir:

- Şirket bağlamından İngilizce ihtiyaç tahmini
- Role göre HR persona çıkarımı
- Pain point üretimi
- Outreach angle üretimi
- Kişiselleştirilmiş DM/email oluşturma
- Reply classification için blueprint

Production versiyonda bu enrichment ve copy generation katmanı OpenAI/Claude gibi bir LLM API'sine bağlanabilir. Demo versiyonunda deterministic fallback var; böylece API key olmadan da çalışır.

## 6. Gerçek hayatta nasıl büyütürdüm?

İlk hedefim 100 lead değil, haftalık tekrar eden bir outbound makinesi kurmak olurdu:

1. Haftalık yeni lead export.
2. Duplicate kontrolü.
3. AI enrichment.
4. Lead scoring.
5. Multi-step LinkedIn + email sequence.
6. Reply classification.
7. CRM stage update.
8. Pozitif yanıtları satış görüşmesine yönlendirme.

Bu yapı 2 gün içinde MVP olarak kurulabilir, sonra reply rate ve meeting conversion'a göre sürekli optimize edilir.
