@echo off
chcp 65001 >nul
echo 正在安装 PyInstaller（若未安装）...
pip install pyinstaller -q
echo.
echo 正在打包 npd_windows.py 为单文件 exe（无控制台窗口）...
pyinstaller --onefile --windowed --name "NPD_Model" --hidden-import=npd --clean npd_windows.py
echo.
if exist "dist\NPD_Model.exe" (
    echo 成功。exe 位置: dist\NPD_Model.exe
    echo 如需中文名，可手动改名为 NPD模型.exe
) else (
    echo 打包可能失败，请查看上方输出。
)
pause
