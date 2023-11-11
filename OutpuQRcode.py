import qrcode
# 要生成QR码的数据
data = "Hello, QR Code!"

# 指定所需的实际大小（以毫米为单位）
width_mm = 100  # 宽度
height_mm = 100  # 高度

# 计算QR码的模块大小（像素/模块）
dpi = 100  # 分辨率（每英寸的像素数）
width_px = int(width_mm * dpi / 25.4)  # 将毫米转换为像素
height_px = int(height_mm * dpi / 25.4)

# 创建QR码对象
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,  # 初始模块大小（可调整）
    border=4,
)

# 添加数据到QR码对象
qr.add_data(data)
qr.make(fit=True)

# 创建QR码图像
img = qr.make_image(fill_color="black", back_color="white")

# 调整图像大小以匹配所需的实际大小
img = img.resize((width_px, height_px))

# 保存QR码图像
img.save("my_qr_code.png")