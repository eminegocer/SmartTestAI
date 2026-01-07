# 4.3 MODEL/METOT

## 4.3.1 GENEL YAKLAŞIM

SmartTestAI projesinde klasik bir "tek makine öğrenmesi modeli" yerine, çok bileşenli, metrik-tabanlı bir değerlendirme metodolojisi benimsenmiştir. Sistem, farklı yapay zekâ destekli **statik kod analizi araçlarının** (Snyk Code ve DeepSource) aynı test projeleri üzerinde ürettikleri çıktıları toplayarak, bu çıktıları önceden tanımlanmış performans metrikleri üzerinden karşılaştırmaktadır.

Bu yaklaşım, modeli "öğrenen" bir yapıdan ziyade **karar destek ve benchmark sistemi** olarak konumlandırmaktadır. Temel hedef, "Hangi AI kod analiz aracı daha başarılı?" sorusuna ölçülebilir ve nesnel cevaplar vermektir.

### Sistemin Temel Bileşenleri

| Bileşen | Açıklama |
|---------|----------|
| **Snyk Code** | Yapay zekâ destekli güvenlik açığı tespit aracı |
| **DeepSource** | AI tabanlı statik kod analizi platformu |
| **MetricResult** | Standart metrik çıktı formatı (dataclass) |
| **AdvancedMetricsCalculator** | Gelişmiş metrik hesaplama modülü |
| **Flask REST API** | Tarama ve sonuç yönetimi için web servisi |

---

## 4.3.2 KULLANILAN ALGORİTMALAR VE TEKNİKLER

### a) Kural Tabanlı Değerlendirme (Rule-Based Scoring)

Kural tabanlı değerlendirme yaklaşımında, kod analizi araçlarından elde edilen çıktılar önceden tanımlanmış ölçütler doğrultusunda otomatik olarak analiz edilmiş ve puanlanmıştır.

#### Temel Metrik Seti (MetricResult)

Her araçtan gelen ham çıktı, aşağıdaki standart formata dönüştürülmektedir:

```python
@dataclass
class MetricResult:
    tool_name: str      # Araç adı (örn: "Snyk Code", "DeepSource")
    critical: int       # Kritik seviye güvenlik açığı sayısı
    high: int           # Yüksek seviye güvenlik açığı sayısı
    medium: int         # Orta seviye güvenlik açığı sayısı
    low: int            # Düşük seviye güvenlik açığı sayısı
    total_issues: int   # Toplam tespit edilen sorun sayısı
    scan_duration: float # Tarama süresi (saniye)
```

#### Severity Mapping (Ciddiyet Eşleştirmesi)

Farklı araçların farklı severity formatları standart formata dönüştürülmektedir:

| Snyk Code (SARIF) | DeepSource | Standart Format |
|-------------------|------------|-----------------|
| priorityScore ≥ 900 | CRITICAL | critical |
| priorityScore ≥ 700 | MAJOR | high |
| priorityScore ≥ 500 | MINOR | medium |
| priorityScore < 500 | INFO | low |

Bu sayede farklı araçların ürettiği çıktılar **nesnel, tutarlı ve karşılaştırılabilir** bir çerçeve içerisinde değerlendirilmektedir.

---

### b) Gelişmiş Metrik Hesaplamaları (Advanced Metrics)

Temel metriklerin ötesinde, araç performanslarını daha kapsamlı değerlendirmek için gelişmiş metrikler hesaplanmaktadır:

#### i) Hata Tespit Başarısı (Defect Detection Accuracy)

Ground truth (bilinen güvenlik açıkları) ile karşılaştırma yapılarak hesaplanır:

| Metrik | Formül | Açıklama |
|--------|--------|----------|
| **Precision** | TP / (TP + FP) | Tespit edilen sorunların ne kadarı gerçek sorun |
| **Recall** | TP / (TP + FN) | Gerçek sorunların ne kadarı tespit edildi |
| **F1 Score** | 2 × (P × R) / (P + R) | Precision ve Recall'ın harmonik ortalaması |

**Örnek Sonuç (Snyk Code - vulnerable_demo projesi):**
```json
{
  "precision": 0.364,      // %36.4 - Tespit edilenlerin doğruluk oranı
  "recall": 0.667,         // %66.7 - Gerçek açıkların yakalanma oranı
  "f1_score": 0.471,       // %47.1 - Genel başarı skoru
  "true_positives": 4,     // Doğru tespit
  "false_positives": 7,    // Yanlış alarm
  "false_negatives": 2     // Kaçırılan açık
}
```

#### ii) Yanlış Alarm Eğilimi (False Positive Rate)

```
FPR = FP / (FP + TN)
```

Düşük FPR değeri, aracın gereksiz uyarı üretmediğini gösterir. Bu metrik, geliştiricilerin araç çıktılarına güven düzeyini belirlemede kritik öneme sahiptir.

#### iii) Kod Kapsama Oranı (Code Coverage)

```json
{
  "code_coverage_percent": 100.0,  // Taranan kod yüzdesi
  "files_analyzed": 1,             // Analiz edilen dosya sayısı
  "lines_analyzed": 0              // Analiz edilen satır sayısı
}
```

