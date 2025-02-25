

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select #下拉式選單使用
from selenium.common.exceptions import NoSuchElementException #Handle exception
from ocr_component import get_captcha_code
import pprint
import time
import os

#Project modlues   
                            ###   把 訂票對話 導入
from booking_info_extraction_flow import(
    ask_booking_infomation,
    ask_missing_infomation,
    convert_date_to_thsr_format
)

def create_drive():
    options = webdriver.ChromeOptions()  # 創立 driver物件所需的參數物件
    options.add_argument("--disable-blink-features=AutomationControlled")  # 禁用自動化檢測 避免被網站檢測
    global driver
    driver = webdriver.Chrome(options=options)  # 創建一個 Chrome 瀏覽器實例
    driver.get("https://irs.thsrc.com.tw/IMINT/")
   


#第一個頁面    
# Choose Booking parameters: startStation, destStation, time
# 找 出發站 到達站 時間
def book_choose_time(start_station, dest_station, start_time, start_date):
#第一個頁面 
    time.sleep(3)
    cookie_confirm = driver.find_element(By.ID, "cookieAccpetBtn")
    cookie_confirm.click()
    # Choose Booking parameters: startStation, destStation, time
    # 找 出發站 到達站 時間
    departure_station = driver.find_element(By.NAME, 'selectStartStation')                                       
    Select(departure_station).select_by_visible_text(start_station)

    arrival_station = driver.find_element(By.NAME, 'selectDestinationStation')                                          
    Select(arrival_station).select_by_visible_text(dest_station)

    departure_time = driver.find_element(By.NAME, 'toTimeTable')
    Select(departure_time).select_by_visible_text(start_time)

    driver.find_element(
        By.XPATH, "//input[@class='uk-input' and @readonly='readonly']").click()

    driver.find_element(
        By.XPATH,
        f"//span[(@class='flatpickr-day' or @class='flatpickr-day today selected') and @aria-label='{start_date}']").click()
   
    while True:
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
    



    # Choose train
    for idx, train in enumerate(trains_info):
        print(
            f"({idx}) - {train['train_code']}, \
            行駛時間={train['duration']} | \
            {train['depart_time']} -> \
            {train['arrival_time']}"
        )

    return trains_info

def select_train_and_submit_booking(trains_info, which_train):

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

    return screenshot_file


if __name__ == "__main__":

    # Booking parameters
    # start_station = '台中'
    # dest_station = '板橋'
    # start_time = '18:00'
    # start_date = '二月 25, 2025'

                     ### 這是導入chatgpt做成一個 訂票對話 的程式 
    #Step 1:
    booking_info = ask_booking_infomation()
    #Step 2:
    booking_info = ask_missing_infomation(booking_info)
    #Step 3:
    booking_info = convert_date_to_thsr_format(booking_info)
    
                        #再將 訂票對話 與原本 訂票爬蟲 合併

    create_drive() # 爬蟲

    #Step 4      
    trains_info = book_choose_time(
    start_station = booking_info['出發點'], 
    dest_station =  booking_info['抵達點'],
    start_date =  booking_info['出發日期'],
    start_time = booking_info['出發時辰']
        )

    # Step 5
    select_train_and_submit_booking(trains_info)    



    time.sleep(20)
    driver.quit()

