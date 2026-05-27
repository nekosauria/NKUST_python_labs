import cv2
import numpy
import plt

# HOG 特徵設定（拿來做數字辨識）

# 輸入圖片大小
# 代表每張數字圖都是 28x28
winSize = (28,28)

# 一次分析多大的區塊
# 這裡等於整張圖一起分析
# blockSize 比 winSize 小的話
# 代表 HOG 會在整張圖裡「滑動視窗」去看不同區域

# ✔ 好處：
# 可以分開看數字的不同部位（上、下、左、右）
# 比較容易分辨 6 / 9 / 8 這種形狀差異

# ❌ 如果 blockSize = winSize
# 就只會看整張圖一次
# 沒有局部資訊，比較粗略

# 簡單講：
# 小 block → 看細節
# 大 block → 看整體
blockSize = (28,28)

# block 每次移動幾個 pixel
# (1,1) = 很密集地掃描
blockStride = (1,1)

# block 裡再切小格子
# HOG 會分析每格的線條方向
# e.g. 一個 28x28 大區塊
# 裡面切成 4 個 14x14 小格子
cellSize = (14,14)

# 線條方向分幾種角度 (向量)
# 9 以辨識數字來說是很常見的設定 (20度一個區間)
# HOG 通常只看 0~180 度
# 因為線條反方向其實長很像
# 例如：
# → 跟 ←
# 對 HOG 來說都是同一種線條
# 所以如果角度超過 180
# 就折回來
nbins = 9

# 建立 HOG descriptor
hog_descriptor = cv2.HOGDescriptor(
    winSize,
    blockSize,
    blockStride,
    cellSize,
    nbins
)


# 1. 預先建立一個大畫布：10 個數字，每個數字佔用 2 個子圖 (原圖 + 直方圖)
# 我們排列成 5 列 x 4 欄 (也就是 5 行，每行放 2 組圖)
rows, cols = 5, 2
fig, axes = plt.subplots(rows, cols * 2, figsize=(15, 12))
axes = axes.flatten()  # 把二維陣列攤平，方便用索引存取

# loading images
for idx in range(10):
    file_name = f"/Users/teddylai/nas_workplace_fetch/git_resources/side_project/NKUST_python_labs/digital_images/HOGs/digit_{idx}.bmp"

    # black & white （抓梯度效果較好）
    mat = cv2.imread(file_name,0)

    # --- HOG 特徵轉換開始 ---
    # 1. 計算 HOG (把圖片裡的「線條方向」抓出來)
    # 這裡把圖片丟進去，它會回傳一個充滿數字的「特徵矩陣」。
    # 這些數字代表了圖片裡每個區塊的邊緣方向資訊。
    hog = hog_descriptor.compute(mat)

    # 2. 拉平 (把多維度陣列變成一條線)
    # 原本的 HOG 格式可能是矩陣 (例如 2D 或 3D)，
    # 我們把它「壓扁」成一條長長的陣列，方便之後丟進機器學習模型 (像 SVM) 去訓練。
    hog = hog.flatten()

    # 3. 轉成浮點數 (確保數學精確度)
    # 將數字轉換成 32-bit 的浮點數 (float32)。
    # 這是為了讓運算速度變快，同時也是大多數 AI 函式庫 (如 Scikit-learn 或 OpenCV) 規定的格式。
    hog = hog.astype(numpy.float32)
    # --- 這樣這組 hog 數據就準備好可以拿去辨識數字了 ---

    # 2. 指定位置繪圖
    # 每一組數字佔用 2 個格子：一個顯示原圖，一個顯示直方圖
    img_ax = axes[idx * 2]
    hist_ax = axes[idx * 2 + 1]

    # 顯示原始數字圖片（灰階）
    img_ax.imshow(mat, cmap='gray')
    # 標題：顯示目前是哪個數字
    img_ax.set_title(f"Digit {idx}")
    # 不顯示座標軸（讓圖更乾淨）
    # img_ax.axis('off')

    # 顯示 HOG 特徵（其實是一串數值）
    # 用 bar chart 看每個方向的強度
    hist_ax.bar(range(len(hog)), hog)
    # 標題：顯示對應的 HOG index
    hist_ax.set_title(f"HOG {idx}")
    # 隱藏 x 軸刻度（不顯示 bin 細節）
    # 因為太細節，看了反而亂
    # hist_ax.set_xticks([])


# 在 HOG 直方圖中，Y 軸數值「越高」，代表該區塊影像在該方向上的「邊緣特徵越強烈」或「像素點分佈越密集」。
# 3. 調整排版並顯示
plt.tight_layout()
plt.draw()
plt.pause(0.001)  # 讓視窗更新
print("按下任意鍵繼續...")
plt.waitforbuttonpress()  # 這是 Matplotlib 的 waitKey，會等待鍵盤輸入
plt.close()  # 關閉視窗
