import re

hello = "https://wap.che.360.cn/share/h5/detail/1285888"

m = re.match(r"^https://wap.che.360.cn/share/h5/detail/(\d+)$", hello)

print(m.group(1))
