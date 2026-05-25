# OpenCV 影像二值化（Thresholding）演算法選擇指南

## 1. Thresholding 演算法總覽

| 演算法 | 方法 | 適合場景 |
| :--- | :--- | :--- |
| **`cv2.THRESH_BINARY`** | 全域固定閾值（Global Fixed Threshold） | 高對比、光線穩定的環境 |
| **`cv2.THRESH_OTSU`** | 全域自動閾值（Global Automatic Threshold） | 直方圖呈現雙峰分佈（前景與背景明顯分離）的影像 |
| **`cv2.THRESH_TRIANGLE`** | 全域自動閾值（Global Automatic Threshold） | 只有單一主要峰值，或前景物件非常小的影像 |
| **`cv2.ADAPTIVE_THRESH`** | 區域自適應閾值（Local Adaptive Threshold） | 光線不均、陰影或背景亮度變化大的影像 |

---

## 2. 建議流程邏輯（Pipeline Strategy）

為了在生產環境中（例如 Flask + OpenCV 專案）獲得穩定結果，建議依照以下決策階層進行。

---

### Step 1：前處理（Pre-processing）

*在進行 thresholding 之前，先降低雜訊以避免雜點與邊界錯誤。*

```python
# 使用 GaussianBlur 平滑感測器雜訊
blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)