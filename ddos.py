"""
DDOS Testing Tool - All-in-One
Menggabungkan website target, attack module, dan tester dalam satu file
Dilengkapi dengan web interface dan API endpoints lengkap
"""

from flask import Flask, jsonify, request, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import threading
import time
import random
import sys
import argparse
from datetime import datetime
from collections import defaultdict

# ============================================================================
# FLASK APP SETUP
# ============================================================================

app = Flask(__name__, template_folder='templates')

# Rate Limiting Configuration
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per hour", "50 per minute"],
    storage_uri="memory://"
)

# ============================================================================
# ATTACK CONTROLLER CLASS
# ============================================================================

class AttackController:
    def __init__(self):
        self.is_running = False
        self.threads = []
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "rate_limited": 0,
            "total_time": 0,
            "errors": [],
            "start_time": None,
            "end_time": None
        }
        self.stats_lock = threading.Lock()
        self.config = {
            "target_url": "",
            "num_threads": 10,
            "num_requests": 100,
            "delay": 0.1,
            "use_random_ip": False
        }
    
    def generate_random_ip(self):
        """Generate random IP address untuk spoofing"""
        return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    def send_request(self, thread_id, request_num, endpoint=""):
        """Mengirim single HTTP request"""
        url = self.config["target_url"].rstrip('/') + endpoint
        
        headers = {}
        if self.config["use_random_ip"]:
            headers["X-Forwarded-For"] = self.generate_random_ip()
            headers["X-Real-IP"] = self.generate_random_ip()
        
        try:
            start_time = time.time()
            response = requests.get(url, headers=headers, timeout=5)
            elapsed_time = time.time() - start_time
            
            with self.stats_lock:
                self.stats["total_requests"] += 1
                self.stats["total_time"] += elapsed_time
                
                if response.status_code == 200:
                    self.stats["successful_requests"] += 1
                elif response.status_code == 429:
                    self.stats["rate_limited"] += 1
                    self.stats["failed_requests"] += 1
                else:
                    self.stats["failed_requests"] += 1
                    self.stats["errors"].append({
                        "thread": thread_id,
                        "request": request_num,
                        "status": response.status_code,
                        "time": datetime.now().isoformat()
                    })
        
        except requests.exceptions.RequestException as e:
            with self.stats_lock:
                self.stats["total_requests"] += 1
                self.stats["failed_requests"] += 1
                self.stats["errors"].append({
                    "thread": thread_id,
                    "request": request_num,
                    "error": str(e),
                    "time": datetime.now().isoformat()
                })
    
    def worker_thread(self, thread_id, endpoints=None):
        """Worker function untuk setiap thread"""
        if endpoints is None:
            endpoints = [""]
        
        request_count = 0
        while self.is_running and request_count < self.config["num_requests"]:
            endpoint = endpoints[request_count % len(endpoints)]
            self.send_request(thread_id, request_count + 1, endpoint)
            request_count += 1
            time.sleep(self.config["delay"])
    
    def start(self, config):
        """Memulai attack dengan konfigurasi tertentu"""
        if self.is_running:
            return False, "Attack sudah berjalan"
        
        self.config = config
        self.is_running = True
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "rate_limited": 0,
            "total_time": 0,
            "errors": [],
            "start_time": datetime.now().isoformat(),
            "end_time": None
        }
        self.threads = []
        
        # Test koneksi awal
        try:
            test_url = self.config["target_url"].rstrip('/')
            response = requests.get(test_url, timeout=5)
        except requests.exceptions.RequestException as e:
            self.is_running = False
            return False, f"Tidak dapat terhubung ke target: {str(e)}"
        
        # Buat dan jalankan thread
        for i in range(self.config["num_threads"]):
            thread = threading.Thread(target=self.worker_thread, args=(i + 1, [""]))
            thread.daemon = True
            self.threads.append(thread)
            thread.start()
        
        return True, "Attack dimulai"
    
    def stop(self):
        """Menghentikan attack"""
        if not self.is_running:
            return False, "Attack tidak sedang berjalan"
        
        self.is_running = False
        
        # Tunggu semua thread selesai
        for thread in self.threads:
            thread.join(timeout=2)
        
        self.stats["end_time"] = datetime.now().isoformat()
        self.threads = []
        
        return True, "Attack dihentikan"
    
    def get_stats(self):
        """Mendapatkan statistik attack"""
        with self.stats_lock:
            stats_copy = self.stats.copy()
            # Batasi error list hanya 100 terakhir
            if len(stats_copy["errors"]) > 100:
                stats_copy["errors"] = stats_copy["errors"][-100:]
        return stats_copy
    
    def is_active(self):
        """Cek apakah attack sedang berjalan"""
        return self.is_running

