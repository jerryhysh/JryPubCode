import logging
import binascii
from binascii import b2a_hex, a2b_hex

# ============================================= 功能选择======================================================
FunctionSelectDict = {1:"平台数据解析",2:"车控请求数据解析",3:"车控应答数据解析",4:"实时数据解析"}

# =======================================TBOX与平台协议数据解析================================================
TboxAndPlatProtolOrderTup = ("头标识","命令标识","应答标志","车辆唯一标识码","数据单元加密方式","流水号","数据单元长度","数据单元内容","校验码")
TboxAndPlatProtolAnlyzDict = {
    "头标识":{"Len":2,"DatTyp":"Number","DatVal":{0x2323:"固定码正确"}},
    
    "命令标识":{"Len":1,"DatTyp":"Number","DatVal":{0x01:"车辆登入",0x02:"实时信息上报",0x03:"补发信息上报",0x04:"车辆登出",
    0x05:"平台传输数据",0x06:"平台传输数据",0x07:"心跳",0x08:"终端较时",0x80:"终端查询",0x81:"终端设置",0x82:"终端控制",
    0xd0:"驾驶行为预处理上报",0xd1:"车辆状态查询",0xd2:"推送消息",0xe0:"控制指令请求",0xe1:"控制状态回馈",0xe2:"升级版本信息请求",
    0xe3:"请求升级信息",0xe4:"升级结果状态",0xea:"蓝牙下行控制请求",0xeb:"蓝牙下行控制应答",0xec:"蓝牙上行请求",0xed:"蓝牙上行应答"}},

    "应答标志":{"Len":1,"DatTyp":"Number","DatVal":{0x01:"成功",0x02:"错误",0x03:"VIN重复",0x10:"无此设备",
    0x11:"设备验证错误",0x12:"参数格式错误",0x13:"服务器内部错误",0x14:"数据包校验错误",0x15:"TSP无升级包",0xfe:"命令包非应答数据包"}},

    "车辆唯一标识码":{"Len":17,"DatTyp":"Bytes","DatVal":{}},

    "数据单元加密方式":{"Len":1,"DatTyp":"Number","DatVal":{0x01:"数据不加密",0x02:"数据RSA加密",0x03:"数据AES128加密",
    0xfe:"异常",0xff:"无效"}},

    "流水号":{"Len":2,"DatTyp":"Bytes","DatVal":{}},

    "数据单元长度":{"Len":2,"DatTyp":"Number","DatVal":{}},

    "数据单元内容":{"Len":0xffff,"DatTyp":"Bytes","DatVal":{}},
    "校验码":{"Len":1,"DatTyp":"Bytes","DatVal":{}}
    }

# ======================================实时数据解析========================================

RealDatCmdAnlyzDict = {
    0x80:"车辆位置扩展数据",0x81:"整车状态扩展数据",0x82:"车门状态扩展数据",0x83:"车灯状态扩展数据",
    0x84:"空调状态扩展数据",0x85:"车窗状态扩展数据",0x86:"故障报警扩展数据",0x87:"安防报警扩展数据",
    0x88:"胎压系统扩展数据",0x89:"加热系统扩展数据",0x8a:"ADAS系统扩展数据"
}

