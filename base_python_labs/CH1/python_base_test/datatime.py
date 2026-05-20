# -*- coding: utf-8 -*-
"""
Python 初學者範例：datetime 與時區處理
環境需求：Python 3.11.9+
"""

from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+ 引入，專門處理時區


def datetime_learning_demo():
    # 1. 設定時區為 Taipei (UTC+8)
    # macOS 內建有 IANA 時區資料庫，ZoneInfo 會自動讀取 "Asia/Taipei"
    taipei_tz = ZoneInfo("Asia/Taipei")

    # 2. 取得目前時間並帶入時區資訊
    # 這是「具備時區意識」(Aware) 的時間物件，比單純的 datetime.now() 更嚴謹
    now_in_taipei = datetime.now(taipei_tz)

    # 3. 定義台灣常用的輸出格式 (例如：2026-05-05 14:30:05)
    # %Y: 四位年份, %m: 月份, %d: 日期, %H: 24小時制, %M: 分鐘, %S: 秒數
    common_format = "%Y-%m-%d %H:%M:%S"

    # 將時間物件轉為格式化字串 (String Format Time)
    formatted_time = now_in_taipei.strftime(common_format)

    # 4. 在 Console 印出結果
    print("--- Python Datetime 學習範例 ---")
    print(f"目前台北時間：{formatted_time}")
    print(f"時區資訊：{now_in_taipei.tzinfo}")
    print("--------------------------------")

    """
    【進階學習：strftime 常用格式註解】
    如果你需要不同的輸出風格，可以替換 strftime 括號內的代碼：

    1. 台灣慣用中文格式：
       now.strftime("%Y年%m月%d日 %H時%M分") 
       -> 2026年05月05日 14時30分

    2. 12小時制 (帶 AM/PM)：
       now.strftime("%Y/%m/%d %I:%M %p") 
       -> 2026/05/05 02:30 PM

    3. 僅日期：
       now.strftime("%Y/%m/%d") 
       -> 2026/05/05

    4. 星期幾：
       now.strftime("%A") -> Tuesday (全稱)
       now.strftime("%a") -> Tue (簡稱)

    5. 檔案名稱常用格式 (不含特殊字元，適合存檔用)：
       now.strftime("%Y%m%d_%H%M%S") 
       -> 20260505_143005
    """


if __name__ == "__main__":
    datetime_learning_demo()