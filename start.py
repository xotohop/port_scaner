import subprocess
import os
#суть Setup.exe и этого файла есть одно и то же
#Цель - автоматизация скрипта scan-threating.py для срабатывания раз в сутки (работает только на не-NT системах)
if os.name == 'nt':
    cmd = ["python", 'auto.py']
else:
    cmd = ["#!/usr/bin/env python3", "auto.py"]


print('\n* Compiling script...')
raw_output = subprocess.check_output(cmd, shell=True)
output = raw_output.decode('utf-8')
print(output)
