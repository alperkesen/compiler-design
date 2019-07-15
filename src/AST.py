#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Node(object):
    def __init__(self, line_no=None):
        self.line_no = line_no


class IntNum(Node):
    def __init__(self, value, line_no=None):
        super().__init__(line_no)
        self.value = value

    def __repr__(self):
        return str(self.value)


class FloatNum(Node):
    def __init__(self, value, line_no=None):
        super().__init__(line_no)
        self.value = value

    def __repr__(self):
        return str(self.value)


class Variable(Node):
    def __init__(self, name, indices=None, line_no=None):
        super().__init__(line_no)
        self.name = name
        self.indices = indices

    def __repr__(self):
        return str(self.name)


class Matrix(Node):
    def __init__(self, matrix, line_no=None):
        super().__init__(line_no)
        self.matrix = matrix


class BinExpr(Node):
    def __init__(self, op, left, right, line_no=None):
        super().__init__(line_no)
        self.op = op
        self.left = left
        self.right = right


class UnaryExpr(Node):
    def __init__(self, op, expr, line_no=None):
        super().__init__(line_no)
        self.op = op
        self.expr = expr


class String(Node):
    def __init__(self, value, line_no=None):
        super().__init__(line_no)
        self.value = value

    def __repr__(self):
        return str(self.value)


class Instruction(Node):
    def __init__(self, instruction_type, value=None, line_no=None):
        super().__init__(line_no)
        self.instruction_type = instruction_type
        self.value = value


class Assign(Node):
    def __init__(self, pid, assign_type, value, line_no=None):
        super().__init__(line_no)
        self.pid = pid
        self.assign_type = assign_type
        self.value = value


class Equality(BinExpr):
    def __init__(self, op, left, right, line_no=None):
        super().__init__(op, left, right, line_no)


class Negation(Node):
    def __init__(self, value, line_no=None):
        super().__init__(line_no)
        self.value = value


class MatrixOperation(Node):
    def __init__(self, op_type, values, line_no=None):
        super().__init__(line_no)
        self.op_type = op_type
        self.values = values


class Transpose(UnaryExpr):
    def __init__(self, op, expr, line_no=None):
        super().__init__(op, expr, line_no)


class Program(Node):
    def __init__(self, instructions_opt, line_no=None):
        super().__init__(line_no)
        self.instructions_opt = instructions_opt


class InstructionsOpt(Node):
    def __init__(self, instructions, line_no=None):
        super().__init__(line_no)
        self.instructions = instructions


class IfCondition(Node):
    def __init__(self, expr, block, else_cond=None,
                 else_block=None, line_no=None):
        super().__init__(line_no)
        self.expr = expr
        self.block = block
        self.else_cond = else_cond
        self.else_block = else_block


class ForCondition(Node):
    def __init__(self, pid, for_range, block, line_no=None):
        super().__init__(line_no)
        self.pid = pid
        self.for_range = for_range
        self.block = block


class WhileCondition(Node):
    def __init__(self, expr, block, line_no=None):
        super().__init__(line_no)
        self.expr = expr
        self.block = block


class Range(Node):
    def __init__(self, start, end, line_no=None):
        super().__init__(line_no)
        self.start = start
        self.end = end


class Error(Node):
    def __init__(self, error_type, line_no=None):
        super().__init__(line_no)
        self.error_type = error_type
