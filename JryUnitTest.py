'''
单元测试
用来对一个函数，一个类或者一个模块来进行正确性校验；
1.单元测试通过：说明我们测试的函数功能正常
2.单元测试不通过：说明函数功能存在BUG，要么测试条件输入有误
'''
import unittest #单元测试
import doctest #文档测试，可以提取注释中的代码执行
# doctest严格按照python交互模式的输入提取

def mySum(x,y):
    '''
    example:
    >>> print(mySum(1,2))
    34
    '''
    return x+y

def mySub(x,y):
    return(x-y)

class Person(object):
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def getVal(self,v):
        print(v)
        return v
    def getAge(self):
        return(self.age)


class Test(unittest.TestCase):
    def setUp(self):
        print("开始测试时，自动调用")
    def tearDown(self):
        print("结束测试时，自动调用")

    def test_mySum(self):
        self.assertEqual(mySum(1,2),3,"加法有误")
    def test_mySub(self):
        self.assertEqual(mySub(2,1),1,"减法有误")

    def test_init(self):
        p = Person("hanmei",20)
        self.assertEqual(p.name,"hanmei","属性有误")
    def test_getAge(self):
        p = Person("hanmei",20)
        self.assertEqual(p.getAge(),p.age,"getAge函数有误")

if __name__ == '__main__':
    # unittest.main()
    doctest.testmod()  #文档测试

