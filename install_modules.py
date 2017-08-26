import subprocess

run_pip = subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
input('Нажмите Enter, чтобы завершить программу: ')

