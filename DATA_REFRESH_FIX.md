# Data Refresh Fix - Dokumentasi

## Masalah
Data di dashboard tidak update otomatis meskipun Excel di OneDrive sudah berubah. Contoh: Data sudah sampai jam 21 di Excel, tapi dashboard masih menampilkan sampai jam 15.

## Penyebab
1. **Backend caching**: API menyimpan data di memory dan tidak refresh otomatis
2. **Tidak ada mekanisme refresh**: User tidak bisa memaksa dashboard untuk reload data terbaru

## Solusi yang Diimplementasikan

### 1. Auto-Refresh Cache (5 Menit)
Backend sekarang otomatis refresh data setiap 5 menit:
```python
# api_main.py
def get_data(force_refresh=False):
    cache_expired = cache_age > 300  # 5 minutes = 300 seconds
    if data_cache is None or force_refresh or cache_expired:
        # Reload data from OneDrive
```

**Benefit:**
- Data otomatis update setiap 5 menit tanpa perlu restart API
- Mengurangi beban ke OneDrive (tidak query setiap request)

### 2. Manual Refresh Button
Tambahan tombol "Refresh" di dashboard untuk force reload data:

**Backend - New Endpoint:**
```python
@app.post("/api/refresh")
def force_refresh():
    """Force refresh data from OneDrive"""
    global data_cache, last_cache_time
    data_cache = None
    last_cache_time = None
    data = get_data(force_refresh=True)
    return {"status": "success", "message": "Data refreshed successfully"}
```

**Frontend - Refresh Button:**
```javascript
const handleRefresh = async () => {
  await axios.post(`${API_BASE_URL}/api/refresh`);
  // Reload current pit data
  const [kpiRes, chartRes] = await Promise.all([...]);
};
```

**UI Location:**
- Tombol "Refresh" di header (sebelah tombol Auto Play)
- Icon: RefreshCw (spinning saat loading)
- Warna: Blue (bg-blue-50, text-blue-600)

### 3. Cache Age Monitoring
Health check endpoint sekarang menampilkan umur cache:
```python
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "cache_age_seconds": cache_age  # Umur cache dalam detik
    }
```

## Cara Menggunakan

### Opsi 1: Tunggu Auto-Refresh (5 Menit)
1. Buka dashboard
2. Tunggu maksimal 5 menit
3. Data akan otomatis refresh

### Opsi 2: Manual Refresh (Instant)
1. Buka dashboard
2. Klik tombol **"Refresh"** di header (sebelah kanan)
3. Tunggu beberapa detik (loading dari OneDrive)
4. Data akan langsung update

### Opsi 3: Restart Backend (Nuclear Option)
1. Stop backend API (Ctrl+C)
2. Jalankan ulang: `python api_main.py`
3. Refresh browser

## Testing

### Test Manual Refresh
```bash
# Jalankan backend
python api_main.py

# Di terminal lain, test refresh
python test_refresh.py
```

**Expected Output:**
```
🧪 TESTING DATA REFRESH
============================================================
1️⃣ Checking health before refresh...
   Status: healthy
   Cache age: 120 seconds

2️⃣ Forcing data refresh...
   Status: success
   Message: Data refreshed successfully
   Sheets available: 13

3️⃣ Checking health after refresh...
   Status: healthy
   Cache age: 0 seconds

4️⃣ Getting chart data for North JO IC...
   Hours with data: 07, 08, 09, ..., 21
   Total hours: 15
   
   Last 5 hours:
      17: OB=1234, CH=567, Rain=0
      18: OB=1234, CH=567, Rain=0
      19: OB=1234, CH=567, Rain=0
      20: OB=1234, CH=567, Rain=0
      21: OB=1234, CH=567, Rain=0

✅ TEST COMPLETE
```

### Test Auto-Refresh
1. Buka dashboard
2. Catat jam terakhir di chart
3. Update Excel di OneDrive (tambah data jam baru)
4. Tunggu 5 menit
5. Refresh browser (F5)
6. Chart harus menampilkan data jam baru

## Files Modified

### Backend
1. **api_main.py**:
   - Added `last_cache_time` global variable
   - Updated `get_data()` with auto-refresh logic (5 minutes)
   - Added `/api/refresh` endpoint (POST)
   - Updated `/api/health` to show cache age
   - Updated `/` root endpoint to list refresh endpoint

### Frontend
2. **frontend/src/App.jsx**:
   - Added `RefreshCw` icon import
   - Added `isRefreshing` state
   - Added `handleRefresh()` function
   - Added Refresh button in header

### Testing
3. **test_refresh.py**: Script untuk test refresh functionality

## Troubleshooting

### Data Masih Tidak Update Setelah Refresh
**Kemungkinan Penyebab:**
1. Excel di OneDrive belum tersimpan (masih draft)
2. Sharing link OneDrive tidak valid
3. Network issue ke OneDrive

**Solusi:**
1. Pastikan Excel sudah saved di OneDrive
2. Cek file `.env` - pastikan `ONEDRIVE_LINKS` benar
3. Cek log backend untuk error messages
4. Test manual download: buka sharing link di browser

### Refresh Button Tidak Muncul
**Kemungkinan Penyebab:**
1. Frontend belum di-rebuild
2. Browser cache

**Solusi:**
```bash
cd frontend
npm run build
# Atau untuk development
npm run dev
```
Kemudian hard refresh browser (Ctrl+Shift+R)

### Refresh Terlalu Lama (Timeout)
**Kemungkinan Penyebab:**
1. File Excel terlalu besar
2. Koneksi internet lambat
3. OneDrive throttling

**Solusi:**
1. Increase timeout di frontend:
   ```javascript
   await axios.post(`${API_BASE_URL}/api/refresh`, {}, { timeout: 60000 }); // 60 detik
   ```
2. Increase timeout di backend `load_data()`:
   ```python
   r = requests.get(dl, timeout=60)  # 60 detik
   ```

## Best Practices

### Untuk User
1. **Jangan spam refresh button** - tunggu sampai loading selesai
2. **Gunakan auto-refresh** - biarkan sistem refresh otomatis setiap 5 menit
3. **Manual refresh hanya jika urgent** - misalnya ada data penting yang harus segera ditampilkan

### Untuk Developer
1. **Monitor cache age** - cek `/api/health` untuk debug
2. **Adjust cache TTL** - ubah `300` seconds di `get_data()` jika perlu
3. **Add logging** - backend sudah log setiap refresh event

## Summary

✅ **Auto-refresh setiap 5 menit** - data selalu fresh  
✅ **Manual refresh button** - user bisa force reload kapan saja  
✅ **Cache age monitoring** - developer bisa debug cache issues  
✅ **Better UX** - loading indicator saat refresh  
✅ **No restart needed** - API tidak perlu restart untuk update data  

**Result:** Data di dashboard sekarang selalu sync dengan Excel di OneDrive! 🎉
