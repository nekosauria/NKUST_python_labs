import cv2
import os
import numpy

# 匯入自定義的工具函式與自製的 MNIST 讀取類別
from utils.pypath import load_PP
from digital_images.HOGs_SVM import MNIST as mnist

# ==========================================
# 1. 環境準備與模型/資料載入
# ==========================================
os.chdir(load_PP("digital_images/HOGs_SVM/"))

# 載入先前訓練好並儲存成 XML 的 SVM 模型（讀取訓練好的大腦）
svm = cv2.ml.SVM_load("svm_mnist_model.xml")

# 實例化 MNIST 類別，讀取測試集圖片（1萬張未見過的手寫數字）與對應的標籤答案
mnist_test = mnist.MNIST("t10k-images.idx3-ubyte", "t10k-labels.idx1-ubyte")

# 獲取測試集資料的總筆數（應該是 10000 筆）
n_test = len(mnist_test)

# 初始化計數器：用來統計預測正確與錯誤的次數
n_correct = 0
n_wrong = 0

# ==========================================
# 2. 初始化 HOG 特徵提取器
# ==========================================
# 設定與訓練模型時「完全相同」的 HOG 參數（若參數不同，提取出的特徵數量會不吻合）
winSize = (28, 28)      # 偵測視窗大小（剛好是 MNIST 圖片大小）
blockSize = (28, 28)    # 區塊大小
blockStride = (1, 1)    # 區塊滑動步長
cellSize = (14, 14)     # 細胞單元大小
nbins = 9               # 梯度方向的統計區間數（0~180度分成9個分箱）

# 建立 OpenCV 的 HOG 處理器，它負責把「視覺圖片」轉化為「幾何邊緣特徵」
HOG = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)

print("開始測試模型準確度...")
# ==========================================
# 3. 測試集預測迴圈
# ==========================================
for idx in range(n_test):
    # 從測試集中依序取出第 idx 張圖片與它真實的數字標籤
    image, label = mnist_test.getitem(idx)

    # 【特徵提取】計算這張測試圖片的 HOG 特徵（會產生一個一維的特徵向量，長度為 36）
    a_hog = HOG.compute(image)

    # 【維度轉換】將一維陣列轉換為二維矩陣（形狀由 (36,) 變成 (1, 36)）
    # 因為 OpenCV SVM 的 predict 規定輸入格式必須是「列矩陣」（每列代表一筆資料）
    # 註：使用 a_hog.reshape((1, -1)) 效果一樣，且更具彈性
    a_hog = a_hog.reshape((1, 36))

    # 將資料型態轉換為符合 OpenCV 要求的 32位元浮點數 (float32)
    a_hog = a_hog.astype(numpy.float32)

    # 【大腦預測】將特徵矩陣餵給 SVM 模型進行預測
    result = svm.predict(a_hog)

    # 【結果解析】從 OpenCV 回傳的繁複結構中（通常是元組），
    # 利用 .item() 拔出唯一的預測數值，並轉換成標準的 Python 整數
    result = int(result[1].item())

    # 【統計準確率】比對模型的預測結果與真實標籤是否一致
    if result == label:
        n_correct += 1  # 猜對了，正確數加 1
    else:
        n_wrong += 1  # 猜錯了，錯誤數加 1

# ==========================================
# 4. 顯示最终測試結果
# ==========================================
# 計算最終預測的準確百分比
accuracy = n_correct / n_test * 100

print("---------------------------------")
print(f"正確預測數 (n_correct) = {n_correct}")
print(f"總測試張數 (n_test)    = {n_test}")
print(f"最終準確度 (accuracy)  = {accuracy:.2f} %")