@echo off
REM 浙商积存金价格监控 - 打包脚本

echo ========================================
echo 浙商积存金价格监控 - PyInstaller 打包脚本
echo ========================================
echo.

REM 检查是否在虚拟环境中
python -c "import sys; sys.exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)"
if %errorlevel% neq 0 (
    echo [警告] 未检测到虚拟环境，建议在虚拟环境中打包
    echo.
    pause
)

echo [1/3] 清理旧的打包文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "浙商积存金价格监控.spec" del "浙商积存金价格监控.spec"

echo [2/3] 开始打包...
pyinstaller --onefile --windowed --name="浙商积存金价格监控" --icon=NONE main.py

if %errorlevel% equ 0 (
    echo.
    echo [3/3] 打包成功！
    echo.
    echo 可执行文件位置: dist\浙商积存金价格监控.exe
    echo.
) else (
    echo.
    echo [错误] 打包失败！
    echo.
)

pause
