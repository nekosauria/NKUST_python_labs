import json
import pandas
import sqlite3
from sqlalchemy import create_engine

db_path = "/Users/teddylai/nas_workplace_fetch/ide_workplace/datagrip/helloworld.db"
engine = create_engine(f"sqlite:///{db_path}")

query = """
SELECT
    u.user_id,
    u.user_name,
    u.city,
    o.product_name,
    o.price
FROM users u
         LEFT JOIN orders o ON u.user_id = o.user_id
where user_name in ('Teddy' , 'Bob');
"""

# 在 Pandas 中調用
# df = pd.read_sql(left_join_sql, engine)
df = pandas.read_sql( query, engine )

df.to_json(
    "/Users/teddylai/Downloads/select_df.json",
    orient="records",
    force_ascii=False,
    indent=2
)