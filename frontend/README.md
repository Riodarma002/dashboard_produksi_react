# React + Vite - Production Dashboard

Dashboard monitoring produksi tambang dengan React, Vite, TailwindCSS, dan ApexCharts.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Setup API Configuration

**PENTING**: Sebelum menjalankan aplikasi, Anda harus mengkonfigurasi API endpoint!

```bash
# Copy file .env.example menjadi .env
copy .env.example .env
```

Edit file `.env` dan sesuaikan dengan environment Anda:

**Development (Local)**:
```env
VITE_API_BASE_URL=http://localhost:8000
```

**Production (Azure)**:
```env
VITE_API_BASE_URL=https://your-app-name.azurewebsites.net
```

### 3. Run Development Server

```bash
npm run dev
```

Buka browser di `http://localhost:5173`

## 🔧 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build untuk production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 📝 Troubleshooting

### Dashboard Loading Terus & Data Tidak Masuk

**Penyebab**: API endpoint tidak dikonfigurasi atau salah.

**Solusi**:
1. Pastikan file `.env` sudah dibuat dan diisi dengan URL yang benar
2. Restart development server setelah mengubah `.env` (Ctrl+C lalu `npm run dev`)
3. Buka browser console (F12) untuk melihat error detail
4. Pastikan backend API sudah running dan accessible

Lihat dokumentasi lengkap di [SETUP_API.md](./SETUP_API.md)

## 🏗️ Tech Stack

- React 19.2.5
- Vite 8.0.10
- TailwindCSS v4
- ApexCharts
- Axios
- Lucide React (icons)

## 📚 Documentation

- [API Setup Guide](./SETUP_API.md) - Panduan lengkap konfigurasi API
- [Migration Notes](./React%20Dashboard%20Data%20Migration.md) - Catatan migrasi dari Streamlit

## 🔗 Backend Requirements

Dashboard ini membutuhkan backend Python (FastAPI) yang menyediakan endpoint:
- `GET /api/kpi?pit={pit_name}` - KPI metrics
- `GET /api/charts/hourly?pit={pit_name}` - Hourly production data

Pastikan backend sudah running sebelum menjalankan frontend!

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
