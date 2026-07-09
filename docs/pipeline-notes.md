# Pipeline Notes

Bu repodaki CI/CD akışı, `.github/workflows/ci.yml` dosyasında duruyor. README ile de uyumlu hale getirilmiştir.

## 1. Test aşaması
- Repo checkout ediliyor.
- Python 3.11 kuruluyor.
- Pip bağımlılıkları yükleniyor.
- Pytest ile testler koşuyor.

Buradaki amaç basit: Docker image üretmeden önce kod sağlam mı diye bakmak.

## 2. Docker build ve güvenlik taraması
- Docker Buildx hazırlanıyor.
- Uygulama image’ı build ediliyor.
- Image local’e yükleniyor.
- Trivy ile security scan yapılıyor.

Burada da amaç image içinde kritik ya da yüksek seviyede açık varsa yakalamak. Trivy böyle bir açık bulursa pipeline patlıyor.

## 3. Registry’ye push
- Bu adım sadece `main` branch’ine push gelince çalışıyor.
- GitHub Container Registry’ye login olunuyor.
- Image için metadata hazırlanıyor.
- Image build edilip GHCR’ye gönderiliyor.

Yani kısaca: sadece ana branch temizse registry’ye image çıkılıyor.

## 4. Kubernetes deploy
- Bu adım da sadece `main` branch push’larında çalışıyor.
- Repo tekrar checkout ediliyor.
- Gerçek deploy kısmı şimdilik yorum satırında bırakılmış.
- Onun yerine log mesajlarıyla ne olacağı gösteriliyor.

Bu bölümün amacı, ileride gerçek cluster’a geçince deploy adımının nereye bağlanacağını net tutmak.

## Ek notlar
- Workflow test adımında bağımlılıkları `app/requirements.txt` dosyasından yüklüyor ve testler başarıyla çalışıyor.
- Uygulama artık tutarlı bir şekilde hem local'de hem de Docker container'ında `5000` portunda çalışmaktadır. Kubernetes manifestlerindeki port tanımlamaları da bu portla uyumlu olacak şekilde (`containerPort: 5000`, `targetPort: 5000`) konfigüre edilmiştir. README ve diğer konfigürasyonlardaki port uyumsuzlukları giderilmiştir.
