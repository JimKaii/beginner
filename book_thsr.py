

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select #下拉式選單使用
from selenium.common.exceptions import NoSuchElementException #Handle exception
from ocr_component import get_captcha_code
import pprint
import time
import os

#第一個頁面
def create_drive():
    options = webdriver.ChromeOptions()  # 創立 driver物件所需的參數物件
    options.add_argument("--disable-blink-features=AutomationControlled")  # 禁用自動化檢測 避免被網站檢測
    global driver
    driver = webdriver.Chrome(options=options)  # 創建一個 Chrome 瀏覽器實例
    driver.get("https://irs.thsrc.com.tw/IMINT/")
    
# Click accept cookie button
    cookie_confirm = driver.find_element(By.ID, "cookieAccpetBtn")
    cookie_confirm.click()

    
# Choose Booking parameters: startStation, destStation, time
# 找 出發站 到達站 時間
def book_choose_time(start_station, dest_station, start_time, start_date):
    departure_station = driver.find_element(By.NAME, 'selectStartStation')                                       
    Select(departure_station).select_by_visible_text(start_station)

    arrival_station = driver.find_element(By.NAME, 'selectDestinationStation')                                          
    Select(arrival_station).select_by_visible_text(dest_station)

    departure_time = driver.find_element(By.NAME, 'toTimeTable')
    Select(departure_time).select_by_visible_text(start_time)

# Choose Booking parameters: date
# 選擇 搭乘日期

    driver.find_element(
        By.XPATH, "//input[@class='uk-input' and @readonly='readonly']").click()

    driver.find_element(
        By.XPATH, f"//span[@class='flatpickr-day' and @aria-label='{start_date}']").click()
    
    # Validation
    while True:
    # captcha
        captcha_pic = driver.find_element(By.ID, "BookingS1Form_homeCaptcha_passCode")
        captcha_pic.screenshot('captcha.png')
        captcha_code = get_captcha_code()
        captcha_enter = driver.find_element(By.ID, "securityCode")
        captcha_enter.send_keys(captcha_code)
        time.sleep(2)

        # submit
        departure_date = driver.find_element(By.ID, "SubmitButton").click()
        departure_date()
    

    # check validation is success or not   
        try:
            time.sleep(5)
            # driver.find_element(By.CLASS_NAME, 'alert-content uk-flex') 
            driver.find_element(By.ID, "BookingS2Form_TrainQueryDataViewPanel")
            print("驗證碼正確, 進入第二步驟")
            break
        except NoSuchElementException:
            print("驗證碼錯誤")
        
#第二個頁面

    trains_info = list()
    trains = driver.find_element(By.CLASS_NAME, "result-listing").find_elements(By.TAG_NAME, "label")
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
    return trains_info


def select_train_and_submit_booking(trains_info):
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

    #  第三個頁面  

    # Check booking infomation for user
    driver.find_element(By.CLASS_NAME, "ticket-summary").screenshot('thsr_summary.png')

    id_number = driver.find_element(By.ID, "idNumber")
    # enter_id = input("請輸入身分證字號")
    enter_id = os.getenv("PERSONAL_ID") #使用環境變數
    id_number.send_keys(enter_id)

    phone_number = driver.find_element(By.ID, "mobilePhone")
    # enter_phone = int(input("請輸入手機號碼"))
    enter_phone = os.getenv("PERSONAL_NUMBER")
    phone_number.send_keys(enter_phone)

    email_addres = driver.find_element(By.ID, "email")
    # enter_email = input("請輸入電子郵件")
    enter_email = os.getenv("PERSONAL_EMAIL")
    email_addres.send_keys(enter_email)

    driver.find_element(By.NAME, "agree").click()
    driver.find_element(By.ID, 'isSubmit').click()

    #Save booking result
    screenshot_file = 'thsr_booking_result.png'
    driver.find_element(
        By.CLASS_NAME, 'ticket-summary').screenshot(screenshot_file)
    print("訂票完成!")

    return

time.sleep(2000)
driver.quit()

