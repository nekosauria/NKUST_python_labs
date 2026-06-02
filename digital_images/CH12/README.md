# 📊 以線性回歸為例：Mini-Batch + Epochs 模型訓練流程模擬

本範例用線性回歸（Linear Regression）說明機器學習模型在訓練階段中，如何透過 **Mini-batch Gradient Descent** 與 **Epochs** 進行參數更新。

---

## 🧠 基本概念

### 1️⃣ Epoch
- 代表模型「完整看過一遍訓練資料」
- 每一個 epoch 都會讓模型參數更新多次（取決於 batch 數量）

---

### 2️⃣ Mini-batch
- 將完整資料集切成小批次（batch）
- 每次只用一小部分資料計算梯度並更新參數

常見設定：
- batch size = 16 / 32 / 64 / 128

---

### 3️⃣ Gradient Descent（梯度下降）
用來更新模型參數：

\[
w := w - \eta \frac{\partial J(w)}{\partial w}
\]

其中：
- \( w \)：模型權重
- \( \eta \)：learning rate
- \( J(w) \)：損失函數

---

## 📉 訓練行為觀察

| 階段 | loss 行為 | 模型狀態 |
|------|----------|----------|
| Epoch 1 | 高且震盪 | 尚未收斂 |
| 中期 | 下降但波動 | 學習中 |
| 後期 | 穩定下降 | 接近收斂 |

---

## 🧩 核心直覺

- Epoch = 看完一輪資料
- Mini-batch = 一次學一小段
- Gradient = 修正方向
- Training = 不斷微調參數

---

## ⚙️ 總結

Mini-batch 線性回歸訓練的本質：

> 透過多次小幅度參數更新，逐步逼近 loss 最小值的最佳解。