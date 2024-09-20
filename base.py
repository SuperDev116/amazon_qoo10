import requests
import json
import os
import getpass
import time
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select


def start_driver():
    
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    # options.add_argument(f"--user-agent={my_user_agent}")
    
    USER_NAME = getpass.getuser()

    try:
        driver_path = ChromeDriverManager().install()
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    except ValueError:
        url = r"https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
        response = requests.get(url)
        data_dict = response.json()
        latest_version = data_dict["channels"]["Stable"]["version"]

        driver_path = ChromeDriverManager(version=latest_version).install()
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    except PermissionError:
        try:
            driver = webdriver.Chrome(
                service=Service(
                    f"C:\\Users\\{USER_NAME}\\.wdm\\drivers\\chromedriver\\win64\\116.0.5845.179\\chromedriver.exe"
                ),
                options=options,
            )
        except:
            driver = webdriver.Chrome(
                service=Service(
                    f"C:\\Users\\{USER_NAME}\\.wdm\\drivers\\chromedriver\\win64\\116.0.5845.96\\chromedriver.exe"
                ),
                options=options,
            )

    return driver


def get_setting_value(file_path):
    
    setting_value = {}
    
    with open(file_path, 'r', encoding='utf-8') as ini_file:
        contents = ini_file.read()
        rows = contents.split('\n')
        
    for row in rows:
        if '<=>' in row:
            key, value = row.split('<=>')
            setting_value[key] = value
    
    return setting_value


def send_alert(product_info, price):
    
    
    setting_value = get_setting_value('assets/base.ini')
    email = setting_value['alertGmail']
    product = json.dumps(product_info)
    # url = "https://xs998400.xsrv.jp/api/v1/alert_mail"
    url = "https://qoo10manageable.info/api/v1/alert_mail"

    payload = {'to': email, "product": product, "price": price}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, headers=headers, data=payload)

    print(response.text)
        
    
def open_setting_window():
    
    setting_value = {}
    file_path = 'assets/base.ini'
    html_path = 'assets/main.html'

    # driver = start_driver()
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(os.path.abspath(html_path))
    
    try:
        setting_form = driver.find_element(By.ID, 'information_form')
        
        file = open(file_path, 'a', encoding='utf-8')
        if os.path.getsize(file_path) == 0:
            file.write('amazonEmail<=>\n')
            file.write('amazonPassword<=>\n')
            file.write('qsmEmail<=>\n')
            file.write('qsmPassword<=>\n')
            file.write('qsmAPIKey<=>\n')
            file.write('multiplier<=>\n')
            file.write('qoo_mainCategory<=>\n')
            file.write('qoo_subCategory<=>\n')
            file.write('qoo_smallCategory<=>\n')
            file.write('exhiAsins<=>\n')
            file.write('ngAsins<=>\n')
            file.write('ngWords<=>\n')
            file.write('alertGmail<=>\n')
            file.close()
            
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
            rows = contents.split('\n')
            
        for row in rows:
            if '<=>' in row:
                key, value = row.split('<=>')
                setting_value[key] = value
                
                if key == 'qoo_mainCategory':
                    options = setting_form.find_element(By.ID, 'qoo_mainCategory').find_elements(By.TAG_NAME, 'option')
                    for o in options:
                        if o.get_attribute('value') == value:
                            o.click()
                elif key == 'qoo_subCategory':
                    options = setting_form.find_element(By.ID, 'qoo_subCategory').find_elements(By.TAG_NAME, 'option')
                    for o in options:
                        if o.get_attribute('value') == value:
                            o.click()
                elif key == 'qoo_smallCategory':
                    options = setting_form.find_element(By.ID, 'qoo_smallCategory').find_elements(By.TAG_NAME, 'option')
                    for o in options:
                        if o.get_attribute('value') == value:
                            o.click()
                elif key == 'exhiAsins':
                    element = setting_form.find_element(By.ID, key)
                    element.send_keys(value.replace(',', '\n'))
                elif key == 'ngAsins':
                    element = setting_form.find_element(By.ID, key)
                    element.send_keys(value.replace(',', '\n'))
                elif key == 'ngWords':
                    element = setting_form.find_element(By.ID, key)
                    element.send_keys(value.replace(',', '\n'))
                else:
                    element = setting_form.find_element(By.ID, key)
                    element.send_keys(value)
                
        WebDriverWait(setting_form, 300).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'clicked'))
        )
        
        setting_value['amazonEmail'] = setting_form.find_element(By.ID, 'amazonEmail').get_attribute('value')
        setting_value['amazonPassword'] = setting_form.find_element(By.ID, 'amazonPassword').get_attribute('value')
        
        setting_value['qsmEmail'] = setting_form.find_element(By.ID, 'qsmEmail').get_attribute('value')
        setting_value['qsmPassword'] = setting_form.find_element(By.ID, 'qsmPassword').get_attribute('value')
        setting_value['qsmAPIKey'] = setting_form.find_element(By.ID, 'qsmAPIKey').get_attribute('value')
        
        setting_value['multiplier'] = setting_form.find_element(By.ID, 'multiplier').get_attribute('value')
        
        setting_value['qoo_mainCategory'] = setting_form.find_element(By.ID, 'qoo_mainCategory').get_attribute('value')
        setting_value['qoo_subCategory'] = setting_form.find_element(By.ID, 'qoo_subCategory').get_attribute('value')
        setting_value['qoo_smallCategory'] = setting_form.find_element(By.ID, 'qoo_smallCategory').get_attribute('value')

        exhiAsins = setting_form.find_element(By.ID, 'exhiAsins').get_attribute('value')
        exhiAsins_list = exhiAsins.split('\n')
        setting_value['exhiAsins'] = ','.join(exhiAsins_list)
        
        ngAsins = setting_form.find_element(By.ID, 'ngAsins').get_attribute('value')
        ngAsins_list = ngAsins.split('\n')
        setting_value['ngAsins'] = ','.join(ngAsins_list)
        
        ngWords = setting_form.find_element(By.ID, 'ngWords').get_attribute('value')
        ngWords_list = ngWords.split('\n')
        setting_value['ngWords'] = ','.join(ngWords_list)
        
        setting_value['alertGmail'] = setting_form.find_element(By.ID, 'alertGmail').get_attribute('value')
        
        with open(file_path, 'w', encoding='utf-8') as file:
            for key, value in setting_value.items():
                file.write(f'{key}<=>{value}\n')
        
        driver.quit()
        messagebox.showinfo('OK', '出品情報が正常に保存されました。')
        
    finally:
        driver.quit()
