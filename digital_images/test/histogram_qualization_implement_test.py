# add import
import cv2
import time
import numpy

in_img = cv2.imread("/Users/teddylai/nas_workplace_fetch/school_achievements/NKUST/workplace/NKUST_python_labs/digital_images/cat.png",0)

in_hist=numpy.zeros(256,dtype=float)
print(in_hist)
print(in_hist.size)


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
numpy.set_printoptions(suppress=True, precision=6, linewidth=100)

print("--- 亮度百分比表 (NumPy 格式化) ---")
print(in_hist)