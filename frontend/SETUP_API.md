# Setup API Configuration

## Masalah: Dashboard Loading Terus & Data Tidak Masuk

Jika dashboard Anda loading terus dan data tidak masuk, kemungkinan besar masalahnya adalah **konfigurasi API endpoint**.

## Solusi

### 1. **Buat File `.env`**

Copy file `.env.example` menjadi `.env`:

```bash
copy .env.example .env
```

### 2. **Konfigurasi URL API**

Edit file `.env` dan sesuaikan dengan environment Anda:

#### **Development (Local)**
```env
VITE_API_BASE_URL=http://localhost:8000
```

#### **Production (Azure)**
```env
VITE_API_BASE_URL=https://your-app-name.azurewebsites.net
```

**Ganti `your-app-name` dengan nama Azure App Service Anda!**

### 3. **Restart Development Server**

Setelah mengubah file `.env`, **WAJIB restart** server Vite:

1. Tekan `Ctrl + C` di terminal untuk stop server
2. Jalankan ulang:
   ```bash
   npm run dev
   ```

### 4. **Verifikasi di Browser Console**

Buka browser console (F12) dan periksa:

- ✅ **Berhasil**: Anda akan melihat data JSON dari API
- ❌ **Gagal**: Anda akan melihat error seperti:
  - `Network Error - Tidak dapat terhubung ke API`
  - `Request timeout - API tidak merespon dalam 10 detik`
  - `CORS Error` (jika Azure belum dikonfigurasi CORS)

## Troubleshooting

### Error: CORS Policy

Jika Anda mendapat error CORS di browser console:

```
Access to XMLHttpRequest at 'https://...' from origin 'http://localhost:5173' 
has been blocked by CORS policy
```

**Solusi**: Tambahkan CORS configuration di backend Python (FastAPI):

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Atau specify domain frontend Anda
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Error: Timeout

Jika API lambat merespon (> 10 detik), Anda bisa ubah timeout di `App.jsx`:

```javascript
axios.get(`${API_BASE_URL}/api/kpi?pit=${pit}`, { timeout: 30000 }) // 30 detik
```

### Error: 404 Not Found

Pastikan endpoint API Anda benar:
- `/api/kpi?pit=North%20JO%20IC`
- `/api/charts/hourly?pit=North%20JO%20IC`

Test manual dengan curl atau browser:
```bash
curl "https://your-app-name.azurewebsites.net/api/kpi?pit=North%20JO%20IC"
```

## Checklist Debugging

- [ ] File `.env` sudah dibuat dan diisi dengan URL Azure yang benar
- [ ] Development server sudah di-restart setelah ubah `.env`
- [ ] Backend API Azure sudah running dan accessible
- [ ] CORS sudah dikonfigurasi di backend
- [ ] Browser console tidak menampilkan error merah
- [ ] Network tab di DevTools menunjukkan status 200 OK

## Contoh URL Azure yang Benar

```
https://produksi-dashboard-api.azurewebsites.net
```

**JANGAN** tambahkan trailing slash atau `/api` di akhir URL di file `.env`!

❌ Salah: `https://produksi-dashboard-api.azurewebsites.net/`  
❌ Salah: `https://produksi-dashboard-api.azurewebsites.net/api`  
✅ Benar: `https://produksi-dashboard-api.azurewebsites.net`
