@echo off
echo Resetting TCP/IP stack...
netsh int ip reset
echo.

echo Releasing IP address...
ipconfig /release
echo.

echo Renewing IP address...
ipconfig /renew
echo.

echo Flushing DNS cache...
ipconfig /flushdns
echo.

echo DNS flushed. Press Enter to continue...
pause >nul
