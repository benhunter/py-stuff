from selenium import webdriver
import time
timer = 0

proxies = open('proxies.txt', 'r+')
file = proxies.readlines()
proxies.close()

for x in range(0, len(file) +1):
    webdriver.DesiredCapabilities.FIREFOX['proxy']={
        "httpProxy":proxies[x],
        "sslProxy":proxies[x],
        "proxyType":"MANUAL"
    }
    driver = webdriver.Firefox()
    # driver.get('https://refer4.cash/KorruptedCrxckz')
    find = driver.search_element_by_id("submit")
    find.click()
    time.sleep(3)
