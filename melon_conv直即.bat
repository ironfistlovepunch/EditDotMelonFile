REM ファイル編集
set pypath=%~dp0
echo %pypath%
echo %1
for /f "usebackq" %%t in (`%pypath%melon編集.py "%1"`) do set work=%%t
echo %work%

REM ビュワーに開かせる
"C:\Program Files (x86)\Melonbooks\melonbooksviewer\melonbooksviewer.exe" %work%

REM tempに保存されたファイルをコピーする
set out=%work:.melon=%
echo %out%
copy %temp%\Melonbooks\temporary.pdf "%out%"

REM Acrobatを強制終了
taskkill /f /im AcroRd32.exe
