import sys
import cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                             QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, 
                             QListWidget, QMessageBox, QGroupBox)
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt
from ultralytics import YOLO
import os

class ObjectDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YOLOv8 İş Güvenliği Tespiti - Mücahit Topçuoğlu")
        self.setGeometry(100, 100, 1200, 750)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")

        # --- MODELİ YÜKLE ---
        # best.pt dosyasının bu kodla AYNI KLASÖRDE olması lazım
        model_path = os.path.join(os.getcwd(), "best.pt")
        
        if not os.path.exists(model_path):
            QMessageBox.critical(self, "Hata", f"Model bulunamadı!\n Lütfen 'best.pt' dosyasını bu kodun yanına koyun.\n Aranan yol: {model_path}")
            self.model = None 
        else:
            try:
                self.model = YOLO(model_path)
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Model yüklenirken hata oluştu:\n{str(e)}")
                self.model = None

        self.original_image_path = None
        self.processed_image = None 

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # --- SOL PANEL (Resimler) ---
        images_layout = QVBoxLayout()
        
        # Orijinal Resim Alanı
        self.group_original = QGroupBox("Orijinal Görüntü")
        self.group_original.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid gray; margin-top: 10px; } QGroupBox::title { top: -10px; left: 10px; }")
        layout_original = QVBoxLayout()
        self.label_original = QLabel("Resim Yükleyiniz")
        self.label_original.setAlignment(Qt.AlignCenter)
        self.label_original.setStyleSheet("border: 2px dashed #555; background-color: #333;")
        layout_original.addWidget(self.label_original)
        self.group_original.setLayout(layout_original)

        # Sonuç Resim Alanı
        self.group_tagged = QGroupBox("YOLOv8 Sonucu")
        self.group_tagged.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid gray; margin-top: 10px; } QGroupBox::title { top: -10px; left: 10px; }")
        layout_tagged = QVBoxLayout()
        self.label_tagged = QLabel("Analiz Bekleniyor...")
        self.label_tagged.setAlignment(Qt.AlignCenter)
        self.label_tagged.setStyleSheet("border: 2px dashed #555; background-color: #333;")
        layout_tagged.addWidget(self.label_tagged)
        self.group_tagged.setLayout(layout_tagged)

        images_layout.addWidget(self.group_original)
        images_layout.addWidget(self.group_tagged)

        # --- SAĞ PANEL (Butonlar ve Liste) ---
        controls_layout = QVBoxLayout()
        controls_layout.setContentsMargins(20, 0, 0, 0)

        # Buton Stilleri
        btn_style = "QPushButton { background-color: #007acc; color: white; border-radius: 5px; padding: 12px; font-weight: bold; font-size: 14px;} QPushButton:hover { background-color: #005f9e; }"
        
        self.btn_select = QPushButton("Resim Seç (Select Image)")
        self.btn_select.setStyleSheet(btn_style)
        self.btn_select.clicked.connect(self.select_image)

        self.btn_test = QPushButton("Test Et (Test Image)")
        self.btn_test.setStyleSheet(btn_style.replace("#007acc", "#28a745").replace("#005f9e", "#1e7e34"))
        self.btn_test.clicked.connect(self.test_image)
        self.btn_test.setEnabled(False)

        self.btn_save = QPushButton("Kaydet (Save Image)")
        self.btn_save.setStyleSheet(btn_style.replace("#007acc", "#dc3545").replace("#005f9e", "#bd2130"))
        self.btn_save.clicked.connect(self.save_image)
        self.btn_save.setEnabled(False)

        # Liste
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("background-color: #444; border: 1px solid #555; font-size: 14px; color: #fff;")
        
        lbl_info = QLabel("Tespit Sonuçları:")
        lbl_info.setFont(QFont("Arial", 12, QFont.Bold))

        controls_layout.addWidget(self.btn_select)
        controls_layout.addWidget(self.btn_test)
        controls_layout.addSpacing(20)
        controls_layout.addWidget(lbl_info)
        controls_layout.addWidget(self.list_widget)
        controls_layout.addWidget(self.btn_save)
        controls_layout.addStretch()

        main_layout.addLayout(images_layout, 70)
        main_layout.addLayout(controls_layout, 30)

    def select_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Images (*.jpg *.jpeg *.png *.bmp)", options=options)
        if file_path:
            self.original_image_path = file_path
            pixmap = QPixmap(file_path)
            self.label_original.setPixmap(pixmap.scaled(self.label_original.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.label_tagged.setText("Analiz için 'Test Et' butonuna basınız.")
            self.label_tagged.setPixmap(QPixmap())
            self.list_widget.clear()
            self.btn_test.setEnabled(True)
            self.btn_save.setEnabled(False)

    def test_image(self):
        if not self.model or not self.original_image_path:
            return

        # Tahmin Yap
        results = self.model(self.original_image_path)
        result = results[0]
        
        # Bounding Box'lı resmi al
        self.processed_image = result.plot() # BGR formatında döner
        
        # PyQt için BGR -> RGB çevir
        rgb_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Ekrana bas
        self.label_tagged.setPixmap(QPixmap.fromImage(q_img).scaled(self.label_tagged.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # Sonuçları Listele
        self.list_widget.clear()
        class_indices = result.boxes.cls.cpu().numpy().astype(int)
        
        if len(class_indices) == 0:
            self.list_widget.addItem("Nesne tespit edilemedi.")
        else:
            names = result.names
            counts = {}
            for idx in class_indices:
                name = names[idx]
                counts[name] = counts.get(name, 0) + 1
            
            for name, count in counts.items():
                self.list_widget.addItem(f"• {name}: {count} adet")
        
        self.btn_save.setEnabled(True)

    def save_image(self):
        if self.processed_image is None: return
        file_path, _ = QFileDialog.getSaveFileName(self, "Kaydet", "sonuc.jpg", "Images (*.jpg *.png)")
        if file_path:
            cv2.imwrite(file_path, self.processed_image)
            QMessageBox.information(self, "Başarılı", "Görüntü kaydedildi.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ObjectDetectionApp()
    window.show()
    sys.exit(app.exec_())