#!/usr/bin/python
# -*- coding: utf-8 -*-

import ply.yacc as yacc
from scanner import Scanner
from AST import *


class Mparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ('left', ','),
        ('right', '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
        ("left", "EQ", "NEQ"),
        ("left", "<", ">", "LEQ", "GEQ"),
        ("left", '+', '-', 'DOTADD', 'DOTSUB'),
        ('left', '*', '/', 'DOTMUL', 'DOTDIV'),
        ('right', 'UMINUS'),
    )

    def p_error(self, p):
        if p:
            error_type = "Syntax error at line " + \
                "{0}, pos {1}: LexToken({2}, '{3}')""".format(
                p.lineno, self.scanner.find_column(p), p.type, p.value)
        else:
            error_type = "Unexpected end of input"

        raise Exception

    def p_program(self, p):
        """program : instructions_opt"""

        p[0] = Program(p[1], line_no=p.lineno)

    def p_instructions_opt_1(self, p):
        """instructions_opt : instructions """

        p[0] = InstructionsOpt(p[1], line_no=p.lineno)

    def p_instructions_opt_2(self, p):
        """instructions_opt : """

    def p_instructions_1(self, p):
        """instructions : instructions instruction """

        p[0] = p[1] + [p[2]]

    def p_instructions_2(self, p):
        """instructions : instruction """

        p[0] = [p[1]]

    def p_instruction(self, p):
        """instruction : inst ';'
                       | condition 
                       | expr ';' 
                       | inst ','
                       | expr ',' """

        p[0] = p[1]

    def p_inst_assign(self, p):
        """inst : ids '=' expr
                | ids ADDASSIGN expr
                | ids SUBASSIGN expr
                | ids MULASSIGN expr
                | ids DIVASSIGN expr """
        
        p[0] = Assign(p[1], p[2], p[3], line_no=p.lineno(2))

    def p_ids(self, p):
        """ids : ID
               | ID '[' values ']' """

        if len(p) <= 2:
            p[0] = Variable(p[1], line_no=p.lineno(1))
        else:
            p[0] = Variable(p[1], p[3], line_no=p.lineno(1))

    def p_break(self, p):
        """inst : BREAK """

        p[0] = Instruction(p[1], line_no=p.lineno(1))

    def p_continue(self, p):
        """inst : CONTINUE """

        p[0] = Instruction(p[1], line_no=p.lineno(1))

    def p_return(self, p):
        """inst : RETURN
                | RETURN values 
                | RETURN expr """

        value = None

        if len(p) > 2:
            value = p[2]

        p[0] = Instruction(p[1], value, line_no=p.lineno(1))

    def p_print(self, p):
        """inst : PRINT values
                | PRINT expr """

        p[0] = Instruction(p[1], p[2], line_no=p.lineno(1))

    def p_expr_binary(self, p):
        """expr : expr '+' expr
                | expr '-' expr
                | expr '*' expr
                | expr '/' expr """

        p[0] = BinExpr(p[2], p[1], p[3], line_no=p.lineno(2))

    def p_expr_elementwise(self, p):
        """expr : expr DOTADD expr
                | expr DOTSUB expr
                | expr DOTMUL expr
                | expr DOTDIV expr """

        p[0] = BinExpr(p[2], p[1], p[3], line_no=p.lineno(2))

    def p_expr_eq(self, p):
        """expr : expr EQ expr
                | expr GEQ expr
                | expr LEQ expr
                | expr NEQ expr
                | expr '<' expr
                | expr '>' expr"""

        p[0] = Equality(p[2], p[1], p[3], line_no=p.lineno(2))

    def p_expr_paren(self, p):
        """expr : '(' expr ')' """

        p[0] = p[2]

    def p_expr_transpose(self, p):
        """expr : expr "'" """

        p[0] = Transpose(p[2], p[1], line_no=p.lineno(2))

    def p_expr_negative(self, p):
        """expr : '-' expr %prec UMINUS"""

        p[0] = Negation(p[2], line_no=p.lineno(1))

    def p_expr(self, p):
        """expr : ids
                | integer
                | float
                | string
                | matrix """

        p[0] = p[1]

    def p_integer(self, p):
        """integer : INTNUM """

        p[0] = IntNum(p[1], line_no=p.lineno(1))

    def p_float(self, p):
        """float : FLOAT """

        p[0] = FloatNum(p[1], line_no=p.lineno(1))

    def p_string(self, p):
        """string : STRING """

        p[0] = String(p[1], line_no=p.lineno(1))

    def p_matrix_operations(self, p):
        """matrix : ZEROS '(' values ')'
                  | ONES '(' values ')'
                  | EYE '(' values ')' """

        p[0] = MatrixOperation(p[1], p[3], line_no=p.lineno(1))

    def p_matrix_init(self, p):
        """matrix : '[' rows ']'
                  | '[' rows ';' ']' """

        p[0] = Matrix(p[2], line_no=p.lineno(1))

    def p_rows(self, p):
        """rows : values """

        p[0] = [p[1]]

    def p_rows_2(self, p):
        """rows : rows ';' values """

        p[0] = p[1] + [p[3]]

    def p_values(self, p):
        """values : expr """

        p[0] = [p[1]]

    def p_values_2(self, p):
        """values : values ',' expr """

        p[0] = p[1] + [p[3]]

    def p_block(self, p):
        """ block : '{' instructions_opt '}' """

        p[0] = p[2]

    def p_block_2(self, p):
        """ block : instruction """

        p[0] = InstructionsOpt([p[1]], line_no=p.lineno)

    def p_conditional(self, p):
        """ condition : if_condition
                      | for_condition
                      | while_condition """

        p[0] = p[1]

    def p_if(self, p):
        """ if_condition : if_cond"""

        p[0] = p[1]

    def p_if_2(self, p):
        """ if_condition : if_cond ELSE block"""

        p[0] = p[1]
        p[0].else_block = p[3]

    def p_if_3(self, p):
        """ if_condition : if_cond ELSE if_condition"""

        p[0] = p[1]
        p[0].else_cond = p[3]

    def p_if_cond(self, p):
        """ if_cond : IF '(' expr ')' block """

        p[0] = IfCondition(p[3], p[5], line_no=p.lineno)

    def p_for(self, p):
        """ for_condition : FOR ids '=' range block """

        p[0] = ForCondition(p[2], p[4], p[5], line_no=p.lineno(3))

    def p_range(self, p):
        """ range : expr ':' expr """

        p[0] = Range(p[1], p[3], line_no=p.lineno(2))

    def p_while(self, p):
        """ while_condition : WHILE '(' expr ')' block """

        p[0] = WhileCondition(p[3], p[5], line_no=p.lineno(1))