# 实时数据解析
RealDataAnlyzDict = {
    "采集时间":{"Len":0x06,"DatTyp":"Bytes","DatVal":{}},
    "车辆位置扩展数据":{"Len":0xff,"DatTyp":"Bytes","DatVal":{}},
    "整车状态扩展数据":{"Len":0xff,"DatTyp":"Bytes","DatVal":{}},
    "车门状态扩展数据":{"Len":0xff,"DatTyp":"Bytes","DatVal":{}},
    "车灯状态扩展数据":{"Len":0xff,"DatTyp":"Bytes","DatVal":{}},
    "空调状态扩展数据":{"Len":0xff,"DatTyp":"Bytes","DatVal":{}},
    "车窗状态扩展数据":{"Len":0xff,"DatTyp":"Bytes","DatVal":{}},
    "故障报警扩展数据":{"Len":0xff,"DatTyp":"Bytes","DatVal":{}},
    "安防报警扩展数据":{"Len":0xff,"DatTyp":"Bytes","DatVal":{}},
    "胎压系统扩展数据":{"Len":0xff,"DatTyp":"Bytes","DatVal":{}},
    "加热系统扩展数据":{"Len":0xff,"DatTyp":"Bytes","DatVal":{}},
    "ADAS系统扩展数据":{"Len":0xff,"DatTyp":"Bytes","DatVal":{}},
}
Rd_VhclAnlyzDict = {
    "车辆状态":{"Len":1,"DatTyp":"Number","DatVal":{0x01:"车辆启动状态",0x02:"熄火",0x03:"其他状态",0xfe:"异常",0xff:"无效"}},
    "充电状态":{"Len":1,"DatTyp":"Number","DatVal":{0x01:"停车充电",0x02:"行驶充电",0x03:"未充电状态",0x04:"充电完成",0xfe:"异常",0xff:"无效"}},
    "运行模式":{"Len":1,"DatTyp":"Number","DatVal":{0x01:"纯电",0x02:"混动",0x03:"燃油",0xfe:"异常",0xff:"无效"}},
    "车速":{"Len":2,"DatTyp":"Bytes","DatVal":{}},
    "累计里程":{"Len":4,"DatTyp":"Bytes","DatVal":{}},
    "总电压":{"Len":2,"DatTyp":"Bytes","DatVal":{}},
    "总电流":{"Len":2,"DatTyp":"Bytes","DatVal":{}},
    "SOC":{"Len":1,"DatTyp":"Bytes","DatVal":{}},
    "DCDC状态":{"Len":1,"DatTyp":"Bytes","DatVal":{0x01:"工作",0x02:"断开",0xfe:"异常",0xff:"无效"}},
    "档位":{"Len":1,"DatTyp":"Bytes","DatVal":{}},
    "绝缘电阻值":{"Len":2,"DatTyp":"Bytes","DatVal":{}},
    "加速踏板行程值":{"Len":1,"DatTyp":"Bytes","DatVal":{}},
    "制动踏板状态":{"Len":1,"DatTyp":"Bytes","DatVal":{}},
}


# =======================================远程车控请求数据解析================================================
RmtCtrl_PlatReqToTboxOrderTup = ("时间","命令ID","命令参数")
RmtCtrl_PlatReqToTboxAnlyzDict = {
    "时间":{"Len":6,"DatTyp":"Number","DatVal":{}},
    "命令ID":{"Len":1,"DatTyp":"Number","DatVal":{0x01:"远程寻车",0x02:"门锁控制",0x03:"发动机控制",
    0x04:"空调开关",0x05:"空调设置温度",0x06:"空调前除雾开关",0x07:"空调后除雾开关",0x08:"主驾驶座座椅加热",
    0x09:"副驾驶座座椅加热",0x0a:"左前窗控制",0x0b:"右前窗控制",0x0c:"左后窗控制",0x0d:"右后窗控制",
    0x0e:"四窗一键",0x0f:"天窗控制",0x10:"遮阳帘控制"}},
    "命令参数":{"Len":0xffff,"DatType":"Number","DatVal":{}}
}

# =======================================远程车控应答数据解析================================================

RmtCtrl_TboxRspToPlatDatOrderTup = ("时间","命令ID","控制结果","失败原因","引擎状态","左前窗位置","右前窗位置",
"左后窗位置","右后窗位置","天窗位置百分比","天窗状态","车门状态","远程启动计时",
"主驾座椅加热档位","副驾座椅加热档位","空调开关状态","空调设置温度1","空调设置温度2",
"空调设置温度3","遮阳帘位置")

