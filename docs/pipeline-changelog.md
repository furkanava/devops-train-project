# Hafta 3 — Pipeline Değişiklikleri

Bu hafta projenin CI/CD pipeline’ı üzerinde çalıştım. Amacım Docker image hakkında daha fazla bilgi görmek ve Trivy güvenlik taramasının sonucunu Pull Request ekranından daha kolay takip edebilmekti.

## Pipeline Branch’ini Düzelttim

İlk olarak pipeline’ın `main` branch’ini takip ettiğini fark ettim. Ancak benim projemin ana branch’i `master` olduğu için bu ayarın doğru çalışmayacağını düşündüm.

Bu yüzden `ci.yml` dosyasındaki `main` değerlerini `master` olarak değiştirdim.

```yaml
on:
  push:
    branches: ["master"]
  pull_request:
    branches: ["master"]
```

Böylece `master` branch’ine bir Pull Request açıldığında veya kod gönderildiğinde pipeline otomatik olarak çalışabilecek.

## Docker Image Boyutunu Ekledim

İkinci olarak, oluşturduğumuz Docker image’ın boyutunu pipeline loglarında görmek istedim.

Bunun için `docker image inspect` komutunu kullanan yeni bir adım ekledim:

```yaml
- name: Docker image boyutunu göster
  run: |
    docker image inspect \
      ${{ env.IMAGE_NAME }}:${{ github.sha }} \
      --format='Image boyutu: {{.Size}} byte'
```

Bu komut oluşturulan image’ı inceliyor ve boyutunu byte olarak ekrana yazıyor.

Önceki hafta Dockerfile’ı multi-stage yapıya çevirmiştik. Bu adım sayesinde ileride Dockerfile’da yaptığımız değişikliklerin image boyutunu nasıl etkilediğini görebileceğiz.

## Trivy Raporunu Dosyaya Yazdırdım

Projede daha önceden Trivy ile güvenlik taraması yapılıyordu. Fakat taramanın sonucu yalnızca GitHub Actions loglarında görünüyordu.

Sonucu daha kolay kullanabilmek için Trivy çıktısını `trivy-results.txt` isimli bir dosyaya yazdıran yeni bir adım ekledim.

Bu adımda `exit-code: "0"` kullandım. Bunun nedeni bu ilk taramanın görevinin pipeline’ı durdurmak değil, yalnızca rapor oluşturmak olmasıdır.

Raporda sadece `HIGH` ve `CRITICAL` seviyesindeki önemli güvenlik açıklarını gösteriyorum.

## Trivy Sonucunu PR Yorumuna Ekledim

Oluşturulan Trivy raporunu Pull Request’e yorum olarak ekleyen bir adım ekledim.

Bu adım yalnızca bir Pull Request açıldığında çalışıyor:

```yaml
if: github.event_name == 'pull_request'
```

Yorum eklemek için `sticky-pull-request-comment` kullandım. Böylece pipeline her çalıştığında ayrı bir yorum oluşturmak yerine mevcut güvenlik yorumunu güncelliyor.

Pipeline’ın Pull Request’e yorum yazabilmesi için şu izinleri de ekledim:

```yaml
permissions:
  contents: read
  pull-requests: write
```

## Güvenlik Açığı Varsa Pipeline’ı Durdurdum

Pipeline’da iki tane Trivy adımı bulunuyor. İlk başta bunun neden gerekli olduğunu anlamakta zorlandım.

İlk Trivy adımı raporu oluşturuyor ve pipeline’ı durdurmuyor. İkinci Trivy adımı ise asıl güvenlik kontrolünü yapıyor.

İkinci taramada `HIGH` veya `CRITICAL` seviyesinde bir açık bulunursa `exit-code: "1"` nedeniyle pipeline başarısız oluyor. Böylece ciddi güvenlik açığı bulunan bir Docker image sonraki yayınlama adımlarına geçemiyor.

## Son Durum

Yaptığım değişikliklerden sonra pipeline’ın çalışma sırası şöyle oldu:

1. Python paketleri yükleniyor.
2. Uygulamanın testleri çalıştırılıyor.
3. Docker image oluşturuluyor.
4. Image boyutu loglara yazılıyor.
5. Trivy raporu hazırlanıyor.
6. Rapor Pull Request’e yorum olarak ekleniyor.
7. Güvenlik açığı varsa pipeline durduruluyor.
8. Her şey başarılıysa sonraki aşamalara geçiliyor.

Dosyalardaki girinti ve gereksiz boşlukları aşağıdaki komutla kontrol ettim:

```bash
git diff --check
```

Pipeline’ın gerçekten çalışıp çalışmadığını ise branch’i GitHub’a gönderip Pull Request açtıktan sonra GitHub Actions ekranından kontrol edeceğim.