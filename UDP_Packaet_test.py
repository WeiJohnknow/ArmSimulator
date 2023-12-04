

# UDP Packet 

def pack_Pocket():

    pass
# Packet Format

# Request Packet(Read Control)
Identifier = 'YERC'
Data_size = [0x0020, 0x0000]
Reserve_1 = [3, 1, 0x00, 0x00]
Block_No =  [0, 0, 0, 0]
Reserve_2 = '99999999'
Sub_header = [0x0072, 0x0001, 0x00, 0x01, 0x0000]

# 定義格式
format_string = '>4sHHBBII8sHHHH'
# chr(65)  把65轉成Unicode = 'A' 
chr(Identifier)

# 轉UTF-8 
# text_data = 'YERC'
# utf8_data = text_data.encode('utf-8')

"""
ASCII（American Standard Code for Information Interchange）:

    ASCII 是一種最早的字符編碼標準，僅使用7位二進制數（後來擴展為8位，稱為Extended ASCII）。
    ASCII 主要定義了英文字母、數字、標點符號和一些控制字符的二進制表示。
    ASCII 編碼是單字節編碼，每個字符使用一個字節。

Unicode:

    Unicode 是一種字符集，它為世界上大多數字符提供了唯一的數字標識。
    Unicode 包括了許多不同的編碼方案，其中最常見的是UTF-8、UTF-16和UTF-32。
    Unicode 編碼可以表示世界上的大多數字符，包括不同語言、符號和表情符號。

UTF-8（Unicode Transformation Format-8）:

    UTF-8 是 Unicode 編碼的一種實現方式，它使用不同數目的字節表示字符。
    UTF-8 是一種變長編碼，基本上可以表示任何Unicode字符，同時保持了對ASCII的向後兼容性。
    UTF-8 中的英文字母和ASCII字符使用一個字節表示，其他字符可能使用多個字節。

註:
字符（Character）:

    1.一個字符通常指的是文本中的一個單一字符，如字母、數字、標點符號等。
    2.在計算機中，字符通常使用編碼方式（如ASCII、UTF-8等）表示，每個字符被映射到一個或多個位元（bits）。
    3.一個常見的字符在ASCII編碼下使用7或8位表示，而在UTF-8等多字節編碼下可能使用更多位。

字節（Byte）:
    1.一個字節是計算機存儲的基本單位，通常由8個位元組成。
    2.字節是計算機中數據的基本單位，存儲二進制數據。
    3.字節可用於存儲字符數據，但它也可以表示其他數據，如圖像、音頻、二進制文件等。

字串（string）是由字符構成的
字節串（bytes）是由字節構成的

"""