RmtCtrl_TboxRspToPlatDatAlyzDict = {
    "时间":{"Len":6,"DatTyp":"Number","DatVal":{}},
    "命令ID":{"Len":1,"DatTyp":"Number","DatVal":{0x01:"远程寻车",0x02:"门锁控制",0x03:"发动机控制",0x04:"空调开关",
    0x05:"空调设置温度",0x06:"空调前除雾开关",0x07:"空调后除雾开关",0x08:"主驾驶座座椅加热",0x09:"副驾驶座座椅加热",
    0x0a:"左前窗控制",0x0b:"右前窗控制",0x0c:"左后窗控制",0x0d:"右后窗控制",0x0e:"四窗一键",0x0f:"天窗控制",
    0x10:"遮阳帘控制"}},
    "控制结果":{"Len":1,"DatTyp":"Number","DatVal":{0x00:"失败",0x01:"成功"}},

    "失败原因":{"Len":1,"DatTyp":"Number","DatVal":{0x00:"Inactive",0x01:"Power mode is not OFF",0x02:"Any door or tailgate open",
    0x03:"Gear shift is not in P",0x04:"More than 2 times RES operation",0x05:"Valid UID in the vehicle",
    0x06:"Vehicle is not locked",0x07:"Not in anti-thief status",0x08:"Battery voltage unnormal",
    0x09:"EMS auth failed",0x0a:"Vehicle speed unnormal",0x0b:"Timeout for waiting EMS status",
    0x0c:"RES off request",0x0d:"EPB is not applied",0x0e:"Driver seatbell is not unbuckle",}},

    "引擎状态":{"Len":1,"DatTyp":"Number","DatVal":{0x00:"Engine Stop(Engine OFF)",0x01:"Key ON",0x02:"Cranking",0x03:"Running"}},

    "左前窗位置":{"Len":1,"DatTyp":"Number","DatVal":{0x00:"Close(top)",0x01:"Open(Bottom)",0x02:"80%-Close",0x03:"Open-80%",
    0xfe:"异常",0xff:"无效值"}},

    "右前窗位置":{"Len":1,"DatTyp":"Number","DatVal":{0x00:"Close(top)",0x01:"Open(Bottom)",0x02:"80%-Close",0x03:"Open-80%",
    0xfe:"异常",0xff:"无效值"}},

    "左后窗位置":{"Len":1,"DatTyp":"Number","DatVal":{0x00:"Close(top)",0x01:"Open(Bottom)",0x02:"80%-Close",0x03:"Open-80%",
    0xfe:"异常",0xff:"无效值"}},

    "右后窗位置":{"Len":1,"DatTyp":"Number","DatVal":{0x00:"Close(top)",0x01:"Open(Bottom)",0x02:"80%-Close",0x03:"Open-80%",
    0xfe:"异常",0xff:"无效值"}},

    "天窗位置百分比":{"Len":1,"DatTyp":"Number","DatVal":{}},

    "天窗状态":{"Len":1,"DatTyp":"Number","DatVal":{0x00:"unknown",0x01:"all closed全闭点",0x02:"all close to tilt 全闭点至起翘点",
    0x03:"tilt 全起翘点",0x04:"tilt to open 全起翘点至全开点",0x05:"Half open 半开",0x06:"Half open to open 半开点至全开",
    0x07:"All open 全开",0xfe:"异常",0xff:"无效"}},
    # p30
    "车门状态":{"Len":2,"DatTyp":"Number","DatVal":{}},
    "远程启动计时":{"Len":2,"DatTyp":"Number","DatVal":{}},
    "主驾座椅加热档位":{"Len":1,"DatTyp":"Number","DatVal":{0x00:"OFF",0x01:"Level 1",0x02:"Level 2",0x03:"Level 3"}},
    "副驾座椅加热档位":{"Len":1,"DatTyp":"Number","DatVal":{0x00:"OFF",0x01:"Level 1",0x02:"Level 2",0x03:"Level 3"}},
    "空调开关状态":{"Len":2,"DatTyp":"Bit","DatVal":{0:{"len":1,"Name":"空调压缩机状态","val":{0:"OFF",1:"ON"}},
    1:{"len":1,"Name":"空调系统开关状态","val":{0:"OFF",1:"ON"}},2:{"len":1,"Name":"后除雾开关状态","val":{0:"OFF",1:"ON"}},
    3:{"len":1,"Name":"前除雾开关状态","val":{0:"OFF",1:"ON"}},4:{"len":1,"Name":"AC指示灯","val":{0:"OFF",1:"ON"}},
    5:{"len":1,"Name":"AUTO模式开关 ","val":{0:"OFF",1:"ON"}},6:{"len":1,"Name":"前AC一键AUTO开关状态 ","val":{0:"OFF",1:"ON"}},
    7:{"len":1,"Name":"后AC一键AUTO开关状态 ","val":{0:"OFF",1:"ON"}},8:{"len":1,"Name":"前AC开关状态 ","val":{0:"OFF",1:"ON"}},
    9:{"len":1,"Name":"后AC开关状态","val":{0:"OFF",1:"ON"}},
    }},
    "空调设置温度1":{"Len":1,"DatTyp":"Number","DatVal":{0xfe:"异常",0xff:"无效"}},
    "空调设置温度2":{"Len":1,"DatTyp":"Number","DatVal":{0xfe:"异常",0xff:"无效"}},
    "空调设置温度3":{"Len":1,"DatTyp":"Number","DatVal":{0xfe:"异常",0xff:"无效"}},
    "遮阳帘位置":{"Len":1,"DatTyp":"Number","DatVal":{0x00:"unknown",0x01:"all closed全闭点",0x02:"all close to tilt 全闭点至起翘点",
    0x03:"tilt 全起翘点",0x04:"tilt to open 全起翘点至全开点",0x05:"Half open 半开",0x06:"Half open to open 半开点至全开",
    0x07:"All open 全开",0xfe:"异常",0xff:"无效"}}
}

