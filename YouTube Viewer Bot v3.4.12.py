import random
import re
from time import sleep
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup as bs
from openpyxl import load_workbook
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

user_agents_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
"Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
]


youtube_url = r"https://www.youtube.com/playlist?list=PLTcOpPJhpXnbh51sMUJPeCPe3Wrlo70DG"
workbook = load_workbook(filename=r"D:/janil user/Downloads/youtube viewer bot/worldcities.xlsx")
PATH = r"C:/Program Files (x86)/chromedriver_win32/chromedriver.exe"
sheet = workbook.active
proxies = []

soup = bs(requests.get(r'https://free-proxy-list.net/').content, "html.parser")
for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
    tds = row.find_all("td")
    try:
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        host = f"{ip}:{port}"
        proxies.append(host)
    except IndexError:
        continue

print("\nList of proxies retrieved:\n\n", *proxies, sep = '\n')
sleep(3)
print('\n# Initiating selenium.webdriver callback from WebDriverWait')
        
def generateNewParameters():
    i = random.randint(1,15000)    
    latitude = sheet['C' + str(i)].value
    longitude = sheet['D' + str(i)].value
    random_user_agent = random.choice(user_agents_list)
    Map_coordinates = dict({
        "latitude": latitude, 
        "longitude": longitude,
        "accuracy": 100})
    return Map_coordinates, random_user_agent


Map_coordinates, random_user_agent = generateNewParameters()
chrome_options_1 = webdriver.ChromeOptions()
# chrome_options_1.add_argument("--incognito")
# chrome_options_1.add_argument("start-maximized")
# chrome_options_1.add_argument('--proxy-server=http://%s' % proxie)
chrome_options_1.add_argument(f'user-agent={random_user_agent}')
chrome_options_1.add_argument(r'window-size=1200x600')
chrome_options_1.add_experimental_option(r"excludeSwitches", ["enable-automation"])
chrome_options_1.add_experimental_option(r'useAutomationExtension', False)
driver_1 = webdriver.Chrome(options=chrome_options_1, executable_path=PATH)
driver_1.execute_cdp_cmd("Emulation.setGeolocationOverride", Map_coordinates)
driver_1.get(url = youtube_url)

sleep(1)

Map_coordinates, random_user_agent = generateNewParameters()
chrome_options_2 = webdriver.ChromeOptions()
# chrome_options_2.add_argument("--incognito")
# chrome_options_2.add_argument("start-maximized")
# chrome_options_2.add_argument('--proxy-server=http://%s' % proxie)
chrome_options_2.add_argument(f'user-agent={random_user_agent}')
chrome_options_2.add_argument(r'window-size=1200x600')
chrome_options_2.add_experimental_option(r"excludeSwitches", ["enable-automation"])
chrome_options_2.add_experimental_option(r'useAutomationExtension', False)
driver_2 = webdriver.Chrome(options=chrome_options_2, executable_path=PATH)
driver_2.execute_cdp_cmd("Emulation.setGeolocationOverride", Map_coordinates)
driver_2.get(url = youtube_url)

sleep(1)

Map_coordinates, random_user_agent = generateNewParameters()
chrome_options_3 = webdriver.ChromeOptions()
# chrome_options_3.add_argument("--incognito")
# chrome_options_3.add_argument("start-maximized")
# chrome_options_3.add_argument('--proxy-server=http://%s' % proxie)
chrome_options_3.add_argument(f'user-agent={random_user_agent}')
chrome_options_3.add_argument(r'window-size=1200x600')
chrome_options_3.add_experimental_option(r"excludeSwitches", ["enable-automation"])
chrome_options_3.add_experimental_option(r'useAutomationExtension', False)
driver_3 = webdriver.Chrome(options=chrome_options_3, executable_path=PATH)
driver_3.execute_cdp_cmd("Emulation.setGeolocationOverride", Map_coordinates)
driver_3.get(url = youtube_url)

sleep(1)

Map_coordinates, random_user_agent = generateNewParameters()
chrome_options_4 = webdriver.ChromeOptions()
# chrome_options_4.add_argument("--incognito")
# chrome_options_4.add_argument("start-maximized")
# chrome_options_4.add_argument('--proxy-server=http://%s' % proxie)
chrome_options_4.add_argument(f'user-agent={random_user_agent}')
chrome_options_4.add_argument(r'window-size=1200x600')
chrome_options_4.add_experimental_option(r"excludeSwitches", ["enable-automation"])
chrome_options_4.add_experimental_option(r'useAutomationExtension', False)
driver_4 = webdriver.Chrome(options=chrome_options_4, executable_path=PATH)
driver_4.execute_cdp_cmd("Emulation.setGeolocationOverride", Map_coordinates)
driver_4.get(url = youtube_url)

sleep(4)
try:
    play_button = WebDriverWait(driver_1, 20).until(
        EC.presence_of_element_located((By.XPATH, r'//*[@id="movie_player"]/div[4]/button'))
    )
    play_button.click()
except: pass

sleep(3)
try:
    play_button = WebDriverWait(driver_2, 20).until(
        EC.presence_of_element_located((By.XPATH, r'//*[@id="movie_player"]/div[4]/button'))
    )
    play_button.click()
except: pass

sleep(3)
try:
    play_button = WebDriverWait(driver_3, 20).until(
        EC.presence_of_element_located((By.XPATH, r'//*[@id="movie_player"]/div[4]/button'))
    )
    play_button.click()
except: pass

sleep(3)
try:
    play_button = WebDriverWait(driver_4, 20).until(
        EC.presence_of_element_located((By.XPATH, r'//*[@id="movie_player"]/div[4]/button'))
    )
    play_button.click()
except: pass

try: 
    video_length = driver_1.find_element_by_xpath(r'//*[@id="movie_player"]/div[28]/div[2]/div[1]/div[1]/span[3]').text
    video_length_min = ' '.join(re.findall(r'([0-9]*):[0-9]{2}', video_length))
    video_length_sec = ' '.join(re.findall(r'[0-9]*:([0-9]{2})', video_length))
    sleep(int(video_length_min) * 60 + int(video_length_sec) + 3)
except: pass

try:
    video_length = driver_2.find_element_by_xpath(r'//*[@id="movie_player"]/div[28]/div[2]/div[1]/div[1]/span[3]').text
    video_length_min = ' '.join(re.findall(r'([0-9]*):[0-9]{2}', video_length))
    video_length_sec = ' '.join(re.findall(r'[0-9]*:([0-9]{2})', video_length))
    sleep(int(video_length_min) * 60 + int(video_length_sec) + 3)
except: pass

try:
    video_length = driver_3.find_element_by_xpath(r'//*[@id="movie_player"]/div[28]/div[2]/div[1]/div[1]/span[3]').text
    video_length_min = ' '.join(re.findall(r'([0-9]*):[0-9]{2}', video_length))
    video_length_sec = ' '.join(re.findall(r'[0-9]*:([0-9]{2})', video_length))
    sleep(int(video_length_min) * 60 + int(video_length_sec) + 3)
except: pass

video_length = driver_4.find_element_by_xpath(r'//*[@id="movie_player"]/div[28]/div[2]/div[1]/div[1]/span[3]').text
video_length_min = ' '.join(re.findall(r'([0-9]*):[0-9]{2}', video_length))
video_length_sec = ' '.join(re.findall(r'[0-9]*:([0-9]{2})', video_length))
sleep(int(video_length_min) * 60 + int(video_length_sec) + 3)

driver_1.quit()
driver_2.quit()
driver_3.quit()
driver_4.quit()