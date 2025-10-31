@echo off
:menu
cls
echo.
echo ════════════════════════════════════════════════════════════
echo 🗂️  NOTEBOOK LM - BACKUP MANAGER
echo ════════════════════════════════════════════════════════════
echo.
echo 1. 💾 Create Local Backup
echo 2. 🔄 Restore from Backup
echo 3. 📤 Upload to Docker Hub
echo 4. 📥 Download from Docker Hub
echo 5. 📋 List All Backups
echo 6. ❌ Exit
echo.
set /p choice="Select (1-6): "
if "%choice%"=="1" (call backup.bat & goto menu)
if "%choice%"=="2" (call restore.bat & goto menu)
if "%choice%"=="3" (call upload_backup_to_dockerhub.bat & goto menu)
if "%choice%"=="4" (call download_backup_from_dockerhub.bat & goto menu)
if "%choice%"=="5" goto list
if "%choice%"=="6" goto end
echo Invalid choice
timeout /t 2 >nul
goto menu
:list
echo.
echo 📋 Local Backups:
dir /B /O:-D backups\ 2>nul || echo (No backups)
echo.
pause
goto menu
:end
echo ✅ Goodbye!
echo.
