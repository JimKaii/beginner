from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException #Handle exception
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = webdriver.ChromeOptions()  # 創立 driver物件所需的參數物件
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=options)
driver.get("https://www.imdb.com/chart/moviemeter/")


# page 1
movies = []

# 使用 CLASS_NAME來提取電影標題和對應的 URL
movie_elements = driver.find_elements(By.CLASS_NAME, 'ipc-title-link-wrapper')

for movie in movie_elements:
    title = movie.text
    movie_url = movie.get_attribute('href')
    movies.append({"title": title, "url": movie_url})

hundred_popular_movies = movies[:100]
    
# 顯示抓取到的電影標題和 URL
for idx, movie in enumerate(hundred_popular_movies):
    print(f"{idx+1}-{movie['title']},{movie['url']}")
    



which_movie = int(input("選擇想查找的片名(數字)"))-1

if 0 <= which_movie < len(hundred_popular_movies):
    selected_movie = hundred_popular_movies[which_movie]
    print(f"你選擇的電影是: {selected_movie['title']}")
    print(f"正在打開 {selected_movie['title']} 的 IMDb 頁面...")
    
    driver.get(selected_movie['url'])
else:
    print("輸入的數字無效，請重新執行程式。")

# Page2
time.sleep(2)
try:
    # 等待最多 5 秒，直到關閉按鈕可點擊
    close_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.ipc-icon-button[aria-label="Close"]'))
    )
    close_button.click()  # 點擊關閉按鈕
    print("成功關閉彈窗！")
except Exception as e:
    print(f"在 5 秒內未找到關閉按鈕: {e}")
try:
    # 方法 1: 用 data-testid 找（最推薦）
    button = driver.find_element(By.CSS_SELECTOR, '[data-testid="hero-subnav-bar-all-topics-button"]')
    ActionChains(driver).move_to_element(button).click().perform()
    print("按鈕點擊成功！")
    # time.sleep(2)

    # 使用LINK_TEXT來定位 "Cast & crew" 連結
    cast_crew_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.LINK_TEXT, 'Cast & crew'))
    )
    cast_crew_button.click()  # 點擊 Cast & Crew 項目
    print("成功點擊 Cast & Crew！")


except Exception as e:
    print(f"找不到按鈕: {e}")



all_links = driver.find_elements(By.XPATH, "//a[contains(text(), 'Technical Specs')]")
if all_links:
    print("next Page")
    all_links[0].click()
else:
    
    # 可以選擇結束程式或做其他操作
    driver.quit()


    
time.sleep(2) 
# camera_spec
li_elements = driver.find_elements(By.CSS_SELECTOR, "ul.ipc-metadata-list > li")

# 創建一個空列表來儲存數據
data = []

# 遍歷每個 li 元素
for li in li_elements:
    label = li.find_element(By.CSS_SELECTOR, ".ipc-metadata-list-item__label").text
    content_items = li.find_elements(By.CSS_SELECTOR, ".ipc-metadata-list-item__list-content-item")
    
    content = []

    if content_items:
        for item in content_items:
            content.append(item.text)
    else:
    # 如果沒有內容項，給個空值
            content.append("No additional info")
    
    
    # 如果有多個內容，將其合併為一個字符串，並儲存這個信息
    data.append({"title": selected_movie["title"], "Label": label, "Content": ", ".join(content)})

# 使用 pandas 將數據轉換為表格
camera_data = pd.DataFrame(data)
camera_data.to_csv('camera_data.csv')
# 顯示整理後的表格
# print(df)


# 關閉瀏覽器
driver.quit()








time.sleep(100)
# 關閉瀏覽器
driver.quit()


# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# import pprint
# import time
# # 設定請求的 URL
# url = "https://www.imdb.com/chart/moviemeter/"

# # 設定 User-Agent 來模擬正常瀏覽器請求
# headers = {
#     "User-Agent": "Chrome/133.0.6943.127 "
# }

# # 發送 GET 請求獲取網頁內容
# response = requests.get(url, headers=headers)

# # 使用 BeautifulSoup 解析網頁內容
# soup = BeautifulSoup(response.text, 'html.parser')

# popular_movies = list()
# # find_all() 方法的 attrs 参数 定義一個字典參數 來搜索包含特殊屬性的 tag
# find_title_names = soup.find_all(attrs={"class": "ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-3713cfda-2 fSzZES cli-title with-margin"})
# for find_title_name in find_title_names:
#     movie_name = find_title_name.a.text.strip()
#     movie_url = find_title_name.a.get("href")
    
#     popular_movie = {
#         "movie": movie_name,
#         "url": movie_url
#     }

#     popular_movies.append(popular_movie)



# movie_df = pd.DataFrame(popular_movies)
# movie_df.index = movie_df.index+1
# movie_df.to_csv('popular_movies.csv')
