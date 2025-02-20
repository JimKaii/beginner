from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select #下拉式選單使用
from selenium.common.exceptions import NoSuchElementException #Handle exception
from ocr_component import get_captcha_code
import time

# Step 1,2
driver = webdriver.Chrome()
driver.get("https://irs.thsrc.com.tw/IMINT/")
cookie_confirm = driver.find_element(By.ID, "cookieAccpetBtn")
cookie_confirm.click()



departure_station = driver.find_element(By.NAME, 'selectStartStation')                                       
Select(departure_station).select_by_visible_text("台中")


arrival_station = driver.find_element(By.NAME, 'selectDestinationStation')                                          
Select(arrival_station).select_by_visible_text("台北")


arrival_time = driver.find_element(By.NAME, 'toTimeTable')
Select(arrival_time).select_by_visible_text("07:30")




driver.find_element(
    By.XPATH, "//input[@class='uk-input' and @readonly='readonly']").click()


start_date = "二月 22, 2025"
driver.find_element(
    By.XPATH, f"//span[@class='flatpickr-day' and @aria-label='{start_date}']").click()
   

while True:
# captcha
    captcha_pic = driver.find_element(By.ID, "BookingS1Form_homeCaptcha_passCode")
    captcha_pic.screenshot('captcha.png')
    captcha_code = get_captcha_code()
    captcha_enter = driver.find_element(By.ID, "securityCode")
    captcha_enter.send_keys(captcha_code)
    time.sleep(2)

    driver.find_element(By.ID, "SubmitButton").click()
    time.sleep(2)

    
    try:
        # driver.find_element(By.CLASS_NAME, 'alert-content uk-flex') 
        driver.find_element(By.ID, 'divErrMSG')
    except NoSuchElementException:
        print("進到第二步驟")
        break

time.sleep(20)
driver.quit()

