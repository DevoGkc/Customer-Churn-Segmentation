# Müşteri Kayıp (Churn) ve Segmentasyon Analizi

Bu proje, bir şirketin müşteri tabanını SQL tabanlı segmentasyon (RFM mantığı) ile analiz etmek ve müşteri kayıp (churn) risklerini belirlemek amacıyla geliştirilmiştir.

## Kullanılan Teknolojiler
- **SQL (SQLite3):** Veri manipülasyonu, koşullu segmentasyon (CASE-WHEN yapısı)
- **Python:** Pandas, NumPy, Seaborn, Matplotlib

## Proje Adımları & Sonuçlar
1. `sqlite3` ile bellek üzerinde ilişkisel bir veri tabanı oluşturulmuş ve müşteri verileri yüklenmiştir.
2. SQL sorguları kullanılarak müşteriler son işlem tarihlerine ve harcama miktarlarına göre segmentlere ayrılmıştır.
3. Elde edilen segmentlerin Churn (terk etme) oranları Python veri görselleştirme kütüphaneleri ile analiz edilerek iş kararlarına yönelik grafikler üretilmiştir.
