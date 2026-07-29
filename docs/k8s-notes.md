# Hafta 4 — Kubernetes Manifestleri ve Konfigürasyon Yönetimi

Bu hafta projenin Kubernetes (K8s) konfigürasyonları ve manifest yönetimi üzerine çalıştım.

---

## 1. Kubernetes Manifestlerinin `k8s/` Dizinine Taşınması

Eski yapıda `deployment.yaml` ve `service.yaml` dosyaları kök dizinde yer alıyordu. 

**Neden Yaptım?**
- Kubernetes standartlarında ve CI/CD pipeline'larında tüm manifestlerin tek bir klasör altında (`k8s/`) toplanması en iyi pratiktir (best practice).
- Bu sayede `kubectl apply -f k8s/` tek bir komutu ile klasördeki tüm kaynaklar (`Deployment`, `Service`, `ConfigMap`) sırasıyla küme üzerine dağıtılabilir (deploy edilebilir).

---

## 2. Pod Sayısının Artırılması (`replicas: 2`)

`k8s/deployment.yaml` dosyasındaki `replicas: 1` değerini `replicas: 2` olarak değiştirdim.

```yaml
spec:
  replicas: 2 # Hafta 4: Yüksek erişilebilirlik ve yük dengeleme
```

### Ne Değişti ve Neden Yaptım?
- **Yüksek Erişilebilirlik (High Availability - HA):** Tek bir pod (`replicas: 1`) çalıştığında, o pod çökerse veya sunucuda bir sorun yaşanırsa uygulama yeni pod ayağa kalkana kadar erişilemez olur (downtime). `replicas: 2` ile Kubernetes arka planda aynı uygulamanın **2 özdeş kopyasını (pod)** çalıştırır. Biri çökse dahi diğeri istekleri karşılamaya devam eder.
- **Yük Dengeleme (Load Balancing):** Gelen HTTP istekleri `Service` tarafından bu 2 pod arasında eşit şekilde paylaştırılır.
- **Kendi Kendini İyileştirme (Self-Healing):** Pod'lardan biri kapanırsa Kubernetes denetleyicisi (Deployment Controller) bunu fark eder ve hedef pod sayısını (2) korumak için otomatik olarak yeni bir pod başlatır.

---

## 3. Merkezi Konfigürasyon Yönetimi (`k8s/configmap.yaml`)

Yeni bir `k8s/configmap.yaml` dosyası oluşturdum:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: intern-app-config
  labels:
    app: intern-app
data:
  APP_ENV: "production"
```

Ve `k8s/deployment.yaml` dosyasında sabitlemiş (hardcoded) olduğumuz `APP_ENV` değerini ConfigMap'ten okuyacak şekilde güncelledim:

```yaml
env:
  - name: APP_ENV
    valueFrom:
      configMapKeyRef:
        name: intern-app-config
        key: APP_ENV
```

### Neden Yaptım?
- **12-Factor App Prensibi:** Modern cloud-native uygulamalarda konfigürasyon (ortam değişkenleri) uygulama kodundan ve Docker imajından kesinlikle ayrılmalıdır.
- **Tek İmaj, Çok Ortam:** İmajı bir kez inşa ederiz (`ghcr.io/furkanava/devops-train-project:latest`). Bu imajı Development, Staging veya Production ortamında çalıştırmak istediğimizde Docker imajını değiştirmek yerine sadece o ortama ait `ConfigMap` değerini güncelleriz.

---

## 4. Trivy PR Yorumu Formatlama İyileştirmesi

Trivy taramasındaki uzun paket yollarının (`root/.local/lib/python3.11/...`) okunabilirliği düşürmesini engellemek için `scripts/format_trivy.py` betiğini ekledim ve `.github/workflows/ci.yml` dosyasını JSON çıktısını işleyip temiz bir Markdown özet tablosu basacak şekilde güncelledim.
