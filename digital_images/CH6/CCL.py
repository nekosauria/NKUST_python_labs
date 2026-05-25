import cv2
import numpy as np

## 背景物體分離演算法
# THRESH_BINARY_INV = 黑白反相
gray_image = cv2.imread("/Users/teddylai/nas_workplace_fetch/git_resources/side_project/NKUST_python_labs/digital_images/license_plate.bmp", 0)
th, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# th, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_TRIANGLE)
# binary_image = cv2.adaptiveThreshold(
#     gray_image,
#     255,
#     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#     cv2.THRESH_BINARY,
#     11, 2
# )

print(f"閥值={th}")
cv2.imshow("binary_image",binary_image)
cv2.waitKey(0) # 等待按鍵
cv2.destroyAllWindows() # 關閉所有視窗

# label_mat = 標籤影像 , n_regions = 有幾個區塊
# 若是真正實作車牌辨識會寫小 function , 去除雜訊
n_regions, label_mat = cv2.connectedComponents(binary_image)
print(f'number of regions: {n_regions}')


# 建立「彩色輸出畫布」
display_mat = np.zeros((label_mat.shape[0], label_mat.shape[1], 3), dtype=np.uint8)
# 建立 color table & 每個 regions set color
color_plate = np.random.randint(0, 256, size=(n_regions, 3))
# paint the background (region 0) with white color
# 定義背景圖片顏色
color_plate[0] = 255

# print image
rows = label_mat.shape[0]
cols = label_mat.shape[1]
for r in range(0, rows):
    for c in range(0, cols):
        label = label_mat[r, c]
        color = color_plate[label] # get the color
        display_mat[r, c] = color # paint the point [r,c]

cv2.imshow("display_mat",display_mat)
cv2.waitKey(0) # 等待按鍵
cv2.destroyAllWindows() # 關閉所有視窗
