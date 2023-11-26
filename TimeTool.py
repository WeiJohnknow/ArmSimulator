from datetime import datetime
import numpy as np

class TimeTool:
    def __init__(self) -> None:
        pass

    def ReadNowTime(self):
        # 讀取現在系統時間
        Now_time = datetime.now()
        # 年
        year = Now_time.year
        # 月
        month = Now_time.month
        # 日
        day = Now_time.day
        # 時
        hour = Now_time.hour    
        # 分
        minute = Now_time.minute
        # 秒
        second = Now_time.second
        # 毫秒
        millisecond = Now_time.microsecond//1000
        # 微秒
        microsecond = Now_time.microsecond
        
        # return [year, month, day, hour, minute, second, millisecond, microsecond]
        return millisecond
    
    def TimeError(self, Before, After):
        '''
        注意計算時單位要相等
        ex: second-second
        '''
        if After < Before:
            # ms已進位
            After += 1000
            Ans = After - Before
        else:
            Ans = After - Before
        
        return Ans
    
# test
# T = TimeTool()
# err = T.TimeError(999, 0)
# print(err)

