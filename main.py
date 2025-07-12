#!/usr/bin/env python3
import hashlib
import argparse
import os
import sys
from typing import Dict, List, Optional

# 常量定义
DEFAULT_BLOCK_SIZE = 65536  # 64KB块大小
MD5_FILE_EXTENSION = '.md5'


def calculate_md5(file_path: str, block_size: int = DEFAULT_BLOCK_SIZE) -> Optional[str]:
    """
    计算文件的MD5哈希值
    :param file_path: 文件路径
    :param block_size: 读取块大小(字节)
    :return: MD5字符串(失败返回None)
    """
    if not os.path.isfile(file_path):
        print(f"错误: 文件不存在 - {file_path}", file=sys.stderr)
        return None

    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                md5.update(block)
        return md5.hexdigest()
    except (IOError, PermissionError) as e:
        print(f"错误: 无法读取文件 {file_path} - {str(e)}", file=sys.stderr)
        return None


def batch_calculate_md5(file_list: List[str]) -> Dict[str, Optional[str]]:
    """
    批量计算MD5值
    :param file_list: 文件路径列表
    :return: 字典{文件路径: MD5值}
    """
    return {file_path: calculate_md5(file_path) for file_path in file_list}


def verify_md5(file_path: str, expected_md5: str) -> bool:
    """
    验证文件MD5值
    :param file_path: 文件路径
    :param expected_md5: 预期MD5值
    :return: 是否匹配
    """
    actual_md5 = calculate_md5(file_path)
    if actual_md5 is None:
        return False

    is_match = actual_md5.lower() == expected_md5.lower()
    print(f"文件: {os.path.abspath(file_path)}")
    print(f"预期MD5: {expected_md5.lower()}")
    print(f"实际MD5: {actual_md5.lower()}")
    print(f"验证结果: {'匹配' if is_match else '不匹配'}")
    return is_match


def generate_md5_file(directory: str, output_file: str = None) -> bool:
    """
    生成目录的MD5校验文件
    :param directory: 目录路径
    :param output_file: 输出文件路径(默认: 目录名.md5)
    :return: 是否成功
    """
    if not os.path.isdir(directory):
        print(f"错误: 目录不存在 - {directory}", file=sys.stderr)
        return False

    if output_file is None:
        output_file = os.path.basename(directory.rstrip('/\\')) + MD5_FILE_EXTENSION

    try:
        with open(output_file, 'w', encoding='utf-8') as f_out:
            for root, _, files in os.walk(directory):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    md5 = calculate_md5(file_path)
                    if md5:
                        relative_path = os.path.relpath(file_path, directory)
                        f_out.write(f"{md5} *{relative_path}\n")
        print(f"成功生成校验文件: {os.path.abspath(output_file)}")
        return True
    except IOError as e:
        print(f"错误: 无法写入校验文件 - {str(e)}", file=sys.stderr)
        return False


def verify_md5_file(md5_file: str) -> bool:
    """
    验证MD5校验文件中的所有条目
    :param md5_file: 校验文件路径
    :return: 是否全部验证通过
    """
    if not os.path.isfile(md5_file):
        print(f"错误: 校验文件不存在 - {md5_file}", file=sys.stderr)
        return False

    all_passed = True
    try:
        with open(md5_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # 解析格式: MD5 *文件名 或 MD5 文件名
                parts = line.split(maxsplit=1)
                if len(parts) != 2:
                    print(f"警告: 第{line_num}行格式错误 - {line}", file=sys.stderr)
                    all_passed = False
                    continue

                expected_md5, file_path = parts
                if file_path.startswith('*'):
                    file_path = file_path[1:]

                if not verify_md5(file_path, expected_md5):
                    all_passed = False
    except IOError as e:
        print(f"错误: 读取校验文件失败 - {str(e)}", file=sys.stderr)
        return False

    return all_passed


def setup_argparse() -> argparse.ArgumentParser:
    """配置命令行参数解析"""
    parser = argparse.ArgumentParser(
        description='MD5校验工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""使用示例:
  计算MD5:  %(prog)s calc file.txt
  验证文件: %(prog)s verify file.txt d41d8cd98f00b204e9800998ecf8427e
  生成校验: %(prog)s gen ./directory
  验证校验: %(prog)s check checksums.md5"""
    )

    subparsers = parser.add_subparsers(dest='command', required=True, help='子命令')

    # calc 子命令
    calc_parser = subparsers.add_parser('calc', help='计算文件MD5值')
    calc_parser.add_argument('file', help='目标文件路径')

    # verify 子命令
    verify_parser = subparsers.add_parser('verify', help='验证文件MD5值')
    verify_parser.add_argument('file', help='要验证的文件路径')
    verify_parser.add_argument('md5', help='预期的MD5值')

    # gen 子命令
    gen_parser = subparsers.add_parser('gen', help='生成目录的MD5校验文件')
    gen_parser.add_argument('directory', help='目标目录路径')
    gen_parser.add_argument('-o', '--output', help='输出文件路径')

    # check 子命令
    check_parser = subparsers.add_parser('check', help='验证MD5校验文件')
    check_parser.add_argument('md5_file', help='MD5校验文件路径')

    return parser


def main():
    parser = setup_argparse()
    args = parser.parse_args()

    if args.command == 'calc':
        md5 = calculate_md5(args.file)
        if md5:
            print(md5)
        else:
            sys.exit(1)

    elif args.command == 'verify':
        if not verify_md5(args.file, args.md5):
            sys.exit(1)

    elif args.command == 'gen':
        if not generate_md5_file(args.directory, args.output):
            sys.exit(1)

    elif args.command == 'check':
        if not verify_md5_file(args.md5_file):
            sys.exit(1)


if __name__ == '__main__':
    main()
