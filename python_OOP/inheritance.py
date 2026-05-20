
# 繼承(inheritance) e.g. 界門綱目科屬種
# e.g. 界=object 門=class 綱=dtype
# e.g. 所有 .py 都繼承自 object

# 當你繼承了 object，你自動獲得了以下能力：

# other test
'''
__new__: 負責分配記憶體，建立實例。
__init__: 負責初始化（我們剛聊過的建構子）。
__str__ / __repr__: 讓物件可以被轉成字串顯示。
__eq__: 讓你可以用 == 比較兩個物件。
__getattribute__: 讓你可以用 . 來存取屬性
'''

class MyProject:
    pass

# 查看繼承路徑
print(MyProject.__mro__)
# 輸出: (<class '__main__.MyProject'>, <class 'object'>)

# !! python 可以使用多重繼承 , 使用時可以用 ',' 分別開來
# e.g.
class READ:
    action='write'
    def __init__(self,action='default_write'):
        self.action=action
    pass
class WRITE:
    action='write'
    def __init__(self,action='default_read'):
        self.action=action
    pass


class SQL(READ,WRITE): # C 繼承自 A 與 Ｂ
    def __init__(self):
        self.write_action=WRITE.action
        self.read_action=READ.action
    pass

if __name__ == '__main__':
    print(f'{READ.action} , {WRITE.action}')
    print(f'{SQL().write_action} , {SQL().read_action}')

    READ.action='sql_read'
    WRITE.action='sql_write'

    print(SQL())
    sql = SQL()
    print(f'{sql.write_action} , {sql.read_action}')