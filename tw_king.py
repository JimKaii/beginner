import requests 
import pandas as pd
from pprint import pprint
from bs4 import BeautifulSoup

url = "https://www.twking.cc/"
r = requests.get(url)
r.encoding = 'utf8' #避免亂碼
# print(len(r.text))
soup = BeautifulSoup(r.text, 'html.parser')



# soup.find_all('div', class_='booktop')
# booktops = soup.find_all('div', attrs={"class": "booktop"})
#     #sol.1
# for booktop in booktops:
#     tops = booktop.find_all('p')
#     top_type = tops[0].text
#     # print(top_type)
#     for top in tops[1:]:
#         top_book_name = top.a.text 
#         top_url = top.a.get('href')
         
        
# collection      
book_summarize = dict()
booktops = soup.find_all('div', attrs={"class": "booktop"})
for booktop in booktops:
    tops = booktop.find_all('p')
    top_type = tops[0].text
    # print(top_type)
    for top in tops[1:]:
        top_book_name = top.a.text.strip()# 小說名稱, 並清除前後空白
        top_url = top.a.get('href')
        if top_book_name in book_summarize:
                book_summarize[top_book_name]["count"] += 1
        else:
                book_summarize[top_book_name]={
                    "count": 1,
                    "herf": top_url
        }
# pprint(book_summarize)

# pprint(sorted
#        (book_summarize.items(), 
#         reverse=True, #降幕
#         key=lambda x:x[1]['count']))

sorted_booktop_summarize = sorted(
        book_summarize.items(), 
        reverse=True, 
        key=lambda x:x[1]['count'])


book_rows = list()
for book in sorted_booktop_summarize:
    book_name = book[0]
    book_count = book[1]['count']
    book_page_url = book[1]['herf']
    book_row = {
        'novel_name': book_name,
        'top_count': book_count,
        'novel_url': book_page_url
        }
    book_rows.append(book_row)



booktop_summarize_df = pd.DataFrame(book_rows)
booktop_summarize_df.to_csv('booktop.csv')


