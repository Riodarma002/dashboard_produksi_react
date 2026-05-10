# 🚀 Cara Setup Dashboard dengan Azure API

## Masalah yang Anda Alami

✅ **Dashboard loading terus dan data tidak masuk**

**Penyebab**: Frontend masih menggunakan `http://localhost:8000` padahal Anda sudah deploy API ke Azure.

## Solusi (3 Langkah Mudah)

### ✅ Langkah 1: Buat File `.env`

Buka terminal di folder `frontend`, lalu jalankan:

```bash
copy .env.example .env
```

### ✅ Langkah 2: Edit File `.env`

Buka file `.env` yang baru dibuat, lalu ganti URL-nya dengan URL Azure API Anda:

```env
VITE_API_BASE_URL=https://nama-app-azure-anda.azurewebsites.net
```

**Contoh**:
```env
VITE_API_BASE_URL=https://produksi-dashboard-api.azurewebsites.net
```

**PENTING**: 
- ❌ JANGAN tambahkan `/` di akhir
- ❌ JANGAN tambahkan `/api` di akhir
- ✅ Cukup URL domain saja

### ✅ Langkah 3: Restart Development Server

1. Tekan `Ctrl + C` di terminal untuk stop server yang sedang berjalan
2. Jalankan ulang:

```bash
npm run dev
```

3. Buka browser di `http://localhost:5173`

## 🔍 Cara Cek Apakah Berhasil

### Di Browser Console (Tekan F12)

Anda akan melihat log seperti ini:

```
🔗 API Base URL: https://produksi-dashboard-api.azurewebsites.net
📍 Environment: development
☁️ Menggunakan Azure API
```

### Jika Berhasil:
- ✅ Dashboard akan menampilkan data KPI
- ✅ Chart akan muncul dengan data produksi
- ✅ Tidak ada error merah di console

### Jika Masih Error:

#### Error 1: CORS Policy
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**Solusi**: Tambahkan CORS di backend Python Anda:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Atau specify domain frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Error 2: Network Error
```
Network Error - Tidak dapat terhubung ke: https://...
```

**Solusi**: 
- Pastikan Azure API sudah running
- Test manual dengan browser: buka `https://nama-app-anda.azurewebsites.net/api/kpi?pit=North%20JO%20IC`
- Jika tidak bisa diakses, berarti Azure API belum deploy dengan benar

#### Error 3: Timeout
```
Timeout - API tidak merespon dalam 10 detik
```

**Solusi**: API Azure terlalu lambat. Bisa jadi:
- Cold start (Azure App Service yang idle)
- Query database terlalu lambat
- Tunggu beberapa detik dan refresh lagi

## 📋 Checklist Debugging

Gunakan checklist ini untuk memastikan semuanya benar:

- [ ] File `.env` sudah dibuat di folder `frontend`
- [ ] URL Azure di `.env` sudah benar (tanpa trailing slash)
- [ ] Development server sudah di-restart setelah ubah `.env`
- [ ] Backend Azure API sudah running dan bisa diakses
- [ ] CORS sudah dikonfigurasi di backend Python
- [ ] Browser console tidak ada error merah
- [ ] Network tab di DevTools menunjukkan request ke Azure (bukan localhost)

## 🧪 Test Manual API

Sebelum menjalankan dashboard, test dulu API Azure Anda dengan curl atau browser:

```bash
curl "https://nama-app-anda.azurewebsites.net/api/kpi?pit=North%20JO%20IC"
```

Atau buka di browser:
```
https://nama-app-anda.azurewebsites.net/api/kpi?pit=North%20JO%20IC
```

Jika muncul JSON data, berarti API sudah benar!

## 💡 Tips

### Development vs Production

**Development (Local Testing)**:
```env
VITE_API_BASE_URL=http://localhost:8000
```
Gunakan ini saat testing dengan backend Python lokal.

**Production (Azure)**:
```env
VITE_API_BASE_URL=https://nama-app-anda.azurewebsites.net
```
Gunakan ini saat connect ke Azure API.

### Ganti Environment dengan Cepat

Cukup edit file `.env`, lalu restart server (`Ctrl+C` dan `npm run dev`).

## 📞 Bantuan Lebih Lanjut

Jika masih ada masalah, buka browser console (F12) dan screenshot error yang muncul. Error message akan memberitahu masalah spesifiknya:

- `Network Error` = Tidak bisa connect ke API
- `CORS Error` = Backend belum setup CORS
- `404 Not Found` = Endpoint API salah
- `Timeout` = API terlalu lambat merespon
- `500 Internal Server Error` = Ada error di backend Python

Semua error akan ditampilkan dengan jelas di dashboard dan console!
