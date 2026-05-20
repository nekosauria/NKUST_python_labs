# 🧠 Python AI / Data Stack 簡易總結

這五個套件是 AI / ML / CV 工程最常見的基礎工具，各自負責不同層級。

---

# 🔢 NumPy
- 核心：數值運算 / matrix / tensor
- 角色：所有 AI 計算基礎
- 重點：`ndarray`

👉 一句話：AI 的數學底層

---

# 📊 Pandas
- 核心：表格資料（DataFrame）
- 角色：資料清理 / feature engineering
- 常見：CSV / Excel / log

👉 一句話：資料整理工具

---

# 🖼 OpenCV
- 核心：影像處理
- 功能：resize / crop / filter / video
- 特點：C++ 高效能底層

👉 一句話：影像處理引擎

---

# 🖼 PIL (Pillow)
- 核心：影像 IO
- 功能：讀圖 / 存圖 / format conversion
- 特點：簡單輕量

👉 一句話：影像讀寫工具

---

# 🧠 PyTorch
- 核心：深度學習框架
- 功能：tensor / training / inference / GPU
- 用途：CNN / LLM / diffusion

👉 一句話：AI 模型核心引擎

---

# 🔁 關係總覽

```text
Pandas → 表格資料
PIL / OpenCV → 影像處理
        ↓
      NumPy → 數值核心
        ↓
     PyTorch → AI 模型
```

```text
資料 (Pandas / Image)
        ↓
前處理 (NumPy / OpenCV / PIL)
        ↓
模型 (PyTorch)
        ↓
輸出結果
```