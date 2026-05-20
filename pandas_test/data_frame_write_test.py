import json
import pandas as pd
import sqlite3



# DataFrame like table
# 字典的 Key 是 Table 的 Header
json_data = '''
[
    {"user_id": 101, "username": "teddy", "dept": "DBA", "status": "online"},
    {"user_id": 102, "username": "alice", "dept": "Dev", "status": "offline"},
    {"user_id": 103, "username": "bob", "dept": "Dev", "status": "online"}
]
'''

# 2. JSON -> Dict (使用標準庫 json)
# json.loads 會把字串轉成 Python 的 list (裡面裝著 dict)
data_list = json.loads(json_data)
print(f"轉換後的類型: {type(data_list)}")
# 輸出: <class 'list'>

# 3. Dict -> DataFrame
df = pd.DataFrame(data_list)

print("\n--- 最終 DataFrame ---")
print(df)


# 轉置 ** 把列改成欄欄改成列
print(df.T)

df.to_csv("/Users/teddylai/Downloads/ora_json_df.csv", encoding="utf8")
df.to_json(
    "/Users/teddylai/Downloads/ora_json_df.json",
    orient="records",
    force_ascii=False,
    indent=2
)
df.to_html(
    "/Users/teddylai/Downloads/ora_json_df.html",
    index=False,
    encoding="utf-8"
)


# 寫一個 sql lite db file
con = sqlite3.connect("/Users/teddylai/nas_workplace_fetch/ide_workplace/datagrip/helloworld.db")
df.to_sql(
    "my_table",
    con,
    # fail(不寫 table), replace(先 drop table), append(接續 insert table)
    if_exists="append",
    index=False
)
# 重要：提交變更
con.commit()

# 關閉連線
con.close()


print('\n')
print(f'\ndf_head={df.head(2)}')
print(f'\ndf_info=')
df.info()
print(f'\ndf_columns={df.columns}')
print(f'\ndf_index{df.index}')
print(f'\ndf_values={df.values}')