import subprocess
import os
import sys

pp = sys.path
if os.name == 'nt':
	print('wow, wmth is wrong...are u on Windows?....')
else:
	cmd = ['chmod', '-x', f'{os.path.abspath(os.curdir)}\scan_treading.py']
	raw_output = subprocess.check_output(cmd, shell=True)

	cmd = ['crontab','-e']
	raw_output = subprocess.check_output(cmd, shell=True)

	cmd = ['*/1 * * * * ', f'{os.path.abspath(os.curdir)}\scan_treading.py']
	raw_output = subprocess.check_output(cmd, shell=True)
'''
os.system('chmod -x scan_treading.py' #(делает файл исполняемым. Вместо файла указываешь путь к файлу)
os.system('crontab -e')# (запуск файла с командами автоматизации)
os.system('* */1 * * * scan_treading.py')# (Строка является командой для открытого файла crontab. после звёздочек указываешь путь к файлу)
'''
