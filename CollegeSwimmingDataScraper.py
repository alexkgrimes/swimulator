# CollegeSwimmingDataScraper.py
# Swimulator
#
# Created by Alex Grimes on 07/18/2018
#
# Goal: Scrape all needed data from college swimming site
#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Constants
timeout = 10

# open college swimming page
wd = webdriver.Firefox()
wd.get('https://www.collegeswimming.com/recruiting/rankings/2015/F/')

# optional for going to next page in college swimming
nextButton = wd.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[1]/ul/li[11]/a')
# nextButton.click()

# get row for table in college swimming
row = wd.find_elements_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[1]/div/table/tbody/tr/td[1]')

for i in range(len(row)):
	# get the name from the row
	fullName = wd.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[1]/div/table/tbody/tr[' + str(i + 1) + ']/td[2]').text
	name = fullName.split()
	firstName = name[0]
	lastName = name[1]
	
	# get homeplace from the row
	homeplace = wd.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[1]/div/table/tbody/tr[' + str(i + 1) + ']/td[4]').text
	fullPlace = homeplace.split(',')
	town = fullPlace[0]
	state = fullPlace[1]

# switch to fastest tab for times
wd.find_element_by_link_text(fullName).click()
wd.find_element_by_link_text("Fastest").click()

# get the rows of times
timesRows = wd.find_elements_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[2]/div/section[2]/div/div/table/tbody/tr/td[1]')

eventTimeDict = {}
for i in range(len(timesRows)):
	event = wd.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[2]/div/section[2]/div/div/table/tbody/tr[' + str(i + 1) + ']/td[1]').text
	if 'Y' not in event:
		continue
	print event
	time = wd.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[2]/div/section[2]/div/div/table/tbody/tr[' + str(i + 1) + ']/td[2]').text
	print time
	eventTimeDict[event] = time
