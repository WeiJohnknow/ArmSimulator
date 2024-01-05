x = 4294966045

# 判斷是否為負數
if x & (1 << 31):
    x -= 1 << 32
print(x)

for i in range(256):
    high = i >> 8
    Low = i - (high << 8)

    # 有號 無號 映射
    if Low > 127:
        Low = -(255 - (Low-1))
    print(i, Low)

    
# 'YERC \x00\x04\x00\x03\x01\x00\x00\x00\x00\x00\x0099999999\x83\x00\x02\x00\x01\x10\x00\x00\x01\x00\x00\x00'
# b'YERC \x00\x04\x00\x03\x01\x00\x00\x00\x00\x00\x0099999999\xc2\x83\x00\x02\x00\x01\x10\x00\x00\x01\x00\x00\x00'
# b'YERC \x00\x04\x00\x03\x01\x00\x00\x00\x00\x00\x0099999999\x83\x00\x02\x00\x01\x10\x00\x00\x01\x00\x00\x00'


# b'YERC \x00\x04\x00\x03\x01\x00\x00\x00\x00\x00\x0099999999\x83\x83\x02\x00\x01\x10\x00\x00\x01\x00\x00\x00'



# Hex = 'YERC \x00\x04\x00\x03\x01\x00\x00\x00\x00\x00\x0099999999\x83\x00\x02\x00\x01\x10\x00\x00\x01\x00\x00\x00'
# byte_data = bytes.fromhex(Hex)
# print(Hex.encode("ascii"))
# print(Hex)