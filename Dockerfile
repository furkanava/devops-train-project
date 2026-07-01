# Bu Dockerfile kasıtlı olarak geliştirilmeye açık bırakılmıştır.
# Görev (Hafta 2): Bu dosyayı multi-stage build'e çevir.

FROM python:3.11 # From komutu base image göstermek için kullanılır. Bu image python 3.11 içerir.
WORKDIR /app # Çalışma dizinini /app olarak ayarlıyoruz. Bu dizin, container içinde çalıştırılacak komutlar için referans noktasıdır.   

COPY requirements.txt . # requirements.txt dosyasını container içine kopyalıyoruz. Bu dosya, uygulamanın bağımlılıklarını listeler. 
RUN pip install -r requirements.txt # requirements.txt dosyasındaki bağımlılıkları yüklemek için pip install komutunu çalıştırıyoruz.   

COPY app/ . # app dizinindeki tüm dosyaları container içine kopyalıyoruz. Bu, uygulamanın kaynak kodunu içerir. 

EXPOSE 5000 # Bu komut, container''ın 5000 numaralı portunu dış dünyaya açar. Flask uygulamaları genellikle bu port üzerinden çalışır.

CMD ["python", "app.py"] # CMD komutu, container başlatıldığında çalıştırılacak varsayılan komutu belirtir. Bu durumda, Flask uygulamasını başlatmak için python app.py komutunu çalıştırıyoruz.    