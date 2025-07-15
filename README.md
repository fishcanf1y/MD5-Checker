# MD5-Checker

**Description:** 

MD5 Checker是一个用于计算并校验文件MD5值的小工具，它基于Python实现。

# 功能
- 计算文件MD5值
- 验证文件MD5值
- 生成目录的MD5校验文件
- 验证MD5校验文件
- updating...

# 安装
```bash
git clone https://github.com/fishcanf1y/MD5-Checker.git
# 无第三方库，无需进行 pip install -r requirements.txt 确保python version >= 3.7
```

# 使用方法
```bash
Workspace> python .\main.py -h                                                                                                 
usage: main.py [-h] {calc,verify,gen,check} ...

MD5校验工具

positional arguments:
  {calc,verify,gen,check}
                        子命令
    calc                计算文件MD5值
    verify              验证文件MD5值
    gen                 生成目录的MD5校验文件
    check               验证MD5校验文件

options:
  -h, --help            show this help message and exit

使用示例:
  计算MD5:  main.py calc file.txt
  验证文件: main.py verify file.txt d41d8cd98f00b204e9800998ecf8427e
  生成校验: main.py gen ./directory
  验证校验: main.py check checksums.md5
```

# 使用实例

**计算文件MD5:**
```bash
python main.py calc test.txt
```

**验证文件:**
```bash
python main.py verify test.txt d41d8cd98f00b204e9800998ecf8427e
```

**生成校验文件:**
```bash
python main.py gen ./project -o project.md5
```

**批量验证:**
```
python main.py check project.md5
```
# TODO
- [ ] 支持更多哈希算法(当前仅支持`MD5`,可以扩展支持`SHA-1`, `SHA-256`, `SHA-512`, `Blake2`等算法)
- [ ] 多线程/多进程加速
- [ ] 生成/验证 SFV 或 JSON 格式
- [ ] API 服务：用 Flask 提供 HTTP 接口，远程调用哈希计算。
- [ ] 彩色终端输出, 使用颜色区分成功/失败、警告等信息，提升可读性

以上是暂时想添加的新功能, 欢迎加入一起改进！

如果它帮到了你，还请赏个star喵~

