import requests as rq
from bs4 import BeautifulSoup as bs
import os
import sys
import time
import getpass as gp

# ################################################
# ############# VARIÁVEIS PRINCIPAIS #############
# ################################################

org_id = '26690'
mainURL = 'https://accounts.highbond.com'
urlAuth = f'{mainURL}/login'
urlReports = f'{mainURL}/orgs/{org_id}/apps/21'
targetReportURL = 'https://reports.highbond.com/MIBrowse.i4;5c43ab63-7da8-4d9b-a8be-326570994c02=8f54e0f7-8b10-4491-8299-9463e675d168?'

currSession = rq.Session()

#Navegando para a página de login
getLoginPage = currSession.get(urlAuth)

authToken = bs(getLoginPage.content, features='html.parser').find(attrs={'name': 'authenticity_token'}, )['value']

buttName = bs(getLoginPage.content, features='html.parser').find(attrs={'type': 'submit'})['name']

buttValue = bs(getLoginPage.content, features='html.parser').find(attrs={'type': 'submit'})['value']



sair = False
currRetry = 0
retryLimit = 2
while sair != True:
    try:
        userEmail = input('E-mail: ')
        userPassword = gp.getpass('Senha: ')

        payload = {
            'user[email]': userEmail, # E-mail de acesso no Highbond
            'user[password]': userPassword, # Senha de acesso no Highbond
            'authenticity_token': authToken, # Campo invisível, token temporário de acesso
            buttName: buttValue # Botão de Login que é apertado pelo usuário
        }

        #Efetuando login no portal
        actionLogin = currSession.post(urlAuth, data=payload)

        if actionLogin.status_code != 200 and actionLogin.status_code != 406:
            print(f'Não foi possível autenticar: Código de Status {actionLogin.status_code}')
            print('============================================')
            print(actionLogin.content)
            raise 'error'

        if actionLogin.content != b'':
            print(f'Não foi possível autenticar, resposta da Página: {actionLogin.text}')
            raise 'error'
        
        sair = True
    except:
        print('============================================')
        print('Falha ao executar a ação de login!')
        currRetry = currRetry + 1
        if currRetry == retryLimit:
            print('Limite de tentativas alcançado.')
            exit()
    else:
        print('Ação de login realizada com sucesso!')

#Acessando a página de Reports
getReportsPage = currSession.get(urlReports)
print('Página de Reports:')
print(getReportsPage.text)

#Acessando o relatório
targetReportURL = 'https://reports.highbond.com/MIPreBrowse.i4;5c43ab63-7da8-4d9b-a8be-326570994c02=8f54e0f7-8b10-4491-8299-9463e675d168?5c43ab63-7da8-4d9b-a8be-326570994c02'

custBody = {
    "action": "openItem",
    "subAction": "REPORT%7C6150064",
    "subSubAction": '',
    "tab_token": "1ddeb99e-56fa-4e78-b86f-d8d51ee57153"
}

custHeaders = {
  "authority": 'reports.highbond.com',
  "method": "POST",
  "path": "/MIBrowse.i4;5c43ab63-7da8-4d9b-a8be-326570994c02=8f54e0f7-8b10-4491-8299-9463e675d168?",
  "scheme": "https",
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  "accept-encoding": "gzip, deflate, br",
  "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6",
  "cache-control": "max-age=0",
  "content-type": "application/x-www-form-urlencoded",
  "origin": "https://reports.highbond.com",
  "referer": "https://reports.highbond.com/MIPreBrowse.i4;5c43ab63-7da8-4d9b-a8be-326570994c02=8f54e0f7-8b10-4491-8299-9463e675d168?5c43ab63-7da8-4d9b-a8be-326570994c02=8f54e0f7-8b10-4491-8299-9463e675d168",
  "sec-ch-ua": '`"Chromium`";v=`"118`", `"Microsoft Edge`";v=`"118`", `"Not=A?Brand`";v=`"99`"',
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": '`"Windows`"',
  "sec-fetch-dest": "document",
  "sec-fetch-mode": "navigate",
  "sec-fetch-site": "same-origin",
  "sec-fetch-user": "?1",
  "upgrade-insecure-requests": "1"
}

postTargetReportPage = currSession.post(targetReportURL, headers=custHeaders, data=custBody)
#print(postTargetReportPage.text)
print(currSession.cookies)

# #Comando de execução do relatório
# runReport = 'https://reports.highbond.com/RunReport.i4;5c43ab63-7da8-4d9b-a8be-326570994c02=8f54e0f7-8b10-4491-8299-9463e675d168?reportUUID=0c241ed6-f27d-46cd-83d4-9fb3ae364fcc&primaryOrg=1&clientOrg=28844&5c43ab63-7da8-4d9b-a8be-326570994c02=8f54e0f7-8b10-4491-8299-9463e675d168'

# custHeaders = {
#   "authority": "reports.highbond.com",
#   "method": "GET",
#   "path": "/RunReport.i4;5c43ab63-7da8-4d9b-a8be-326570994c02=8f54e0f7-8b10-4491-8299-9463e675d168?reportUUID=0c241ed6-f27d-46cd-83d4-9fb3ae364fcc&primaryOrg=1&clientOrg=28844&5c43ab63-7da8-4d9b-a8be-326570994c02=8f54e0f7-8b10-4491-8299-9463e675d168",
#   "scheme": "https",
#   "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#   "accept-encoding": "gzip, deflate, br",
#   "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6",
#   "cache-control": "max-age=0",
#   "referer": "https://reports.highbond.com/MIPreBrowse.i4;5c43ab63-7da8-4d9b-a8be-326570994c02=8f54e0f7-8b10-4491-8299-9463e675d168?5c43ab63-7da8-4d9b-a8be-326570994c02=8f54e0f7-8b10-4491-8299-9463e675d168",
#   "sec-ch-ua": '`"Chromium`";v=`"118`", `"Microsoft Edge`";v=`"118`", `"Not=A?Brand`";v=`"99`"',
#   "sec-ch-ua-mobile": "?0",
#   "sec-ch-ua-platform": '`"Windows`"',
#   "sec-fetch-dest": "document",
#   "sec-fetch-mode": "navigate",
#   "sec-fetch-site": "same-origin",
#   "sec-fetch-user": "?1",
#   "upgrade-insecure-requests": "1"
# }

# getRunReport = currSession.get(runReport, headers=custHeaders)

#Testando o download
