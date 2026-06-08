import torch
import cv2
from torch.utils.data import Dataset
import digital_images.HOGs_SVM.MNIST as mnist
import numpy

class DatasetImpl(Dataset):
    # 樣本資料（答案）：由 6 個 (x, y) 座標組成的 NumPy 陣列
    def __init__(self, images_file,labels_file):
        # create dataset
        self.mnist_dataset = mnist.MNIST(images_file,labels_file)

        # ==========================================
        # 2. 初始化 HOG 特徵提取器
        # ==========================================
        # 設定與訓練模型時「完全相同」的 HOG 參數（若參數不同，提取出的特徵數量會不吻合）
        winSize = (28, 28)  # 偵測視窗大小（剛好是 MNIST 圖片大小）
        blockSize = (28, 28)  # 區塊大小
        blockStride = (1, 1)  # 區塊滑動步長
        cellSize = (14, 14)  # 細胞單元大小
        nbins = 9  # 梯度方向的統計區間數（0~180度分成9個分箱）

        # 建立 OpenCV 的 HOG 處理器，它負責把「視覺圖片」轉化為「幾何邊緣特徵」
        self.HOG = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)

    def __len__(self):
        return len(self.mnist_dataset)

    def __getitem__(self, idx):
        # 從測試集中依序取出第 idx 張圖片與它真實的數字標籤
        image, label = self.mnist_dataset.getitem(idx)

        # 【特徵提取】計算這張測試圖片的 HOG 特徵（會產生一個一維的特徵向量，長度為 36）
        hog = self.HOG.compute(image)

        # 【維度轉換】轉換指定格式
        hog = hog.reshape(-1)

        # 將資料型態轉換為符合 OpenCV 要求的 32位元浮點數 (float32)
        hog = hog.astype(numpy.float32)

        # change hog to tensor type
        hog = torch.tensor(hog)
        label = torch.tensor(label, dtype=torch.long)

        return hog, label


class NNModelImpl(torch.nn.Module):

    # 兩層 train 出來的 .pth size = 8KB
    # 準確度約為: 90.36%

    # def __init__(self):
    #     super(ModelImpl, self).__init__()
    #
    #     # 層數可自行調整
    #     # 隱藏層
    #     # 第一層：輸入 36 維，輸出 20 維
    #     # input-hidden layer: fully connected layer: (36-->20)
    #     self.fc_1 = torch.nn.Linear(36, 20, bias=True)
    #
    #     # 輸出層
    #     # hidden-output layer: fully connected layer (20-->10)
    #     # 第二層：輸入必須是 20 維（必須等於上一層的輸出！），輸出 10 維
    #     self.fc_2 = torch.nn.Linear(20, 10, bias=True)
    #
    #
    # def forward(self, x):
    #     # 隱藏層跑激活函數 (本例只有一層)
    #     x = torch.nn.functional.relu(self.fc_1(x))
    #     # 跑輸出層 (不一定要激活函數)
    #     y =  self.fc_2(x)
    #     return y

# ------------------------------------------------------------------

    # 四層 train 出來的 .pth size = 24kB
    # 準確度約為: 93.87%
    # 注意訓練,測試,跑真實案例 時間都會相應拉長！

    def __init__(self):
        super(NNModelImpl, self).__init__()

        # === 隱藏層 1 ===
        # 輸入 36 維 (HOG 特徵)，我們把它放大到 64 維，讓模型有更多空間寬度去拆解特徵
        self.fc_1 = torch.nn.Linear(36, 64, bias=True)

        # === 隱藏層 2 ===
        # 輸入必須是上一層的輸出 64，這次我們把它收攏到 32 維
        self.fc_2 = torch.nn.Linear(64, 32, bias=True)

        # === 隱藏層 3 ===
        # 輸入必須是 32，再收攏到 16 維
        self.fc_3 = torch.nn.Linear(32, 16, bias=True)

        # === 輸出層 ===
        # 輸入必須是 16，最終輸出 10 維（對應 0~9 個數字的機率）
        self.fc_4 = torch.nn.Linear(16, 10, bias=True)

    def forward(self, x):
        # 每一層線性轉換後，都要緊跟著一個非線性激活函數 (ReLU)
        x = torch.nn.functional.relu(self.fc_1(x))
        x = torch.nn.functional.relu(self.fc_2(x))
        x = torch.nn.functional.relu(self.fc_3(x))

        # 最後一層輸出層「不需要」加 ReLU，直接送出原始預測值 (Logits)
        y = self.fc_4(x)
        return y



class LeNetImpl(torch.nn.Module):

    def __init__(self):
        super(LeNetImpl, self).__init__()

        # 卷積 + pooling 激活函數
        # padding = 對齊格式至規定 (e.g. 灰階影像 28*28*1 -> 32*32*1 = +0 黑邊)
        self.conv_1 = torch.nn.Conv2d(
            in_channels=1, out_channels=6,
            kernel_size=5, stride=1, padding=2, bias=True)

        self.maxpool_1 = torch.nn.MaxPool2d(kernel_size=2)

        self.conv_2 = torch.nn.Conv2d(
            in_channels=6, out_channels=16,
            kernel_size=5, stride=1, padding=0, bias=True)

        self.maxpool_2 = torch.nn.MaxPool2d(kernel_size=2)

        # Fully Connected Layer
        # 這組數字完全是當年 Yann LeCun 在 1998 年發表 LeNet-5 論文時，原封不動的官方實作數字！
        # 唯一的小差別只有當年的第一層輸入是 32，而現代因為 MNIST 數據集開源後被標準化成 28，
        # 大家用 PyTorch 重寫時，通常會在第一層加上 padding=2 把它墊回 32，
        # 好讓後面的 120 -> 84 -> 10 可以完美對齊論文。
        self.fc1 = torch.nn.Linear(in_features=5 * 5 * 16, out_features=120, bias=True)
        self.fc2 = torch.nn.Linear(in_features=120, out_features=84, bias=True)
        self.fc3 = torch.nn.Linear(in_features=84, out_features=10, bias=True)

    def  forward(self,  x):
        # 訓練 LeNet
        x  =  torch.nn.functional.relu(self.conv_1(x))
        x  =  self.maxpool_1(x)
        x  =  torch.nn.functional.relu(self.conv_2(x))
        x  =  self.maxpool_2(x)

        # flatten 攤平參數
        x = x.view(-1, 5*5*16)
        x = torch.nn.functional.relu(self.fc1(x))
        x = torch.nn.functional.relu(self.fc2(x))
        y = self.fc3(x)
        return y
