@echo off

set VPN_NAME="DN-vpngw"

echo VPN_NAME=%VPN_NAME%

for /f "usebackq" %%A in (` ipconfig ^| find %VPN_NAME% `) do set VPN_ON=%%A

if "%VPN_ON%"=="" (
    echo VPN OFF
    echo connect
    rasdial %VPN_NAME%
) else (
    echo VPN ON
    echo disconnect
    rasdial %VPN_NAME% /disconnect
)