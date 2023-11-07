import time # Para aguardar o download antes de fechar
import getpass as gp # Para pegar a senha do usuário (não funciona no robô Highbond)
import os # para alterar os arquivos baixados (não implementado)

# Importações de métodos da library do selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# ##########################################
# ############### VARIAVEIS ################
# ##########################################
username = input('E-mail: ')
password = gp.getpass('Senha: ')
mainURL = 'https://accounts.highbond.com/orgs/26690'
ProcessamentoPath = f'c:\\teste\\Processamento'
ResultadoPath = f'c:\\teste\\Download'

if not os.path.exists(ProcessamentoPath):
    os.mkdir(ProcessamentoPath)

if not os.path.exists(ResultadoPath):
    os.mkdir(ResultadoPath)

print('='*60)
print(f'Os arquivos serão baixados para {ProcessamentoPath}')
print('='*60)


print('Configurando as opções do Edge')

try:
    EdgeOptions = webdriver.EdgeOptions()
    EdgeOptions.add_experimental_option(name='prefs', value={"download.default_directory": ProcessamentoPath}) # Altera a pasta de download do arquivo
    EdgeOptions.add_experimental_option(name='excludeSwitches', value=['enable-logging']) #Desativa os avisos causados pelo bug do Edge na versão 4.15.2 do Selenium
except:
    print('---> Não foi possível definir as preferências')
    print('='*60)
    exit()
else:
    print('---> Configrações Definidas com Sucesso!')
    print('='*60)


print('Iniciando a automação do Edge: ')
try:
    objNavigator = webdriver.Edge(options=EdgeOptions, keep_alive=False)
except:
    print('---> Não foi possível iniciar a automação')
    print('='*60)
    exit()
else:
    print('---> Automação iniciada com sucesso')
    print('='*60)

# Acessando a página de login

print('Acessando a página de login: ')
try:
    objNavigator.get(mainURL)
except:
    print('---> Não foi possível acessar a página de login')
    print('='*60)
    exit()
else:
    print('---> Página acessada com sucesso!')
    print('='*60)


print('Autenticando no portal: ')
try:
    # Insere Usuário
    objNavigator.find_element(By.ID, "user_email").send_keys(username)
    # Insere Senha
    objNavigator.find_element(By.ID, "user_password").send_keys(password)
    #Autentica no portal
    objNavigator.find_element(By.NAME, "commit").click()
    
except:
    print('---> Não foi possível definir as preferências')
    print('='*60)
    exit()
else:
    print('---> Configrações Definidas com Sucesso!')
    print('='*60)

# Clica no link de relatórios

print('Entrando na página de relatórios: ')
try:
    objNavigator.find_element(By.LINK_TEXT, "Relatórios").click()
except:
    print('---> Não foi possível acessar a página de relatórios')
    print('='*60)
    exit()
else:
    print('---> Página de relatórios acessada com sucesso!')
    print('='*60)


print('Aguardando o relatório de planos de ação ficar visível e acessando-o')
try:
    # Espera 30 segundos até que o link do relatório "Relatório de Planos de Ação" esteja visível na página
    WebDriverWait(objNavigator, 30000).until(expected_conditions.visibility_of_element_located((By.XPATH, "//div[@title='Relatório de Planos de Ação']")))
    # Clica uma vez sobre o div para permitir a ação de clique duplo
    objNavigator.find_element(By.XPATH, "//div[@title='Relatório de Planos de Ação']").click()
    # Faz um clique duplo no div do relatório
    element = objNavigator.find_element(By.XPATH, "//div[@title='Relatório de Planos de Ação']")
    actions = ActionChains(objNavigator)
    actions.double_click(element).perform()
except:
    print('---> O relatório de planos de ação não está disponível ou a execução falhou')
    print('='*60)
    exit()
else:
    print('---> Página do relatório acessada com sucesso!')
    print('='*60)


# Espera 2 minutos até que o filtro do dashboard esteja visível (indicando que o relatório terminou de carregar)

print('Aguardando o carregamento do relatório: ')
try:
    WebDriverWait(objNavigator, 120000).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".filterList")))
except:
    print('---> A automação não identificou o carregamento do relatório')
    print('='*60)
    exit()
else:
    print('---> Relatório carregado!')
    print('='*60)

# Clica no botão exportar para abrir o menu de exportação e depois clica no primeiro item do menu (se Deus quiser é a opção de csv)

print('Abrindo dropdownlist de exportação e selecionando a opção de CSV')
try:
    objNavigator.find_element(By.XPATH, "//img[@title='Exportar']").click()
    objNavigator.find_element(By.XPATH, "//li[@class='menuItem menuFirstItem hasLink']").click()
except:
    print('---> Não foi possível abrir as preferências de exportação de CSV')
    print('='*60)
    exit()
else:
    print('---> Janela de preferências de exportação aberta!')
    print('='*60)

# Aguarda até que o botão de exportação esteja disponível e depois clica nele
# Obs.: Como o botão possui uma classe dinâmica que muda com a ação "mouse_over", foi preciso clicar nela utilizando o caminho de XML dele, se o caminho mudar, o sistema não funciona

print('Aguardando o carregamento do menu de exportação: ')
try:
    WebDriverWait(objNavigator, 30000).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[7]/table/tbody/tr/td/div/table/tbody/tr/td[2]/span")))
    objNavigator.find_element(By.XPATH, "//div[7]/table/tbody/tr/td/div/table/tbody/tr/td[2]/span").click()
except:
    print('---> Não foi possível definir as preferências')
    print('='*60)
    exit()
else:
    print('---> Configrações Definidas com Sucesso!')
    print('='*60)

time.sleep(10)

# files_to_rename = os.listdir(ProcessamentoPath)
# i = 0
# for file in files_to_rename:
#     filepath = ProcessamentoPath + f'\\' + file
#     filename = ResultadoPath + f'\\teste{i}.txt'
    
#     sair = False
#     while sair != True:
#         if not os.path.exists(filename):
#             sair = True
#         else:
#             i = i + 1
                
#     os.replace(filepath, filename)
#     i = i + 1
objNavigator.quit()