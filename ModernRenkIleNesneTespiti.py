import cv2
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageTk
from collections import deque
import threading
import time
import os
from datetime import datetime

# CustomTkinter tema ayarları
ctk.set_appearance_mode("dark")  # Koyu tema
ctk.set_default_color_theme("blue")  # Mavi renk teması

class ModernRenkTakipUygulamasi:
    def __init__(self):
        # Ana pencere
        self.root = ctk.CTk()
        self.root.title("Modern Renk Takip Uygulaması")
        self.root.geometry("1400x900")
        self.root.configure(fg_color="#1a1a1a")
        
        # Kamera başlat
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        
        # Nesne takip değişkenleri
        self.buffer_size = 32
        self.pts = deque(maxlen=self.buffer_size)
        self.is_running = True
        
        # Video kayıt değişkenleri
        self.is_recording = False
        self.video_writer = None
        self.recordings_folder = "video_kayitlari"
        self.recording_start_time = None
        self.recording_timer_id = None
        self.frame_counter = 0
        
        # Kayıt klasörünü oluştur
        if not os.path.exists(self.recordings_folder):
            os.makedirs(self.recordings_folder)
        
        # HSV sınırları
        self.lower_bound = (90, 50, 50)
        self.upper_bound = (130, 255, 255)
        
        # Renk paleti tanımları (HSV değerleri)
        self.renk_paleti = {
            "🔴 Kırmızı": {"lower": (0, 100, 100), "upper": (10, 255, 255)},
            "🟠 Turuncu": {"lower": (10, 100, 100), "upper": (25, 255, 255)},
            "🟡 Sarı": {"lower": (25, 100, 100), "upper": (35, 255, 255)},
            "🟢 Yeşil": {"lower": (35, 100, 100), "upper": (85, 255, 255)},
            "🔵 Mavi": {"lower": (100, 100, 100), "upper": (130, 255, 255)},
            "🟣 Mor": {"lower": (130, 100, 100), "upper": (170, 255, 255)},
            "🩷 Pembe": {"lower": (170, 100, 100), "upper": (180, 255, 255)},
            "⚪ Beyaz": {"lower": (0, 0, 200), "upper": (180, 30, 255)},
            "⚫ Siyah": {"lower": (0, 0, 0), "upper": (180, 255, 30)}
        }
        
        # Arayüz oluştur
        self.arayuz_olustur()
        
        # Kamera thread'ini başlat
        self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.camera_thread.start()
    
    def arayuz_olustur(self):
        # Ana container
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sol panel - Kontroller (genişlik artırıldı)
        left_panel = ctk.CTkFrame(main_container, fg_color="#2b2b2b", corner_radius=15, width=400)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        left_panel.pack_propagate(False)  # Panel boyutunu sabitle
        
        # Sol panel içeriği için scrollable frame
        left_scroll = ctk.CTkScrollableFrame(left_panel, fg_color="transparent", height=800)
        left_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Başlık
        title_label = ctk.CTkLabel(
            left_scroll, 
            text="🎯 Renk Takip Kontrolleri", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=(20, 20))
        
        # Renk Paleti Başlığı
        palette_title = ctk.CTkLabel(
            left_scroll,
            text="🎨 Hızlı Renk Seçimi",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        palette_title.pack(pady=(0, 15))
        
        # Renk Paleti Butonları
        palette_frame = ctk.CTkFrame(left_scroll, fg_color="transparent")
        palette_frame.pack(pady=(0, 20))
        
        # İlk satır (3 buton)
        row1_frame = ctk.CTkFrame(palette_frame, fg_color="transparent")
        row1_frame.pack(pady=5)
        
        self.create_color_button(row1_frame, "🔴 Kırmızı", "#ff0000", 0)
        self.create_color_button(row1_frame, "🟠 Turuncu", "#ff8000", 1)
        self.create_color_button(row1_frame, "🟡 Sarı", "#ffff00", 2)
        
        # İkinci satır (3 buton)
        row2_frame = ctk.CTkFrame(palette_frame, fg_color="transparent")
        row2_frame.pack(pady=5)
        
        self.create_color_button(row2_frame, "🟢 Yeşil", "#00ff00", 0)
        self.create_color_button(row2_frame, "🔵 Mavi", "#0080ff", 1)
        self.create_color_button(row2_frame, "🟣 Mor", "#8000ff", 2)
        
        # Üçüncü satır (3 buton)
        row3_frame = ctk.CTkFrame(palette_frame, fg_color="transparent")
        row3_frame.pack(pady=5)
        
        self.create_color_button(row3_frame, "🩷 Pembe", "#ff0080", 0)
        self.create_color_button(row3_frame, "⚪ Beyaz", "#ffffff", 1)
        self.create_color_button(row3_frame, "⚫ Siyah", "#000000", 2)
        
        # Manuel Kontrol Başlığı
        manual_title = ctk.CTkLabel(
            left_scroll,
            text="⚙️ Manuel HSV Kontrolü",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        manual_title.pack(pady=(20, 15))
        
        # HSV Kontrolleri
        self.hue_min = ctk.CTkSlider(
            left_scroll, 
            from_=0, 
            to=179, 
            number_of_steps=179,
            command=self.update_values,
            button_color="#007acc",
            button_hover_color="#005a99",
            progress_color="#007acc"
        )
        self.hue_min.set(90)
        
        self.hue_max = ctk.CTkSlider(
            left_scroll, 
            from_=0, 
            to=179, 
            number_of_steps=179,
            command=self.update_values,
            button_color="#007acc",
            button_hover_color="#005a99",
            progress_color="#007acc"
        )
        self.hue_max.set(130)
        
        self.sat_min = ctk.CTkSlider(
            left_scroll, 
            from_=0, 
            to=255, 
            number_of_steps=255,
            command=self.update_values,
            button_color="#00cc7a",
            button_hover_color="#00995a",
            progress_color="#00cc7a"
        )
        self.sat_min.set(50)
        
        self.sat_max = ctk.CTkSlider(
            left_scroll, 
            from_=0, 
            to=255, 
            number_of_steps=255,
            command=self.update_values,
            button_color="#00cc7a",
            button_hover_color="#00995a",
            progress_color="#00cc7a"
        )
        self.sat_max.set(255)
        
        self.val_min = ctk.CTkSlider(
            left_scroll, 
            from_=0, 
            to=255, 
            number_of_steps=255,
            command=self.update_values,
            button_color="#cc7a00",
            button_hover_color="#995a00",
            progress_color="#cc7a00"
        )
        self.val_min.set(50)
        
        self.val_max = ctk.CTkSlider(
            left_scroll, 
            from_=0, 
            to=255, 
            number_of_steps=255,
            command=self.update_values,
            button_color="#cc7a00",
            button_hover_color="#995a00",
            progress_color="#cc7a00"
        )
        self.val_max.set(255)
        
        # Slider etiketleri
        ctk.CTkLabel(left_scroll, text="🎨 Hue Min", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        self.hue_min.pack(pady=(0, 10), padx=20)
        
        ctk.CTkLabel(left_scroll, text="🎨 Hue Max", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        self.hue_max.pack(pady=(0, 10), padx=20)
        
        ctk.CTkLabel(left_scroll, text="🌈 Saturation Min", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        self.sat_min.pack(pady=(0, 10), padx=20)
        
        ctk.CTkLabel(left_scroll, text="🌈 Saturation Max", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        self.sat_max.pack(pady=(0, 10), padx=20)
        
        ctk.CTkLabel(left_scroll, text="💡 Value Min", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        self.val_min.pack(pady=(0, 10), padx=20)
        
        ctk.CTkLabel(left_scroll, text="💡 Value Max", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        self.val_max.pack(pady=(0, 10), padx=20)
        
        # Değer göstergeleri
        self.hue_label = ctk.CTkLabel(
            left_scroll, 
            text="Hue: 90-130", 
            font=ctk.CTkFont(size=12),
            text_color="#cccccc"
        )
        self.hue_label.pack(pady=10)
        
        self.sat_label = ctk.CTkLabel(
            left_scroll, 
            text="Saturation: 50-255", 
            font=ctk.CTkFont(size=12),
            text_color="#cccccc"
        )
        self.sat_label.pack(pady=5)
        
        self.val_label = ctk.CTkLabel(
            left_scroll, 
            text="Value: 50-255", 
            font=ctk.CTkFont(size=12),
            text_color="#cccccc"
        )
        self.val_label.pack(pady=5)
        
        # Butonlar - Şimdi görünür olacak
        button_frame = ctk.CTkFrame(left_scroll, fg_color="transparent")
        button_frame.pack(pady=20)
        
        # Başlat/Duraklat butonu
        self.start_button = ctk.CTkButton(
            button_frame,
            text="▶️ Başlat",
            command=self.toggle_camera,
            fg_color="#00cc7a",
            hover_color="#00995a",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=120
        )
        self.start_button.pack(pady=8)
        
        # Video Kayıt butonu
        self.record_button = ctk.CTkButton(
            button_frame,
            text="🔴 Kayıt Başlat",
            command=self.toggle_recording,
            fg_color="#cc0000",
            hover_color="#990000",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=120
        )
        self.record_button.pack(pady=8)
        
        # Sıfırla butonu - Büyük ve kalın
        self.reset_button = ctk.CTkButton(
            button_frame,
            text="🔄 Sıfırla",
            command=self.reset_values,
            fg_color="#cc7a00",
            hover_color="#995a00",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=140
        )
        self.reset_button.pack(pady=8)
        
        # Çıkış butonu
        self.exit_button = ctk.CTkButton(
            button_frame,
            text="❌ Çıkış",
            command=self.close_app,
            fg_color="#cc0000",
            hover_color="#990000",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=120
        )
        self.exit_button.pack(pady=8)
        
        # Sağ panel - Video
        right_panel = ctk.CTkFrame(main_container, fg_color="#2b2b2b", corner_radius=15)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Video başlığı
        video_title = ctk.CTkLabel(
            right_panel, 
            text="📹 Kamera Görüntüsü", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        video_title.pack(pady=20)
        
        # Kayıt süresi göstergesi
        self.recording_timer_label = ctk.CTkLabel(
            right_panel,
            text="⏱️ Kayıt Süresi: 00:00:00",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#cc0000"
        )
        self.recording_timer_label.pack(pady=(0, 10))
        self.recording_timer_label.pack_forget()  # Başlangıçta gizli
        
        # Video container
        self.video_container = ctk.CTkFrame(right_panel, fg_color="#1a1a1a", corner_radius=10)
        self.video_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Video label
        self.video_label = ctk.CTkLabel(
            self.video_container, 
            text="Kamera başlatılıyor...",
            font=ctk.CTkFont(size=16),
            text_color="#888888"
        )
        self.video_label.pack(expand=True)
        
        # Durum bilgisi
        self.status_label = ctk.CTkLabel(
            right_panel,
            text="🟡 Hazır",
            font=ctk.CTkFont(size=12),
            text_color="#cccccc"
        )
        self.status_label.pack(pady=10)
    
    def create_color_button(self, parent, text, color, column):
        """Renk paleti butonları oluştur"""
        # Açık renkler için siyah yazı, koyu renkler için beyaz yazı
        text_color = "#000000" if color in ["#ffff00", "#ffffff", "#00ff00"] else "#ffffff"
        
        button = ctk.CTkButton(
            parent,
            text=text,
            command=lambda: self.select_color(text),
            fg_color=color,
            hover_color=self.adjust_color_brightness(color, 0.8),
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35,
            width=80,
            corner_radius=20,
            text_color=text_color
        )
        button.grid(row=0, column=column, padx=5, pady=2)
        return button
    
    def adjust_color_brightness(self, color, factor):
        """Renk parlaklığını ayarla"""
        if color.startswith('#'):
            color = color[1:]
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def select_color(self, color_name):
        """Seçilen rengin HSV değerlerini ayarla"""
        if color_name in self.renk_paleti:
            color_data = self.renk_paleti[color_name]
            lower = color_data["lower"]
            upper = color_data["upper"]
            
            # Slider değerlerini güncelle
            self.hue_min.set(lower[0])
            self.hue_max.set(upper[0])
            self.sat_min.set(lower[1])
            self.sat_max.set(upper[1])
            self.val_min.set(lower[2])
            self.val_max.set(upper[2])
            
            # HSV sınırlarını güncelle
            self.lower_bound = lower
            self.upper_bound = upper
            
            # Etiketleri güncelle
            self.update_labels()
            
            # Durum mesajını güncelle
            self.status_label.configure(text=f"🎨 {color_name} seçildi", text_color="#00cc7a")
    
    def update_labels(self):
        """Etiketleri güncelle"""
        self.hue_label.configure(text=f"Hue: {int(self.hue_min.get())}-{int(self.hue_max.get())}")
        self.sat_label.configure(text=f"Saturation: {int(self.sat_min.get())}-{int(self.sat_max.get())}")
        self.val_label.configure(text=f"Value: {int(self.val_min.get())}-{int(self.val_max.get())}")
    
    def update_values(self, value):
        self.lower_bound = (int(self.hue_min.get()), int(self.sat_min.get()), int(self.val_min.get()))
        self.upper_bound = (int(self.hue_max.get()), int(self.sat_max.get()), int(self.val_max.get()))
        
        # Etiketleri güncelle
        self.update_labels()
    
    def reset_values(self):
        self.hue_min.set(90)
        self.hue_max.set(130)
        self.sat_min.set(50)
        self.sat_max.set(255)
        self.val_min.set(50)
        self.val_max.set(255)
        self.update_values(0)
        
        # Durum mesajını güncelle
        self.status_label.configure(text="🔄 Varsayılan değerler yüklendi", text_color="#cc7a00")
    
    def toggle_camera(self):
        if self.is_running:
            self.is_running = False
            self.start_button.configure(text="▶️ Başlat", fg_color="#00cc7a")
            self.status_label.configure(text="⏸️ Duraklatıldı", text_color="#cc7a00")
        else:
            self.is_running = True
            self.start_button.configure(text="⏸️ Duraklat", fg_color="#cc7a00")
            self.status_label.configure(text="🟢 Çalışıyor", text_color="#00cc7a")
    
    def toggle_recording(self):
        """Video kaydını başlat/durdur"""
        if not self.is_recording:
            # Kayıt başlat
            self.start_recording()
        else:
            # Kayıt durdur
            self.stop_recording()
    
    def start_recording(self):
        """Video kaydını başlat"""
        if not self.is_running:
            self.status_label.configure(text="❌ Önce kamerayı başlatın!", text_color="#cc0000")
            return
        
        # Kayıt dosya adını oluştur
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"kayit_{timestamp}.avi"
        filepath = os.path.join(self.recordings_folder, filename)
        
        # Video writer oluştur
        # MJPG codec kullan (daha iyi performans için)
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Sabit FPS kullan (kamera FPS'i yerine)
        target_fps = 15.0  # 15 FPS ile kayıt
        
        self.video_writer = cv2.VideoWriter(filepath, fourcc, target_fps, (frame_width, frame_height))
        
        if self.video_writer.isOpened():
            self.is_recording = True
            self.record_button.configure(text="⏹️ Kayıt Durdur", fg_color="#cc7a00")
            self.status_label.configure(text=f"🔴 Kayıt başladı: {filename}", text_color="#cc0000")
            
            # Kayıt süresi sayacını başlat
            self.recording_start_time = datetime.now()
            self.frame_counter = 0  # Frame sayacını sıfırla
            self.recording_timer_label.pack(pady=(0, 10))
            self.update_recording_timer()
        else:
            self.status_label.configure(text="❌ Kayıt başlatılamadı!", text_color="#cc0000")
    
    def stop_recording(self):
        """Video kaydını durdur"""
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        
        self.is_recording = False
        self.record_button.configure(text="🔴 Kayıt Başlat", fg_color="#cc0000")
        self.status_label.configure(text="✅ Kayıt durduruldu", text_color="#00cc7a")
        
        # Kayıt süresi göstergesini gizle ve timer'ı durdur
        self.recording_timer_label.pack_forget()
        if self.recording_timer_id:
            self.root.after_cancel(self.recording_timer_id)
            self.recording_timer_id = None
        self.recording_start_time = None
    
    def update_recording_timer(self):
        """Kayıt süresini güncelle"""
        if self.is_recording and self.recording_start_time:
            elapsed = datetime.now() - self.recording_start_time
            hours = int(elapsed.total_seconds() // 3600)
            minutes = int((elapsed.total_seconds() % 3600) // 60)
            seconds = int(elapsed.total_seconds() % 60)
            
            timer_text = f"⏱️ Kayıt Süresi: {hours:02d}:{minutes:02d}:{seconds:02d}"
            self.recording_timer_label.configure(text=timer_text)
            
            # Her 1 saniyede bir güncelle
            self.recording_timer_id = self.root.after(1000, self.update_recording_timer)
    
    def camera_loop(self):
        while True:
            if self.is_running:
                ret, imgOriginal = self.cap.read()
                if ret:
                    # Blur ve HSV dönüştürme
                    blurred = cv2.GaussianBlur(imgOriginal, (11, 11), 0)
                    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

                    # Maske oluştur
                    mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound)
                    mask = cv2.erode(mask, None, iterations=2)
                    mask = cv2.dilate(mask, None, iterations=2)

                    # Kontur bulma
                    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    center = None

                    if len(contours) > 0:
                        c = max(contours, key=cv2.contourArea)
                        rect = cv2.minAreaRect(c)
                        ((x, y), (width, height), rotation) = rect
                        
                        box = cv2.boxPoints(rect)
                        box = np.int64(box)

                        M = cv2.moments(c)
                        if M["m00"] != 0:
                            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                        else:
                            center = (0, 0)

                        cv2.drawContours(imgOriginal, [box], 0, (0, 255, 255), 2)
                        cv2.circle(imgOriginal, center, 5, (255, 0, 255), -1)

                        # Deque kullanarak nesnenin hareketini takip et
                        self.pts.appendleft(center)

                        for i in range(1, len(self.pts)):
                            if self.pts[i-1] is None or self.pts[i] is None:
                                continue
                            cv2.line(imgOriginal, self.pts[i-1], self.pts[i], (0, 255, 0), 3)

                    # Video kaydı yap
                    if self.is_recording and self.video_writer:
                        # Frame sayacını artır
                        self.frame_counter += 1
                        
                        # Her 2 frame'de bir kaydet (15 FPS için)
                        if self.frame_counter % 2 == 0:
                            self.video_writer.write(imgOriginal)
                    
                    # OpenCV görüntüsünü CustomTkinter formatına çevirme
                    imgOriginal = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(imgOriginal)
                    
                    # Görüntüyü yeniden boyutlandır
                    img = img.resize((800, 600), Image.Resampling.LANCZOS)
                    imgtk = ImageTk.PhotoImage(image=img)

                    # Ana thread'de güncelle
                    self.root.after(0, self.update_video_display, imgtk)
            
            # Minimum sleep süresi (çok hızlı döngüyü önle)
            time.sleep(0.001)
    
    def update_video_display(self, imgtk):
        self.video_label.configure(image=imgtk, text="")
        self.video_label.image = imgtk
    
    def close_app(self):
        """Uygulamayı tamamen kapat ve durdur"""
        # Video kaydını durdur
        if self.is_recording:
            self.stop_recording()
        
        # Timer'ı durdur
        if self.recording_timer_id:
            self.root.after_cancel(self.recording_timer_id)
        
        self.is_running = False
        if self.cap.isOpened():
            self.cap.release()
        try:
            cv2.destroyAllWindows()
        except:
            pass  # OpenCV hatası olursa görmezden gel
        self.root.quit()
        self.root.destroy()
        # Windows'ta tüm Python süreçlerini sonlandır
        import os
        os._exit(0)
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.mainloop()

if __name__ == "__main__":
    # CustomTkinter kurulu mu kontrol et
    try:
        import customtkinter
        app = ModernRenkTakipUygulamasi()
        app.run()
    except ImportError:
        print("CustomTkinter kurulu değil. Kuruluyor...")
        import subprocess
        subprocess.check_call(["pip", "install", "customtkinter"])
        print("CustomTkinter kuruldu. Uygulamayı tekrar çalıştırın.")
