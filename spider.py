from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time 
import json
import os


display = Display(visible=0, size=(800, 600))
display.start()

# GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
# CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
# chrome_options.headless = True
chrome_options.add_argument("window-size=1400,800")
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
def twitter():
	headers = {"Authorization": "Bearer **********************************"}
	with open("data.json", "r") as jsonFile:
		jsonObject = json.load(jsonFile)
		for hash_name in jsonObject['hashtags']:
			response = requests.get("https://api.twitter.com/2/tweets/counts/recent?query="+hash_name.split("#")[1], headers=headers).json()
			# return hash_name.split("#")[1]
			if len(jsonObject['data']['twitter']) != 0:
				finded = False
				for obj in jsonObject['data']['twitter']:
					if hash_name in obj:
						obj[hash_name] = int(obj[hash_name]) + (int(response['meta']['total_tweet_count']) - int(obj[hash_name]))
						finded = True
						break
				if not finded:
					jsonObject['data']['twitter'].append({hash_name:response['meta']['total_tweet_count']})
			else:
				jsonObject['data']['twitter'].append({hash_name: response['meta']['total_tweet_count']})
		jsonFile.close()
	jsonString = json.dumps(jsonObject)
	with open("data.json", "w") as file:
		file.write(jsonString)
		file.close()




def parser():
	driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_options)
	try:
		driver.get("https://www.instagram.com/")
		driver.maximize_window()
		with open("file_access.json", "r") as f:
			obj = json.load(f)
			f.close()
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(obj["instagram"]["login"])
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(obj["instagram"]["password"])
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).submit()
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section/main/div/div/div/div/button"))).click()
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div/div[3]/button[2]"))).click()
		input_el = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']")))
		with open("data.json", "r") as jsonFile:
			jsonObject = json.load(jsonFile)
			jsonObject["data"]["instagram"] = []
			for hash_name in jsonObject['hashtags']:
				input_el.send_keys(hash_name)
				time.sleep(3)
				hashtag = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a/div/div[2]/div[2]/div/span/span"))).text
				input_el.clear()
				jsonObject["data"]["instagram"].append({hash_name:hashtag})
				jsonString = json.dumps(jsonObject)
			jsonFile.close()
		with open("data.json", "w") as file:
			file.write(jsonString)
			file.close()
	finally:
		driver.close()


# https://github.com/heroku/heroku-buildpack-google-chrome
# https://github.com/heroku/heroku-buildpack-chromedriver
# os.environ.get("CHROMEDRIVER_PATH")
def test(type, login, password):
	if type == "instagram":
		driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_options)
		print ("Headless Chrome with default window-size")
		size = driver.get_window_size()
		print("Window size: width = {}px, height = {}px".format(size["width"], size["height"]))
		# driver.get("https://www.instagram.com/")
		# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(login)
		# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(password)
		# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).submit()
		# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section/main/div/div/div/div/button"))).click()
		# return False
		try:
			driver.get("https://www.instagram.com/")
			driver.maximize_window()
			WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(login)
			WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(password)
			WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).submit()
			WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/section/main/div/div/div/div/button"))).click()
			return True
		except:
			return False
		finally:
			driver.close()
