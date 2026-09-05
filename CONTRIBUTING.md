# Contributing to DDOS Testing Tool

Terima kasih atas minat Anda untuk berkontribusi pada DDOS Testing Tool! 🎉

## Code of Conduct

Dengan berpartisipasi dalam proyek ini, Anda setuju untuk:
- Menghormati semua kontributor
- Menerima kritik yang konstruktif
- Fokus pada apa yang terbaik untuk komunitas
- Menunjukkan empati terhadap anggota komunitas lainnya

## How to Contribute

### Reporting Bugs

Jika Anda menemukan bug, silakan buat issue dengan:
- **Judul yang jelas dan deskriptif**
- **Deskripsi langkah-langkah untuk mereproduksi bug**
- **Perilaku yang diharapkan vs perilaku aktual**
- **Screenshots jika memungkinkan**
- **Informasi sistem** (OS, Python version, dll)

### Suggesting Enhancements

Untuk saran fitur baru:
- Cek apakah fitur sudah ada di roadmap
- Jelaskan use case dan manfaatnya
- Berikan contoh implementasi jika memungkinkan

### Pull Requests

1. **Fork repository**
2. **Buat branch baru** (`git checkout -b feature/amazing-feature`)
3. **Commit perubahan** (`git commit -m 'Add amazing feature'`)
4. **Push ke branch** (`git push origin feature/amazing-feature`)
5. **Buat Pull Request**

## Development Setup

1. Clone repository:
```bash
git clone https://github.com/yourusername/ddos-testing-tool.git
cd ddos-testing-tool
```

2. Setup virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# atau
.venv\Scripts\Activate.ps1  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run tests:
```bash
python ddos.py --help
```

## Coding Standards

### Python Code Style

- Ikuti **PEP 8** style guide
- Gunakan **4 spaces** untuk indentation
- Maksimal **79 karakter** per baris
- Gunakan **docstrings** untuk semua fungsi dan class

### Example

```python
def example_function(param1, param2):
    """
    Deskripsi singkat fungsi.
    
    Args:
        param1: Deskripsi parameter 1
        param2: Deskripsi parameter 2
    
    Returns:
        Deskripsi return value
    """
    # Implementation
    return result
```

### Commit Messages

Gunakan format berikut:
```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: Fitur baru
- `fix`: Bug fix
- `docs`: Dokumentasi
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Menambah test
- `chore`: Maintenance

**Example:**
```
feat(api): Add attack history endpoint

- Add GET /api/attack/history endpoint
- Implement history storage in memory
- Add tests for history endpoint

Closes #123
```

## Testing

Sebelum submit PR, pastikan:
- ✅ Code berjalan tanpa error
- ✅ Tidak ada breaking changes
- ✅ Dokumentasi diupdate jika perlu
- ✅ Test manual untuk fitur baru

## Documentation

- Update README.md untuk perubahan besar
- Update API_DOCUMENTATION.md untuk perubahan API
- Tambahkan comments untuk kode yang kompleks
- Update contoh penggunaan jika perlu

## Questions?

Jika Anda memiliki pertanyaan:
- Buka issue dengan label `question`
- Email: support@example.com
- Discord: [Link jika ada]

Terima kasih atas kontribusi Anda! 🙏

