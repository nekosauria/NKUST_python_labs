# add import
import cv2
import time

# show test images
# 若沒有轉檔,直接改檔名 , 編碼器會看 image content header 切換編碼 type
#in_img = cv2.imread("/Users/teddylai/nas_workplace_fetch/git_resources/side_project/NKUST_python_labs/digital_images/cat.bmp")
in_img = cv2.imread("/Users/teddylai/nas_workplace_fetch/git_resources/side_project/NKUST_python_labs/digital_images/cat.png")
cv2.imshow("Original Image", in_img)
print("提示: 請按 enter 鍵關閉圖片視窗以繼續執行後續代碼...")
cv2.waitKey(0) # 等待按鍵
cv2.destroyAllWindows() # 關閉所有視窗


## 取得像素

# 確認像素顏色
p_value = in_img[1000,2000]
print(f"color={p_value}") ## 是抓到的那個像素點的 value


# 更換 block color
#  切片更換顏色與計算時間
start_time = time.time()

#in_img[1:1000,1:2000] = [255,155,50]
#in_img[1:1000,1:2000] = 255 # white
#colab.cv2_imshow(in_img)

end_time = time.time()    # 紀錄結束時間
print(f"執行時間: {end_time - start_time:.6f} 秒")
# cpu 執行時間: 0.017337 秒 & 1.339709
# t4 gpu 執行時間: 0.015658 秒 & 1.189957


# read a block
b_value = in_img[1000:1005, 2000:2005]

def print_pixel_table(area, start_y, start_x):
    height, width, _ = area.shape

    # 印出表頭 (X 座標)
    header = "Y and X |" + "".join([f"      {start_x + x:^10}      |" for x in range(width)])
    print(header)
    print("-" * len(header))

    # 逐行印出像素
    for y in range(height):
        row_str = f"{start_y + y:<5} |"
        for x in range(width):
            b, g, r = area[y, x]
            # 格式化成 (B:xxx, G:xxx, R:xxx)
            pixel_str = f"(B:{b:>3}, G:{g:>3}, R:{r:>3})"
            row_str += f" {pixel_str} |"
        print(row_str)

# 執行列印 (傳入起始座標以便標記)
print_pixel_table(b_value, 1000, 2000)