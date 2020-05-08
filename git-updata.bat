@echo off
title upDataGit.bat
color 0a
set DIR=%cd%
cd %DIR%
::echo %DIR%
:: 推送时间
set THISDATETIME=%DATE:~0,4%-%DATE:~5,2%-%DATE:~8,2% %TIME:~0,2%:%TIME:~3,2%:%TIME:~6,2%

:: 分支名称
set branch_name=%DATE:~0,4%.%DATE:~5,2%.%DATE:~8,2%

:: 版本号
set version=20.%DATE:~5,2%.%DATE:~8,2%

:: 打标签，版本
git tag %version%

git add -A
git commit -m "%THISDATETIME%"
git branch dev-%branch_name%
:: 创建并切换分支
git checkout -b dev-%branch_name%
git checkout -b dev-2020.05.08


TIMEOUT /T 5
::pause