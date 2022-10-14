# selenium 4
from selenium import webdriver
from selenium.webdriver.common.by import By
#Utiliza webdriver_manager para facilitar 
#https://github.com/SergeyPirogov/webdriver_manager

driver = webdriver.Firefox()
# create webdriver object
  
# get google.co.in
driver.get("https://www.google.com/")
element = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
element.send_keys("youtube")
element.submit()
print(element.find_elements(By.XPATH,))