import numpy as np
import csv

# 初始化一个 1x3 的 NumPy 数组
initial_array = np.array([[1, 2, 3]])
header = np.array([['Xx', 'Xy', 'Xz', 'Yx', 'Yy', 'Yz', 'Zx', 'Zy', 'Zz', 'Px', 'Py', 'Pz']])
# 打开 CSV 文件以进行写入（如果不存在会自动创建）
with open('example_update.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    if file.tell() == 0:
        writer.writerows(header)

    # 将初始化数组写入 CSV 文件的一行
    writer.writerow(initial_array.flatten())
    
    # 模拟更新数组的过程
    for _ in range(5):
        # 这里模拟更新数组的过程，你可以根据你的实际需求更新数组的值
        updated_array = np.random.randint(1, 10, (1, 3))

        # 将更新后的数组写入新行
        writer.writerow(updated_array.flatten())

print("CSV file with updated arrays has been written.")