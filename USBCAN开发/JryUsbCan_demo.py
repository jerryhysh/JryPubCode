import os
import logging
from ctypes import *

CanDeviceTypeDict = {"USBCAN-2A":4,"USBCAN-2C":4,"CANalyst-II":4}
CanBaudRateDict =  {
            "10_Kbps":{"BTR0":0x31,"BTR1":0x1c},
            "500_Kbps":{"BTR0":0x00,"BTR1":0x1c}
        }
CanWorkMode =   {
                "Normal":0x00,      # 正常模式（相当于正常节点）
                "Listen":0x01,
                "LoopBack":0x02
                }
CanFilterMode = {
                "RCV_ALL_MSG":0x00,     # 接收所有类型
                "RCV_STD_MSG":0x02,     # 只接收标准帧
                "RCV_EXT_MSG":0x03      # 只接收扩展帧
                }

STATUS_OK = 1
STATUS_ERR = -1
# VCI_BOARD_INFO结构体包含USB-CAN系列接口卡的设备信息。结构体将在VCI_ReadBoardInfo函数中被填充。
class VCI_BOARD_INFO(Structure):
    _fields_ = [("hw_Version", c_ushort),   # 硬件版本号，用16进制表示。比如0x0100表示V1.00。
                ("fw_Version", c_ushort),   # 固件版本号，用16进制表示。比如0x0100表示V1.00。
                ("dr_Version", c_ushort),   # 驱动程序版本号，用16进制表示。比如0x0100表示V1.00。
                ("in_Version", c_ushort),   # 接口库版本号，用16进制表示。比如0x0100表示V1.00。
                ("irq_Num", c_ushort),      # 保留参数。
                ("can_Num", c_ubyte),       # 表示有几路CAN通道。
                ("str_Serial_Num", c_ubyte*20), # 此板卡的序列号。
                ("str_hw_Type", c_ubyte*40),    # 硬件类型，比如“USBCAN V1.00”（注意：包括字符串结束符’\0’）
                ("Reserved", c_ushort*4)       # 系统保留。
                ]  

# VCI_INIT_CONFIG结构体定义了初始化CAN的配置。
# 结构体将在VCI_InitCan函数中被填充，即初始化之前，要先填好这个结构体变量。
class VCI_INIT_CONFIG(Structure):  
    _fields_ = [
                # 验收码。SJA1000的帧过滤验收码。对经过屏蔽码过滤为“有关位”进行匹配，全部匹配成功后，此帧可以被接收。否则不接收。
                ("AccCode", c_ulong),
                # 屏蔽码。SJA1000的帧过滤屏蔽码。对接收的CAN帧ID进行过滤，对应位为0的是“有关位”，对应位为1的是“无关位”。
                # 屏蔽码推荐设置为0xFFFFFFFF，即全部接收。
                ("AccMask", c_ulong),
                # 保留。
                ("Reserved", c_ulong),
                ("Filter", c_ubyte),        # 滤波方式，允许设置为0-3，
                ("Timing0", c_ubyte),       # 波特率定时器  0（BTR0）。
                ("Timing1", c_ubyte),       # 波特率定时器  1（BTR1）。
                ("Mode", c_ubyte)   # 模式。=0表示正常模式（相当于正常节点），=1表示只听模式（只接收，不影响总线），=2表示自发自收模式（环回模式）。
                ]  

# VCI_CAN_OBJ结构体是CAN帧结构体，即1个结构体表示一个帧的数据结构。
# 在发送函数VCI_Transmit和接收函数VCI_Receive中，被用来传送CAN信息帧。
class VCI_CAN_OBJ(Structure):  
    _fields_ = [("ID", c_uint),             # 帧ID。32位变量，数据格式为靠右对齐。
                ("TimeStamp", c_uint),      # 设备接收到某一帧的时间标识。时间标示从CAN卡上电开始计时，计时单位为0.1ms。
                ("TimeFlag", c_ubyte),      # 是否使用时间标识，为1时TimeStamp有效，TimeFlag和TimeStamp只在此帧为接收帧时有意义。
                # 发送帧类型(二次开发，建议SendType=1，提高发送的响应速度):
                # =0时为正常发送（发送失败会自动重发，重发时间为4秒，4秒内没有发出则取消）；
                # =1时为单次发送（只发送一次，发送失败不会自动重发，总线只产生一帧数据）；
                # 其它值无效。
                ("SendType", c_ubyte),
                ("RemoteFlag", c_ubyte),    # 是否是远程帧。=0时为为数据帧，=1时为远程帧（数据段空）。
                ("ExternFlag", c_ubyte),    # 是否是扩展帧。=0时为标准帧（11位ID），=1时为扩展帧（29位ID）。
                ("DataLen", c_ubyte),       # 数据长度  DLC (<=8)，即CAN帧Data有几个字节。约束了后面Data[8]中的有效字节。
                ("Data", c_ubyte*8),        # CAN帧的数据。
                ("Reserved", c_ubyte*3)     # 系统保留。
                ] 





