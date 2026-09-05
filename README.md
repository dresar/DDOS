# ⚡ DDOS Testing Tool - Educational Platform

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)]()

Platform edukasi lengkap untuk mempelajari konsep **DDOS (Distributed Denial of Service)** attack, keamanan jaringan, dan performa web server melalui stress testing di lingkungan localhost yang aman.

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Persyaratan Sistem](#-persyaratan-sistem)
- [Instalasi](#-instalasi)
- [Cara Menggunakan](#-cara-menggunakan)
- [API Documentation](#-api-documentation)
- [Konfigurasi](#-konfigurasi)
- [Arsitektur](#-arsitektur)
- [Keamanan](#-keamanan)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Fitur Utama

### 🌐 Web Interface
- **Dashboard Interaktif**: Interface web modern dan user-friendly
- **Real-time Monitoring**: Statistik update setiap detik saat attack berjalan
- **Console Terminal**: Log real-time untuk melihat progress attack
- **Form Konfigurasi**: Atur semua parameter attack langsung dari browser
- **Visual Statistics**: Card-based statistics dengan color coding

### ⚙️ Attack Features
- **Multi-threading**: Support hingga 1000 concurrent threads
- **Configurable Requests**: Hingga 10,000 requests per thread
- **IP Spoofing**: Simulasi random IP address melalui HTTP headers
- **Rate Limiting Detection**: Otomatis mendeteksi dan tracking rate limit responses
- **Multiple Endpoints**: Support testing multiple endpoints sekaligus
- **Flexible Delay**: Konfigurasi delay antar request (0-10 detik)

### 📊 Monitoring & Analytics
- **Real-time Stats**: Total requests, success rate, failed requests, rate limited
- **Attack History**: Menyimpan history semua attack dengan ID
- **Request Logging**: Log semua request dengan timestamp dan IP
- **IP Tracking**: Monitoring dan statistik per IP address
- **Performance Metrics**: Response time, throughput, success rate

### 🔌 API Endpoints
- **RESTful API**: Lengkap dengan CRUD operations
- **Health Check**: `/api/health` untuk monitoring
- **Attack Control**: Start, stop, stats, history
- **Logs Management**: View dan clear logs
- **IP Statistics**: Top IP addresses dan connection stats

### 📚 Educational Content
- **DDOS Explanation**: Penjelasan lengkap tentang konsep DDOS
- **Attack Process**: Step-by-step proses serangan
- **IP Manipulation**: Penjelasan tentang IP spoofing dan manipulation
- **Security Measures**: Cara melindungi dari DDOS attack
- **Best Practices**: Tips dan best practices untuk testing

## 💻 Persyaratan Sistem

### Minimum Requirements

**Hardware:**
- **Processor**: Intel Core i3 / AMD Ryzen 3 atau setara
- **RAM**: 4 GB
- **Storage**: 500 MB free space
- **Network**: Localhost connection (tidak perlu internet)

**Software:**
- **OS**: Windows 10/11, Linux (Ubuntu 18.04+), macOS 10.14+
- **Python**: 3.7 atau lebih baru
- **pip**: Python package manager

### Recommended Requirements

**Hardware:**
- **Processor**: Intel Core i5 / AMD Ryzen 5 atau lebih baik
- **RAM**: 8 GB atau lebih
- **Storage**: 1 GB free space (untuk logs dan history)
- **Network**: Localhost dengan bandwidth yang cukup

**Software:**
- **OS**: Windows 11, Linux (Ubuntu 20.04+), macOS 12+
- **Python**: 3.9 atau lebih baru (untuk performa optimal)
- **Browser**: Chrome 90+, Firefox 88+, Edge 90+ (untuk web interface)

### Optimal Requirements (untuk testing berat)

**Hardware:**
- **Processor**: Intel Core i7 / AMD Ryzen 7 atau lebih baik
- **RAM**: 16 GB atau lebih
- **Storage**: SSD dengan 2 GB free space
- **Network**: High-speed localhost connection

**Software:**
- **OS**: Latest stable version
- **Python**: 3.10+ (untuk performa terbaik)
- **Browser**: Latest version dengan hardware acceleration

### Spesifikasi Laptop yang Disarankan

#### Entry Level (Testing Ringan)
```
- Laptop: Acer Aspire 5, Lenovo IdeaPad 3
- CPU: Intel Core i3-1115G4 / AMD Ryzen 3 5300U
- RAM: 8 GB DDR4
- Storage: 256 GB SSD
- OS: Windows 11 / Ubuntu 22.04
- Harga: $400-600
```

#### Mid Range (Testing Sedang)
```
- Laptop: Dell Inspiron 15, HP Pavilion 15
- CPU: Intel Core i5-1135G7 / AMD Ryzen 5 5500U
- RAM: 16 GB DDR4
- Storage: 512 GB SSD
- OS: Windows 11 / Ubuntu 22.04
- Harga: $600-900
```

#### High End (Testing Berat)
```
- Laptop: Dell XPS 15, MacBook Pro M1/M2
- CPU: Intel Core i7-11800H / Apple M1/M2
- RAM: 32 GB DDR4/DDR5
- Storage: 1 TB SSD
- OS: Windows 11 / macOS Ventura / Ubuntu 22.04
- Harga: $1200+
```

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/ddos-testing-tool.git
cd ddos-testing-tool
```

### 2. Setup Virtual Environment

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verifikasi Instalasi

```bash
python ddos.py --help
```

## 📖 Cara Menggunakan

### Metode 1: Web Interface (Recommended)

1. **Jalankan Server:**
```bash
python ddos.py
```

2. **Buka Browser:**
```
http://127.0.0.1:5000
```

3. **Konfigurasi Attack:**
   - Masukkan Target URL
   - Set Jumlah Thread (1-1000)
   - Set Total Request per Thread (1-10000)
   - Set Delay antar Request (0-10 detik)
   - Pilih "Gunakan Random IP" untuk IP spoofing
   - Klik "Mulai Attack"

4. **Monitor Real-time:**
   - Lihat statistik di dashboard
   - Monitor console log
   - Klik "Stop Attack" untuk menghentikan

### Metode 2: Command Line Interface

**Basic Usage:**
```bash
python ddos.py --url http://127.0.0.1:5000/
```

**Advanced Usage:**
```bash
python ddos.py \
  --url http://127.0.0.1:5000/ \
  --threads 50 \
  --requests 1000 \
  --delay 0.05 \
  --endpoints / /api/status /api/info
```

**Options:**
- `--url, -u`: Target URL (default: http://127.0.0.1:5000/)
- `--threads, -t`: Jumlah thread (default: 10)
- `--requests, -r`: Request per thread (default: 100)
- `--delay, -d`: Delay antar request (default: 0.1)
- `--endpoints, -e`: List endpoints (default: /)

## 📡 API Documentation

### Health & Status

#### `GET /api/health`
Health check endpoint (tanpa rate limiting)

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "server": "DDOS Testing Tool",
  "version": "1.0.0"
}
```

#### `GET /api/status`
Status server dan informasi client

**Rate Limit:** 100 per minute

#### `GET /api/info`
Informasi lengkap tentang server dan endpoints

**Rate Limit:** 50 per minute

#### `GET /api/stats`
Statistik server dan request logging

**Rate Limit:** 20 per minute

### Attack Control (CRUD)

#### `POST /api/attack/start`
Memulai attack baru

**Request Body:**
```json
{
  "target_url": "http://127.0.0.1:5000/",
  "num_threads": 10,
  "num_requests": 100,
  "delay": 0.1,
  "use_random_ip": false
}
```

#### `POST /api/attack/stop`
Menghentikan attack yang sedang berjalan

#### `GET /api/attack/stats`
Mendapatkan statistik attack real-time

#### `GET /api/attack/history`
Mendapatkan history semua attack

#### `GET /api/attack/<id>`
Mendapatkan detail attack tertentu

#### `DELETE /api/attack/<id>`
Menghapus attack dari history

#### `POST /api/attack/clear`
Menghapus semua history attack

### Logs & Monitoring

#### `GET /api/logs?limit=100`
Mendapatkan request logs

#### `POST /api/logs/clear`
Menghapus semua logs

#### `GET /api/ips?top=10`
Mendapatkan statistik IP addresses

**Dokumentasi lengkap:** Lihat [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## ⚙️ Konfigurasi

### Web Interface Configuration

| Parameter | Range | Default | Deskripsi |
|-----------|-------|---------|-----------|
| Target URL | - | `http://127.0.0.1:5000/` | URL target untuk attack |
| Jumlah Thread | 1-1000 | 10 | Concurrent connections |
| Request per Thread | 1-10000 | 100 | Total request per thread |
| Delay | 0-10 detik | 0.1 | Delay antar request |
| Random IP | true/false | false | IP spoofing via headers |

### Rate Limiting

Default rate limits:
- **200 requests per hour**
- **50 requests per minute**

Endpoints yang exempt:
- `/api/health`
- `/api/attack/*` (kecuali history)
- `/api/logs/clear`

### Contoh Konfigurasi

**Light Test:**
- Threads: 10
- Requests/Thread: 100
- Total: 1,000 requests
- Estimated Time: ~10 detik

**Medium Test:**
- Threads: 50
- Requests/Thread: 200
- Total: 10,000 requests
- Estimated Time: ~40 detik

**Heavy Test:**
- Threads: 100
- Requests/Thread: 1000
- Total: 100,000 requests
- Estimated Time: ~100 detik

## 🏗️ Arsitektur

```
ddos.py (All-in-One)
├── AttackController Class
│   ├── Multi-threading support
│   ├── IP spoofing
│   ├── Statistics tracking
│   └── Error handling
├── Flask Web Server
│   ├── Web Interface (templates/index.html)
│   ├── RESTful API
│   ├── Rate Limiting
│   └── Request Logging
└── CLI Interface
    ├── Command line arguments
    ├── Real-time output
    └── Statistics reporting
```

### File Structure

```
ddos-testing-tool/
├── ddos.py                 # Main application (all-in-one)
├── templates/
│   └── index.html         # Web interface
├── requirements.txt       # Dependencies
├── README.md             # This file
├── API_DOCUMENTATION.md  # API docs
└── LICENSE              # MIT License
```

## 🔒 Keamanan

### Built-in Security Features

1. **Rate Limiting**: Membatasi request per IP address
2. **Request Logging**: Mencatat semua request untuk audit
3. **IP Tracking**: Monitoring koneksi per IP
4. **Connection Monitoring**: Deteksi pola traffic yang tidak normal
5. **Error Handling**: Comprehensive error handling dan validation

### Security Best Practices

- ✅ Hanya untuk testing di localhost
- ✅ Tidak mengirim data sensitif
- ✅ Rate limiting aktif untuk semua endpoints
- ✅ Input validation untuk semua user input
- ✅ Error messages tidak expose sensitive information

### ⚠️ Peringatan Penting

**JANGAN gunakan tool ini untuk:**
- ❌ Testing server yang bukan milik Anda
- ❌ Serangan terhadap sistem produksi
- ❌ Aktivitas ilegal apapun
- ❌ Mengganggu layanan pihak ketiga

**Tool ini HANYA untuk:**
- ✅ Edukasi dan pembelajaran
- ✅ Testing server sendiri di localhost
- ✅ Penelitian keamanan dengan izin
- ✅ Development dan testing environment

## 📊 Fitur Monitoring

### Real-time Statistics
- Total Requests
- Successful Requests
- Failed Requests
- Rate Limited (429)
- Success Rate (%)
- Average Response Time
- Throughput (requests/second)

### Attack History
- Attack ID
- Configuration
- Start/End Time
- Final Statistics
- Status (running/stopped)

### Request Logs
- Timestamp
- IP Address
- Endpoint
- Status Code
- Response Time

## 🎓 Educational Content

Tool ini dilengkapi dengan penjelasan lengkap tentang:

1. **Konsep DDOS**: Apa itu DDOS dan bagaimana cara kerjanya
2. **Proses Serangan**: Step-by-step proses serangan DDOS
3. **IP Manipulation**: Teknik IP spoofing dan manipulation
4. **Security Measures**: Cara melindungi dari DDOS attack
5. **Best Practices**: Tips dan best practices untuk testing

Akses melalui web interface dengan klik tombol "Tampilkan/Sembunyikan Penjelasan DDOS"

## ❓ FAQ

### Q: Apakah tool ini aman digunakan?
**A:** Ya, tool ini aman untuk digunakan di localhost untuk tujuan edukasi. Jangan gunakan untuk testing server yang bukan milik Anda.

### Q: Apakah IP spoofing benar-benar mengubah IP?
**A:** Tidak, tool ini hanya menggunakan HTTP headers (X-Forwarded-For, X-Real-IP) untuk simulasi. IP spoofing sebenarnya memerlukan akses level rendah ke network stack.

### Q: Berapa banyak request yang bisa dikirim?
**A:** Secara teknis tidak ada batasan, tetapi disarankan untuk tidak melebihi kapasitas sistem Anda. Default: 10 threads × 100 requests = 1,000 requests.

### Q: Apakah tool ini bisa digunakan untuk serangan nyata?
**A:** TIDAK. Tool ini hanya untuk edukasi di localhost. Menggunakan teknik serupa untuk serangan nyata adalah ILEGAL dan dapat mengakibatkan konsekuensi hukum.

### Q: Bagaimana cara menghentikan attack?
**A:** Klik tombol "Stop Attack" di web interface atau tekan Ctrl+C di command line.

### Q: Apakah data attack disimpan?
**A:** Ya, attack history disimpan di memory selama server berjalan. Logs dibatasi hingga 1000 entri terakhir.

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

### Guidelines

- Ikuti PEP 8 untuk Python code
- Tambahkan comments untuk kode yang kompleks
- Update dokumentasi untuk fitur baru
- Test semua perubahan sebelum commit

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Flask team untuk framework yang luar biasa
- Flask-Limiter untuk rate limiting functionality
- Requests library untuk HTTP client
- Semua contributor yang telah membantu

## 📈 Roadmap

- [ ] WebSocket support untuk real-time updates
- [ ] Database integration untuk persistent storage
- [ ] Grafana integration untuk advanced monitoring
- [ ] Docker containerization
- [ ] Kubernetes deployment guide
- [ ] Advanced attack patterns (Slowloris, HTTP Flood, dll)
- [ ] Machine learning untuk anomaly detection
- [ ] Multi-language support

## 📞 Support

Jika Anda memiliki pertanyaan atau butuh bantuan:

- 📧 Email: support@example.com
- 💬 Issues: [GitHub Issues](https://github.com/yourusername/ddos-testing-tool/issues)
- 📖 Documentation: [Wiki](https://github.com/yourusername/ddos-testing-tool/wiki)

---

<div align="center">

**⚠️ DISCLAIMER: Tool ini hanya untuk tujuan edukasi. Gunakan dengan bijak dan bertanggung jawab.**

Made with ❤️ for educational purposes

[⭐ Star this repo](https://github.com/yourusername/ddos-testing-tool) | [🐛 Report Bug](https://github.com/yourusername/ddos-testing-tool/issues) | [💡 Request Feature](https://github.com/yourusername/ddos-testing-tool/issues)

</div>
