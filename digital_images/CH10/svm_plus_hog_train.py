import cv2
import os
import numpy

# 匯入自定義的工具函式與自製的 MNIST 讀取類別
from utils.pypath import load_PP
from digital_images.HOGs_SVM import MNIST as mnist

# ==========================================
# 1. 環境準備與資料載入
# ==========================================

# 確保程式的工作目錄切換到資料檔案所在的資料夾
os.chdir(load_PP("digital_images/HOGs_SVM/"))

# 實例化 MNIST 類別，讀取手寫數字訓練集圖片與標籤答案
mnist_train = mnist.MNIST("train-images.idx3-ubyte", "train-labels.idx1-ubyte")

# 獲取訓練集資料的總筆數
n_train = len(mnist_train)
print(f"n_train={n_train}")  # 修正原本印出物件的 bug，改印出數量

# ==========================================
# 2. 建立特徵與標籤的容器（準備餵給 SVM 的資料格式）
# ==========================================
# 創建一個空矩陣來存放所有圖片的 HOG 特徵。每張圖片會被 HOG 轉成 36 個特徵數值
train_image_mat = numpy.zeros((n_train, 36), dtype=numpy.float32)
# 創建一個空陣列來存放對應的正確答案（標籤）
train_image_labels = numpy.zeros(n_train, dtype=numpy.int32)

# ==========================================
# 3. 初始化 HOG 特徵提取器
# ==========================================
# 設定 HOG 的參數（視窗大小、區塊大小、細胞單元大小、梯度方向數量）
winSize = (28, 28)
blockSize = (28, 28)
blockStride = (1, 1)
cellSize = (14, 14)
nbins = 9
# 建立 OpenCV 的 HOG 處理器，它負責把「視覺圖片」轉化為「幾何邊緣特徵」
HOG = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)

# ==========================================
# 4. 特徵提取迴圈（HOG 登場）
# ==========================================
for i in range(n_train):
    # 從讀取器中取出一張圖片與它對應的數字標籤
    image, label = mnist_train.getitem(i)

    # 【核心步驟】利用 HOG 計算這張圖片的梯度直方圖特徵（降維、擷取邊緣線條）
    a_hog = HOG.compute(image)
    a_hog = a_hog.astype(numpy.float32)

    # 將計算出來的 36 個特徵值存入矩陣的第 i 列
    train_image_mat[i] = a_hog
    # 將正確答案存入標籤陣列
    train_image_labels[i] = label

# ==========================================
# 5. 建立與設定 SVM 分類器（大腦訓練）
# ==========================================
# 建立 OpenCV 的支持向量機 (SVM) 模型
svm = cv2.ml.SVM_create()
# 設定 SVM 類型為 C-SVC（用於多分類任務）
svm.setType(cv2.ml.SVM_C_SVC)
# 設定核函數為線性核 (Linear Kernel)，適合特徵已經被 HOG 很好分離的資料
svm.setKernel(cv2.ml.SVM_LINEAR)
# 設定訓練終止條件：最大迭代 10000 次，或誤差小於 1e-6 時停止運算
svm.setTermCriteria((cv2.TERM_CRITERIA_MAX_ITER, 10000, 1e-6))

# ==========================================
# 6. 開始訓練模型
# ==========================================
# 【最終結合】把 HOG 提取出的特徵矩陣 (ROW_SAMPLE 代表一列是一筆資料)
# 與正確答案丟給 SVM。SVM 會開始尋找最優公式，學會如何「看特徵認數字」。
svm.train(train_image_mat, cv2.ml.ROW_SAMPLE, train_image_labels)

# ==========================================
# 7. 儲存 SVM 模型至 XML 檔案
# ==========================================
# 定義你想儲存的 XML 檔案名稱（會直接存在目前 os.chdir 指定的資料夾下）
xml_filename = "svm_mnist_model.xml"

# 呼叫 save 函式進行儲存
svm.save(xml_filename)
print(f"成功將模型儲存至：{os.path.join(os.getcwd(), xml_filename)}")