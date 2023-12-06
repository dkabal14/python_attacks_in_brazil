from classes.Print2 import Print2

from bs4 import BeautifulSoup as bs
import requests as rq
import pandas as pd
import json
import sys

curSess = rq.Session()
orgId = '26690'
mainURL = "https://accounts.highbond.com/login"
orgURL = f"https://accounts.highbond.com/orgs/{orgId}"
userEmail = sys.argv[1]
userPassword = sys.argv[2]

#Criação dos cookies pra manter o usuário conectado
curSes = rq.Session()

#Recebendo os dados da página de logon
startPage = curSes.get(mainURL).content

#Recebendo o valor do token temporário de acesso bs() é um método da biblioteca BeautifulSoup da classe bs4
authToken = bs(startPage, features='lxml').find(attrs={'name': 'authenticity_token'})['value']

buttName = bs(startPage, features='lxml').find(attrs={'type': 'submit'})['name']

buttValue = bs(startPage, features='lxml').find(attrs={'type': 'submit'})['value']

#Montando a hastable com os parâmetros de entrada no site (os campos visíveis e invisíveis que precisam ser preenchidos para logar no site)
payload = {
    'user[email]': userEmail, # E-mail de acesso no Highbond
    'user[password]': userPassword, # Senha de acesso no Highbond
    'authenticity_token': authToken, # Campo invisível, token temporário de acesso 
    buttName: buttValue # Botão de Login que é apertado pelo usuário
}

actionLogon = curSes.post(mainURL, data=payload, allow_redirects=True).content

orgPage = curSes.get(orgURL).text
print(bs(orgPage))



