from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path="~PATH~", options=chrome_options)
driver.get("~~")
a = driver.find_elements_by_tag_name("a")
count =0
for element in a:
    print(element.get_attribute('innerHTML'))
    print(element.get_attribute('href'))
    count=count+1
    if (count>10) :
        break

driver.quit()