def main():
    # 获取工作目录
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # CAN收发器dll文件名
    CanDLLName = 'ControlCAN.dll'
    # 加载DLL文件
    CanDLL = windll.LoadLibrary(os.path.join(BASE_DIR,CanDLLName))


    # 打开设备,注意一个设备只能打开一次
    # DWORD __stdcall VCI_OpenDevice(DWORD DevType,DWORD DevIndex,DWORD Reserved); 
    #   DevType:    设备类型
    #   DevIndex:   设备索引，比如当只有一个USB-CAN适配器时，索引号为0，这时再插入一个USB-CAN适
    #               配器那么后面插入的这个设备索引号就是1，以此类推。
    #   Reserved:   保留参数，通常为  0。 
    #   返回值：    返回值=1，表示操作成功； =0表示操作失败； =-1表示USB-CAN设备不存在或USB掉线。
    ret = CanDLL.VCI_OpenDevice(CanDeviceTypeDict["CANalyst-II"], 0, 0)
    if ret != STATUS_OK:
        logging.error('调用 VCI_OpenDevice出错\r\n')

    #初始0通道
    vci_initconfig = VCI_INIT_CONFIG(0x80000008, 0xFFFFFFFF, 
                                    0,  # 保留位
                                    CanFilterMode["RCV_STD_MSG"], 
                                    CanBaudRateDict["500_Kbps"]["BTR0"], 
                                    CanBaudRateDict["500_Kbps"]["BTR1"], 
                                    CanWorkMode["Normal"])
    
    # 初始化指定的CAN通道。有多个CAN通道时，需要多次调用。
    # DWORD __stdcall VCI_InitCAN(DWORD DevType, DWORD DevIndex, DWORD CANIndex, PVCI_INIT_CONFIG pInitConfig);
    #   DevType:    设备类型
    #   DevIndex:   设备索引，比如当只有一个USB-CAN适配器时，索引号为0，这时再插入一个USB-CAN适
    #               配器那么后面插入的这个设备索引号就是1，以此类推。
    #   CANIndex:   CAN通道索引。第几路  CAN。即对应卡的CAN通道号，CAN1为0，CAN2为1。
    #   pInitConfig:    初始化参数结构。
    #   返回值：    返回值=1，表示操作成功； =0表示操作失败； =-1表示USB-CAN设备不存在或USB掉线。
    ret = CanDLL.VCI_InitCAN(CanDeviceTypeDict["CANalyst-II"], 0, 0, byref(vci_initconfig))
    if ret != STATUS_OK:
        logging.error('调用 VCI_InitCAN出错\r\n')


    vci_BoardInfo = VCI_BOARD_INFO()
    # 获取设备信息
    # DWORD __stdcall VCI_ReadBoardInfo(DWORD DevType,DWORD DevIndex,PVCI_BOARD_INFO pInfo);
    #   DevType:    设备类型
    #   DevIndex:   设备索引，比如当只有一个USB-CAN适配器时，索引号为0，这时再插入一个USB-CAN适
    #               配器那么后面插入的这个设备索引号就是1，以此类推。
    #   pInfo       用来存储设备信息的VCI_BOARD_INFO结构指针。
    #   返回值：    返回值=1，表示操作成功； =0表示操作失败； =-1表示USB-CAN设备不存在或USB掉线
    ret = CanDLL.VCI_ReadBoardInfo(CanDeviceTypeDict["CANalyst-II"], 0, vci_BoardInfo)
    if ret != STATUS_OK:
        logging.error('调用 VCI_ReadBoardInfo出错\r\n')
    else:
        logging.info(str(vci_BoardInfo.hw_Version))
        pass

    # 此函数用以复位  CAN。主要用与 VCI_StartCAN配合使用，无需再初始化，即可恢复CAN卡的正常状态。
    # 比如当CAN卡进入总线关闭状态时，可以调用这个函数。
    # DWORD __stdcall VCI_ResetCAN(DWORD DevType,DWORD DevIndex,DWORD CANIndex);
    #   DevType:    设备类型
    #   DevIndex:   设备索引，比如当只有一个USB-CAN适配器时，索引号为0，这时再插入一个USB-CAN适
    #               配器那么后面插入的这个设备索引号就是1，以此类推。
    #   CANIndex:   CAN通道索引。第几路  CAN。即对应卡的CAN通道号，CAN1为0，CAN2为1。
    #   返回值：    返回值=1，表示操作成功； =0表示操作失败； =-1表示USB-CAN设备不存在或USB掉线。
    ret = CanDLL.VCI_ResetCAN(CanDeviceTypeDict["CANalyst-II"], 0, 0)
    if ret != STATUS_OK:
        logging.error('调用 VCI_ResetCAN出错\r\n')


    # 此函数用以清空指定CAN通道的缓冲区。主要用于需要清除接收缓冲区数据的情况,同时发送缓冲区数据也会一并清除。
    # DWORD __stdcall VCI_ClearBuffer(DWORD DevType,DWORD DevIndex,DWORD CANIndex);
    #   DevType:    设备类型
    #   DevIndex:   设备索引，比如当只有一个USB-CAN适配器时，索引号为0，这时再插入一个USB-CAN适
    #               配器那么后面插入的这个设备索引号就是1，以此类推。
    #   CANIndex:   CAN通道索引。第几路  CAN。即对应卡的CAN通道号，CAN1为0，CAN2为1。
    #   返回值：    返回值=1，表示操作成功； =0表示操作失败； =-1表示USB-CAN设备不存在或USB掉线。
    ret = CanDLL.VCI_ClearBuffer(CanDeviceTypeDict["CANalyst-II"], 0, 0)
    if ret != STATUS_OK:
        logging.error('调用 VCI_ClearBuffer出错\r\n')

    # 此函数用以启动CAN卡的某一个CAN通道。有多个CAN通道时，需要多次调用。
    # DWORD __stdcall VCI_StartCAN(DWORD DevType,DWORD DevIndex,DWORD CANIndex);
    #   DevType:    设备类型
    #   DevIndex:   设备索引，比如当只有一个USB-CAN适配器时，索引号为0，这时再插入一个USB-CAN适
    #               配器那么后面插入的这个设备索引号就是1，以此类推。
    #   CANIndex:   CAN通道索引。第几路  CAN。即对应卡的CAN通道号，CAN1为0，CAN2为1。
    #   返回值：    返回值=1，表示操作成功； =0表示操作失败； =-1表示USB-CAN设备不存在或USB掉线。
    ret = CanDLL.VCI_StartCAN(CanDeviceTypeDict["CANalyst-II"], 0, 0)
    if ret != STATUS_OK:
        logging.error('调用 VCI_StartCAN出错\r\n')


    # 此函数用以获取指定CAN通道的接收缓冲区中，接收到但尚未被读取的帧数量。主要用途是配合VCI_Receive使用，即缓冲区有数据，再接收。
    # 实际应用中， 用户可以忽略该函数，直接循环调用VCI_Receive，可以节约PC系统资源，提高程序效率。 
    # DWORD __stdcall VCI_GetReceiveNum(DWORD DevType,DWORD DevIndex,DWORD CANIndex); 
    #   DevType:    设备类型
    #   DevIndex:   设备索引，比如当只有一个USB-CAN适配器时，索引号为0，这时再插入一个USB-CAN适
    #               配器那么后面插入的这个设备索引号就是1，以此类推。
    #   CANIndex:   CAN通道索引。第几路  CAN。即对应卡的CAN通道号，CAN1为0，CAN2为1。
    #   返回值：    返回尚未被读取的帧数，=-1表示USB-CAN设备不存在或USB掉线。 
    ret = CanDLL.VCI_GetReceiveNum (CanDeviceTypeDict["CANalyst-II"], 0, 0)
    if ret == STATUS_ERR:
        logging.error('调用 VCI_GetReceiveNum出错\r\n')

    # CAN数据发送函数。返回值为实际发送成功的帧数。
    # DWORD __stdcall VCI_Transmit(DWORD DeviceType,DWORD DeviceInd,DWORD CANInd,PVCI_CAN_OBJ pSend,DWORD Length); 
    #   DevType:    设备类型
    #   DevIndex:   设备索引，比如当只有一个USB-CAN适配器时，索引号为0，这时再插入一个USB-CAN适
    #               配器那么后面插入的这个设备索引号就是1，以此类推。
    #   CANIndex:   CAN通道索引。第几路  CAN。即对应卡的CAN通道号，CAN1为0，CAN2为1。
    #   pSend:      要发送的帧结构体 VCI_CAN_OBJ数组的首指针。
    #   Length:     要发送的帧结构体数组的长度（发送的帧数量）。最大为1000，建议设为1，每次发送单帧，以提高发送效率。
    #   返回值：    返回实际发送的帧数，=-1表示USB-CAN设备不存在或USB掉线。
    ubyte_array = c_ubyte*8
    a = ubyte_array(1,2,3,4, 5, 6, 7, 64)
    ubyte_3array = c_ubyte*3
    b = ubyte_3array(0, 0 , 0)
    vci_can_obj = VCI_CAN_OBJ(0x0, 0, 0, 1, 0, 0,  8, a, b)
    '''
    ret = CanDLL.VCI_Transmit(CanDeviceTypeDict["CANalyst-II"], 0, 0, byref(vci_can_obj), 1)
    if ret != STATUS_OK:
        print('调用 VCI_Transmit 出错\r\n')
    '''


    # 接收函数。此函数从指定的设备CAN通道的接收缓冲区中读取数据。
    # DWORD __stdcall VCI_Receive(DWORD DevType, DWORD DevIndex, DWORD  CANIndex, PVCI_CAN_OBJ pReceive, ULONG Len, INT WaitTime); 
    #   DevType:    设备类型
    #   DevIndex:   设备索引，比如当只有一个USB-CAN适配器时，索引号为0，这时再插入一个USB-CAN适
    #               配器那么后面插入的这个设备索引号就是1，以此类推。
    #   CANIndex:   CAN通道索引。第几路  CAN。即对应卡的CAN通道号，CAN1为0，CAN2为1。
    #   pReceive:   用来接收的帧结构体VCI_CAN_OBJ数组的首指针。注意：数组的大小一定要比下面的len参数大，否则会出现内存读写错误。
    #   Len:        用来接收的帧结构体数组的长度（本次接收的最大帧数，实际返回值小于等于这个值）。该值为所提供的存储空间大小，
    #               适配器中为每个通道设置了2000帧左右的接收缓存区，用户根据自身系统和工作环境需求，在1到2000之间选取适当的接收数组长度。
    #               。一般pReceive数组大小与Len都设置大于2000，如：2500为宜，可有效防止数据溢出导致地址冲突。
    #               同时每隔30ms调用一次VCI_Receive为宜。
    #   WaitTime:   保留参数。
    #   返回值：    返回实际读取的帧数，=-1表示USB-CAN设备不存在或USB掉线。
    a = ubyte_array(0, 0, 0, 0, 0, 0, 0, 0)
    vci_can_obj = VCI_CAN_OBJ(0x0, 0, 0, 1, 0, 0,  8, a, b)

    import time
    # 接收单数据方法
    ret = CanDLL.VCI_Receive(CanDeviceTypeDict["CANalyst-II"], 0, 0, byref(vci_can_obj), 1, 0)
    while ret <= 0:
        time.sleep(1)
        print('调用 VCI_Receive 出错\r\n')
        ret = CanDLL.VCI_Receive(CanDeviceTypeDict["CANalyst-II"], 0, 0, byref(vci_can_obj), 1, 0)
    if ret > 0:
        Msg = []
        print(hex(vci_can_obj.ID))
        print(vci_can_obj.DataLen)
        # print(list(vci_can_obj.Data))
        for i in list(vci_can_obj.Data):
            Msg.append(hex(i))
        print(Msg)
    
    # 接收多数据方法
    vci_can_obj_array = VCI_CAN_OBJ*5
    c = vci_can_obj_array()
    while True:
        ret = CanDLL.VCI_Receive(CanDeviceTypeDict["CANalyst-II"], 0, 0, (c), 5, 0)
        if ret > 0:
            for j in range(ret):
                Msg = []
                print(hex(c[j].ID))
                print(c[j].DataLen)
                for i in list(c[j].Data):
                    Msg.append(hex(i))
                print(Msg)
        else:
            break
        
        
    # 关闭CAN设备。
    # DWORD __stdcall VCI_CloseDevice(DWORD DevType,DWORD DevIndex); 
    #   DevType :   设备类型
    #   DevIndex:   设备索引，比如当只有一个USB-CAN适配器时，索引号为0，这时再插入一个USB-CAN适
    #               配器那么后面插入的这个设备索引号就是1，以此类推。
    #   返回值：    返回值=1，表示操作成功； =0表示操作失败； =-1表示USB-CAN设备不存在或USB掉线。
    CanDLL.VCI_CloseDevice(CanDeviceTypeDict["CANalyst-II"], 0)



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

















