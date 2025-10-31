@echo off
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%a%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
set BACKUP_FILE=backups\notebook_backup_%mydate%_%mytime%.sql
if not exist backups mkdir backups
docker-compose exec -T notebook-db pg_dump -U postgres notebook_lm_db > %BACKUP_FILE% && tar -czf "%BACKUP_FILE%.tar.gz" "%BACKUP_FILE%" && del %BACKUP_FILE% && echo ✅ Backup: %BACKUP_FILE%.tar.gz || echo ❌ Failed
pause
