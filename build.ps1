# 浙商积存金价格监控 - 打包脚本 (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "浙商积存金价格监控 - PyInstaller 打包脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否在虚拟环境中
$inVenv = python -c "import sys; print(hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))"
if ($inVenv -ne "True") {
    Write-Host "[警告] 未检测到虚拟环境，建议在虚拟环境中打包" -ForegroundColor Yellow
    Write-Host ""
    pause
}

Write-Host "[1/3] 清理旧的打包文件..." -ForegroundColor Green
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "浙商积存金价格监控.spec") { Remove-Item -Force "浙商积存金价格监控.spec" }

Write-Host "[2/3] 开始打包..." -ForegroundColor Green
pyinstaller --onefile --windowed --name="浙商积存金价格监控" --icon=icon.ico main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[3/3] 打包成功！" -ForegroundColor Green
    Write-Host ""
    Write-Host "可执行文件位置: dist\浙商积存金价格监控.exe" -ForegroundColor Cyan
    Write-Host ""
}
else {
    Write-Host ""
    Write-Host "[错误] 打包失败！" -ForegroundColor Red
    Write-Host ""
}

pause
