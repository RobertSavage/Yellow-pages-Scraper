from selenium import webdriver
from time import sleep
import urllib.request
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import bs4
import webbrowser
from selenium.webdriver.common.by import By
import random
import datetime as dt
import colordolist as CL

print('START TIME: ', dt.datetime.now())

class Yellowpages():

	def __init__(self, places):
		

		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument("--headless")  
		self.driver = webdriver.Chrome(executable_path=r'D:/SAVED PROJECTS/Python/BOTS/Yellowpages scraper/chromedriver_win32/chromedriver.exe', chrome_options=chrome_options)
		sleep(2)
		self.driver.set_window_position(-10000,0)
		self.driver.get('https://www.yellowpages.com/')
		sleep(2)

		Buisness = 'restaurant'
		location = places

		self.driver.find_element_by_xpath('//*[@id="query"]').send_keys(Buisness)
		self.driver.find_element_by_xpath('//*[@id="location"]').click()
		sleep(2)
		self.driver.find_element_by_xpath('//*[@id="location"]').send_keys(location)

		#hit search
		STWII = self.driver.find_element_by_xpath('//*[@id="search-form"]/button')
		STWII.click()
		sleep(4)
		#type where you are looking for

		links_for_buisnesses = []

		res = requests.get(self.driver.current_url)
		res.raise_for_status()
		soup = bs4.BeautifulSoup(res.text, 'html.parser')

		for div in soup.find_all("div", {"class": "info"}):
			a = div.find('a')
			href = a.get('href')
			links_for_buisnesses.append(href)

		nextbutton1 = soup.find("a", {"next ajax-page"})

		search = True
		while search == True:

			try:
				nextbutton2 = nextbutton1.get('href')
			except:
				print('done')
				search = False
			#hits next button
			try:
				newres = requests.get('https://www.yellowpages.com'+nextbutton2)
				newres.raise_for_status()
				newsoup = bs4.BeautifulSoup(newres.text, 'html.parser')
				nextbutton1 = newsoup.find("a", {"next ajax-page"})
			except:
				print(' ')
				search = False


			try:
				for div in newsoup.find_all("div", {"class": "info"}):
					a = div.find('a')
					href = a.get('href')
					links_for_buisnesses.append(href)
				sleep(5)

			except:
				search = False

		print('amount of links: ', len(links_for_buisnesses))
		#this part gets urls
		name = []
		phone = [] 
		emaillist = []
		going = True
#----------------------------email
		for div in links_for_buisnesses:
			try:
				#print('https://www.yellowpages.com'+div)
				res = requests.get('https://www.yellowpages.com'+div)
				res.raise_for_status()
				newsoup = bs4.BeautifulSoup(res.text, 'html.parser')
				a = newsoup.find('a', {"class": "email-business"})
				href = a.get('href')
				emaillist.append(href)
				print(counter)
			except:
				#emaillist.append(' ')
				continue
		print('done with emails')

##----------------------------name
#		for div in links_for_buisnesses:
#			try:
#				#print('https://www.yellowpages.com'+div)
#				res = requests.get('https://www.yellowpages.com'+div)
#				res.raise_for_status()
#				newsoup = bs4.BeautifulSoup(res.text, 'html.parser')
#				a = newsoup.find('div', {"class": "sales-info"})
#				h1 = a.get('h1')
#				name.append(h1)
#			except:
#				name.append(' ')
#				continue
#		print('done with names')
##----------------------------phone
#		for div in links_for_buisnesses:
#			try:
#				#print('https://www.yellowpages.com'+div)
#				res = requests.get('https://www.yellowpages.com'+div)
#				res.raise_for_status()
#				newsoup = bs4.BeautifulSoup(res.text, 'html.parser')
#				a = newsoup.find('div', {"class": "contact"})
#				p = a.get('p')
#				phone.append(p)
#			except:
#				phone.append(' ')
#				continue
#		print('done with phone')

		for i in emaillist:

			with open("colorado_rest.txt", "a") as chkc:
				chkc.write(i+"\n")

		self.driver.quit()
count = 1

for i in CL.colo:
	print('LOCATION: ',i)
	botstart = Yellowpages(i)
	botstart
	print('operation: ',count,'/',len(CL.colo),' done')
	count += 1