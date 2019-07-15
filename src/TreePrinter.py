#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)

        return func
    return decorator


filler = '|  '


def indented(k):
    print(k * filler, end='')


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " +
                        self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        indented(indent)
        print(self.value)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        indented(indent)
        print(self.value)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        indented(indent)

        if not self.indices:
            print(self.name)
        else:
            print("REF")
            indented(indent + 1)
            print(self.name)

            for i in self.indices:
                indented(indent + 1)
                print(i)

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        indented(indent)
        print("MATRIX")

        for row in self.matrix:
            indented(indent + 1)
            print("VECTOR")

            for num in row:
                indented(indent + 2)
                print(num)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        indented(indent)
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.UnaryExpr)
    def printTree(self, indent=0):
        indented(indent)
        print(self.op)
        indented(indent + 1)
        print(self.expr)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        indented(indent)
        print(self.value)

    @addToClass(AST.Instruction)
    def printTree(self, indent=0):
        indented(indent)
        print(self.instruction_type.upper())

        if self.value:
            for val in self.value:
                val.printTree(indent + 1)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        indented(indent)
        print(self.assign_type)
        self.pid.printTree(indent + 1)
        self.value.printTree(indent + 1)

    @addToClass(AST.Equality)
    def printTree(self, indent=0):
        indented(indent)
        print(self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Negation)
    def printTree(self, indent=0):
        indented(indent)
        print(self.value)

    @addToClass(AST.MatrixOperation)
    def printTree(self, indent=0):
        indented(indent)
        print(self.op_type)

        for value in self.values:
            value.printTree(indent + 1)

    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        indented(indent)
        print("TRANSPOSE")
        self.expr.printTree(indent + 1)

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        self.instructions_opt.printTree(indent)

    @addToClass(AST.InstructionsOpt)
    def printTree(self, indent=0):
        for inst in self.instructions:
            inst.printTree(indent)

    @addToClass(AST.IfCondition)
    def printTree(self, indent=0):
        indented(indent)
        print("IF")
        self.expr.printTree(indent + 1)

        indented(indent)
        print("THEN")
        self.block.printTree(indent + 1)

        if self.else_cond:
            indented(indent)
            print("ELSE")
            self.else_cond.printTree(indent)

        if self.else_block:
            indented(indent)
            print("ELSE")
            self.else_block.printTree(indent + 1)

    @addToClass(AST.ForCondition)
    def printTree(self, indent=0):
        indented(indent)
        print("FOR")
        indented(indent + 1)
        print(self.pid)
        self.for_range.printTree(indent + 1)
        self.block.printTree(indent + 1)

    @addToClass(AST.WhileCondition)
    def printTree(self, indent=0):
        indented(indent)
        print("WHILE")
        self.expr.printTree(indent + 1)
        self.block.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        indented(indent)
        print("RANGE")
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        print(self.error_type)
