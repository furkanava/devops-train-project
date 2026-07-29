# 1. Aşama: Derleme (Build) Aşaması
# Python 3.11 tabanlı hafif Alpine imajını builder olarak kullanıyoruz
FROM python:3.11-alpine AS builder

# Derleme işlemlerinin yapılacağı çalışma dizinini /build olarak belirliyoruz
WORKDIR /build

# Bağımlılık listesini içeren requirements.txt dosyasını kopyalıyoruz
COPY app/requirements.txt .

# Bağımlılıkları kullanıcıya özel dizine yüklüyoruz, pip önbelleğini temiz tutarak boyutu küçük tutuyoruz
RUN pip install --no-cache-dir --user -r requirements.txt

# 2. Aşama: Çalışma (Runtime) Aşaması
# Çalışma ortamı için yine temiz ve hafif Alpine imajını kullanıyoruz
FROM python:3.11-alpine AS runtime

# Setuptools yalnızca paket hazırlarken gerekir, uygulama çalışırken gerekli değildir
# Trivy'nin bulduğu güvenlik açıklarını runtime image'dan kaldırmak için siliyoruz
RUN pip uninstall --yes setuptools

# Uygulama dosyalarının bulunacağı çalışma dizinini /app olarak belirliyoruz
WORKDIR /app

# İlk aşamada (builder) yüklediğimiz python paketlerini çalışma ortamına kopyalıyoruz
COPY --from=builder /root/.local /root/.local

# Uygulama kodlarımızı (/app dizinine) kopyalıyoruz
COPY app/ .

# Bağımlılıkların çalıştırılabilir dosyalarını bulabilmek için PATH ortam değişkenine ekliyoruz
ENV PATH=/root/.local/bin:$PATH
# Python loglarının arabelleğe alınmadan anında terminale yazılmasını sağlıyoruz
ENV PYTHONUNBUFFERED=1
# Uygulama ortamını production olarak tanımlıyoruz
ENV APP_ENV=production

# Uygulamanın çalışacağı 5000 portunu dış dünyaya açıyoruz
EXPOSE 5000

# Uygulamayı başlatan ana komutu tanımlıyoruz
CMD ["python", "app.py"]