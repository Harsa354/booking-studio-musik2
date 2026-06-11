# Backend - Flask API

VM Backend menjalankan aplikasi Python Flask sebagai REST API.

## Teknologi
- Python Flask
- MySQLdb
- Flask-CORS

## Endpoint API
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | /api/booking | Mengambil semua data booking |
| POST | /api/booking | Menambah booking baru |
| DELETE | /api/booking/{id} | Menghapus booking |

## Cara Menjalankan
```bash
python3 app.py
```