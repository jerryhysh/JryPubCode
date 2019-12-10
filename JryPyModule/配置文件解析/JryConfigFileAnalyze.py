'''
import sys
绝对路径方式导入：
sys.path.append("E:\\PythonWorkspace\\mycompany") #这里是我的mycompany文件路径

相对路径方式导入：
# print(__file__)#获取当前程序路径，注意：这里打印出来的路径为相对路径
#动态获取绝对路径
# print(os.path.abspath(__file__)) #这才是当前程序绝对路径
# print(os.path.dirname(os.path.abspath(__file__))) #当前程序上一级目录，其中dirname返回目录名，不要文件名
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))#当前程序上上一级目录

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为mycompany
sys.path.append(BASE_DIR) #添加环境变量

特别注意：sys.path.append()添加路径时注意是在Windows还是在Linux下，Windows下需要'\\'否则会报错
'''

'''
    解析TBOX配置文件，并返回配置数据
'''
import os
import logging


def JryConfigFileAnalyze(ConfigFilePathIn = r'JryConfig.ini',KeyValueSplitStrIn = ':',ConfigItemSplitStrIn = ';'):
    # 输入：配置文件路径
    ConfigFilePath = ConfigFilePathIn
    # 输入：配置命令和配置数据分隔符
    KeyValueSplitStr = KeyValueSplitStrIn
    # 输入：各配置项的分隔符
    ConfigItemSplitStr = ConfigItemSplitStrIn
    # 输出：配置数据字典
    ConfigDataDict = {}

    logging.debug('Config file path:{FilePath}'.format(FilePath = ConfigFilePath))

    # 打开配置文件
    with open(ConfigFilePath,encoding='utf-8') as ConfigFileHandle:
        while True:
            # 读取文件内容，每次最多读取500行
            ContentLines = ConfigFileHandle.readlines(500)
            if ContentLines:    # 读取到内容
                # 遍历列表，处理每一行数据
                for OriginContentLine in ContentLines:
                    # 去掉头尾的空白符
                    ContentLine = OriginContentLine.strip('\n')
                    # '#'号开头的表示注释，不处理
                    if '#' == ContentLine[0]:
                        continue
                    for OriginConfigItem in ContentLine.split(ConfigItemSplitStr):
                        # 配置项非空白数据
                        if False == OriginConfigItem.isspace():
                            # 后续有进行数据过滤，此处直接赋值即可
                            ConfigItem = OriginConfigItem
                            # 存在配置命令和配置值分隔符
                            if ConfigItem.find(KeyValueSplitStr,1) != -1:
                                ConfigDataDict[ConfigItem.split(KeyValueSplitStr,1)[0].strip()] = ConfigItem.split(KeyValueSplitStr,1)[1].strip()
                    
            else:    # 未读取到文件内容，说明文件读取完毕，可以结束
                break
    # logging.debug('Config data dict:\r\n{CfgItms}'.format(CfgItms = str(ConfigDataDict)))
    ConfigDataDictOut = ConfigDataDict
    return ConfigDataDictOut

def JryConfigItemsDictGet(FilePathIn):
    ConfigItemsDict = JryConfigFileAnalyze(FilePathIn)
    logging.debug('Config data:{CfgItms}'.format(CfgItms = str(ConfigItemsDict)))
    return ConfigItemsDict


def JryConfigCmdListGet(FilePathIn):
    ConfigItemsDict = JryConfigFileAnalyze(FilePathIn)
    ConfigDataKeyList = list(ConfigItemsDict.keys())
    logging.debug('Config cmd:{CfgKeys}'.format(CfgKeys = str(ConfigDataKeyList)))
    return ConfigDataKeyList

def JryConfigValueGet(FilePathIn,OriginCmdStrIn):
    CmdStr = OriginCmdStrIn.strip()
    ValueStr = ""
    ConfigItemsDict = JryConfigFileAnalyze(FilePathIn)
    if CmdStr in ConfigItemsDict.keys():
        ValueStr = ConfigItemsDict[CmdStr]
    logging.debug('Config cmd {CfgKey}:{CfgValue}'.format(CfgKey = CmdStr,CfgValue = ValueStr))
    return ValueStr


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print()

    # 配置文件目录
    ConfigFileDir = r""
    # 获取当前工作目录
    # ConfigFileDir = os.path.abspath('.')
    # 获取Py文件所在目录
    ConfigFileDir = os.path.abspath(os.path.dirname(__file__))
    # logging.debug('ConfigFileDir:%s'%(ConfigFileDir))
    # 配置文件的文件名
    ConfigFileName = r"JryConfig.ini"
    # 配置文件路径
    ConfigFilePath = os.path.join(ConfigFileDir,ConfigFileName)
    # logging.debug('ConfigFilePath:%s'%(ConfigFilePath))
    # 获取配置数据
    JryConfigItemsDictGet(ConfigFilePath)
    JryConfigCmdListGet(ConfigFilePath)
    JryConfigValueGet(ConfigFilePath,"IpAddress")
    # logging.debug(JryConfigDict)

if __name__ == "__main__":
    main()
    os.system("pause")


    


