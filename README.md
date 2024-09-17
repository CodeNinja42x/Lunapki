# Cosmic Bot Performance Dashboard

Bu proje, **Cosmic Bot Performance Dashboard** adlı bir web uygulaması oluşturur. Uygulama, Flask kullanarak bir arka uç sunucusu ve Three.js kullanarak 3D görsellerle performans verilerini gerçek zamanlı olarak görselleştirir.

## Özellikler

- **3D Görseller:** Three.js kullanarak, 3D küre ve yıldızlardan oluşan bir sahne oluşturulur.
- **Gerçek Zamanlı Veri:** API üzerinden alınan gerçek zamanlı veri, 3D sahneye ve sayfa üzerindeki öğelere yansıtılır.
- **Loglama:** Uygulama boyunca oluşan hata ve bilgilendirme mesajları, `logs/app.log` dosyasına kaydedilir.

## Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki araçlar ve kütüphaneler gereklidir:

- Python 3.9+
- Flask
- Three.js

## Kurulum

1. Projeyi klonlayın:
    ```bash
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. Sanal ortamı oluşturun ve etkinleştirin:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    # .venv\Scriptsctivate  # Windows
    ```

3. Gerekli bağımlılıkları yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

## Kullanım

Uygulamayı başlatmak için aşağıdaki komutu çalıştırın:

```bash
python /path/to/app.py
```

Tarayıcınızda `http://127.0.0.1:5000` adresine gidin ve uygulamanın çalıştığını görün.

## Geliştirme

- Uygulama geliştirildikçe yeni özellikler ve iyileştirmeler README dosyasına eklenecektir.
- `logs/app.log` dosyasını kontrol ederek hata ve uyarıları izleyebilirsiniz.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.
