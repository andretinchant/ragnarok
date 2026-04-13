@echo off
echo =====================================================
echo   rAthena Client Setup - WARP Patcher
echo   Packetver: 20211103
echo =====================================================
echo.

set WARP_DIR=N:\Users\tinch\Documents\Projetos\Warp2025\win32
set CLIENT_DIR=%~dp0
set SESSION_FILE=%CLIENT_DIR%session_rathena.yml

REM Check if Ragexe.exe exists
if not exist "%CLIENT_DIR%Ragexe.exe" (
    echo [ERRO] Ragexe.exe nao encontrado na pasta client!
    echo.
    echo Voce precisa baixar o kRO client e copiar o Ragexe.exe para:
    echo   %CLIENT_DIR%
    echo.
    echo Opcoes para obter o Ragexe.exe:
    echo   1. Baixar o kRO full client (instalador coreano oficial)
    echo   2. Usar um Ragexe.exe de uma data compativel com packetver 20211103
    echo      (datas proximas: 2021-11-03 ou similar)
    echo.
    pause
    exit /b 1
)

echo [OK] Ragexe.exe encontrado!
echo [INFO] Aplicando patches com WARP...
echo.

"%WARP_DIR%\WARP_console.exe" -using "%SESSION_FILE%" -from "%CLIENT_DIR%Ragexe.exe" -to "%CLIENT_DIR%Ragexe_patched.exe"

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao aplicar patches. Tente usar o WARP GUI:
    echo   %WARP_DIR%\WARP.exe
    echo.
    pause
    exit /b 1
)

echo.
echo =====================================================
echo   [OK] Client patcheado com sucesso!
echo   Arquivo: Ragexe_patched.exe
echo =====================================================
echo.
echo Para jogar, execute Ragexe_patched.exe nesta pasta.
echo Certifique-se de que os arquivos GRF estao aqui tambem.
echo.
pause
