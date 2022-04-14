#imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re
import os
import sys

#Variables
checkurl = input("Enter URL to rate: ")
zulu = "https://zulu.zscaler.com/"
path = "C:\chromedriver.exe"
chrome = Service(path)
invalid = "invalid"
timeStr = time.strftime("%Y%m%d-%H%M%S")
from os.path import expanduser
home = expanduser("~")
line = '---------------------------------------'

#Chrome Driver Setup
#options.add_argument('window-size=1920x1080')
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=chrome, options=options)

#Get ZULU
driver.get(zulu)

#Find URL text box and enter text
#checkurl = "test.com"
inputElement = driver.find_element(By.ID, "url")
inputElement.send_keys(checkurl)
#inputElement.send_keys("test.com")

#Find Analyze button and click
submit = driver.find_element(By.CSS_SELECTOR, '[value="Analyze"]')
submit.click()

#add Variable to Clipboard
def clipped(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)

#Logging output to Desktop
def logging():
	with open(home+'\\Desktop\\log.txt', "a") as external_file:
		add_text = timeStr, checkurl, score, isSafe, myURL
		print(add_text, file=external_file)
		external_file.close()

#Printing output to console
def printoutput():
	print(line)
	print("---------Zulu URL Risk Analyzer--------")
	print(line)
	print(timeStr, checkurl, score, isSafe, myURL)
	print(line)
	clipped(myURL)
	print("Reprot URL copied to Clipboard")
	print("Log entry created, "+home+'\\Desktop\\log.txt')
	print(line)

#validate page and fetch Reputation Score using logging()/printoutput()/restart()
while True:
	InvalidURL = driver.current_url
	if  invalid in InvalidURL or zulu == InvalidURL:
		driver.quit()
		print(line)
		print("Invalid URL - " + checkurl)
		print(line)
		print("Please make sure that you supplied valid url. (only ipv4 and FQDN)")
		print(line)
		os.execv(sys.executable, ['python'] + sys.argv)
		break
	else:
		rep = driver.find_element(By.ID, "rep-status").text
	if rep == "Completed":
		score = driver.find_element(By.ID, "rep-score").text
		score = re.sub('/100', '', score)
		#intScore = int(score)
		if int(score) >= 60:
			isSafe = "Fail"
		else:	
			isSafe = "Pass"
		myURL = driver.current_url
		logging()
		printoutput()
		driver.quit()
		os.execv(sys.executable, ['python'] + sys.argv)
		break
	else:
		print("Analyzing...")
		time.sleep(2)
