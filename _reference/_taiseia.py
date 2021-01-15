""" TaiSEIA 101 """
from enum import Enum

ID: H'00
HEX: 0x00
Type: ENUM
name: 電源
關閉: 0
開啟: 1

ID: H'01
HEX: 0x01
Type: ENUM
name: 模式
冷氣: 0
除濕: 1
送風: 2
自動: 3
暖氣: 4

ID: H'02
HEX: 0x02
name: 風速
Type: ENUM
# 0 ~ 15 級
Auto: 0
Min: 1
Max: 5

