
@echo off
pushd %~dp0
if exist pyproject.toml (
    python -m poetry check --lock || python -m poetry lock
)

wsl -d Ubuntu --cd "%~dp0" sh -c "./deploy.sh"
