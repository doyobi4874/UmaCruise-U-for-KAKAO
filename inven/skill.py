from selenium import webdriver
from bs4 import BeautifulSoup
import os
import re
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(r"d:\Chromedriver.exe",options=options)
driver.get('https://uma.inven.co.kr/dataninfo/deckbuilder/')
driver.implicitly_wait(10)