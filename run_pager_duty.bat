>log.txt 2>&1

python %cd%\pager_duty.py

@echo off
echo Ran pager_duty.py on %date% - %time%>> log.txt