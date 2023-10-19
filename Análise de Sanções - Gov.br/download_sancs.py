import datetime
import requests as rq
import pathlib
import bs4

currDate = datetime.datetime.today().strftime('%Y%m%d')
liOrgaoSanc = ['ceis', 'cepim', 'cnep', 'acordos-leniencia']

for OS in liOrgaoSanc:

    url = f'https://dadosabertos-download.cgu.gov.br/PortalDaTransparencia/saida/ceis/{currDate}_{OS}.zip'

    Response = rq.get(url)
        
    if Response.status_code != 200:
        print(f'Falha ao obter dados do CGU, código da API: {Response.status_code}')
        print('\nResposta do Website:')
        bs4.BeautifulSoup(Response.content).get('Code')
        
        exit()

    filename = pathlib.Path(f'{currDate}_{OS}.zip')
    filename.write_bytes(Response.content)