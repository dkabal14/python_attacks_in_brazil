from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

mainURL = 'https://accounts.highbond.com/orgs/26690'
objNavigator = webdriver.Edge()
objNavigator.get(mainURL)
objNavigator.quit()