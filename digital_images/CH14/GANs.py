import os
import matplotlib
import torchvision
import torch
import matplotlib.pyplot as plt
# 引入自訂模組：MNIST 資料集解析器與專案路徑載入工具
import digital_images.HOGs_SVM.MNIST as mnist
from utils.pypath import load_PP

# 切換工作目錄到指定專案路徑，確保讀取 MNIST 權重與資料集時的相對路徑正確
os.chdir(load_PP("digital_images/HOGs_SVM/"))


def imshow(image_tensors):
    """顯示圖片，暫停 1 秒後自動關閉"""
    # 建立 8x8 grid
    grid_image = torchvision.utils.make_grid(image_tensors)

    # 顯示圖片
    plt.figure(figsize=(6, 6))
    plt.imshow(grid_image.permute(1, 2, 0))
    plt.axis("off")

    # 非阻塞顯示 + 暫停 1 秒
    plt.show(block=False)  # 重要：block=False
    plt.pause(1)  # 暫停 1 秒



# =====================================================================
# 1. 判別器模型定義 (Discriminator) - 採用修改版 LeNet 卷積神經網路
# =====================================================================
class Discriminator(torch.nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()

        # 二維卷積層 1：輸入單通道(灰階)，輸出 6 通道，特徵圖大小透過 Padding 補平
        # Input: [N, 1, 28, 28] -> Output: [N, 6, 28, 28]
        self.conv_1 = torch.nn.Conv2d(in_channels=1, out_channels=6,
                                      kernel_size=5, stride=1, padding=2, bias=False)

        # 二維卷積層 2：Input: [N, 6, 14, 14] (經過池化後) -> Output: [N, 16, 10, 10]
        self.conv_2 = torch.nn.Conv2d(in_channels=6, out_channels=16,
                                      kernel_size=5, stride=1, padding=0, bias=False)

        # 全連接層線性映射 (Fully Connected Layers)
        # 卷積與池化最終輸出的特徵圖大小為 16 通道 * 5x5 像素 = 400 維
        self.fc_1 = torch.nn.Linear(5 * 5 * 16, 120, bias=True)
        self.fc_2 = torch.nn.Linear(120, 84, bias=True)
        self.fc_3 = torch.nn.Linear(84, 1, bias=True)  # 最終輸出一個標量，代表是真圖的信心分數

        # 隨機失活層，防止判別器過擬合、實力過快碾壓生成器
        self.dropout = torch.nn.Dropout(0.4)

    def forward(self, x):
        """
        判別器前向傳播
        :param x: 輸入影像張量，Shape: [Batch_Size, 1, 28, 28]
        :return: 預測分數張量，Shape: [Batch_Size]
        """
        # [N, 1, 28, 28] -> 卷積 [N, 6, 28, 28] -> ReLU 激活
        x = torch.nn.functional.relu(self.conv_1(x))

        # 最大池化層下採樣：[N, 6, 28, 28] -> [N, 6, 14, 14]
        x = torch.nn.functional.max_pool2d(x, kernel_size=2)

        # [N, 6, 14, 14] -> 卷積 [N, 16, 10, 10] -> ReLU 激活
        x = torch.nn.functional.relu(self.conv_2(x))

        # 最大池化層下採樣：[N, 16, 10, 10] -> [N, 16, 5, 5]
        x = torch.nn.functional.max_pool2d(x, kernel_size=2)

        # 特徵圖拉直攤平 (Flatten)：[N, 16, 5, 5] -> [N, 400]
        x = x.view(-1, 16 * 5 * 5)

        # 全連接層 1 映射：[N, 400] -> [N, 120] -> ReLU
        x = torch.nn.functional.relu(self.fc_1(x))

        # 全連接層 2 映射：[N, 120] -> [N, 84] -> ReLU
        x = torch.nn.functional.relu(self.fc_2(x))

        # 全連接層 3 映射：[N, 84] -> [N, 1]
        x = self.fc_3(x)

        # 💥【關鍵數學設計】將 [Batch_Size, 1] 降維壓縮成一維張量 [Batch_Size]
        # 💡 注意：這裡最後沒有加 Sigmoid，是因為後續搭配的損失函數是 BCEWithLogitsLoss()，
        # 該損失函數內部已經自帶了高穩定性的 Sigmoid 計算，所以這裡輸出原始數值（Logits）即可。
        x = x.view(-1)

        return x


# =====================================================================
# 2. 生成器模型定義 (Generator) - 採用轉置卷積網路 (DCGAN 核心架構)
# =====================================================================
class Generator(torch.nn.Module):
    def __init__(self, in_dim):
        super(Generator, self).__init__()

        # 轉置卷積層 (ConvTranspose2d) 用於將低維度的特徵圖「上採樣/放大」成高維度影像
        # Layer 1: 輸入隨機噪點 [N, 100, 1, 1] -> 放大為 [N, 256, 7, 7]
        self.conv_1 = torch.nn.ConvTranspose2d(in_dim, 256, kernel_size=7, stride=1, padding=0, bias=False)

        # Layer 2: [N, 256, 7, 7] -> 放大為 [N, 128, 14, 14]
        self.conv_2 = torch.nn.ConvTranspose2d(256, 128, kernel_size=4, stride=2, padding=1, bias=False)

        # Layer 3: [N, 128, 14, 14] -> 放大為 [N, 64, 28, 28]
        self.conv_3 = torch.nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1, bias=False)

        # Layer 4: [N, 64, 28, 28] -> 調整通道數，輸出單通道假圖片 [N, 1, 28, 28]
        self.conv_4 = torch.nn.ConvTranspose2d(64, 1, kernel_size=3, stride=1, padding=1, bias=False)

        # 二維批歸一化 (Batch Normalization)，用來穩定深層卷積網路中的梯度傳導，防止模式崩潰
        self.bn_1 = torch.nn.BatchNorm2d(256)
        self.bn_2 = torch.nn.BatchNorm2d(128)
        self.bn_3 = torch.nn.BatchNorm2d(64)

    def forward(self, x):
        """
    生成器前向傳播
    :param x: 隨機噪點張量，Shape: [Batch_Size, 100, 1, 1]
    :return: 生成的偽造影像張量，Shape: [Batch_Size, 1, 28, 28]
    """
        # 第一層轉置卷積 -> 批歸一化 -> ReLU 激活
        x = torch.nn.functional.relu(self.bn_1(self.conv_1(x)))

        # 第二層轉置卷積 -> 批歸一化 -> ReLU 激活
        x = torch.nn.functional.relu(self.bn_2(self.conv_2(x)))

        # 第三層轉置卷積 -> 批歸一化 -> ReLU 激活
        x = torch.nn.functional.relu(self.bn_3(self.conv_3(x)))

        # 最終輸出層卷積 -> 透過 Sigmoid 將所有像素值壓制在 [0, 1] 區間，對應影像亮度
        x = torch.nn.functional.sigmoid(self.conv_4(x))

        return x


