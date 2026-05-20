class Student(object):
    # 類別屬性：所有學生共用的資訊 (例如學校名稱)
    school = "Linux Academy"

    def __init__(self, name='Unknown', math=0, english=0, chinese=0):
        # 實體屬性：每個學生獨立的資料 (就像資料庫的一筆 Row)
        print('Student_constructor')
        self.name = name
        self.math_score = math
        self.english_score = english
        self.chinese_score = chinese


# 子類別
class Student2(Student):
    # 若沒寫這個建構子 , 實際上還是會有隱式的建構子
    def __init__(self, name):
        # 呼叫父類別的建構子，確保父類的屬性被正確初始化
        super().__init__(name)
        print('Student2_constructor')

    # 子類別自己建構子若不想寫可用 pass 省略
    #pass

if __name__ == '__main__':
    # Student test -------------------------
    student = Student()
    print(' Student test ----------------------------')
    print(student.name)
    print(student.math_score)
    print(student.english_score)
    print(student.chinese_score)


    # Student1 test -------------------------
    print(' Student1 test ----------------------------')
    student1 = Student()
    student1.name = 'jerry'
    student1.math_score = '100'

    #盡量用 fstring 比較新,較現代 > Python 3.6
    # 在 Python 的演進史中，字串格式化經歷了三個主要階段：從最早的 `%` (C-style)，到中間的 `.format()`，再到現在主流推薦的 **f-string (Formatted String Literals)**。
    print(f'modify student_name = {student1.name}')
    print('modify math core :' + str(student1.math_score))
    print(student1.english_score)
    print(student1.chinese_score)


    # Student2 test -------------------------
    print(' Student2 test ----------------------------')
    student2 = Student2(Student)
    print(student2)

    # Student3 test -------------------------
    print(' Student3 test ----------------------------')
    student3 = Student2(student1)
    print(student3)