# YOLOv8 Nesne Tespiti

Bu proje, YOLOv8 mimarisi ile nesne tespiti uygulamasını içermektedir. Eğitim ve test süreçleri Jupyter Notebook ve Python GUI ile desteklenmiştir.

## İçerik
 - `yolov8.ipynb`: YOLOv8 ile model eğitimi ve test adımlarını içeren notebook.
 - `gui_app.py`: Eğitilmiş modeli kullanarak görsel arayüzde nesne tespiti yapan Python uygulaması.
 - `best.pt`: Eğitilmiş en iyi model ağırlıkları.
 - `dataset/`: Eğitim ve test için kullanılan veri seti klasörü.
 - `sanal_ortam/`: Proje için oluşturulan sanal Python ortamı.

## Kurulum
1. Sanal ortamı etkinleştirin:
   ```powershell
   .\sanal_ortam\Scripts\Activate.ps1
   ```
2. Gerekli paketleri yükleyin:
   ```bash
   pip install ultralytics opencv-python PyQt5
   ```
3. Sanal ortamdan çıkmak için:
   ```powershell
   deactivate
   ```

## Notebook Kullanımı
- `yolov8.ipynb` dosyasında adım adım model eğitimi, veri hazırlama ve test işlemleri açıklanmıştır.
- Google Colab ortamı için örnek kodlar ve açıklamalar mevcuttur.

## GUI Kullanımı
- `gui_app.py` dosyasını çalıştırarak eğitilmiş model ile görsel arayüzde nesne tespiti yapabilirsiniz.
   ```bash
   python gui_app.py
   ```

## Katkı
Pull request ve issue açarak katkıda bulunabilirsiniz.

## Lisans
MIT

---
**Hazırlayan:** Mücahit Topçuoğlu

**Öğrenci No:** 2112721061

**Github:** https://github.com/mucahit-topcuoglu/YoloV8_Nesne_Tespiti