def BytesDataAnlyz(KeyStr,DataBytes,ReferDict):
    # {"keyStr":{"Val":"","Mean":}}
    RetItemDict = {}
    RetLen = 0
    if (False == isinstance(KeyStr,str)) or (False == isinstance(DataBytes,bytes)) or (False == isinstance(ReferDict,dict)):
        return(None,None)

    # 如果字典中有该关键字
    if (KeyStr in ReferDict.keys()):
        # 数据为数字类型
        RetItemDict[KeyStr] = {}
        if "Number" == ReferDict[KeyStr]["DatTyp"]:
            if ReferDict[KeyStr]["Len"] <= len(DataBytes):
                DatVal = 0
                RetItemDict[KeyStr]["Val"] = ""
                for i in list(range(ReferDict[KeyStr]["Len"])):
                    DatVal <<= 8
                    DatVal |= DataBytes[i]
                    RetItemDict[KeyStr]["Val"] += "{:0>2X}".format(DataBytes[i])
                if (DatVal in ReferDict[KeyStr]["DatVal"]):
                    RetItemDict[KeyStr]["Mean"] = ReferDict[KeyStr]["DatVal"][DatVal]
                else:
                    RetItemDict[KeyStr]["Mean"] = ""
                RetLen = ReferDict[KeyStr]["Len"]
            else:
                RetItemDict[KeyStr]["Val"] = (b2a_hex(DataBytes)).decode("utf-8")
                RetItemDict[KeyStr]["Mean"] = ""
                RetLen = len(DataBytes)
                logging.error("Byte length is too short!") 
        else: # "Bytes" == ReferDict[KeyStr]["DatTyp"]:
            if 0 == ReferDict[KeyStr]["Len"]:
                RetItemDict[KeyStr]["Val"] = ""
                RetItemDict[KeyStr]["Mean"] = ""
                RetLen = ReferDict[KeyStr]["Len"] 
            elif ReferDict[KeyStr]["Len"] <= len(DataBytes):
                RetItemDict[KeyStr]["Val"] = (b2a_hex(DataBytes[:ReferDict[KeyStr]["Len"]])).decode("utf-8")
                RetItemDict[KeyStr]["Mean"] = ""
                RetLen = ReferDict[KeyStr]["Len"] 
            else:
                RetItemDict[KeyStr]["Val"] = (b2a_hex(DataBytes)).decode("utf-8")
                RetItemDict[KeyStr]["Mean"] = ""
                RetLen = len(DataBytes)
                # logging.info("Byte length is {DatLen}.".format(DatLen=RetLen)) 
        return(RetLen,RetItemDict)


