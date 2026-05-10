# Cara Update Data Dashboard

## 🎯 Masalah yang Diperbaiki
**Sebelum:** Data di Excel sudah update sampai jam 21, tapi dashboard masih menampilkan sampai jam 15.  
**Sekarang:** Dashboard otomatis refresh setiap 5 menit + ada tombol manual refresh.

---

## 🚀 Cara Menggunakan Dashboard

### Metode 1: Auto-Refresh (Otomatis) ⏰
Dashboard sekarang **otomatis refresh data setiap 5 menit**.

**Langkah:**
1. Buka dashboard di browser
2. Biarkan dashboard terbuka
3. Data akan otomatis update setiap 5 menit

**Kapan Menggunakan:**
- Untuk monitoring rutin
- Saat tidak perlu data real-time instant
- Untuk menghemat beban server

---

### Metode 2: Manual Refresh (Instant) 🔄
Klik tombol **"Refresh"** untuk langsung update data dari OneDrive.

**Langkah:**
1. Buka dashboard di browser
2. Klik tombol **"Refresh"** di header (sebelah kanan, warna biru)
3. Tunggu 5-10 detik (loading dari OneDrive)
4. Data langsung update

**Kapan Menggunakan:**
- Saat baru update Excel dan perlu lihat hasilnya segera
- Saat presentasi ke management
- Saat data sangat penting dan tidak bisa tunggu 5 menit

**Lokasi Tombol:**
```
┌─────────────────────────────────────────────────────────┐
│ Logo  Planning Dashboard Production                     │
│                                                          │
│ [North JO IC] [North JO GAM] [South JO IC] [South JO GAM]│
│                                                          │
│                    📅 Date | Time  [🔄 Refresh] [▶ Auto ON]│
└─────────────────────────────────────────────────────────┘
```

---

### Metode 3: Restart Dashboard (Nuclear Option) 🔥
Restart backend dan frontend dari awal.

**Langkah:**
1. Double-click file **`RESTART_DASHBOARD.bat`**
2. Tunggu 15-20 detik
3. Buka browser: http://localhost:5173

**Kapan Menggunakan:**
- Saat dashboard error atau blank screen
- Saat tombol refresh tidak bekerja
- Saat ada update code/konfigurasi

---

## 📊 Cara Update Data di Excel

### Langkah Update Data
1. **Buka Excel di OneDrive**
   - Buka file Excel produksi di OneDrive
   - Pastikan menggunakan Excel Online atau Excel Desktop yang tersync

2. **Update Data**
   - Isi data produksi per jam di kolom yang sesuai
   - **PENTING:** 
     - Jika ada data (misal: 1410) → tulis angkanya
     - Jika hujan/downtime → tulis **0** (angka nol)
     - Jika belum ada data → **kosongkan** (jangan tulis apa-apa)

3. **Save Excel**
   - Klik Save atau Ctrl+S
   - Pastikan Excel sudah tersimpan (tidak ada "Saving..." di title bar)

4. **Refresh Dashboard**
   - **Opsi A:** Tunggu 5 menit (auto-refresh)
   - **Opsi B:** Klik tombol "Refresh" di dashboard (instant)

### Contoh Data Excel

**Benar ✅:**
```
| Hour | Volume |
|------|--------|
| 07   | 1410   |  ← Ada data
| 08   | 1410   |  ← Ada data
| 09   | 0      |  ← Hujan/downtime (tulis 0)
| 10   | 0      |  ← Hujan/downtime (tulis 0)
| 11   | 1410   |  ← Ada data lagi
| 12   |        |  ← Belum ada data (kosong)
| 13   |        |  ← Belum ada data (kosong)
```

**Hasil di Chart:**
- Jam 07-08: Line naik (ada data)
- Jam 09-10: Line flat (0 = hujan/downtime)
- Jam 11: Line naik lagi (ada data)
- Jam 12-13: Chart berhenti (kosong = belum ada data)

**Salah ❌:**
```
| Hour | Volume |
|------|--------|
| 07   | 1410   |
| 08   | 1410   |
| 09   | -      |  ← JANGAN tulis "-" atau "N/A"
| 10   | null   |  ← JANGAN tulis "null"
| 11   | 1410   |
```

---

## 🔍 Troubleshooting

### Problem 1: Data Tidak Update Setelah Klik Refresh
**Kemungkinan Penyebab:**
- Excel belum saved di OneDrive
- Sharing link OneDrive tidak valid
- Network issue

**Solusi:**
1. Pastikan Excel sudah saved (cek title bar Excel)
2. Tunggu 30 detik, coba refresh lagi
3. Jika masih tidak update, restart dashboard:
   ```
   Double-click RESTART_DASHBOARD.bat
   ```

### Problem 2: Tombol Refresh Tidak Muncul
**Kemungkinan Penyebab:**
- Frontend belum di-rebuild
- Browser cache

**Solusi:**
1. Hard refresh browser: **Ctrl + Shift + R**
2. Jika masih tidak muncul, restart dashboard:
   ```
   Double-click RESTART_DASHBOARD.bat
   ```

### Problem 3: Chart Berhenti di Jam yang Salah
**Contoh:** Data Excel sampai jam 21, tapi chart berhenti di jam 15

**Kemungkinan Penyebab:**
- Data jam 16-21 kosong (bukan 0)
- Cache belum refresh

**Solusi:**
1. Cek Excel: pastikan jam 16-21 ada data (angka atau 0)
2. Klik tombol **"Refresh"** di dashboard
3. Jika masih salah, cek apakah ada cell yang berisi formula error (#N/A, #REF!, dll)

### Problem 4: Dashboard Blank/Error
**Solusi:**
1. Restart dashboard:
   ```
   Double-click RESTART_DASHBOARD.bat
   ```
2. Tunggu 15-20 detik
3. Buka browser: http://localhost:5173
4. Jika masih error, cek log di terminal backend

---

## 📝 Catatan Penting

### Untuk User
1. **Jangan spam tombol refresh** - tunggu sampai loading selesai (icon berhenti berputar)
2. **Gunakan auto-refresh untuk monitoring rutin** - lebih efisien
3. **Manual refresh hanya jika urgent** - misalnya saat presentasi

### Untuk Admin/Developer
1. **Cache TTL = 5 menit** - bisa diubah di `api_main.py` (line ~30)
2. **Monitor cache age** - cek http://localhost:8000/api/health
3. **Log refresh events** - cek terminal backend untuk debug

---

## 🎉 Summary

| Metode | Kecepatan | Kapan Digunakan |
|--------|-----------|-----------------|
| **Auto-Refresh** | 5 menit | Monitoring rutin |
| **Manual Refresh** | Instant | Urgent/Presentasi |
| **Restart Dashboard** | 20 detik | Error/Update code |

**Best Practice:**
1. Update Excel → Save
2. Klik "Refresh" di dashboard (jika urgent)
3. Atau tunggu 5 menit (auto-refresh)

**Hasil:** Data di dashboard selalu sync dengan Excel! ✅
