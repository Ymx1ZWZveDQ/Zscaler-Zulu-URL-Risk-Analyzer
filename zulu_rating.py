#imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import time
import re


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

#scrub page for Reputation Score
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
			print("----SCORE----")
			print(timestr, checkurl, score, isSafe, myURL)
			break
		else:
			print("Scanning...")
	except StaleElementReferenceException:
		continue
