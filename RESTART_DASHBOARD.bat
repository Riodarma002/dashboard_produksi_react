@echo off
echo ============================================================
echo RESTART DASHBOARD - Kill and Restart Backend + Frontend
echo ============================================================
echo.

echo [1/4] Stopping existing processes...
echo.

REM Kill Python processes (backend API)
taskkill /F /IM python.exe /T 2>nul
if %errorlevel% equ 0 (
    echo    ✓ Backend API stopped
) else (
    echo    ℹ No backend API running
)

REM Kill Node processes (frontend dev server)
taskkill /F /IM node.exe /T 2>nul
if %errorlevel% equ 0 (
    echo    ✓ Frontend dev server stopped
) else (
    echo    ℹ No frontend dev server running
)

echo.
echo [2/4] Waiting 3 seconds for cleanup...
timeout /t 3 /nobreak >nul
echo.

echo [3/4] Starting Backend API...
echo    Starting Python API on http://localhost:8000
start "Backend API" cmd /k "python api_main.py"
timeout /t 5 /nobreak >nul
echo    ✓ Backend API started
echo.

echo [4/4] Starting Frontend Dev Server...
echo    Starting React dev server on http://localhost:5173
cd frontend
start "Frontend Dev" cmd /k "npm run dev"
cd ..
timeout /t 3 /nobreak >nul
echo    ✓ Frontend dev server started
echo.

echo ============================================================
echo ✅ DASHBOARD RESTARTED SUCCESSFULLY
echo ============================================================
echo.
echo 📍 Backend API:  http://localhost:8000
echo 📍 Frontend:     http://localhost:5173
echo 📚 API Docs:     http://localhost:8000/docs
echo.
echo ⚠️  CATATAN:
echo    - Tunggu 10-15 detik untuk backend load data dari OneDrive
echo    - Buka http://localhost:5173 di browser
echo    - Jika data tidak muncul, klik tombol "Refresh" di dashboard
echo.
echo Press any key to close this window...
pause >nul