def TboxAndPlatSpclDatAnlyz(TansferDict):
    if "车辆唯一标识码" in TansferDict.keys():
        DatStr = TansferDict["车辆唯一标识码"]["Val"]
        DatBytes = a2b_hex(DatStr)
        DatStr = TansferDict["车辆唯一标识码"]["Mean"] = DatBytes.decode("utf-8")



def TboxAndPlatProtolAnlyz(FuncSel = 1,OriginStr = None):
    OutputStr = ""
    if (FuncSel not in FunctionSelectDict.keys()):
        # logging.error("功能选择错误！")
        return OutputStr

    AnalyzeStr = OriginStr
    if 1 == FuncSel:
        # logging.info(FunctionSelectDict[FuncSel])
        OutputStr += (FunctionSelectDict[FuncSel]+"\r\n")
        TboxAndPlatStr = AnalyzeStr
        if (None == TboxAndPlatStr):
            TboxAndPlatStr = "2323E0024C444E4743374643584B3031393433353001000E0000B4"
        # 去除字符串中的空白字符
        PreProcStr = "".join(TboxAndPlatStr.split())
        # logging.info(PreProcStr)
        OutputStr += (PreProcStr+"\r\n")
        # 将ASCII码表示的数据转换为字节流数据
        TboxAndPlatBytes = a2b_hex(PreProcStr)
        # logging.info(TboxAndPlatBytes)

        idxByte = 0
        for Item in TboxAndPlatProtolOrderTup:
            DatLen,ItemDatDict = BytesDataAnlyz(Item,TboxAndPlatBytes[idxByte:],TboxAndPlatProtolAnlyzDict)
            TboxAndPlatSpclDatAnlyz(ItemDatDict)
            if "数据单元长度" in ItemDatDict.keys():
                TboxAndPlatProtolAnlyzDict["数据单元内容"]["Len"] = int((ItemDatDict["数据单元长度"]['Val']),16)
            if None == DatLen:
                logging.error("analyze error!")
                break
            else:
                idxByte += DatLen
                # logging.info(ItemDatDict)
                OutputStr += (str(ItemDatDict)+"\r\n")

    if 2 == FuncSel:
        
        pass
    
    if 3 == FuncSel:
        # logging.info(FunctionSelectDict[FuncSel])
        OutputStr += (FunctionSelectDict[FuncSel]+"\r\n")
        # 远程控制应答数据解析
        RmtCtrl_TboxRspToPlatStr = AnalyzeStr
        if None == RmtCtrl_TboxRspToPlatStr:
            RmtCtrl_TboxRspToPlatStr = " 130C030A0E0F02010001 070207070100001F00000202000008080803"
        # 去除字符串中的空白字符
        PreProcStr = "".join(RmtCtrl_TboxRspToPlatStr.split())
        # logging.info(PreProcStr)
        OutputStr += (PreProcStr+"\r\n")
        RmtCtrl_TboxRspToPlatBytes = a2b_hex(PreProcStr)

        idxByte = 0
        for Item in RmtCtrl_TboxRspToPlatDatOrderTup:
            DatLen,ItemDatDict = BytesDataAnlyz(Item,RmtCtrl_TboxRspToPlatBytes[idxByte:],RmtCtrl_TboxRspToPlatDatAlyzDict)
            if "时间" in ItemDatDict.keys():
                DatStr = ItemDatDict["时间"]["Val"]
                DatBytes = a2b_hex(DatStr)
                for DatByte in DatBytes:
                    ItemDatDict["时间"]["Mean"] += "{:0>2}".format(DatByte)
            if None == DatLen:
                logging.error("analyze error!")
                break
            else:
                idxByte += DatLen
                # logging.info(ItemDatDict)
                OutputStr += (str(ItemDatDict)+"\r\n")
    # 实时数据解析
    if 4 == FuncSel:
        pass
        '''
        OutputStr += (FunctionSelectDict[FuncSel]+"\r\n")
        RealDataStr = AnalyzeStr
        if None == RealDataStr:
            RealDataStr = "130C0411131F800C0100 00000000000000000081 33030200000000000E00 0000028B0000000E0000 \
                000000005AFF0000000F FF03FF03FF0000800000 00000000AA0000000000 018203001F8303000084 0D00C000000000000E0E \
                0E0202850A0000000000   00000000861100000000 01060606000000000000 00008704000000FE0544 583923  "
        idxByte = 0
        DatLen,ItemDatDict = BytesDataAnlyz("采集时间",RealDataStr[idxByte:],RealDataAnlyzDict)
        idxByte += DatLen

        CmdInt = int(RealDataStr[idxByte],16)
        CmdDatLen = (int(RealDataStr[idxByte+1],16)<<8)|(int(RealDataStr[idxByte+2],16))
        if CmdInt in RealDatCmdAnlyzDict.keys():
            CmdStr = RealDatCmdAnlyzDict[CmdInt]
            if CmdStr in RealDataAnlyzDict.keys():
                RealDataAnlyzDict[CmdStr]["Len"] = CmdDatLen
        if None == DatLen:
            logging.error("analyze error!")
        else:
            idxByte += DatLen
        '''

    logging.info(OutputStr)
    return OutputStr
    





