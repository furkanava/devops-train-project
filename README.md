# 🚀 DevOps Staj Projesi — CI/CD Pipeline ile Flask Uygulaması

> Merhaba! Bu repo, staj sürecinde CI/CD kavramlarını gerçek bir proje üzerinde öğrenmek için hazırlanmıştır.

---

## 📋 İçindekiler

- [Proje Hakkında](#proje-hakkında)
- [Teknoloji Stack](#teknoloji-stack)
- [Başlangıç](#başlangıç)
- [CI/CD Pipeline](#cicd-pipeline)
- [Görev Listesi](#görev-listesi)
- [PR & Review Kuralları](#pr--review-kuralları)
- [Sık Sorulan Sorular](#sık-sorulan-sorular)

---

## Proje Hakkında

Bu proje kasıtlı olarak **basit bir Python/Flask web uygulaması** üzerine kurulu. Amaç uygulamanın kendisi değil; uygulamanın etrafındaki **DevOps süreçlerini** yaşamak:

- Kodunu container içine almak (Docker)
- Her push'ta otomatik test + build çalıştırmak (GitHub Actions)
- Image'ı bir registry'e göndermek
- Kubernetes ile deploy etmek

---

## Teknoloji Stack

| Katman | Araç |
|---|---|
| Uygulama | Python 3.11 / Flask |
| Container | Docker |
| CI/CD | GitHub Actions |
| Registry | GitHub Container Registry (ghcr.io) |
| Orchestration | Kubernetes (manifest tabanlı) |
| Secret Yönetimi | GitHub Secrets + K8s Secrets |

---

## Başlangıç

### 1. Repo'yu Fork Et

```bash
# GitHub UI'dan "Fork" butonuna bas
# Sonra kendi fork'unu clone et:
git clone https://github.com/<kullanici-adin>/intern-cicd-project.git
cd intern-cicd-project
```

### 2. Local'de Çalıştır (Docker olmadan)

```bash
cd app
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

### 3. Docker ile Çalıştır

```bash
docker build -t intern-app:local .
docker run -p 5000:5000 intern-app:local
# → http://localhost:5000
```

### 4. Docker Compose ile Çalıştır

```bash
docker compose up
```

---

## CI/CD Pipeline

```
Push / PR açılır
      ↓
[Lint & Test]        → Python testleri çalışır, kod kalitesi kontrol edilir
      ↓
[Docker Build]       → Image build alınır
      ↓
[Security Scan]      → Trivy ile image taranır (CRITICAL/HIGH açıklar engeller)
      ↓
[Push to Registry]   → ghcr.io'ya image gönderilir (sadece main branch)
      ↓
[Deploy to K8s]      → Kubernetes manifest apply edilir (sadece main branch)
```

> ⚠️ **Not:** Pipeline adımlarını `.github/workflows/` klasöründe inceleyebilirsin.
> Her adımın neden orada olduğunu anlamaya çalış — mentor'una sormaktan çekinme.

---

## Görev Listesi

Staj sürecinde aşağıdaki görevleri sırasıyla tamamlamanı bekliyoruz.
Her görev için **ayrı bir branch** aç ve **PR ile** teslim et.

### 🟢 Hafta 1 — Anla & Çalıştır

- [ ] Repo'yu fork et, local'de çalıştır (hem düz Python hem Docker ile)
- [ ] `app/app.py` dosyasını incele — ne iş yapıyor?
- [ ] `Dockerfile`'ı incele — her satırın ne anlama geldiğini bir yorum satırı olarak ekle
- [ ] `.github/workflows/ci.yml` dosyasını incele — pipeline adımlarını `docs/pipeline-notes.md` dosyasında açıkla
- [ ] **İlk PR:** `docs/pipeline-notes.md` dosyasını oluştur ve PR aç

### 🟡 Hafta 2 — Değiştir & İyileştir

- [ ] `app/app.py` dosyasına yeni bir endpoint ekle: `GET /health` → `{"status": "ok"}` dönsün
- [ ] Bu endpoint için `app/test_app.py` dosyasına test yaz
- [ ] `Dockerfile`'ı multi-stage build'e çevir (ipucu: `docs/tasks/multi-stage.md`)
- [ ] **PR:** Tüm değişiklikleri tek bir PR ile sun, CI'ın geçtiğinden emin ol

### 🔵 Hafta 3 — Pipeline'a Katkı

- [ ] `.github/workflows/ci.yml` dosyasına yeni bir adım ekle: `docker image inspect` ile image boyutunu loglasın
- [ ] Trivy scan sonucunu PR comment olarak yazan bir adım araştır ve ekle
- [ ] **PR:** Pipeline değişikliklerini açıklayan bir `docs/pipeline-changelog.md` oluştur

### 🟣 Hafta 4 — Kubernetes

- [ ] `k8s/` klasöründeki manifest dosyalarını incele
- [ ] `k8s/deployment.yaml` dosyasında `replicas: 1` olan değeri `2`'ye çıkar — ne değişti?
- [ ] Yeni bir `k8s/configmap.yaml` oluştur: uygulamanın `APP_ENV` ortam değişkenini oradan okusun
- [ ] **PR:** Değişiklikleri ve nedenlerini açıklayan bir PR description yaz

---

## PR & Review Kuralları

### Branch İsimlendirme

```
feature/<kisa-aciklama>     → feat/health-endpoint
fix/<kisa-aciklama>         → fix/dockerfile-layer-cache
docs/<kisa-aciklama>        → docs/pipeline-notes
```

### PR Description Şablonu

Her PR açarken şu bilgileri ekle:

```markdown
## Ne Yaptım?
...

## Neden Yaptım?
...

## Nasıl Test Ettim?
...

## Ekran Görüntüsü / Log (varsa)
...
```

### Review Süreci

1. PR açarsın
2. Mentor review ister
3. Yorumları okursun — her yoruma cevap verirsin (kabul ettiysen "Done ✅", katılmıyorsan nedenini açıklarsın)
4. Gerekli değişiklikleri yapıp "Re-review" istersin
5. Approve gelince merge edilir

> 💡 Review yorumları kişisel değil, kod hakkında. "Sen yanlış yaptın" değil, "bu yaklaşım şu soruna yol açar" zihniyetiyle oku.

---

## Sık Sorulan Sorular

**S: Pipeline neden fail oldu?**
Önce Actions sekmesinde kırmızı adımın üzerine tıkla, log'u oku. Sorunu anlayamazsan log'u mentor'a at.

**S: Branch'imde conflict var, ne yapayım?**
```bash
git fetch origin
git rebase origin/main
# Conflict'leri çöz
git rebase --continue
```

**S: Commit history'im çok karışık, squash yapabilir miyim?**
Evet, PR merge edilmeden önce `git rebase -i HEAD~N` ile squash edebilirsin. Mentor'a sor, birlikte yapalım.

**S: Bir şeyi kırdım, ne yapayım?**
Normal! Hata yapmak öğrenmenin parçası. Main branch'e doğrudan push yoksa (ve yoktur) sistemi kıramazsın. Branch'ini sil, yeniden başla veya mentor'a sor.

---

*Sorularını Issue açarak veya Teams'den mentor'una iletebilirsin.*

*İyi stajlar! 🎉*
