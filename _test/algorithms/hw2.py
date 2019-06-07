# x= int(input('输入小于1000的整数'))
# # x= 60
# str = '%s=1'%x
# while x>1:
#     for i in range(2,x+1):
#         if x%i==0:
#             x= int(x/i)
#             str+='X%s'%i
#             break
# print(str)

# l1 = [random.choice(range(10000)) for i in range(20)]
# odd = l1[::2]
# odd.sort(reverse=True)
# l1[::2]=odd
# print()

class Student():

    def __init__(self):
        self.__name = ''
        self.__age = 0
        self.__gender = ''
        self.__clazz = ''
        self.__math = 0
        self.__chinese = 0
        self.__english = 0

    def getName(self):
        return self.__name

    def setName(self, newValue):
        self.__name = newValue

    def getAge(self):
        return self.__age

    def setAge(self, newValue):
        self.__age = newValue

    def getGender(self):
        return self.__gender

    def setGender(self, newValue):
        self.__gender = newValue
        
    def getClazz(self):
        return self.__clazz

    def setClazz(self, newValue):
        self.__clazz = newValue
        
    def getMath(self):
        return self.__math

    def setMath(self, newValue):
        self.__math = newValue
        
    def getChinese(self):
        return self.__chinese

    def setChinese(self, newValue):
        self.__chinese = newValue
        
    def getEnglish(self):
        return self.__english

    def setEnglish(self, newValue):
        self.__english = newValue

    def __str__(self) -> str:
        return self.__name+" "+self.__gender+" "+ self.__clazz+"班 "+str(self.__age)+"岁 "

    def avg(self):
        return (self.getChinese()+self.getEnglish()+self.getMath())/3

studentA = Student()
studentA.setAge(19)
studentA.setChinese(80)
studentA.setClazz(1)
studentA.setEnglish(90)
studentA.setGender("男")
studentA.setMath(100)
studentA.setName("张三")

studentB = Student()
studentB.setAge(20)
studentB.setChinese(95)
studentB.setClazz(2)
studentB.setEnglish(100)
studentB.setGender("女")
studentB.setMath(91)
studentB.setName("李四")


print(studentA.getName())
print(studentA.getGender())
print(studentA.getAge())
print(studentA.getClazz())
print(studentA.getChinese())
print(studentA.getEnglish())
print(studentA.getMath())
print("平均分："+str(studentA.avg()))
print()
print(studentB.getName())
print(studentB.getGender())
print(studentB.getAge())
print(studentB.getClazz())
print(studentB.getChinese())
print(studentB.getEnglish())
print(studentB.getMath())
print("平均分："+str(studentB.avg()))


