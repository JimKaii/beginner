from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select #下拉式選單使用
from selenium.common.exceptions import NoSuchElementException #Handle exception
from ocr_component import get_captcha_code
import pprint
import time
import os

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
    

    
    try:
        time.sleep(5)
        # driver.find_element(By.CLASS_NAME, 'alert-content uk-flex') 
        driver.find_element(By.ID, "BookingS2Form_TrainQueryDataViewPanel")
        print("驗證碼正確, 進入第二步驟")
        break
    except NoSuchElementException:
        print("驗證碼錯誤")
        

trains_info = list()
trains = driver.find_element(By.CLASS_NAME, "result-listing").find_elements(By.TAG_NAME, "label")
# choose_times =driver.find_element(By.CLASS_NAME, "result-listing")
# departure_time =driver.find_element(By.ID, 'QueryDeparture').text
# arrival_time = driver.find_element(By.ID, 'QueryArrival').text
# duration_time = driver.find_element(By.CLASS_NAME, 'duration').text[1]

for train in trains:   
    info = train.find_element(By.CLASS_NAME, "uk-radio")
    trains_info.append(
        {
            'depart_time': info.get_attribute('querydeparture'),
            'arrival_time': info.get_attribute('queryarrival'),
            'duration': info.get_attribute('queryestimatedtime'),
            'train_code': info.get_attribute('querycode'),
            'radio_box': info,
        }   
    )
# pprint.pprint(all_choose)


# Choose train
for idx, train in enumerate(trains_info):
    print(
        f"({idx}) - {train['train_code']}, \
        行駛時間={train['duration']} | \
        {train['depart_time']} -> \
        {train['arrival_time']}"
    )

which_train = int(input("Choose your train. Enter from 0~9: "))
trains_info[which_train]['radio_box'].click()

driver.find_element(By.NAME, "SubmitButton").click()
print("車次選擇完成，進入第三步驟")
time.sleep(5)

id_number = driver.find_element(By.ID, "idNumber")
phone_number = driver.find_element(By.ID, "mobilePhone")
email_addres = driver.find_element(By.ID, "email")

# enter_id = input("請輸入身分證字號")
enter_id = os.getenv("PERSONAL_ID")
# enter_phone = int(input("請輸入手機號碼"))
enter_phone = os.getenv("PERSONAL_NUMBER")
# enter_email = input("請輸入電子郵件")
enter_email = os.getenv("PERSONAL_EMAIL")

id_number.send_keys(enter_id)
phone_number.send_keys(enter_phone)
email_addres.send_keys(enter_email)

driver.find_element(By.NAME, "agree").click()
driver.find_element(By.ID, 'isSubmit').click()





time.sleep(20)
driver.quit()

