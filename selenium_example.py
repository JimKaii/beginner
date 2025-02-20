from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select #下拉式選單使用

import time
# Step 1,2
driver = webdriver.Chrome()
driver.get("https://www.selenium.dev/selenium/web/web-form.html")



#Step 4:
driver.implicitly_wait(0.5)
print('driver already wait 2 sec')

#Step 5:
#text_box = soup.find(name="my-text")       #bs4寫法
text_box = driver.find_element(by=By.NAME, value="my-text")

#text_box = soup.find('button')             #bs4寫法
submit_button = driver.find_element(by=By.TAG_NAME, value="button")

#submit_button = soup.css.select('button')  #bs4寫法
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")


#Step 5-1 :  查找其他資訊
password_box = driver.find_element(by=By.NAME, value="my-password")
Textarea_button = driver.find_element(by=By.TAG_NAME, value="textarea")

#Step 5-2: 找到Dropdown, 選擇TWO         #"//select[]"
number_dropdown = driver.find_element(By.XPATH, 
                                      "//select[@class='form-select' and @name='my-select']") 
number_select = Select(number_dropdown)
number_select.select_by_visible_text('Two')






#Step 6:
text_box.send_keys("Selenium")
password_box.send_keys("gjidkdkdk")
Textarea_button.send_keys("gjidkdkdk")
time.sleep(3)
submit_button.click()

#Step 7:
message = driver.find_element(by=By.CLASS_NAME, value="container")
print(message.text)




time.sleep(10)
driver.quit()