#### iv) Operasyonel Verimlilik (Operational Efficiency)

Sistem kaynak kullanımı ve performans metrikleri:

```json
{
  "average_scan_time": 0.0,        // Ortalama tarama süresi (saniye)
  "cpu_usage_percent": 14.3,       // CPU kullanım yüzdesi
  "memory_usage_mb": 20.61         // Bellek kullanımı (MB)
}
```

---

### c) İstatistiksel Performans Analizi

İstatistiksel performans analizi kapsamında, karşılaştırılan araçlar arasındaki performans farklılıklarının anlamlılığını değerlendirmek amacıyla temel istatistiksel yöntemler kullanılmaktadır:

| Analiz Türü | Uygulama Alanı |
|-------------|----------------|
| **Ortalama Hesaplama** | Severity dağılımı, tarama süreleri |
| **Standart Sapma** | Sonuçların tutarlılığı |
| **Karşılaştırmalı Analiz** | Araçlar arası performans farkları |

#### Örnek Karşılaştırma Tablosu

| Metrik | Snyk Code | DeepSource |
|--------|-----------|------------|
| Critical | 0 | 0 |
| High | 10 | 0 |
| Medium | 1 | 0 |
| Low | 0 | 0 |
| **Toplam** | **11** | **0** |
| Precision | %36.4 | %0.0 |
| Recall | %66.7 | %0.0 |
| F1 Score | %47.1 | %0.0 |

> **Not:** DeepSource sonuçları repository-based çalıştığı için local test projelerinde farklılık gösterebilir.

---

### d) Öğrenme Türü

Bu çalışmada **supervised**, **unsupervised** veya **transfer learning** gibi öğrenme yaklaşımları kullanılmamıştır. Sistem, doğrudan model eğitmeye odaklanmak yerine, mevcut araçların performanslarını karşılaştırmayı amaçlayan **benchmark ve metrik tabanlı** bir değerlendirme yaklaşımı benimsemektedir.

#### Tercih Gerekçeleri

1. **Nesnel Karşılaştırma:** Farklı AI araçlarının çıktıları aynı metrik seti üzerinden değerlendirilmektedir
2. **Tekrarlanabilirlik:** Aynı test projeleri üzerinde tutarlı sonuçlar elde edilmektedir
3. **Genişletilebilirlik:** Yeni araçlar (TestSigma, Applitools vb.) kolayca sisteme entegre edilebilir
4. **Şeffaflık:** Tüm hesaplamalar açık formüllerle yapılmakta, "kara kutu" yaklaşımı bulunmamaktadır

---

## 4.3.3 SİSTEM MİMARİSİ

### Klasör Yapısı

```
SmartTestAI-feature-metrics-engine/
├── backend/
│   ├── app.py                    # Flask REST API
│   ├── metric_runner.py          # Snyk Code tarama modülü
│   ├── deepsource_runner.py      # DeepSource tarama modülü
│   ├── snyk_runner.py            # Container tarama modülü
│   ├── metrics/
│   │   ├── base_metric.py        # Soyut metrik sınıfı
│   │   ├── result_model.py       # MetricResult dataclass
│   │   ├── snyk_metrics.py       # Snyk metrik hesaplayıcı
│   │   ├── deepsource_metrics.py # DeepSource metrik hesaplayıcı
│   │   └── advanced_metrics.py   # Gelişmiş metrik hesaplayıcı
│   └── tests/
│       ├── test_advanced_metrics.py
│       └── test_deepsource_api.py
├── results/                      # Tarama sonuçları (JSON)
├── test_projects/                # Test edilecek projeler
│   ├── flask_demo/
│   └── vulnerable_demo/
└── docs/
    └── MODEL_METOT_RAPORU.md
```

### API Endpoint'leri

| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/scan/code` | POST | Snyk Code taraması |
| `/scan/code/all` | POST | Tüm projeler için Snyk taraması |
| `/scan/deepsource` | POST | DeepSource taraması |
| `/scan/deepsource/all` | POST | Tüm projeler için DeepSource taraması |
| `/projects` | GET | Mevcut test projelerini listele |
| `/scan/latest` | GET | Son tarama sonucunu getir |

---

## 4.3.4 SONUÇ

SmartTestAI projesi, yapay zekâ destekli kod analizi araçlarını **standart metrikler** üzerinden karşılaştıran bir benchmark sistemi olarak tasarlanmıştır. Sistem:

- **Kural tabanlı değerlendirme** ile tutarlı puanlama sağlar
- **Gelişmiş metrikler** (Precision, Recall, F1) ile detaylı analiz sunar
- **İstatistiksel yöntemler** ile anlamlı karşılaştırmalar yapar
- **Modüler mimari** ile yeni araç entegrasyonuna açıktır

Bu yaklaşım, "Hangi AI kod analiz aracı daha başarılı?" sorusuna **ölçülebilir, tekrarlanabilir ve nesnel** cevaplar vermektedir.

