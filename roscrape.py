from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import requests as req; from bs4 import BeautifulSoup
import time
from colorama import Fore
import logging
import pandas as pd
import undetected_chromedriver as uc
import os

#  Chrome Options

logging.basicConfig(level=logging.WARNING)
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('webdriver_manager').setLevel(logging.WARNING)


username = "USERNAME-HERE"
password = "PASSWORD-HERE"
usernameList= []
loopVariableButton=3
loopVariableAdd=0                    

os.system('cls')
print(Fore.RED + """
    (        )   (           (              (         
    )\ )  ( /(   )\ )   (    )\ )    (      )\ )      
   (()/(  )\()) (()/(   )\  (()/(    )\    (()/( (    
    /(_))((_)\   /(_))(((_)  /(_))((((_)(   /(_)))\   
   (_))    ((_) (_))  )\___ (_))   )\ _ )\ (_)) ((_)  
   | _ \  / _ \ / __|((/ __|| _ \  (_)_\(_)| _ \| __| 
   |   / | (_) |\__ \ | (__ |   /   / _ \  |  _/| _|  
   |_|_\  \___/ |___/  \___||_|_\  /_/ \_\ |_|  |___|""")

print(Fore.BLUE + """    https://github.com/adambielat""")
    
print(Fore.RED + """    
    1. Scrape owners of a limited.
    2. Add the scraped usernames on roblox.
    """)

def menu():
    choice = int(input("    Please enter a number: "))
    if not int(choice):
        print("    Please enter a valid number.")
        menu()
    else:
        if choice == 1:
            open_rolimons()
        elif choice == 2:
            open_roblox()
        else: 
            print("    Please enter a valid number.")
            menu()
    

def open_rolimons():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    os.system('cls')
    print()
    itemUID = int(input("   Please enter the UID of the limited:  "))
    if not int(itemUID):
        print("    Please enter a valid number.")
        open_rolimons()
    driver.get(f"https://www.rolimons.com/item/{itemUID}")
    driver.implicitly_wait(2)
    actions = ActionChains(driver)
    actions.send_keys(Keys.ARROW_DOWN*40).perform()
    cookies = driver.find_elements(By.XPATH, '//*[@id="ncmp__tool"]/div/div/div[3]/div[1]/button[2]')
    cookies[0].click()
    scrape_rolimons()
   
def scrape_rolimons():
    global loopVariableButton; global driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    odd = driver.find_elements(By.CLASS_NAME, 'odd')
    even = driver.find_elements(By.CLASS_NAME, 'even')
    oddeven = []
    for i in odd+even:
        oddeven.append("i")
    loopVariableUsers = 1
    while loopVariableUsers < 10:
        usernames = driver.find_elements(By.XPATH, f'//*[@id="bc_owners_table"]/tbody/tr[{loopVariableUsers}]/td[2]/a[1]')
        for i in usernames:
            print("  Scraped username:",i.text)
            usernameList.append([i.text])
        loopVariableUsers=loopVariableUsers+1
    nextButton = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[2]/div[14]/div/div[1]/div/div[3]/div[2]/div/ul/li[9]/a')
    try:
        nextButton[0].click()
    except ElementClickInterceptedException:
        create_file()
    else:
        scrape_rolimons()

def create_file():
    df = pd.DataFrame(usernameList, columns=['Username'])
    df.to_csv('usernames.csv', mode='w', index=False)
    os.system('cls')
    print("    Done. Usernames added to usernames.csv")
    menu()

def open_roblox():
    global options
    options = webdriver.ChromeOptions()

    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    os.system('cls')
    driver.get("https://www.roblox.com/login")
    print("    ROBLOX opened.")
    driver.implicitly_wait(2)
    try:
        cookiesElement = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'cookie-banner-bg'))
        )
        cookiesElement.click()
    except Exception as e:
        print("    Cookie banner not found or not clickable:", e)
    userElement = driver.find_element(By.ID, "login-username")
    userElement.click()
    userElement.send_keys(username)

    passElement = driver.find_element(By.ID, "login-password")
    passElement.click()
    passElement.send_keys(password)

    loginElement = driver.find_element(By.ID, "login-button")
    loginElement.click()
    print("    You have 60 seconds to complete any 2FA.")
    time.sleep(60)
    options.add_argument("--headless")
    add_friends()

def add_friends():
    global loopVariableAdd
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    df = pd.read_csv('usernames.csv')
    iterations = int(df.size)
    while iterations >= 0:
        searchTerm = df['Username'].loc[df.index[loopVariableAdd]]
        search = driver.find_elements(By.XPATH, '//*[@id="navbar-search-input"]')
        print(f"Found {len(search)} search bars.")
        search[0].click()
        search[0].send_keys(searchTerm)
        time.sleep(1)
        people = driver.find_elements(By.XPATH, "//*[contains(text(), 'in People')]")
        time.sleep(1)
        people[0].click()
        time.sleep(2)
        add = driver.find_elements(By.XPATH, '/html/body/div[3]/main/div[2]/div/div/div/div/ul/li/div/ng-include/div[1]/button')
        time.sleep(3)
        try: 
            add[0].click()
        except Exception:
            print("    User not found.")
        loopVariableAdd+=1
        iterations-=1
        search = driver.find_elements(By.XPATH, '//*[@id="navbar-search-input"]')
        search[0].click()  # Ensure focus
        search[0].send_keys(Keys.CONTROL + 'a')  # Select all text
        search[0].send_keys(Keys.BACKSPACE)  # Delete it
    menu()



menu()
