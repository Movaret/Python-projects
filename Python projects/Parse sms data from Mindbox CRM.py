
pip install selenium webdriver-manager pandas

# import libraries
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import pandas as pd
import selenium

print(selenium.__version__)

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

# define the URL
url = ""

# load the web page
driver.get(url)


# set maximum time to load the web page in seconds (optional)
#driver.implicitly_wait(10)

Login = driver.find_element(By.NAME, 'login');
Login.click()
Login.send_keys("")

Password = driver.find_element(By.NAME, 'password');
Password.click()
Password.send_keys("")

Enter = driver.find_element(By.ID, 'SubmitCredentials');
Enter.click()

# check if page title is correct
print(driver.title)

# scroll till the end of the page
lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match=False
while(match==False):
    lastCount = lenOfPage
    time.sleep(3)
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount==lenOfPage:
        match=True

# open every interactive object
Open = driver.find_elements(By.XPATH, "//div[@data-testid ='Text' and @class = 'sc-jKvnYE boDXlG sc-eJhAIA ZwXfd']")

for i in Open:
    i.click()
    time.sleep(2)

# parse message data
Theme = driver.find_elements(By.XPATH, "//div[@data-testid ='Text' and @class = 'sc-hmTbGb ZROp sc-YkBNp ijECFl']")
Time = driver.find_elements(By.XPATH, "//div[@data-testid ='SimpleTableCell' and @class = 'sc-kmtlux jbowlq sc-jSCYWa hLhGym']")
Brand = driver.find_elements(By.XPATH, "//div[@data-testid ='GridAny.GridContainer' and @class = 'sc-fJNrnh sc-ddfMyL fbYAHB bNRSaN']")
Number = driver.find_elements(By.XPATH, "//div[@data-testid ='MailingContact' and @class = 'sc-bIquoJ disRhm']")
Status = driver.find_elements(By.XPATH, "//div[@data-testid ='MessageTransportStatusName' and @class = 'sc-bIquoJ disRhm']")
Text = driver.find_elements(By.XPATH, "//div[@data-testid ='SmsContent' and @class = 'sc-bIquoJ disRhm']")


theme = []
time = []
b = []
name = []
brand= []
number = []
status = []
text = []



for i in Theme:
    theme.append(i.text)

for i in Time:
    time.append(i.text.split('\n')[0])

for i in Brand:
    b.append(i.text)

for i in Number:
    number.append(i.text.replace('Контакт\n', ''))

for i in Status:
    status.append(i.text.replace('Статус\n', ''))

for i in Text:
    text.append(i.text.replace('Текст\n',''))


# cut off all excess
name = b[::2]
brand = b[1::2]



# check if the lenght of lists are equal
print(len(theme))
print(len(time))
print(len(name))
print(len(brand))
print(len(number))
print(len(status))
print(len(text))


# put all data to dict
dict = { 'Тема': theme, 'Дата отправки': time, 'Имя получателя': name, 'Исходный номер': brand, 'Номер назначения': number, 'Статус': status, 'Текст сообщения': text }

# create dataset and save as csv
df = pd.DataFrame(dict)
df.to_csv('D:/Python/df.csv', index = False, encoding = 'utf-8')