# Global instance
attack_controller = AttackController()

# ============================================================================
# MONITORING & LOGGING
# ============================================================================

request_log = []
connection_stats = defaultdict(int)
attack_history = []  # History semua attack yang pernah dijalankan
stats_lock = threading.Lock()

def log_request(ip, endpoint, status_code, response_time):
    """Mencatat request ke log"""
    with stats_lock:
        request_log.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": ip,
            "endpoint": endpoint,
            "status": status_code,
            "response_time": response_time
        })
        connection_stats[ip] += 1
        # Batasi log hanya 1000 entri terakhir
        if len(request_log) > 1000:
            request_log.pop(0)

# ============================================================================
# WEB ROUTES
# ============================================================================

@app.route('/')
def index():
    """Halaman utama website dengan web interface untuk attack"""
    start_time = time.time()
    client_ip = get_remote_address()
    
    response_time = time.time() - start_time
    log_request(client_ip, '/', 200, response_time)
    
    return render_template('index.html')

# ============================================================================
# API ENDPOINTS - HEALTH & STATUS
# ============================================================================

@app.route('/api/health', methods=['GET'])
@limiter.exempt
def api_health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": "DDOS Testing Tool",
        "version": "1.0.0"
    }), 200

@app.route('/api/status', methods=['GET'])
@limiter.limit("100 per minute")
def api_status():
    """API endpoint untuk status server"""
    start_time = time.time()
    client_ip = get_remote_address()
    
    response_data = {
        "status": "aktif",
        "server_time": datetime.now().isoformat(),
        "client_ip": client_ip,
        "total_requests_from_ip": connection_stats.get(client_ip, 0),
        "uptime": "running",
        "attack_active": attack_controller.is_active()
    }
    
    response_time = time.time() - start_time
    log_request(client_ip, '/api/status', 200, response_time)
    
    return jsonify(response_data), 200

@app.route('/api/info', methods=['GET'])
@limiter.limit("50 per minute")
def api_info():
    """API endpoint untuk informasi server"""
    start_time = time.time()
    client_ip = get_remote_address()
    
    response_data = {
        "server": "DDOS Testing Tool",
        "version": "1.0.0",
        "purpose": "Edukasi DDOS Testing",
        "security_features": [
            "Rate Limiting",
            "Request Logging",
            "Connection Monitoring",
            "IP Tracking"
        ],
        "client_info": {
            "ip": client_ip,
            "user_agent": request.headers.get('User-Agent', 'Unknown')
        },
        "endpoints": {
            "web": "/",
            "health": "/api/health",
            "status": "/api/status",
            "info": "/api/info",
            "stats": "/api/stats",
            "attack_start": "/api/attack/start",
            "attack_stop": "/api/attack/stop",
            "attack_stats": "/api/attack/stats",
            "attack_history": "/api/attack/history",
            "attack_get": "/api/attack/<id>",
            "attack_delete": "/api/attack/<id>",
            "logs": "/api/logs",
            "ips": "/api/ips"
        }
    }
    
    response_time = time.time() - start_time
    log_request(client_ip, '/api/info', 200, response_time)
    
    return jsonify(response_data), 200

@app.route('/api/stats', methods=['GET'])
@limiter.limit("20 per minute")
def api_stats():
    """API endpoint untuk statistik server"""
    start_time = time.time()
    client_ip = get_remote_address()
    
    # Ambil 10 request terakhir
    recent_requests = request_log[-10:] if len(request_log) > 10 else request_log
    
    response_data = {
        "total_unique_ips": len(connection_stats),
        "total_requests_logged": len(request_log),
        "recent_requests": recent_requests,
        "top_ips": dict(sorted(connection_stats.items(), key=lambda x: x[1], reverse=True)[:5]),
        "attack_active": attack_controller.is_active()
    }
    
    response_time = time.time() - start_time
    log_request(client_ip, '/api/stats', 200, response_time)
    
    return jsonify(response_data), 200

# ============================================================================
# API ENDPOINTS - ATTACK CONTROL (CRUD)
# ============================================================================

