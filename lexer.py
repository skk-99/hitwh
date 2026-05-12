#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os

file_name = ""  # 全局变量

KEYWORD_LIST = [
    "if",
    "else",
    "while",
    "int",
    "float"
]

SEPARATOR_LIST = ["(", ")", "'", ";"]

OPERATOR_LIST = [
    "+",
    "-",
    "*",
    "/",
    ">",
    "<",
    ">=",
    "<=",
    "=",
    "==",
    "!="
]

current_row = -1
current_line = 0
input_str = []
symbol_table = []
token_list = []

def addto_symbol(name):
    for sym in symbol_table:
        if sym['name'] == name:
            return
    symbol_table.append({'name': name, 'kind': '变量'})

def is_keyword(s):
    return s in KEYWORD_LIST


def is_separator(s):
    return s in SEPARATOR_LIST


def is_operator(s):
    return s in OPERATOR_LIST



def getchar():
    global current_row
    global current_line
    current_row += 1

    if current_row == len(input_str[current_line]):
        current_line += 1
        current_row = 0

    if current_line == len(input_str):
        return "SCANEOF"

    return input_str[current_line][current_row]


def ungetc():
    global current_row
    global current_line
    current_row = current_row - 1
    if current_row < 0:
        current_line = current_line - 1
        current_row = len(input_str[current_row]) - 1
    return input_str[current_line][current_row]


def read_source_file(file):
    global input_str
    f = open(file, "r")
    input_str = f.readlines()
    f.close()


def lexical_error(msg, line=None, row=None):
    if line is None:
        line = current_line + 1
    if row is None:
        row = current_row + 1
    print(str(line) + ":" + str(row) + " Lexical error: " + msg)


def scanner():
    current_char = getchar()
    if current_char == "SCANEOF":
        return ("SCANEOF", "", "")
    if current_char.strip() == "":
        return
    # 整数
    if current_char.isdigit():
        int_value = 0
        while current_char.isdigit():
            int_value = int_value * 10 + int(current_char)
            current_char = getchar()
        ungetc()
        token = ("常数", str(int_value), current_line + 1)
        token_list.append(token)
        return token
    # 标识符
    if current_char.isalpha() or current_char == "_":
        string = ""
        while current_char.isalpha() or current_char.isdigit() or current_char == "_":
            string += current_char
            current_char = getchar()
            if current_char == "SCANEOF":
                break

        ungetc()
        if is_keyword(string):
            token = ("关键字", string, current_line + 1)
        else:
            token = ("标识符", string, current_line + 1)
            addto_symbol(string)

        token_list.append(token)
        return token
    # 运算符
    if current_char in [">", "<", "=", "!"]:
        op = current_char
        next_char = getchar()
        if next_char == "=":
            op += "="
        else:
            ungetc()
        if is_operator(op):
            token = ("运算符", op, current_line + 1)
            token_list.append(token)
            return token
        else:
            lexical_error(f"unknown operator: {op}")
            return None

    if current_char in ["+", "-", "*", "/"]:
        token = ("运算符", current_char, current_line + 1)
        token_list.append(token)
        return token

    if is_separator(current_char):
        token = ("分隔符", current_char, current_line + 1)
        token_list.append(token)
        return token

    lexical_error(f"unknown character: '{current_char}'")
    return None

def savefile(filename = "token_output.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write("           TOKEN 串表\n")
        f.write("=" * 50 + "\n")
        f.write(f"{'序号':<6} {'类型':<10} {'值':<12} {'行号':<6}\n")
        f.write("-" * 50 + "\n")
        for i, t in enumerate(token_list):
            f.write(f"{i+1:<6} {t[0]:<10} {t[1]:<12} {t[2]:<6}\n")

        f.write("\n" + "=" * 40 + "\n")
        f.write("           符 号 表\n")
        f.write("=" * 40 + "\n")
        f.write(f"{'序号':<6} {'名字':<12} {'种类':<10}\n")
        f.write("-" * 40 + "\n")
        for i, s in enumerate(symbol_table):
            f.write(f"{i+1:<6} {s['name']:<12} {s['kind']:<10}\n")
        f.write("=" * 40 + "\n")

    print(f"\n结果已保存到 {filename}")

def main():
    global file_name

    print("=" * 50)
    print("     类C语言词法扫描器")
    print("=" * 50)
    print("请输入源代码（每行以分号结束，输入空行结束输入）：")

    global input_str
    input_str = []
    line_num = 1
    while True:
        line = input(f"{line_num}: ")
        if line.strip() == "":
            break
        input_str.append(line + "\n")
        line_num += 1

    file_name = "console_input"

    print("\n开始词法分析...")
    print("-" * 50)

    while True:
        r = scanner()
        if r is not None:
            if r[0] == "SCANEOF":
                break
            print(f"{r[0]:<10} {r[1]:<12} (行{r[2]})")

    print("-" * 50)
    print(f"分析完成，共 {len(token_list)} 个Token，{len(symbol_table)} 个符号表项。")

    savefile()

if __name__ == "__main__":
    main()