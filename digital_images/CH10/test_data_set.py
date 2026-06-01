import cv2
import os
from utils.pypath import load_PP

# import 函式庫 (看測試集物件)
from HOGs_SVM import MNIST as mnist


# add 訓練集
# MNIST("手寫數字","標籤答案")
os.chdir(load_PP("digital_images/HOGs_SVM/"))
mnist_train = mnist.MNIST("train-images.idx3-ubyte","train-labels.idx1-ubyte")


images, labels = mnist_train.getitem(40)

print(f"labels: {labels}")
cv2.imshow("images",images)
cv2.waitKey(0) # 等待按鍵
cv2.destroyAllWindows() # 關閉所有視窗