@app.route('/api/attack/start', methods=['POST'])
@limiter.exempt
def api_attack_start():
    """API untuk memulai attack (CREATE)"""
    try:
        data = request.get_json() or {}
        
        config = {
            "target_url": data.get("target_url", ""),
            "num_threads": int(data.get("num_threads", 10)),
            "num_requests": int(data.get("num_requests", 100)),
            "delay": float(data.get("delay", 0.1)),
            "use_random_ip": bool(data.get("use_random_ip", False))
        }
        
        if not config["target_url"]:
            return jsonify({"success": False, "message": "Target URL tidak boleh kosong"}), 400
        
        success, message = attack_controller.start(config)
        
        if success:
            # Simpan ke history
            attack_record = {
                "id": len(attack_history) + 1,
                "config": config,
                "start_time": datetime.now().isoformat(),
                "status": "running"
            }
            attack_history.append(attack_record)
            
            return jsonify({
                "success": True,
                "message": message,
                "attack_id": attack_record["id"],
                "config": config
            }), 200
        else:
            return jsonify({"success": False, "message": message}), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/attack/stop', methods=['POST'])
@limiter.exempt
def api_attack_stop():
    """API untuk menghentikan attack"""
    try:
        success, message = attack_controller.stop()
        
        if success:
            # Update history terakhir
            if attack_history:
                attack_history[-1]["status"] = "stopped"
                attack_history[-1]["end_time"] = datetime.now().isoformat()
                attack_history[-1]["final_stats"] = attack_controller.get_stats()
        
        if success:
            return jsonify({"success": True, "message": message}), 200
        else:
            return jsonify({"success": False, "message": message}), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/attack/stats', methods=['GET'])
@limiter.exempt
def api_attack_stats():
    """API untuk mendapatkan statistik attack real-time (READ)"""
    try:
        stats = attack_controller.get_stats()
        stats["is_running"] = attack_controller.is_active()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/attack/history', methods=['GET'])
