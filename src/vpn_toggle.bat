@echo off

set VPN_NAME="DN-vpngw"

echo VPN_NAME=%VPN_NAME%

set action="%1"
echo action=%action%

for /f "usebackq" %%A in (` ipconfig ^| find %VPN_NAME% `) do set VPN_ON=%%A

if %action%=="connect" (
    if "%VPN_ON%" == "" (
        echo connect
        rem rasdial %VPN_NAME%
    ) else (
        echo already connect
    )
) else if %action%=="disconnect" (
    if %VPN_ON% == "" (
        echo already disconnect
    ) else (
        echo VPN ON
        echo disconnect
        rem rasdial %VPN_NAME% /disconnect

    )
) else (
    echo wrong usecase
)