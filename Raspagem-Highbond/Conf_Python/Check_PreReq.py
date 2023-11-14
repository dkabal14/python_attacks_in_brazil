"""
Script para checagem dos pré-requisitos
Download de pacotes com pip no script, ref.: 'https://www.activestate.com/resources/quick-reads/how-to-install-python-packages-using-a-script/'
"""
import sys
import subprocess

liModules = [
    'datetime',
    'selenium'
]
for module in liModules:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', '--no-warn-script-location', '--disable-pip-version-check', '--no-warn-script-location', '--no-warn-conflicts', module])
    except:
        print('Atualização falhou')