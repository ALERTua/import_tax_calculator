
@echo off
cd %~dp0
set DOCKER_HOST=tcp://gitlab:2375
set DOCKER_REMOTE=1
call deploy.cmd %*
where nircmd >nul 2>nul && nircmd beep 500 500
