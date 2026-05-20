請編寫一個Python flask 程式給初學Python Coding的人當學習範例

該程式規格如下
<spec>
1.python3 本地環境規格為 : Python 3.11.9 , pip 26.1
2.生成一個簡單的 flask demo_flask.py 檔案與 html檔案 demo_html.html
3.demo_html 中間有一張圖片 test.png , 此圖片為flask渲染的
4.demo_html 上面有兩個個輸入區塊可以輸入一個 opencv 的python 格式指令 還有一個送出按鈕可以跟 flask 溝通
5.輸入參數為 opencv 的格式可以參考以下代碼
range=[1:1000,1:2000]
color=[255,155,50]
6.demo_flask.py 收到這個參數幫這個圖片那個範圍的 pixel 修改成對應顏色
7.修改對應顏色核心代碼請參考以下代碼
import cv2
in_img = cv2.imread("test.png")
in_img[1:1000,1:2000] = [255,155,50]
</spec>