@limiter.limit("30 per minute")
def api_attack_history():
    """API untuk mendapatkan history semua attack (READ ALL)"""
    try:
        return jsonify({
            "total": len(attack_history),
            "history": attack_history[-20:]  # 20 terakhir
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/attack/<int:attack_id>', methods=['GET'])
@limiter.limit("30 per minute")
def api_attack_get(attack_id):
    """API untuk mendapatkan detail attack tertentu (READ ONE)"""
    try:
        attack = next((a for a in attack_history if a["id"] == attack_id), None)
        
        if attack:
            # Tambahkan stats jika attack masih berjalan atau sudah selesai
            if attack.get("status") == "running" and attack_controller.is_active():
                attack["current_stats"] = attack_controller.get_stats()
            return jsonify(attack), 200
        else:
            return jsonify({"error": "Attack tidak ditemukan"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/attack/<int:attack_id>', methods=['DELETE'])
@limiter.exempt
def api_attack_delete(attack_id):
    """API untuk menghapus attack dari history (DELETE)"""
    try:
        global attack_history
        attack = next((a for a in attack_history if a["id"] == attack_id), None)
        
        if attack:
            attack_history = [a for a in attack_history if a["id"] != attack_id]
            return jsonify({
                "success": True,
                "message": f"Attack ID {attack_id} dihapus dari history"
            }), 200
        else:
            return jsonify({"error": "Attack tidak ditemukan"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/attack/clear', methods=['POST'])
@limiter.exempt
def api_attack_clear():
    """API untuk menghapus semua history attack"""
    try:
        global attack_history
        count = len(attack_history)
        attack_history = []
        return jsonify({
            "success": True,
            "message": f"{count} attack dihapus dari history"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# API ENDPOINTS - LOGS & MONITORING
# ============================================================================

@app.route('/api/logs', methods=['GET'])
@limiter.limit("30 per minute")
def api_logs():
    """API untuk mendapatkan request logs"""
    try:
        limit = int(request.args.get('limit', 100))
        limit = min(limit, 1000)  # Max 1000
        
        logs = request_log[-limit:] if len(request_log) > limit else request_log
        
        return jsonify({
            "total": len(request_log),
            "returned": len(logs),
            "logs": logs
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/logs/clear', methods=['POST'])
@limiter.exempt
def api_logs_clear():
    """API untuk menghapus semua logs"""
    try:
        global request_log
        count = len(request_log)
        request_log = []
        return jsonify({
            "success": True,
            "message": f"{count} log dihapus"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ips', methods=['GET'])
@limiter.limit("30 per minute")
def api_ips():
    """API untuk mendapatkan statistik IP addresses"""
    try:
        top_n = int(request.args.get('top', 10))
        top_n = min(top_n, 50)  # Max 50
        
        sorted_ips = sorted(connection_stats.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        return jsonify({
            "total_unique_ips": len(connection_stats),
            "top_ips": [{"ip": ip, "count": count} for ip, count in sorted_ips]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(429)
def ratelimit_handler(e):
    """Handler untuk rate limit exceeded"""
    client_ip = get_remote_address()
    log_request(client_ip, request.path, 429, 0)
    
    return jsonify({
        "error": "Rate limit exceeded",
        "message": "Terlalu banyak request. Silakan coba lagi nanti.",
        "retry_after": str(e.retry_after) if hasattr(e, 'retry_after') else "60"
    }), 429

@app.errorhandler(404)
def not_found_handler(e):
    """Handler untuk 404"""
    return jsonify({"error": "Not Found", "message": "Endpoint tidak ditemukan"}), 404

@app.errorhandler(500)
def internal_error_handler(e):
    """Handler untuk 500"""
    return jsonify({"error": "Internal Server Error", "message": "Terjadi kesalahan pada server"}), 500

# ============================================================================
# COMMAND LINE INTERFACE (Tester)
# ============================================================================

def run_cli_tester():
    """Fungsi untuk menjalankan tester dari command line"""
    DEFAULT_TARGET_URL = "http://127.0.0.1:5000/"
    NUM_THREADS = 10
    REQUESTS_PER_THREAD = 100
    DELAY_BETWEEN_REQUESTS = 0.1
    
    # Statistik global
    stats = {
        "total_requests": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "rate_limited": 0,
        "total_time": 0,
        "errors": []
    }
    stats_lock = threading.Lock()
    
    def send_request(thread_id, request_num, endpoint="", target_url=""):
        """Mengirim single HTTP request"""
        url = target_url.rstrip('/') + endpoint
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=5)
            elapsed_time = time.time() - start_time
            
            with stats_lock:
                stats["total_requests"] += 1
                stats["total_time"] += elapsed_time
                
                if response.status_code == 200:
                    stats["successful_requests"] += 1
                    status_icon = "✓"
                elif response.status_code == 429:
                    stats["rate_limited"] += 1
                    stats["failed_requests"] += 1
                    status_icon = "⚠"
                else:
                    stats["failed_requests"] += 1
                    stats["errors"].append(f"Thread {thread_id}, Request {request_num}: Status {response.status_code}")
                    status_icon = "✗"
            
            print(f"[Thread {thread_id}] Request {request_num}: {status_icon} {response.status_code} ({elapsed_time:.3f}s)")
            
        except requests.exceptions.RequestException as e:
            with stats_lock:
                stats["total_requests"] += 1
                stats["failed_requests"] += 1
                stats["errors"].append(f"Thread {thread_id}, Request {request_num}: {str(e)}")
            
            print(f"[Thread {thread_id}] Request {request_num}: ✗ ERROR - {str(e)}")
    
    def worker_thread(thread_id, endpoints, target_url):
        """Worker function untuk setiap thread"""
        if endpoints is None:
            endpoints = [""]
        
        for i in range(REQUESTS_PER_THREAD):
            endpoint = endpoints[i % len(endpoints)]
            send_request(thread_id, i + 1, endpoint, target_url)
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    def print_statistics(target_url):
        """Mencetak statistik hasil testing"""
        print("\n" + "=" * 60)
        print("STATISTIK HASIL LOAD TESTING")
        print("=" * 60)
        print(f"Target URL: {target_url}")
        print(f"Total Request: {stats['total_requests']}")
        print(f"Request Berhasil: {stats['successful_requests']}")
        print(f"Request Gagal: {stats['failed_requests']}")
        print(f"Rate Limited (429): {stats['rate_limited']}")
        
        if stats['total_requests'] > 0:
            success_rate = (stats['successful_requests'] / stats['total_requests']) * 100
            avg_time = stats['total_time'] / stats['total_requests']
            print(f"Success Rate: {success_rate:.2f}%")
            print(f"Rata-rata Response Time: {avg_time:.3f} detik")
            
            if stats['rate_limited'] > 0:
                rate_limit_percent = (stats['rate_limited'] / stats['total_requests']) * 100
                print(f"Rate Limit Hit: {rate_limit_percent:.2f}%")
                print("  → Server memiliki rate limiting yang aktif!")
        
        if stats['errors']:
            print(f"\nJumlah Error: {len(stats['errors'])}")
            print("Contoh Error (5 pertama):")
            for error in stats['errors'][:5]:
                print(f"  - {error}")
        
        print("=" * 60)
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='DDOS Testing Tool - Command Line Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python ddos.py --url http://127.0.0.1:5000/
  python ddos.py --url http://localhost:5000/ --threads 20 --requests 200
  python ddos.py --url http://127.0.0.1:5000/api/status --delay 0.05
        """
    )
    parser.add_argument('--url', '-u', 
                       default=DEFAULT_TARGET_URL,
                       help=f'URL target untuk testing (default: {DEFAULT_TARGET_URL})')
    parser.add_argument('--threads', '-t',
                       type=int,
                       default=NUM_THREADS,
                       help=f'Jumlah thread bersamaan (default: {NUM_THREADS})')
    parser.add_argument('--requests', '-r',
                       type=int,
                       default=REQUESTS_PER_THREAD,
                       help=f'Jumlah request per thread (default: {REQUESTS_PER_THREAD})')
    parser.add_argument('--delay', '-d',
                       type=float,
                       default=DELAY_BETWEEN_REQUESTS,
                       help=f'Delay antar request dalam detik (default: {DELAY_BETWEEN_REQUESTS})')
    parser.add_argument('--endpoints', '-e',
                       nargs='+',
                       default=[''],
                       help='List endpoint untuk testing (default: root "/")')
    
    args = parser.parse_args()
    
    # Update konfigurasi
    TARGET_URL = args.url.rstrip('/') + '/'
    NUM_THREADS = args.threads
    REQUESTS_PER_THREAD = args.requests
    DELAY_BETWEEN_REQUESTS = args.delay
    endpoints = args.endpoints
    
    print("=" * 60)
    print("DDOS TESTING TOOL - COMMAND LINE INTERFACE")
    print("=" * 60)
    print(f"Target URL: {TARGET_URL}")
    print(f"Jumlah Thread: {NUM_THREADS}")
    print(f"Request per Thread: {REQUESTS_PER_THREAD}")
    print(f"Total Request: {NUM_THREADS * REQUESTS_PER_THREAD}")
    print(f"Delay antar Request: {DELAY_BETWEEN_REQUESTS} detik")
    print(f"Endpoints: {', '.join(endpoints) if endpoints else '/'}")
    print("=" * 60)
    
    # Test koneksi awal
    try:
        print("\nMenguji koneksi ke server...")
        test_url = TARGET_URL.rstrip('/') + (endpoints[0] if endpoints else '')
        response = requests.get(test_url, timeout=5)
        if response.status_code == 200:
            print("✓ Server merespons dengan baik!")
        elif response.status_code == 429:
            print("⚠ Server merespons dengan Rate Limit (429)")
            print("  → Server memiliki rate limiting yang aktif")
        else:
            print(f"⚠ Server merespons dengan status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ ERROR: Tidak dapat terhubung ke server!")
        print(f"  Pastikan server sudah berjalan di {TARGET_URL}")
        print(f"  Error: {str(e)}")
        sys.exit(1)
    
    print("\nMemulai load testing...")
    print("Tekan Ctrl+C untuk menghentikan lebih awal\n")
    
    start_time = time.time()
    threads = []
    
    try:
        # Membuat dan memulai semua thread
        for i in range(NUM_THREADS):
            thread = threading.Thread(target=worker_thread, args=(i + 1, endpoints, TARGET_URL))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # Menunggu semua thread selesai
        for thread in threads:
            thread.join()
        
        elapsed_time = time.time() - start_time
        
        print_statistics(TARGET_URL)
        if elapsed_time > 0:
            print(f"\nTotal waktu testing: {elapsed_time:.2f} detik")
            print(f"Throughput: {stats['total_requests'] / elapsed_time:.2f} request/detik")
        
    except KeyboardInterrupt:
        print("\n\nLoad testing dihentikan oleh user (Ctrl+C)")
        print_statistics(TARGET_URL)

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    import sys
    
    # Cek jika dijalankan dengan mode CLI (ada argument)
    if len(sys.argv) > 1 and sys.argv[1] not in ['--help', '-h']:
        # Jalankan sebagai CLI tester
        run_cli_tester()
    else:
        # Jalankan sebagai web server
        print("=" * 60)
        print("DDOS TESTING TOOL - WEB SERVER")
        print("=" * 60)
        print("Server dimulai di http://127.0.0.1:5000")
        print("Fitur:")
        print("  - Web Interface: http://127.0.0.1:5000")
        print("  - API Health: http://127.0.0.1:5000/api/health")
        print("  - API Status: http://127.0.0.1:5000/api/status")
        print("  - API Info: http://127.0.0.1:5000/api/info")
        print("  - API Attack: http://127.0.0.1:5000/api/attack/*")
        print("  - API Logs: http://127.0.0.1:5000/api/logs")
        print("  - Rate Limiting: 200/hour, 50/minute")
        print("  - Request Logging: Aktif")
        print("  - Connection Monitoring: Aktif")
        print("  - IP Tracking: Aktif")
        print("=" * 60)
        print("Tekan Ctrl+C untuk menghentikan server")
        print("=" * 60)
        
        app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)

