from chatgpt_example import chat_with_chatgpt
from datetime import date
import json

standard_format = {
        "出發點":"出發站名",
        "到達點":"到達站名 ",
        "出發時間":" YYYY/MM/DD ",
        "出發時辰":" H/S "       
}
today = date.today().strftime("%Y/%m/%d")

def asd_booking_infomation():
    print("Ask booking infomation")

    user_reponse = input("請輸入你的高鐵訂位資訊，出發點、抵達點、出發日期及時辰")
    system_prompt =f"""
    
        我想從回話的內容取得訂票資訊，資訊內容包括:出發點、抵達點、出發日期、出發時辰。
        今天是{today}
        請把資料整理成 python dictionary格式，例如:{standard_format}不包含其他內容

        """
    return chat_with_chatgpt(user_reponse, system_prompt)


def ask_missing_infomation(booking_info):
    # print("Ask missing infomation")
    
    missing_slots = [key for key, value in booking_info.items() if not value ]
    if not missing_slots:
        print("All slots are filled")
        return booking_info
    else:
        user_response = input(f"請補充您的訂位資訊，包含:{','.join(missing_slots)}")
        
        system_prompt = f"""
                將補充的訊息 {','.join(missing_slots)}
                和{(booking_info)}合併,今天是{today}
                並已python dictionary格式，
                例如{standard_format}，且不包含其他內容，
                若不知道就回空字串               
                
                """
        
        return chat_with_chatgpt(user_response, system_prompt)
    

def convert_number_become_chinese():
    return








    
if __name__ == '__main__':
    # Step 1
    booking_info = asd_booking_infomation()
    # Step 2
    booking_info = ask_missing_infomation(json.loads(booking_info.replace("'", "\"")))
    # Step 3

