import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Gelecek versiyon uyarılarını tamamen sessize alalım
warnings.filterwarnings('ignore')

print("1. Adım: Sahte veri tabanı ve müşteri verileri oluşturuluyor...")
# Hafızada geçici bir SQL veri tabanı oluşturuyoruz
conn = sqlite3.connect(':memory:')

# 100 müşteri için mantıklı veriler üretiyoruz
np.random.seed(42)
customer_data = pd.DataFrame({
    'customer_id': range(1001, 1101),
    'age': np.random.randint(22, 60, size=100),
    'tenure_months': np.random.randint(1, 48, size=100),
    'total_spent': np.round(np.random.uniform(100, 5000, size=100), 2),
    'last_transaction_days_ago': np.random.randint(1, 150, size=100),
    'churn_label': np.random.choice([0, 1], size=100, p=[0.7, 0.3]) # 1 = Terk etmiş, 0 = Aktif
})

# Veriyi 'customers' adında bir SQL tablosuna yüklüyoruz
customer_data.to_sql('customers', conn, index=False, if_exists='replace')

print("\n2. Adım: SQL Sorgusu çalıştırılıyor (CASE-WHEN ile Segmentasyon)...")
# CV'de fark yaratacak SQL sorgusu
sql_query = """
SELECT 
    customer_id,
    total_spent,
    last_transaction_days_ago,
    CASE 
        WHEN last_transaction_days_ago <= 30 THEN 'Aktif Musteri'
        WHEN last_transaction_days_ago > 30 AND last_transaction_days_ago <= 90 THEN 'Riskli (Sessiz)'
        ELSE 'Kayip (Churn) Adayi'
    END AS customer_segment,
    CASE 
        WHEN total_spent > 3000 THEN 'VIP'
        WHEN total_spent BETWEEN 1000 AND 3000 THEN 'Standart'
        ELSE 'Dusuk Hacimli'
    END AS value_segment,
    churn_label
FROM customers;
"""

df_analyzed = pd.read_sql_query(sql_query, conn)
print("\n--- Analiz Edilen Müşteri Verilerinden İlk 5 Satır ---")
print(df_analyzed.head(5))

print("\n3. Adım: Grafik çiziliyor ve kaydediliyor...")
# Segmentlere göre gerçek churn oranını hesaplayıp grafik çiziyoruz
churn_rates = df_analyzed.groupby('customer_segment')['churn_label'].mean().reset_index()

plt.figure(figsize=(8, 5))
# hue ve legend parametreleri uyarı almamak için güncellendi
sns.barplot(data=churn_rates, x='customer_segment', y='churn_label', hue='customer_segment', palette='coolwarm', legend=False)

plt.title('Musteri Segmentlerine Gore Kayip (Churn) Oranlari')
plt.ylabel('Churn Orani (Yuzde)')
plt.xlabel('Musteri Segmenti')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Grafiği klasöre resim olarak kaydediyoruz
plt.savefig('churn_analizi_grafik.png', dpi=300, bbox_inches='tight')
print("\n[BAŞARILI] Grafik 'churn_analizi_grafik.png' adıyla klasörünüze kaydedildi!")

conn.close()