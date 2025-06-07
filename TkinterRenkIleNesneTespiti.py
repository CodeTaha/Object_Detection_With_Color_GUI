import cv2
import numpy as np
import tkinter as tk
from tkinter import Scale
from PIL import Image, ImageTk
from collections import deque

# Kamera başlat
cap = cv2.VideoCapture(0)
cap.set(3, 1440)
cap.set(4, 810)

# Tkinter arayüzü
root = tk.Tk()
root.title("Renk Takip Uygulaması")

# Ana Frame, içerikleri yerleştirecek
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Butonlar için Frame
button_frame = tk.Frame(main_frame)
button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

# Video görüntüsü için Frame
video_frame = tk.Frame(main_frame)
video_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")

# Frame içinde kamera görüntüsü
video_label = tk.Label(video_frame)
video_label.pack()

# Nesne merkezini depolayacak veri tipi
buffer_size = 16
pts = deque(maxlen=buffer_size)

# HSV sınırlarını güncelleme fonksiyonu
def update_values():
    global lower_bound, upper_bound
    h_min = hue_min.get()
    h_max = hue_max.get()
    s_min = sat_min.get()
    s_max = sat_max.get()
    v_min = val_min.get()
    v_max = val_max.get()
    
    lower_bound = (h_min, s_min, v_min)
    upper_bound = (h_max, s_max, v_max)

# Trackbarlar (HSV sınırlarını ayarlamak için)
hue_min = Scale(button_frame, from_=0, to=179, label="Hue Min", orient="horizontal", command=lambda x: update_values())
hue_min.set(90)
hue_min.grid(row=0, column=0, padx=5, pady=5)

hue_max = Scale(button_frame, from_=0, to=179, label="Hue Max", orient="horizontal", command=lambda x: update_values())
hue_max.set(130)
hue_max.grid(row=1, column=0, padx=5, pady=5)

sat_min = Scale(button_frame, from_=0, to=255, label="Saturation Min", orient="horizontal", command=lambda x: update_values())
sat_min.set(50)
sat_min.grid(row=2, column=0, padx=5, pady=5)

sat_max = Scale(button_frame, from_=0, to=255, label="Saturation Max", orient="horizontal", command=lambda x: update_values())
sat_max.set(255)
sat_max.grid(row=3, column=0, padx=5, pady=5)

val_min = Scale(button_frame, from_=0, to=255, label="Value Min", orient="horizontal", command=lambda x: update_values())
val_min.set(50)
val_min.grid(row=4, column=0, padx=5, pady=5)

val_max = Scale(button_frame, from_=0, to=255, label="Value Max", orient="horizontal", command=lambda x: update_values())
val_max.set(255)
val_max.grid(row=5, column=0, padx=5, pady=5)

# Başlangıç HSV sınırları
lower_bound = (hue_min.get(), sat_min.get(), val_min.get())
upper_bound = (hue_max.get(), sat_max.get(), val_max.get())

# Kamera görüntüsünü güncelleme fonksiyonu
def update_frame():
    global cap, lower_bound, upper_bound, pts
    
    ret, imgOriginal = cap.read()
    if ret:
        # Blur ve HSV dönüştürme
        blurred = cv2.GaussianBlur(imgOriginal, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # Maske oluştur
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
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
            pts.appendleft(center)

            for i in range(1, len(pts)):
                if pts[i-1] is None or pts[i] is None:
                    continue
                cv2.line(imgOriginal, pts[i-1], pts[i], (0, 255, 0), 3)

        # OpenCV görüntüsünü Tkinter formatına çevirme
        imgOriginal = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(imgOriginal)
        imgtk = ImageTk.PhotoImage(image=img)

        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

    root.after(10, update_frame)

# Kamerayı kapatma fonksiyonu
def close_app():
    global cap
    if cap.isOpened():
        cap.release()  # Kamerayı serbest bırak
    cv2.destroyAllWindows()  # OpenCV pencerelerini kapat
    root.quit()  # Tkinter döngüsünü sonlandır
    root.destroy()  # Tkinter penceresini kapat

# Kapatma butonu
btn_exit = tk.Button(button_frame, text="Çıkış", command=close_app)
btn_exit.grid(row=6, column=0, padx=5, pady=10)

# Kamerayı başlat
update_frame()

# Tkinter çalıştır
root.mainloop()