# =====================================================================
# 3. 超參數設定與環境初始化 (Hyper-parameters & Initialization)
# =====================================================================
n_epochs = 400  # 總訓練輪數
# MNIST 訓練集總共有 60,000 張 圖片
# 你設定的 batch_size = 64
# 所以理論上應該有 60000 ÷ 64 = 937.5
batch_size = 64  # 每個批次的樣本數

z_dim = 100  # 輸入隨機雜訊的維度 (隱空間 Latent Space 維度)
h_dim = 128  # 隱藏層維度（此腳本模型內暫未使用）

# 💥 實務經驗：判別器通常學得比生成器快，所以 D 的學習率設得比 G 低 (0.00005 vs 0.0002)，有助於動態平衡
D_learning_rate = 0.00005
G_learning_rate = 0.0002

# 載入 MNIST 訓練數據集並建立資料加載器 (DataLoader)
mnist_train = mnist.MNIST("train-images.idx3-ubyte", "train-labels.idx1-ubyte")
mnist_loader = torch.utils.data.DataLoader(dataset=mnist_train, batch_size=batch_size, shuffle=True, drop_last=True)

# 動態檢測跨平台硬體裝置
if torch.cuda.is_available():
    device = torch.device("cuda")  # NVIDIA GPU 加速
elif torch.backends.mps.is_available():
    device = torch.device("mps")  # Apple Silicon (M1/M2/M3) 晶片加速
else:
    device = torch.device("cpu")  # 備用方案：純 CPU 運算

# 實例化判別器與生成器，並推送至指定運算核心 (GPU / MPS / CPU)
D = Discriminator().to(device)
G = Generator(z_dim).to(device)

# 為兩個模型分別配置獨立的 Adam 優化器
D_optimizer = torch.optim.Adam(D.parameters(), lr=D_learning_rate)
G_optimizer = torch.optim.Adam(G.parameters(), lr=G_learning_rate)

# 預先建立好訓練時與 BCE 損失函數比對用的標籤答案板 (真影像為 1.0，假影像為 0.0)
ones_label = torch.ones(batch_size).to(device)
zeros_label = torch.zeros(batch_size).to(device)

# 採用帶有 Logits 的二分類交叉熵損失函數
# 內部自帶 Sigmoid 計算，具備極高的數值穩定性，能有效防止指數爆炸或 log(0) 噴錯
bce_loss = torch.nn.BCEWithLogitsLoss()

# 用於紀錄每個 Epoch 平均 Loss 的歷史看板
loss_history = []

# =====================================================================
# 4. 核心對抗訓練迴圈 (Adversarial Training Loop)
# =====================================================================
# 💡 【手動停止訓練的時機判斷】
# 同時滿足以下三個條件即可中斷訓練（直接 Ctrl+C）：
#   1. D 平均 Loss 穩定在 1.3863 附近（= ln(2)×2，代表 D 完全猜不準真假）
#   2. 圖片品質肉眼看起來清晰、像真實數字
#   3. 圖片多樣性足夠（64 張圖中 0~9 都有出現，沒有一堆長一樣的）
# ⚠️  注意：D loss = 1.3863 但圖片都長一樣 → Mode Collapse，不能停

