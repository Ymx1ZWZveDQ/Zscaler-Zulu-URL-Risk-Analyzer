#imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import time
import re
import os
import sys

#Variables
checkurl = input("Enter URL to scan: ")
#https://sites.google.com/chromium.org/driver/downloads
PATH = "C:\chromedriver.exe"
timestr = time.strftime("%Y%m%d-%H%M%S")

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
driver.get("https://zulu.zscaler.com/")

#Find URL text box and enter text
inputElement = driver.find_element_by_id("url")
inputElement.send_keys(checkurl)

#devtest#
#checkurl = "test.com"
#inputElement.send_keys("test.com")

#Find Analyze button and click
submit = driver.find_element_by_css_selector('[value="Analyze"]')
submit.click()

#exit Script
def exit(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    os.system("taskkill /im py.exe")

#add to Clipboard
def clipped(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)

#restart Script
def restart():
    print("restarting",sys.argv)
    os.execv(sys.executable, ['python'] + sys.argv)

#scrub page for Reputation Score and print output
while True:
	try:
		test = driver.find_element_by_id("rep-status").text
		if test == "Completed":
			score = driver.find_element_by_id("rep-score").text
			score = re.sub('/100', '', score)
			if int(score) >= 60:
				isSafe = "Fail"
			else:
				isSafe = "Pass"
			myURL = driver.current_url
			with open(home+'\\Desktop\\log.txt', "a") as external_file:
		    		add_text = timestr, checkurl, score, isSafe, myURL
    				print(add_text, file=external_file)
    				external_file.close()
			print("---------------------------------------")
			print("---------Zulu URL Risk Analyzer--------")
			print("---------------------------------------")
			print(timestr, checkurl, score, isSafe, myURL)
			print("---------------------------------------")
			clipped(myURL)
			print("Reprot copied to Clipboard")
			print("---------------------------------------")
			askrestart = input("Restart Script? (Y/N): ")
			if askrestart=='Y' or askrestart=='y' or askrestart=='yes':
				restart()
			else:
				print("Exiting...")
				exit(int(10))
			break
		else:
			print("Scanning...")
			time.sleep(1)
	except StaleElementReferenceException:
		continue
