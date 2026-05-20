# data_frame 名詞解釋

# --- 資料結構組成 (The Anatomy of DataFrame) ---

df.columns  # 橫向標籤：定義資料的欄位名稱（類似資料庫的 Schema）。
            # 範例：Index(['name', 'age', 'dept'], dtype='object')

df.index    # 縱向標籤：資料的列索引（類似 Primary Key），定義每一列的身分。
            # 範例：RangeIndex(start=0, stop=100, step=1)

df.values   # 核心數據：去除標籤後的純資料陣列（底層為 NumPy 矩陣）。
            # 範例：以二維陣列形式回傳 [[ 'Teddy', 31, 'DBA' ], ... ]


# --- 快速檢視指令 (Quick Inspection) ---

df.head(n)  # 讀取前 n 筆資料：預設為 5，用於快速確認資料匯入格式是否正確。
            # 註解：類似 Linux 的 head 指令，避免一次讀取大檔案造成記憶體溢位。

df.tail(n)  # 讀取最後 n 筆資料：常用於檢查時間序列資料是否更新到最新日期。
            # 註解：類似 Linux 的 tail 指令，適合觀察檔案末端的日誌紀錄。

df.info()   # 顯示硬體級資訊：包含各欄位型態、非空值數量與記憶體消耗。
            # 註解：運維人員必備，可藉此判斷是否需優化資料型別以節省 RAM。

df.describe() # 生成敘述性統計：自動計算平均值、標準差、最大最小值與四分位數。
              # 註解：僅針對數值欄位運算，可快速抓出資料中的異常離群值 (Outliers)。

# --- loc索引器 ---

DataFrame物件的loc索引器是使用標籤索引來
選取資料，iloc索引器是使用位置索引，其操作
方式就是切割運算子，如下所示：

e.g. 取得第四列
print(df.iloc[3]) # 第 4 筆

e.g. 取得一個矩陣
print(df.iloc[3:5, 1:3]) # 切割
'''