for epoch in range(n_epochs):
    batch = 0
    D_total_loss = 0
    G_total_loss = 0

    for x_reals, y_labels in mnist_loader:
        # 在 Terminal 印出當前進度標籤 (例如 "0:140" 代表第 0 個 Epoch，第 140 個 Batch)
        print(f'\rEpoch:{epoch}, Batch:{batch}', end='')
        # 將真實的 MNIST 圖片推送至運算裝置
        x_reals = x_reals.to(device)

        # -----------------------------------------------------------------
        # 隨機採樣噪點 z (符合標準高斯分佈)，Shape: [64, 100, 1, 1]
        # 先透過生成器 G 製造出一批假照片，並使用 .detach() 截斷梯度傳導。
        # 這是因為在訓練判別器時，我們「不需要」去更新生成器 G 的網路權重。
        # -----------------------------------------------------------------
        z_noises = torch.randn(batch_size, z_dim, 1, 1).to(device)
        x_fakes = G(z_noises).detach()

        # -----------------------------------------------------------------
        # 【階段一：訓練判別器 D】
        # 策略：凍結生成器 G 的參數更新，專心活化並升級判別器 D 的辨識能力
        # -----------------------------------------------------------------
        for p in G.parameters(): p.requires_grad = False
        for p in D.parameters(): p.requires_grad = True

        # 正向傳播：讓 D 分別去猜真實影像與偽造影像的分數
        y_reals = D(x_reals)
        y_fakes = D(x_fakes)

        # 計算判別器總損耗：希望真實影像被猜成 1，偽造影像被猜成 0
        D_loss = bce_loss(y_reals, ones_label) + bce_loss(y_fakes, zeros_label)
        D_total_loss += D_loss.item()

        # 判別器反向傳播與參數權重更新
        D_optimizer.zero_grad()
        D_loss.backward()
        D_optimizer.step()

        # -----------------------------------------------------------------
        # 【階段二：訓練生成器 G】
        # 策略：轉而凍結判別器 D，活化生成器 G，試圖優化線條以欺騙 D
        # -----------------------------------------------------------------
        for p in D.parameters(): p.requires_grad = False
        for p in G.parameters(): p.requires_grad = True

        # 重新抽樣噪點，讓 G 生成全新的假影像（此處不加 detach，必須保留梯度鏈結）
        z_noises = torch.randn(batch_size, z_dim, 1, 1).to(device)
        x_fakes = G(z_noises)

        # 讓凍結中的 D 去審查這批新假圖
        y_fakes = D(x_fakes)

        # 計算生成器損耗：生成器最大的心願，就是逼判別器把這批假圖全部誤判為真貨（標籤 1）
        G_loss = bce_loss(y_fakes, ones_label)
        G_total_loss += G_loss.item()

        # 生成器反向傳播與參數權重更新
        G_optimizer.zero_grad()
        G_loss.backward()
        G_optimizer.step()

        # 累加 Batch 計數器
        batch = batch + 1

    # =====================================================================
    # 5. 輪次結束監控與影像視覺化 (Per-Epoch Diagnostics & Visualization)
    # =====================================================================
    # 計算此輪（Epoch）所有批次的平均對抗損益
    D_average_loss = D_total_loss / batch
    G_average_loss = G_total_loss / batch
    print(f"\n判別器 (D) 平均 Loss: {D_average_loss:.4f}")
    print(f"生成器 (G) 平均 Loss: {G_average_loss:.4f}")
    print(f"=== Epoch {epoch + 1}/{n_epochs} 完成 ===\n")

    loss_history.append((D_average_loss, G_average_loss))

    # 每隔 1 個輪次（Epoch），進行一次 AI 生產線抽查，彈出視窗展示生成圖片
    if (epoch + 1) % 1 == 0:
        # 固定使用一批隨機噪點來測試當前生成器的還原實力
        z_noises = torch.randn(batch_size, z_dim, 1, 1).to(device)
        x_fakes = G(z_noises)

        # 將產出的 64 張影像送入我們為 Mac 優化過的 imshow 函式進行展示
        imshow(x_fakes.detach().cpu())

# =====================================================================
# 6. 訓練完全結束：繪製 200 輪的對抗損耗收斂曲線 (Loss Curve Display)
# =====================================================================
print("\n訓練完成！正在編譯 200 輪的對抗損耗曲線...")

# 配置全新的 Matplotlib 畫布尺寸
plt.figure(figsize=(10, 5))

# 分別繪製判別器與生成器的損耗軌跡線
plt.plot(range(len(loss_history)), [x[0] for x in loss_history], label="D loss")
plt.plot(range(len(loss_history)), [x[1] for x in loss_history], label="G loss")

# 補上標準圖表元素
plt.xlabel("Epochs")
plt.ylabel("BCE Loss")
plt.title("GAN Training Loss History")
plt.legend()
plt.grid(True)

# 💡 [macOS 關鍵最後一小步]
# 強迫 Mac 彈出最後的損耗對抗收斂曲線視窗，看完整體戰況、將視窗關閉後，Python 腳本才會乾淨收尾
plt.show(block=True)
print("感謝使用，常駐記憶體與畫布視窗資源已全數安全釋放。")