import re
from enum import Enum


class TokenStyle(Enum):
    KEY_WORD = 0
    IDENTIFIER = 1
    DIGIT_CONSTANT = 2
    OPERATOR = 3
    SEPARATOR = 4
    STRING_CONSTANT = 5


DETAIL_TOKEN_STYLE = {
    'include': 'INCLUDE',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'double': 'DOUBLE',
    'for': 'FOR',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'return': 'RETURN',
    '=': 'ASSIGN',
    '&': 'ADDRESS',
    '<': 'LT',
    '>': 'GT',
    '++': 'SELF_PLUS',
    '--': 'SELF_MINUS',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MUL',
    '/': 'DIV',
    '>=': 'GET',
    '<=': 'LET',
    '(': 'LL_BRACKET',
    ')': 'RL_BRACKET',
    '{': 'LB_BRACKET',
    '}': 'RB_BRACKET',
    '[': 'LM_BRACKET',
    ']': 'RM_BRACKET',
    ',': 'COMMA',
    '"': 'DOUBLE_QUOTE',
    ';': 'SEMICOLON',
    '#': 'SHARP',
}

keywords = [
    ['int', 'float', 'double', 'char', 'void'],
    ['if', 'for', 'while', 'do', 'else'], ['include', 'return'],
]

# operators
operators = [
    '=', '&', '<', '>', '++', '--', '+', '-', '*', '/', '>=', '<=', '!='
]

# delimiters
delimiters = ['(', ')', '{', '}', '[', ']', ',', '\"', ';']


def is_blank(char):
    return char == ' ' or char == '\t' or char == '\n' or char == '\r'


def is_keyword(str):
    for item in keywords:
        if str in item:
            return True
    return False


class Token(object):
    def __init__(self, style, value):
        self.style = DETAIL_TOKEN_STYLE[value] if style is TokenStyle.KEY_WORD or \
                                                  style is TokenStyle.OPERATOR or \
                                                  style is TokenStyle.SEPARATOR else style.name
        self.value = value
        print('Token {}: <style> {} <value> {}'.format(self, self.style + (16 - len(self.style)) * ' ', self.value))


def lexer(str):
    tokens = []
    lens = len(str)

    def next(index):
        while index < lens and is_blank(str[index]):
            index += 1
        return index

    i = 0
    while i < lens:
        # process '#'
        if str[i] == '#':
            tokens.append(Token(TokenStyle.SEPARATOR, str[i]))
            i = next(i + 1)
            while i < lens:
                # match 'include'
                if re.match('include', str[i:]):
                    tokens.append(Token(TokenStyle.KEY_WORD, 'include'))
                    i = next(i + 7)
                # match " or <
                elif str[i] == '\"' or str[i] == '<':
                    tokens.append(Token(TokenStyle.SEPARATOR, str[i]))
                    i = next(i + 1)
                    close_flag = '\"' if str[i] == '\"' else '>'
                    lib = ''
                    while str[i] != close_flag:
                        lib += str[i]
                        i += 1
                    tokens.append(Token(TokenStyle.IDENTIFIER, lib))
                    tokens.append(Token(TokenStyle.SEPARATOR, close_flag))
                    i = next(i + 1)
                    break  # important
                else:
                    print('compile error: include error.')
                    exit()

        # process alpha or '_'
        elif str[i].isalpha() or str[i] == '_':
            temp = ''
            while i < lens and (str[i].isalpha() or str[i] == '_' or str[i].isdigit()):
                temp += str[i]
                i += 1
            if is_keyword(temp):
                tokens.append(Token(TokenStyle.KEY_WORD, temp))
            else:
                tokens.append(Token(TokenStyle.IDENTIFIER, temp))
            i = next(i)
        # process digit
        elif str[i].isdigit():
            temp = ''
            while i < lens:
                if str[i].isdigit() or (str[i] == '.' and str[i + 1].isdigit()):
                    temp += str[i]
                    i += 1
                elif str[i] == ';':
                    break
                else:
                    print('compile error: wrong number format.')
                    exit()
                tokens.append(Token(TokenStyle.DIGIT_CONSTANT, temp))
                i = next(i)
        # process separator
        elif str[i] in delimiters:
            tokens.append(Token(TokenStyle.SEPARATOR, str[i]))
            # if is a string
            if str[i] == '\"':
                i += 1
                temp = ''
                while i < lens:
                    if str[i] != '\"':
                        temp += str[i]
                        i += 1
                    else:
                        break
                else:
                    print('compile error: lack of \"')
                    exit()
                tokens.append(Token(TokenStyle.STRING_CONSTANT, temp))
                tokens.append(Token(TokenStyle.SEPARATOR, '\"'))
            i = next(i + 1)
        # process operator
        elif str[i] in operators:
            # ++ or --
            if (str[i] == '+' or str[i] == '-') and (str[i + 1] == str[i]):
                tokens.append(Token(TokenStyle.OPERATOR, str[i] * 2))
                i = next(i + 2)
            # >= or <=
            elif (str[i] == '>' or str[i] == '<') and str[i + 1] == '=':
                tokens.append(Token(TokenStyle.OPERATOR, str[i] + '='))
                i = next(i + 2)
            else:
                tokens.append(Token(TokenStyle.OPERATOR, str[i]))
                i = next(i + 1)
    return tokens
