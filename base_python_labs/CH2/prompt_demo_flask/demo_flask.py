from flask import Flask, render_template, request, send_from_directory
import cv2
import os
import re

app = Flask(__name__)

# 設定圖片路徑
IMG_PATH = "static/test.png"
OUTPUT_PATH = "static/output.png"


def parse_range(range_str):
    """將字串 '1:100, 1:200' 解析為 Python slice"""
    # 使用正規表達式抓取數字
    parts = re.findall(r'(\d+):(\d+)', range_str)
    if len(parts) == 2:
        y_slice = slice(int(parts[0][0]), int(parts[0][1]))
        x_slice = slice(int(parts[1][0]), int(parts[1][1]))
        return y_slice, x_slice
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    img_to_show = "test.png"  # 預設顯示原始圖片

    if request.method == 'POST':
        # 4. 取得前端輸入
        raw_range = request.form.get('range_input')  # 例如 1:100,1:200
        raw_color = request.form.get('color_input')  # 例如 255,155,50

        try:
            # 6. 修改圖片邏輯
            in_img = cv2.imread(IMG_PATH)

            # 解析範圍與顏色
            slices = parse_range(raw_range)
            color = [int(c.strip()) for c in raw_color.split(',')]

            if slices and in_img is not None:
                # 7. 修改對應顏色核心代碼
                in_img[slices[0], slices[1]] = color
                # 存檔供渲染，加上 cache 破解避免瀏覽器不更新
                cv2.imwrite(OUTPUT_PATH, in_img)
                img_to_show = "output.png"
        except Exception as e:
            print(f"Error processing image: {e}")

    return render_template('demo_html.html', display_image=img_to_show)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)