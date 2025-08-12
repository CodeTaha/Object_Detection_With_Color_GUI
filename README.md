# 🎯 Modern Renk Takip Uygulaması

Bu proje, **OpenCV** ve **CustomTkinter** kullanılarak geliştirilmiş modern ve şık bir Windows uygulamasıdır. Kamera görüntüsünden belirli renkleri tespit eder ve nesnelerin hareketini takip eder.

## ✨ Özellikler

### 🎨 **Hızlı Renk Seçimi**
- **9 ana renk** için önceden ayarlanmış HSV değerleri
- Tek tıkla renk seçimi
- Otomatik HSV aralığı ayarlama
- Renkler: Kırmızı, Turuncu, Sarı, Yeşil, Mavi, Mor, Pembe, Beyaz, Siyah

### ⚙️ **Manuel Kontrol**
- HSV (Hue, Saturation, Value) slider'ları
- Gerçek zamanlı değer güncelleme
- Hassas renk ayarlama imkanı

### 📹 **Kamera Kontrolü**
- Başlat/Duraklat butonu
- 30 FPS kamera akışı
- Gerçek zamanlı nesne takibi
- Hareket izi çizimi

### 🎯 **Nesne Takibi**
- Kontur tespiti
- Merkez nokta hesaplama
- Hareket yolu çizimi
- Buffer tabanlı takip sistemi

## 🚀 Kurulum

### Gereksinimler
- Python 3.8 veya üzeri
- Windows 10/11
- Webcam

### Adım 1: Projeyi İndir
```bash
git clone https://github.com/kullaniciadi/RenkIleTespitGUI.git
cd RenkIleTespitGUI
```

### Adım 2: Sanal Ortam Oluştur (Önerilen)
```bash
python -m venv venv
venv\Scripts\activate
```

### Adım 3: Gerekli Kütüphaneleri Kur
```bash
pip install -r requirements.txt
```

## 🎮 Kullanım

### Uygulamayı Başlat
```bash
python ModernRenkIleNesneTespiti.py
```

### Hızlı Renk Seçimi
1. Sol paneldeki renk butonlarından birine tıkla
2. HSV değerleri otomatik olarak ayarlanır
3. Kamera görüntüsünde seçilen renk tespit edilir

### Manuel Ayar
1. HSV slider'larını kullanarak hassas ayar yap
2. Değerler gerçek zamanlı olarak güncellenir
3. İstediğin sonucu elde et

### Kamera Kontrolü
- **▶️ Başlat**: Kamerayı başlat
- **⏸️ Duraklat**: Kamerayı durdur
- **🔄 Sıfırla**: Varsayılan değerlere dön
- **❌ Çıkış**: Uygulamayı tamamen kapat

## 🛠️ Teknik Detaylar

### Kullanılan Teknolojiler
- **OpenCV**: Görüntü işleme ve kamera kontrolü
- **CustomTkinter**: Modern GUI arayüzü
- **NumPy**: Matematiksel işlemler
- **PIL**: Görüntü formatı dönüşümleri

### Mimari
- **Multi-threading**: Kamera akışı ayrı thread'de
- **Event-driven**: GUI olaylarına dayalı programlama
- **Modüler yapı**: Sınıf tabanlı organizasyon

### Performans
- **30 FPS** kamera akışı
- **Gerçek zamanlı** işleme
- **Düşük CPU** kullanımı

## 🎨 Renk Paleti

| Renk | Emoji | HSV Aralığı |
|------|-------|-------------|
| 🔴 Kırmızı | 🔴 | Hue: 0-10, Sat: 100-255, Val: 100-255 |
| 🟠 Turuncu | 🟠 | Hue: 10-25, Sat: 100-255, Val: 100-255 |
| 🟡 Sarı | 🟡 | Hue: 25-35, Sat: 100-255, Val: 100-255 |
| 🟢 Yeşil | 🟢 | Hue: 35-85, Sat: 100-255, Val: 100-255 |
| 🔵 Mavi | 🔵 | Hue: 100-130, Sat: 100-255, Val: 100-255 |
| 🟣 Mor | 🟣 | Hue: 130-170, Sat: 100-255, Val: 100-255 |
| 🩷 Pembe | 🩷 | Hue: 170-180, Sat: 100-255, Val: 100-255 |
| ⚪ Beyaz | ⚪ | Hue: 0-180, Sat: 0-30, Val: 200-255 |
| ⚫ Siyah | ⚫ | Hue: 0-180, Sat: 0-255, Val: 0-30 |

## 🔧 Sorun Giderme

### Kamera Açılmıyor
- Webcam'in başka uygulamada kullanılmadığından emin ol
- Kamera sürücülerini güncelle
- Windows kamera izinlerini kontrol et

### Performans Sorunları
- Kamera çözünürlüğünü düşür
- Buffer boyutunu azalt
- Diğer uygulamaları kapat

### Renk Tespiti Çalışmıyor
- Işık koşullarını kontrol et
- HSV değerlerini manuel olarak ayarla
- Farklı renk paleti dene

## 🤝 Katkıda Bulunma

1. Fork yap
2. Feature branch oluştur (`git checkout -b feature/AmazingFeature`)
3. Commit yap (`git commit -m 'Add some AmazingFeature'`)
4. Push yap (`git push origin feature/AmazingFeature`)
5. Pull Request oluştur

## 📞 İletişim

- **Proje Linki**: [https://github.com/kullaniciadi/RenkIleTespitGUI](https://github.com/kullaniciadi/RenkIleTespitGUI)
- **Sorun Bildirimi**: [Issues](https://github.com/kullaniciadi/RenkIleTespitGUI/issues)

## 🙏 Teşekkürler

- **OpenCV** ekibine görüntü işleme kütüphanesi için
- **CustomTkinter** geliştiricilerine modern GUI için
- **Python** topluluğuna harika araçlar için

---

⭐ **Bu projeyi beğendiysen yıldız vermeyi unutma!** ⭐
