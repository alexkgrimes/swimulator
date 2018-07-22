# UsaSwimmingDataScraper.py
# Swimulator
#
# Created by Alex Grimes on 07/15/2018
#
# Goal: Reference data from college swimming and download excel sheets from usa swimming SWIMS
#

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# ----- Constants ----- #
scyEvents = ['50 FR SCY', '100 FR SCY', '200 FR SCY', '500 FR SCY', '1000 FR SCY', '1650 FR SCY', '50 BK SCY', '100 BK SCY', '200 BK SCY', '50 BR SCY', '100 BR SCY', '200 BR SCY', '50 FL SCY', '100 FL SCY', '200 FL SCY', '100 IM SCY', '200 IM SCY', '400 IM SCY']
lcmEvents = ['50 FR LCM', '100 FR LCM', '200 FR LCM', '400 FR LCM', '800 FR LCM', '1500 FR LCM', '50 BK LCM', '100 BK LCM', '200 BK LCM', '50 BR SCY','100 BR LCM', '200 BR LCM', '50 FL LCM', '100 FL LCM', '200 FL LCM', '200 IM LCM', '400 IM LCM']
allEvents = scyEvents + lcmEvents

# ----- Paths ----- #
afterDatePath = '//*[@id="UsasTimeSearchIndividual_Index_Div_1StartDate"]'
beforeDatePath = '//*[@id="UsasTimeSearchIndividual_Index_Div_1EndDate"]'
byEventSelectorArrowPath = '/html/body/div[1]/div/div/div[11]/div[1]/form/fieldset/div[6]/div/span/span/span[2]'
nextButtonPath = '/html/body/div[1]/div[2]/div[1]/div/div[1]/ul/li[11]/a'
collegeSwimTablePath = '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/table/tbody/tr/td[1]'
firstNameBoxPath = '//*[@id="UsasTimeSearchIndividual_Index_Div_1FirstName"]'
lastNameBoxPath = '//*[@id="UsasTimeSearchIndividual_Index_Div_1LastName"]'
findTimesButtonPath = '//*[@id="UsasTimeSearchIndividual_Index_Div_1-saveButton"]'
usaSwimTablePath = '/html/body/div[1]/div/div/div[11]/div[2]/div[2]/div[2]/table/tbody/tr/td[1]'

# ----- Scripts ----- #
selectOnlyFastestScript = '$(\'#UsasTimeSearchIndividual_Index_Div_1ddlTimesFilter\').data(\'kendoDropDownList\').value(\'FastestByEvent\')'

def getTimesForSwimmer():
	timesTableSize = len(wd.find_elements_by_xpath(usaSwimTablePath))

	eventIndex = 0
	timesIndex = 0
	while timesIndex < range(timesTableSize) and eventIndex < len(scyEvents):
		# get eventName but only if you have gotten to times results
		try:
			eventName = wd.find_element_by_xpath('/html/body/div[1]/div/div/div[11]/div[2]/div[2]/div[2]/table/tbody/tr[' + str(timesIndex + 1) + ']/td[1]').text
		except NoSuchElementException:
			print("There is more than one person with this name.")
			return

		eventTime = wd.find_element_by_xpath('/html/body/div[1]/div/div/div[11]/div[2]/div[2]/div[3]/table/tbody/tr[' + str(timesIndex + 1) + ']/td[1]').text
		if eventTime.endswith('r'):
			eventTime = eventTime[:len(eventTime) - 1]

		# handle repeat events for one event
		if eventIndex != 0 and eventName == scyEvents[eventIndex - 1]:
			timesIndex += 1
			continue

		# handle matching eventNames 
		if eventName == allEvents[eventIndex]:
			timesIndex += 1
		# if there is a missing time
		else:
			eventTime = ''
		print 'eventName: ', scyEvents[eventIndex], '\t', eventTime
		eventIndex += 1
	print

# open college swimming page
wd = webdriver.Firefox()
wd.get('https://www.collegeswimming.com/recruiting/rankings/2015/F/')

# open new tab and load usa swimming swims database, set up query besides name
wd.execute_script("window.open('');")
wd.switch_to.window(wd.window_handles[1])
wd.get('https://www.usaswimming.org/Home/times/individual-times-search')

afterDate = wd.find_element_by_xpath(afterDatePath)
beforeDate = wd.find_element_by_xpath(beforeDatePath)
afterDate.send_keys('01/01/2006')
beforeDate.send_keys('12/31/2013')

byEventSelectorArrow = wd.find_element_by_xpath(byEventSelectorArrowPath)
byEventSelectorArrow.click

# switch back to college swimming
wd.switch_to.window(wd.window_handles[0])

# optional for going to next page in college swimming
nextButton = wd.find_element_by_xpath(nextButtonPath)
# nextButton.click()

# get row and column for table in college swimming
tableSize = len(wd.find_elements_by_xpath(collegeSwimTablePath))

# loop through all your swimmers
for i in range(tableSize):
	# get the name from the row
	fullName = wd.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[1]/div/table/tbody/tr[' + str(i + 1) + ']/td[2]').text
	print fullName
	name = fullName.split()
	firstName = name[0]
	lastName = name[1]

	# get the hometown
	homeplace = wd.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[1]/div/table/tbody/tr[' + str(i + 1) + ']/td[4]').text
	fullPlace = homeplace.split(',')
	town = fullPlace[0]
	state = fullPlace[1]

	# go to usa swimming and fill in the query stuff
	wd.switch_to.window(wd.window_handles[1])
	firstNameBox = wd.find_element_by_xpath(firstNameBoxPath)
	lastNameBox = wd.find_element_by_xpath(lastNameBoxPath)
	firstNameBox.clear()
	lastNameBox.clear()
	firstNameBox.send_keys(firstName)
	lastNameBox.send_keys(lastName)

	# select only fastest times by event
	wd.execute_script(selectOnlyFastestScript)

	# click find times button
	findTimesButton = wd.find_element_by_xpath(findTimesButtonPath)
	findTimesButton.click()
	time.sleep(2)

	getTimesForSwimmer()

	# go back to college swimming
	wd.switch_to.window(wd.window_handles[0])

print 'all done'