'''
def RmtCtrl_TboxRspToPlatDataAnlyz(OriginStr):
    logging.debug(OriginStr)
    # 去除字符串中的空白字符
    TboxRspToPlatStr = "".join(OriginStr.split())
    logging.info(TboxRspToPlatStr)
    # 将ASCII码表示的数据转换为字节流数据
    RmtCtrl_TboxRspToPlatBytes = a2b_hex(TboxRspToPlatStr)
    # logging.debug(RmtCtrl_TboxRspToPlatBytes)
    idxByte = 0
    for item in RmtCtrl_TboxRspToPlatDatOrderTup:
        ItemAnlyzOutputStr = ""
        ItemAnlyzOutputStr = item+":"
        DatVal = 0
        # 获取数据
        ItemAnlyzOutputStr += "\""
        for i in list(range(RmtCtrl_TboxRspToPlatDatAlyzDict[item]["Len"])):
            # RmtCtrl_TboxRspToPlatDatAlyzDict[item][idxByte]
            if (idxByte+RmtCtrl_TboxRspToPlatDatAlyzDict[item]["Len"]) <= len(RmtCtrl_TboxRspToPlatBytes):
                ItemAnlyzOutputStr += "{:0>2X}".format(RmtCtrl_TboxRspToPlatBytes[idxByte])
                DatVal <<= 8
                DatVal |= RmtCtrl_TboxRspToPlatBytes[idxByte]
            else:
                DatVal = None
            idxByte += 1
        ItemAnlyzOutputStr += "\""
        # 数据转译
        if "Number" == RmtCtrl_TboxRspToPlatDatAlyzDict[item]["Mode"]:
            if (DatVal in RmtCtrl_TboxRspToPlatDatAlyzDict[item]["DatVal"].keys()):
                ItemAnlyzOutputStr += " {"
                ItemAnlyzOutputStr += RmtCtrl_TboxRspToPlatDatAlyzDict[item]["DatVal"][DatVal]
                ItemAnlyzOutputStr += "}"
        elif "Bit" == RmtCtrl_TboxRspToPlatDatAlyzDict[item]["Mode"]:
            pass
        else:
            pass

        print(ItemAnlyzOutputStr)
'''

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # InputStr = " 130C030A0E0F02010001 070207070100001F0000 0202000008080803"
    while(1):
        try:
            InputSelStr = input("选择功能{FuncList}:".format(FuncList = str(FunctionSelectDict)))
            if (int(InputSelStr) not in FunctionSelectDict.keys()):
                logging.error("功能选择错误！")
                continue

            InputStr = input("输入解析字符串:")
            print("\r\n")
            # a2b_hex(InputStr)
            TboxAndPlatProtolAnlyz(int(InputSelStr),InputStr)
        except:
            print("输入字符有误！")
        print("\r\n")
        # input("输入回车结束")
    
    input("输入回车结束")
    
    