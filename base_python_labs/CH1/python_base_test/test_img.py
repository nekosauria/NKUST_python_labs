import os
from PIL import Image

def main():
    file_path = '../../CH2/prompt_demo_flask/static/test.png'

    # 1. 檢查檔案是否存在
    if not os.path.exists(file_path):
        print(f"找不到檔案: {file_path}，請確認檔案已放在正確位置。")
        return

    # 2. 計算檔案大小
    # os.path.getsize 會回傳位元組 (Bytes)
    file_size_bytes = os.path.getsize(file_path)
    file_size_kb = file_size_bytes / 1024
    
    print(f"--- 檔案資訊 ---")
    print(f"檔名: {file_path}")
    print(f"大小: {file_size_bytes} Bytes ({file_size_kb:.2f} KB)")

    # 3. 將圖顯示在 macOS 畫面上
    try:
        # 開啟影像檔案
        with Image.open(file_path) as img:
            print("正在開啟圖片...")
            # .show() 會呼叫 macOS 內建的「預覽 (Preview)」程式來開啟圖片
            img.show()
    except Exception as e:
        print(f"開啟圖片時發生錯誤: {e}")

if __name__ == "__main__":
    main()