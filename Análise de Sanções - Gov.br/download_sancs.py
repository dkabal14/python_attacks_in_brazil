import datetime
import requests as rq
import pathlib
from IPython.core.display import display_html
from IPython.core.display import HTML
import os

currDate = datetime.datetime.today().strftime('%Y%m%d')
liOrgaoSanc = [
    'ceis', 
    'cepim', 
    'cnep', 
    'acordos-leniencia'
]

for OSanc in liOrgaoSanc:

    url = f'https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/ceis/{currDate}_{OSanc}.zip'

    Response = rq.get(url)
        
    if Response.status_code != 200:
        print(f'Falha ao obter dados do CGU, código da API: {Response.status_code}')
        print('\nResposta do Website:')
        # display_html(HTML(Response.text))
        print(Response.text)
        
        exit()
    else:
        print(f'Executando o download do arquivo {currDate}_{OSanc}.zip')
        if os.path.exists(f'{currDate}_{OSanc}.zip'):
            os.remove(f'{currDate}_{OSanc}.zip')
        filename = pathlib.Path(f'{currDate}_{OSanc}.zip')
        filename.write_bytes(Response.content)