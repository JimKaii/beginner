import pandas as pd
import requests
from pprint import pprint
from bs4 import BeautifulSoup

#Step 1. 讀取主頁排行榜名單
book_tops = pd.read_csv('booktop.csv')
# print(book_tops.head(10))
book_top10s = book_tops.head(10)

last_chapters_titles = list()
last_chapters_urls = list()
num_last_chapters = list()
for book_top10 in book_top10s.iterrows():
    print(book_top10[1]['novel_name'], book_top10[1]['novel_url'])

# Step 2
page_url = book_top10[1]['novel_url']
r = requests.get(page_url)
r.encoding = 'utf8' #避免亂碼
page_soup = BeautifulSoup(r.text, 'html.parser')

#  取得所有章節的版面節點
chapter_wrapper = page_soup.find('div', attrs={'class': 'info-chapters flex flex-wrap'})

chapters = chapter_wrapper.find_all('a')
print(f"{book_top10[1]['novel_name']}, # of chapter :{len(chapters)}")
last_chapters= chapters[-1]
last_chapters_title = last_chapters.get('title')
last_chapters_url = last_chapters.get('herf')
print(f"last_chapter:{last_chapters_title}")
print(f"which at : {last_chapters_url}")
print()

#Step 3 :蒐集資訊
last_chapters_titles.append(last_chapters_title)
last_chapters_urls.append(last_chapters_url)
num_last_chapters.append(len(chapters))


book_top10s['chapter_numbers'] = num_last_chapters
book_top10s['last_chapter_url'] = last_chapters_titles
book_top10s['last_chapter_title'] = last_chapters_titles

book_top10s.to_csv("book_top10.csv")
 