import logging
'''
=======================================================================
高级函数 map(fn,lsd)
参数1：函数
参数2：列表
功能:讲传入的函数依次作用在序列中的每一个元素，并把结果作为新的Iterator返回
=======================================================================
'''
def chr2int(chr):
    '''
    将单个字符转换为相应的字面量整数
    '''
    return{"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9}[chr]

def JryFuncMapTest():
    logging.info(">>Function map() test")
    list1 = ["2","1","6","5"]
    Rslt = map(chr2int,list1) # 该对象为惰性列表
    ListRslt = list(Rslt)   # 转成真正的列表
    logging.info(ListRslt)



'''
=======================================================================
高阶函数 reduce
参数1：函数
参数2：列表
功能：一个函数作用在序列上，这个函数必须接收两个参数，reduce将结果继续和序列中的
下一个元素累计运算
reduce(f,[a,b,c,d]) = f(f(f(a,b),c),d)
=======================================================================
'''
from functools import reduce
def mysum(x,y):
    return(x+y)

def JryFuncReduceTest():
    '''
    求一个序列的和
    '''
    logging.info(">>Function reduce() Test")
    list2 = [1,2,3,4,5]
    Rslt = reduce(mysum,list2)
    logging.info("Test result = %d"%(Rslt))
    

'''
=======================================================================
高阶函数 map and reduce 综合运用
=======================================================================
'''
def str2int(str):
    def fc(x,y):
        return x*10+y
    def fs(chr):
        return{"0":0,"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9}[chr]
    return(reduce(fc,map(fs,list(str))))

def JryFuncMapReduceTest():
    '''
    map和reduce综合运用
    字符串转整数
    '''
    logging.info(">>Function map() and reduce() Test")
    logging.info(str2int("12345"))

'''
=======================================================================
原型:filter(fn,lsd)
参数1 为函数
参数2 为序列
功能：用于过滤序列，把传入的函数依次作用于序列每个元素，根据返回是True还是
False决定是否保留该元素
=======================================================================
'''
def JryFuncFilterTest():
    '''
    获取偶数
    '''
    logging.info(">>Function filter() Test")
    list1 = [1,2,3,4,5,6,7]

    def func(num):
        if num%2 == 0:
            return True
        return False

    l = filter(func,list1)
    print(list(l))

    '''
    数据过滤
    '''
    data = [["姓名","年龄","爱好"],["tom","26","无"],["xiaoming","29","金钱"]]
    def func2(v):
        v = str(v)
        if v == "无":
            return False
        return True
    for line in data:
        m = filter(func2,line)
        print(list(m))


'''
=======================================================================
# 排序:冒泡，选择
# 快速，插入，计数器
=======================================================================
'''
def JryFuncSortedTest():
    logging.info(">>Function sorted() Test")
    list1 = [4,7,2,6,3]
    list2 = sorted(list1) # 默认升序排序
    print(list2)

    #按绝对值大小排序
    list3 = [4,-7,2,6,-3]
    # key 接收函数实现自定义排序规则
    list4 = sorted(list3,key=abs) # 默认升序排序
    print(list4)
    list5 = sorted(map(abs,list3))
    print(list5)

    # 降序排序
    list6 = [2,7,6,3,1,9]
    list7 = sorted(list6,reverse = True)
    print(list7)

    def myLen(str):
        return(len(str))
    list8 = ['b333','a111111','c22','d5t54']
    list9 = sorted(list8,key=myLen)
    print(list9)    



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(">> main test begin...")
    JryFuncMapTest()
    JryFuncReduceTest()
    JryFuncMapReduceTest()
    JryFuncFilterTest()
    JryFuncSortedTest()
