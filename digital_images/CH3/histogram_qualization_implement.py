# add import
import cv2
import time
import numpy
import plt

# show test images
# 讀取影像 show 灰階
#in_img = cv2.imread("/Users/teddylai/nas_workplace_fetch/git_resources/side_project/NKUST_python_labs/digital_images/cat.png",0)
in_img = cv2.imread("/Users/teddylai/nas_workplace_fetch/git_resources/side_project/NKUST_python_labs/digital_images/cat.png",0)

'''
# cv2 套件實作
# 執行直方圖均衡化
equ = cv2.equalizeHist(in_img)
# 顯示結果
cv2.imshow('Result', numpy.hstack((in_img, equ))) # 左圖原圖，右圖均衡化後
print("提示: 請按 enter 鍵關閉圖片視窗以繼續執行後續代碼...")
cv2.waitKey(0)
cv2.destroyAllWindows() # 關閉所有視窗
'''


# 手動實作
#########################  Step 1: Compute the histogram of input image  #########################
# 定義一個亮度表 0~256 個 , 每個值初始化為 0
in_hist=numpy.zeros(256,dtype=float)

# 算圖片 pixel size
# 直 row size
rows = in_img.shape[0]
# 橫 column size
cols = in_img.shape[1]

# for each black-white pixel
for r in range(rows):
  for c in range(cols):
    #每個 pixel 灰階拿出來存到亮度表內
    gray_value=in_img[r,c]
    # 把灰階表對應統計數字+1 # in_hist[gray_value] default = 0
    in_hist[gray_value] = in_hist[gray_value]+1


# 每個灰階表除 rows*column 得到各個亮度對應全部 pixel 百分比
for j in range(in_hist.size):
    in_hist[j] = in_hist[j] / (rows*cols)


# 把直方圖算法的函數曲線畫一個直方圖出來 f()
plt.bar(range(256),in_hist )
plt.show()



#########################  Step 2: Compute the transformation function  #########################
# 畫轉換函數曲線
T = numpy.zeros(256,dtype=int)

# acc_pr 代表數學中的累加符號
acc_pr=0.0

# 跑一個迴圈把每個 array index[x] 的 0 都存成一個值 , 最後一個值是100
for x in range(T.size):
    acc_pr = acc_pr + in_hist[x]
# 轉顆粒度為最近似整數值
    T[x] = int(255.0 * acc_pr)

print(T)

# 把 T[x] 這個 array 照順序畫出圖來 , 就可以得到轉換函數圖
plt.title('Transfer Function T')
plt.xlabel('input val')
plt.ylabel('output val')
# 'r' = 藍色的圖
plt.plot(range(256),T,'r')
plt.show()



#########################  Transform the value of each pixel   #########################
# create an output image
# 輸出格式為 numpy.uint8 = 8bit , 用8bit可以避免整數 range 超過255 , 且節省資源
# numpy浮點數可使用 float or  numpy.float64 -> 輸入 float numpy 會自動轉換為 numpy.float64
# 輸出一個空白的 image with same size
out_img = numpy.zeros((rows, cols) ,dtype=numpy.uint8)

# 改變原圖的每一個像素為新的像素 , 並輸出到新 image
for o in range(rows):
    for p in range(cols):
        out_img[o][p] = T[(in_img[o,p] )]


cv2.imshow('Result', numpy.hstack((in_img, out_img))) # 左圖原圖，右圖均衡化後
print("提示: 請按 enter 鍵關閉圖片視窗以繼續執行後續代碼...")
cv2.waitKey(0)
cv2.destroyAllWindows() # 關閉所有視窗



