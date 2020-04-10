from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--kiosk')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome('chromedriver', options = options)

driver.get('file:///E:/Data/Code/CoronavirusTimelapse/old/html/2020-04-01-2.html')
screenshot = driver.save_screenshot('screenshot.png')
driver.quit()