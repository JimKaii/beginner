from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options)

def get_movie_list(driver):
    driver.get("https://www.imdb.com/chart/moviemeter/")
    movies = []
    movie_elements = driver.find_elements(By.CLASS_NAME, 'ipc-title-link-wrapper')
    for movie in movie_elements:
        title = movie.text
        movie_url = movie.get_attribute('href')
        movies.append({"title": title, "url": movie_url})
    return movies[:100]

def select_movie(driver, movie):
    driver.get(movie['url'])
    time.sleep(2)
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.ipc-icon-button[aria-label="Close"]'))
        )
        close_button.click()
    except:
        pass
    try:
        button = driver.find_element(By.CSS_SELECTOR, '[data-testid="hero-subnav-bar-all-topics-button"]')
        ActionChains(driver).move_to_element(button).click().perform()
        cast_crew_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Tech specs'))
        )
        cast_crew_button.click()
    except:
        pass
    time.sleep(2)
    return extract_movie_data(driver, movie['title'])


def extract_movie_data(driver, title):
    data = []
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.ipc-metadata-list > li"))
        )
        li_elements = driver.find_elements(By.CSS_SELECTOR, "ul.ipc-metadata-list > li")
        for li in li_elements:
            try:
                label_elem = li.find_element(By.CSS_SELECTOR, ".ipc-metadata-list-item__label")
                # 抓兩種 class 的項目：主要內容 + 子文字
                content_items = li.find_elements(By.CSS_SELECTOR, ".ipc-metadata-list-item__list-content-item, .ipc-metadata-list-item__list-content-item--subText")
                content = [item.text for item in content_items if item.text.strip()] if content_items else ["No additional info"]
                data.append({"Movie": title, "Technical specifications": label_elem.text, "": ", ".join(content)})
                
            except:
                continue
    except Exception as e:
        print(f"抓資料出錯：{e}")
    data = data[:-2]

    for i in range(1, len(data)):
        data[i]["Movie"] = ""

    return pd.DataFrame(data)



if __name__ == "__main__":
    driver = setup_driver()
    try:
        movies = get_movie_list(driver)
        for idx, movie in enumerate(movies):
            print(f"{idx+1}. {movie['title']}")

        movie_index = int(input("請輸入電影編號: ")) - 1
        if 0 <= movie_index < len(movies):
            selected_movie = movies[movie_index]
            print(f"正在查詢: {selected_movie['title']} 的詳細資訊...")
            movie_data = select_movie(driver, selected_movie)
            print(movie_data)

            # 儲存為 CSV
            # 清理檔名：只留下中英數字和底線
            safe_title = re.sub(r'[\\/*?:"<>|]', "_", selected_movie['title'])
            movie_data.to_csv(f"{safe_title}_data.csv", index=False)
            print(f"已將 {selected_movie['title']} 的數據存入 CSV 檔案")
        else:
            print("無效的電影編號！")
    finally:
        driver.quit()