# 🚗 Smart Traffic Counter v3.3

> **Sistem Deteksi & Penghitungan Kendaraan Real-time dengan AI**  
> Powered by YOLO11 | Multi-Input Support | Database Integration

<div align="center">

![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-0078D6?style=for-the-badge&logo=windows)
![Python](https://img.shields.io/badge/Python-3.9--3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![YOLO](https://img.shields.io/badge/YOLO-v11-00FFFF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## ✨ Highlights

**SmartTrafficCounter** adalah aplikasi canggih untuk menghitung kendaraan secara otomatis menggunakan kecerdasan buatan. Dengan antarmuka GUI yang intuitif dan performa tinggi, aplikasi ini cocok untuk monitoring lalu lintas, analisis data transportasi, dan penelitian.

<img width="1920" height="1080" alt="SmartTrafficCounter Interface" src="https://github.com/user-attachments/assets/c51caad7-a9d9-4a93-ab4a-b76c4fb0d705" />

---

## 🎯 Fitur Unggulan

### 🎥 **Multi-Source Input**
- **Screen Capture** - Rekam area layar (region/fullscreen) dengan performa tinggi via `mss`
- **Webcam** - Support multiple webcam dengan pemilihan index mudah
- **Network Stream** - RTSP/HTTP streaming untuk CCTV dan IP camera

### 🧠 **Mode Deteksi Fleksibel**
| Mode | Deskripsi | Use Case |
|------|-----------|----------|
| **RAW + Counting** ⭐ | Bbox asli YOLO + counting background | Visualisasi akurat & analisis simultan |
| **RAW Only** | Pure detection tanpa tracking | Debugging & validasi model |
| **Tracking Mode** | Tracker dengan ID & trajectory | Monitoring detail pergerakan |

### 📊 **Smart Counting System**
- ✅ Deteksi arah **UP/DOWN** dengan single line counter
- ✅ Multi-class detection (mobil, motor, truk, bus)
- ✅ Adjustable counting band untuk akurasi maksimal
- ✅ Invert direction untuk fleksibilitas setup

### 💾 **Database & Analytics**
- **SQLite** (default) atau **MySQL** support
- Data Viewer built-in dengan search & filter
- Export data untuk analisis lanjutan
- Backup & Restore functionality

### ⚡ **Performance Optimization**
- ROI-based processing untuk efisiensi CPU/GPU
- FPS control & threading untuk smoothness
- CUDA acceleration support (NVIDIA GPU)
- Half-precision (FP16) untuk speed boost

---

## 📋 Daftar Isi

- [Persyaratan Sistem](#-persyaratan-sistem)
- [Quick Start](#-quick-start)
- [Build dari Source](#-build-dari-source)
- [Panduan Penggunaan](#-panduan-penggunaan)
- [Konfigurasi](#-konfigurasi)
- [Tips & Tricks](#-tips--tricks)
- [Troubleshooting](#-troubleshooting)
- [Dokumentasi](#-dokumentasi)
- [Contributing](#-contributing)
- [License](#-license)

---

## 💻 Persyaratan Sistem

### Minimum Requirements
| Component | Specification |
|-----------|---------------|
| **OS** | Windows 10/11 (64-bit) |
| **CPU** | Intel Core i5 / AMD Ryzen 5 (generasi 6+) |
| **RAM** | 8 GB |
| **Storage** | 2 GB free space |
| **GPU** | Integrated Graphics |

### Recommended Requirements
| Component | Specification |
|-----------|---------------|
| **CPU** | Intel Core i7 / AMD Ryzen 7 (generasi 8+) |
| **RAM** | 16 GB |
| **GPU** | NVIDIA GTX 1660+ with CUDA |
| **Storage** | SSD with 5 GB free space |

> 💡 **Catatan:** GPU NVIDIA dengan CUDA akan meningkatkan performa hingga **3-5x** lebih cepat!

---

## 🚀 Quick Start

### Metode 1: Jalankan .exe (Paling Mudah)

1. **Download Release**
   ```
   Unduh file .exe terbaru dari halaman Releases
   ```

2. **Extract & Run**
   ```
   📁 dist/SmartTrafficCounter/
   └── 🚀 SmartTrafficCounter.exe  ← Klik 2x
   ```

3. **Bypass SmartScreen** (jika muncul)
   - Klik **"More info"**
   - Klik **"Run anyway"**

4. **Setup Awal**
   - Pilih sumber input (Screen/Webcam/Network)
   - Klik **"Start Preview"**
   - Gambar garis counting dengan **"Draw Line"**
   - Klik **"Start Detection"** 🎉

---

## 🛠️ Build dari Source

### Persiapan Environment

```bash
# 1. Clone repository
git clone https://github.com/yourusername/SmartTraffic-eyes.git
cd SmartTraffic-eyes

# 2. Buat virtual environment
python -m venv .venv

# 3. Aktivasi venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 4. Upgrade pip
python -m pip install --upgrade pip
```

### Install Dependencies

```bash
# Install semua dependencies
pip install pyinstaller ultralytics torch torchvision opencv-python numpy Pillow mss pyautogui

# Untuk GPU support (NVIDIA CUDA)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Build Executable

```bash
# Build dengan PyInstaller (mode onedir)
python -m PyInstaller --noconfirm --clean SmartTrafficCounter.spec

# Output akan tersedia di:
# dist/SmartTrafficCounter/SmartTrafficCounter.exe
```

> 📦 **Mode OneDIR vs OneFile:**  
> - **OneDir** (Recommended): Lebih cepat startup, mudah debug
> - **OneFile**: Single executable, tapi ekstraksi saat runtime

---

## 📖 Panduan Penggunaan

### 1️⃣ Pilih Input Source

<table>
<tr>
<td width="33%">

#### 🖥️ Screen Capture
- Klik **"Select Region"**
- Drag area yang ingin dimonitor
- Atau gunakan **"Full Screen"**
- Tekan **"Start Preview"**

</td>
<td width="33%">

#### 📷 Webcam
- Pilih **Webcam Index** (0, 1, 2...)
- Tekan **"Start Preview"**
- Pastikan webcam terdeteksi

</td>
<td width="33%">

#### 🌐 Network Stream
- Paste **URL Stream**
  ```
  rtsp://user:pass@ip:port/stream
  http://ip:port/video
  ```
- Tekan **"Start Preview"**

</td>
</tr>
</table>

<img width="1920" height="1069" alt="Input Selection" src="https://github.com/user-attachments/assets/6b9c2f8b-78a3-4788-b572-9db2183835e8" />

### 2️⃣ Atur Counting Line

```
┌─────────────────────────┐
│                         │
│   🚗  →  →  →  →  →    │ ⬆️ UP
│  ═══════════════════    │ ← Counting Line
│   ←  ←  ←  🚗  ←  ←    │ ⬇️ DOWN
│                         │
└─────────────────────────┘
```

1. Klik **"Draw Line"**
2. Klik-drag untuk menggambar garis
3. Lepas mouse untuk menetapkan
4. Jika arah terbalik → Enable **"invert_direction"**

### 3️⃣ Mulai Deteksi

```
Start Detection → Mode RAW + Counting aktif
                ↓
        [YOLO Deteksi] → [Tracker] → [Counter]
                ↓
        Visualisasi Real-time + Count UP/DOWN
```

### 4️⃣ Simpan & Analisis Data

- Klik **"Save to Database"**
- Buka **"Data Viewer"** untuk melihat history
- Export data untuk analisis Excel/Python

<img width="945" height="1072" alt="Data Viewer" src="https://github.com/user-attachments/assets/09f266d2-3a00-49c6-be2b-a91162853674" />

---

## ⚙️ Konfigurasi

Semua pengaturan disimpan di `settings.json`. Berikut parameter penting:

### 🎯 Model Settings

```json
{
  "model": {
    "model_path": "yolo11n.pt",      // yolo11n/s/m/l/x
    "confidence_threshold": 0.45,     // 0.25 - 0.70
    "detection_confidence": 0.45,
    "iou_threshold": 0.45,
    "device": "auto"                  // auto/cpu/cuda
  }
}
```

### 📏 Line Settings

```json
{
  "line_settings": {
    "band_px": 15,                    // 12-20 untuk akurasi
    "invert_direction": false         // Flip UP/DOWN
  }
}
```

### ⚡ Runtime Optimization

```json
{
  "runtime": {
    "imgsz": 576,                     // 416/512/576/640
    "use_half": true,                 // FP16 untuk GPU
    "use_roi_around_line": true,      // ROI optimization
    
    // RAW Mode Settings
    "raw_counting_mode": true,        // RAW visual + counting
    "raw_detections_mode": false,     // RAW only (no count)
    "raw_conf": 0.25,                 // Confidence threshold
    "raw_iou": 0.70,                  // NMS IoU threshold
    "raw_draw_ids": true,             // Show Track ID
    "raw_show_all_classes": false     // Filter vehicle only
  }
}
```

### 🔧 Tracking Tuning (`config.py`)

```python
TRACKING_CONFIG = {
    'max_match_distance': 70,         # 50-80, turunkan jika ID merge
    'max_track_lost_frames': 30,      # Persistence track
    'min_track_stability': 3,         # Frame sebelum count
    'position_smoothing': 0.3         # Smoothing factor
}
```

---

## 💡 Tips & Tricks

### 🎨 Untuk Visualisasi Terbaik

```python
✅ Gunakan RAW + Counting mode (default)
✅ Enable raw_draw_ids untuk tracking visual
✅ Set raw_iou = 0.70-0.75 untuk dense traffic
✅ Disable raw_show_all_classes untuk fokus kendaraan
```

### 🏃 Untuk Performa Maksimal

```python
⚡ Gunakan GPU CUDA (3-5x lebih cepat)
⚡ Enable use_half (FP16) di GPU
⚡ Turunkan imgsz ke 512 jika FPS rendah
⚡ Aktifkan use_roi_around_line
⚡ Disable raw_draw_ids jika tidak perlu
```

### 🎯 Untuk Akurasi Counting

```python
🎯 Perbesar band_px jika banyak miss (coba 18-20)
🎯 Naikkan raw_iou ke 0.75 jika bbox merge
🎯 Turunkan max_match_distance (50-60) untuk dense
🎯 Pastikan garis melintang sempurna jalur kendaraan
🎯 Gunakan invert_direction jika arah salah
```

---

## 🔧 Troubleshooting

<details>
<summary><b>❌ Tidak ada dist/ atau .exe setelah build</b></summary>

**Solusi:**
```bash
# Pastikan PyInstaller terinstall
pip install pyinstaller

# Jalankan build dengan spec
python -m PyInstaller --noconfirm --clean SmartTrafficCounter.spec

# Cek output
dir dist\SmartTrafficCounter
```
</details>

<details>
<summary><b>🚫 Bbox RAW tidak muncul</b></summary>

**Cek settings.json:**
```json
{
  "runtime": {
    "raw_counting_mode": true,      // HARUS true
    "raw_detections_mode": false,   // HARUS false
    "raw_conf": 0.25,
    "raw_iou": 0.70
  }
}
```
</details>

<details>
<summary><b>📉 Tidak menghitung saat kendaraan lewat</b></summary>

**Checklist:**
- [ ] Garis counting melintang jalur kendaraan?
- [ ] Band_px cukup besar (15-20)?
- [ ] Coba enable invert_direction
- [ ] Pastikan mode bukan RAW-only
- [ ] Cek min_track_stability tidak terlalu tinggi
</details>

<details>
<summary><b>🚗🚗🚗 Tiga kendaraan berdampingan hanya terhitung 1-2</b></summary>

**Solusi:**
```json
{
  "runtime": {
    "raw_iou": 0.75  // Naikkan dari 0.70
  }
}
```

Dan turunkan di `config.py`:
```python
TRACKING_CONFIG = {
    'max_match_distance': 55  // Turunkan dari 70
}
```
</details>

<details>
<summary><b>🐌 FPS rendah / lag</b></summary>

**Optimasi:**
1. Turunkan `imgsz` → 512 atau 448
2. Disable `raw_draw_ids`
3. Enable `use_half` jika pakai GPU
4. Gunakan model lebih kecil (yolo11n)
5. Aktifkan `use_roi_around_line`
6. Install CUDA + torch-gpu
</details>

---

## 📚 Dokumentasi

| Dokumen | Deskripsi |
|---------|-----------|
| 📘 [User Manual](docs/User_Manual_SmartTrafficCounter.md) | Panduan lengkap pengguna |
| ⚡ [Quick Start](docs/Quick_Start_CheatSheet.md) | Cheat sheet & shortcuts |
| 🔧 [Troubleshooting](docs/Troubleshooting_FAQ.md) | FAQ & pemecahan masalah |
| ⚙️ [Settings Reference](docs/Settings_Reference.md) | Referensi lengkap konfigurasi |
| 📝 [Release Notes v3.3](docs/Release_Notes_v3.3.md) | Changelog & fitur baru |

---

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:

1. **Fork** repository ini
2. **Buat branch** feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** ke branch (`git push origin feature/AmazingFeature`)
5. **Open Pull Request**

### Development Setup

```bash
# Clone repo
git clone https://github.com/yourusername/SmartTraffic-eyes.git

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 SmartTrafficCounter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🌟 Acknowledgments

- **Ultralytics YOLO** - State-of-the-art object detection
- **OpenCV** - Computer vision library
- **PyTorch** - Deep learning framework
- **Community Contributors** - Thank you for your support!

---

## 📞 Support & Contact

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/SmartTraffic-eyes/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/SmartTraffic-eyes/discussions)
- 📧 **Email**: support@smarttraffic.com
- 🌐 **Website**: [smarttraffic.com](https://smarttraffic.com)

---

<div align="center">

### ⭐ Jika proyek ini bermanfaat, berikan bintang di GitHub!

**Made with ❤️ by SmartTrafficCounter Team**

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=smarttraffic.eyes)
![Stars](https://img.shields.io/github/stars/yourusername/SmartTraffic-eyes?style=social)
![Forks](https://img.shields.io/github/forks/yourusername/SmartTraffic-eyes?style=social)

</div>
