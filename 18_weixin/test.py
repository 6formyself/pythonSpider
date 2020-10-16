import re

pattern = re.compile(r"url \+=.*?;")  # 查找数字
result1 = pattern.findall("""
        url += 'http://mp.w';
        url += 'eixin.qq.co';
        url += 'm/s?src=3&t';
        url += 'imestamp=16';
        url += '02492987&ve';
        url += 'r=1&signatu';""")
print(result1)