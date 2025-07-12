# MD5-Checker

**Description:** 

MD5 CHecker是一个用于计算并校验文件MD5值的小工具，它基于Python实现。

开发过程中使用了以下库
```
hashlib
```
```
argparse
```
```
os
```
```
sys
```
```
typing
```

**使用实例：**

计算文件MD5：
```bash
python main.py calc test.txt
```

验证文件：
```bash
python main.py verify test.txt d41d8cd98f00b204e9800998ecf8427e
```

生成校验文件：
```bash
python main.py gen ./project -o project.md5
```

批量验证：
```
python main.py check project.md5
```

如果它帮到了你，还请赏个star喵~
