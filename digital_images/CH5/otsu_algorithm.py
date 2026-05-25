import cv2

## 背景物體分離演算法

# 讀取圖片 , 轉成黑白
gray_image = cv2.imread("/Users/teddylai/nas_workplace_fetch/git_resources/side_project/NKUST_python_labs/digital_images/license_plate.bmp", 0)
cv2.imshow("license_plate.bmp",gray_image)
cv2.waitKey(0) # 等待按鍵
cv2.destroyAllWindows() # 關閉所有視窗

# 灰階轉純黑白
# 輸出形式 cv2.THRESH_BINARY
# 輸出閥值定義 cv2.THRESH_OTSU
# 方法 1: 使用 Otsu
th, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# 方法 2: 使用 Triangle
# th, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
# 方法 3: 使用 ADAPTIVE_THRESH (閥值是切成區塊的 , 每個區塊閥值不同 , 沒有固定的)
# binary_image = cv2.adaptiveThreshold(
#     gray_image,
#     255,
#     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#     cv2.THRESH_BINARY,
#     11, 2
# )

print(f"閥值={th}")

cv2.imshow("binary_imagep",binary_image)
cv2.waitKey(0) # 等待按鍵
cv2.destroyAllWindows() # 關閉所有視窗
