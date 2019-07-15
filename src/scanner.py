#!/usr/bin/env python
# -*- coding: utf-8 -*-


import ply.lex as lex


class Scanner(object):
    def find_column(self, token):
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)

        if last_cr < 0:
            last_cr = 0

        column = (token.lexpos - last_cr) + 1

        return column

    def build(self):
        self.lexer = lex.lex(object=self)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()

    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',
        'zeros': 'ZEROS',
        'ones': 'ONES',
        'eye': 'EYE',
        'print': 'PRINT'
    }

    tokens = [
        'DOTADD',
        'DOTSUB',
        'DOTMUL',
        'DOTDIV',
        'ADDASSIGN',
        'SUBASSIGN',
        'MULASSIGN',
        'DIVASSIGN',
        'NEQ',
        'GEQ',
        'LEQ',
        'EQ',
        'INTNUM',
        'FLOAT',
        'ID',
        'STRING',
    ]

    tokens += list(reserved.values())

    t_DOTADD = r'\.\+'
    t_DOTSUB = r'\.\-'
    t_DOTMUL = r'\.\*'
    t_DOTDIV = r'\.\/'

    t_ADDASSIGN = r'\+\='
    t_SUBASSIGN = r'\-\='
    t_MULASSIGN = r'\*\='
    t_DIVASSIGN = r'\/\='

    t_NEQ = r'\!\='
    t_GEQ = r'\>\='
    t_LEQ = r'\<\='
    t_EQ = r'\=\='

    t_ignore = ' \t'

    literals = "+-*/(){}[],;'=:<>"

    def t_FLOAT(self, t):
        r"(\d*\.\d+(e[+-]\d+)?)|(\d+\.)"

        t.value = float(t.value)
        return t

    def t_INTNUM(self, t):
        r'\d+'
        t.value = int(t.value)

        return t

    def t_ID(self, t):
        r'[a-zA-Z_]\w*'
        t.type = self.reserved.get(t.value, 'ID')

        return t

    def t_STRING(self, t):
        r"\"(.*)+\""
        t.value = str(t.value)

        return t

    def t_COMMENT(self, t):
        r'\#.*'
        pass

    def t_newline(self, t):
        r'\n+'

        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
