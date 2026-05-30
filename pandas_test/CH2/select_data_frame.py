import pandas as pd

data_path = "/Users/teddylai/nas_workplace_fetch/git_resources/side_project/NKUST_python_labs/pandas_test/products.csv"

df = pd.read_csv(data_path, encoding="utf8")

# head()函數顯示前幾筆記錄，預設是5筆，如下所示：
print(df.head())
print(df.head(3))

# tail()函數顯示最後幾筆記錄，預設也是5筆，如下所示
# print(df.tail())
# print(df.tail(3))

# 改 columns 別名
df.columns = ["id", "type", "name", "price"]
print(df.head(3))

# get csv info
print(df.index) # RangeIndex(start=0, stop=11, step=1)
print(df.columns) # Index(['index', '商店', '分類', '價格'], dtype='str')
print(df.values)

# print("資料數= ", len(df)) # 資料數=  11
# print("形狀= ", df.shape) # 形狀=  (11, 4)

# df.info()
# <class 'pandas.DataFrame'>
# RangeIndex: 11 entries, 0 to 10
# Data columns (total 4 columns):
#  #   Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   index   11 non-null     str
#  1   商店      11 non-null     str
#  2   分類      11 non-null     str
#  3   價格      11 non-null     float64
# dtypes: float64(1), str(3)
# memory usage: 484.0 bytes

# for index, row in df.iterrows() :
#     print(index, row["id"], row["type"], row["name"], row["price"])

# 更改 ＆ reset index
# df2 = df.set_index("分類")
# print(df2.head())
# df3 = df2.reset_index()
# print(df3.head())

# 分類 with 多重索引
# df2 = df.set_index(["分類", "商店"])
# df2.sort_index(ascending=False, inplace=True)
# print(df2)

# 此處範例都是匯入products.csv檔案建立DataFrame
# 物件df，並且更改欄位標籤成為英文，和自訂索引
# 清單"A"~"F"，如下所示
# 補齊到 11 個元素，對應 11 筆資料
ordinals = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
df.index = ordinals
# print(df)

# print column with name
# print(df["price"].head(3))
# print(df.price.head(3))
# print(df[["type","name"]].head(3))

# print with index
# print(df[0:3]) # 不含 3
# print(df["C":"E"]) # 含 "E"

# loc 標籤索引索引器, 選取資料 (Label-based Location)
# 查字典，你必須輸入那個字（如 "B"、"價格"）。
# print(df.loc[ordinals[1]])
# print(type(df.loc[ordinals[1]]))

# iloc索引器是使用位置索引
# 依據：資料的絕對整數位置（0-based Index）。
# print(df.iloc[3]) # 第 4 筆
# print(df.iloc[3:5, 1:3]) # 切割

# 過濾資料
# DataFrame物件的索引可以使用布林索引，讓我
# 們只選擇條件成立的記錄資料，如下所示：
# print(df[df.price > 50])
# • DataFrame物件的isin()函數可以檢查指定欄位值
# 是否在清單中，可以讓我們過濾出清單中的記錄
# 資料，如下所示：
# print(df[df["name"].isin(["科技","居家"])])

# 排序資料
# df2 = df.set_index("price")
# print(df2)
# df2.sort_index(ascending=False, inplace=True)
# print(df2)

# df2 = df.sort_values("price", ascending=False)
# print(df2)
# df.sort_values(["type","price"], inplace=True)
# print(df)