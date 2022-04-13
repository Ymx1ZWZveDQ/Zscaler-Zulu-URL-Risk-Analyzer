#imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import os
import sys

#Variables
checkurl = input("Enter URL to scan: ")
PATH = "C:\chromedriver.exe"
timestr = time.strftime("%Y%m%d-%H%M%S")
line = '---------------------------------------'
invalid = "invalid"
ZULU = "https://zulu.zscaler.com/"

#Get LocalDir
from os.path import expanduser
home = expanduser("~")

#Browser Driver Setup
options = webdriver.ChromeOptions()
options.add_argument('headless')
#options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome(PATH, chrome_options=options)

#Get ZULU
driver.get(ZULU)

#devtest#
#checkurl = "test.com"

#Find URL text box and enter text
inputElement = driver.find_element_by_id("url")
inputElement.send_keys(checkurl)

#devtest#
#inputElement.send_keys("test.com")

#Find Analyze button and click
submit = driver.find_element_by_css_selector('[value="Analyze"]')
submit.click()

#add Variable to Clipboard
def clipped(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)

#restart Script with prompt
def restart():
	askrestart = input("Restart Script? (Y/N): ")
	if askrestart=='Y' or askrestart=='y' or askrestart=='yes':
		print("restarting",sys.argv)
		os.execv(sys.executable, ['python'] + sys.argv)
	else:
		print("Exiting...")

#Logging output to Desktop
def logging():
	with open(home+'\\Desktop\\log.txt', "a") as external_file:
		add_text = timestr, checkurl, score, isSafe, myURL
		print(add_text, file=external_file)
		external_file.close()

#Printing output to console
def printoutput():
	print(line)
	print("---------Zulu URL Risk Analyzer--------")
	print(line)
	print(timestr, checkurl, score, isSafe, myURL)
	print(line)
	clipped(myURL)
	print("Reprot URL copied to Clipboard")
	print(line)

#validate page and fetch Reputation Score using logging()/printoutput()/restart()
while True:
		InvalidURL = driver.current_url
		if  invalid in InvalidURL or ZULU == InvalidURL:
			driver.quit()
			print(line)
			print("Invalid URL - " + checkurl)
			print(line)
			print("Please make sure that you supplied valid url. (only ipv4 and FQDN)")
			print(line)
			restart()
			break
		else:
			rep = driver.find_element_by_id("rep-status").text
		if rep == "Completed":
			score = driver.find_element_by_id("rep-score").text
			score = re.sub('/100', '', score)
			intScore = int(score)
			if int(score) >= 60:
				isSafe = "Fail"
			else:	
				isSafe = "Pass"
			myURL = driver.current_url
			logging()
			printoutput()
			driver.quit()
			restart()
			break
		else:
			print("Scanning...")
			time.sleep(1)
