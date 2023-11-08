from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

objNavigator = webdriver.Edge()
objNavigator.get('https://www.google.com/search?q=python+selenium+webdriver+get+xpath+of+an+element&newwindow=1&sca_esv=580252979&sxsrf=AM9HkKnHyXH9pTXLkHm5daZXkW9tlE9-aw%3A1699399988971&source=hp&ei=NMlKZfW4ONrF5OUP07uqmA0&iflsig=AO6bgOgAAAAAZUrXRFZRuLWtiBm2c788aKtfXmQr9imc&oq=&gs_lp=Egdnd3Mtd2l6IgAqAggAMgcQIxjqAhgnMgcQIxjqAhgnMgcQIxjqAhgnMgcQIxjqAhgnMgcQIxjqAhgnMgcQIxjqAhgnMgcQIxjqAhgnMgcQIxjqAhgnMgcQIxjqAhgnMgcQIxjqAhgnSI4bUABYAHABeACQAQCYAQCgAQCqAQC4AQPIAQCoAgo&sclient=gws-wiz')
element = objNavigator.find_element(By.XPATH, "/html/body/div[5]/div/div[10]/div/div[2]/div[2]/div/div/div[4]/div/div/div[1]/div/div/span/a/h3")
parent = element.find_element(By.XPATH, '.parent::*')
print(parent)
