#!/usr/bin/python

from SymbolTable import *


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        # print(method, visitor, node)

        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def visit_Program(self, node):
        self.global_table = SymbolTable('global')
        self.tables = [self.global_table]

        self.loop = 0

        return self.visit(node.instructions_opt)

    def visit_InstructionsOpt(self, node):
        return self.visit(node.instructions)

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        name = node.name
        line_no = node.line_no

        symbol = self.tables[-1].get(name)

        try:
            if not symbol:
                error_type = "Not existing variable: " + str(name)
            else:
                return symbol.type
        except Exception as error_type:
            print("Line {0}: {1}".format(line_no, error_type))
    
    def visit_Assign(self, node):
        expr = self.visit(node.value)
        line_no = node.line_no

        try:
            name = node.pid.name
            assign_type = node.assign_type

            old_symbol = self.tables[-1].get(name)

            if old_symbol == None and assign_type != '=':
                error_type = "Variable does not exist!"
                raise Exception(error_type)
            elif assign_type == '=':
                new_symbol = VariableSymbol(node.pid, expr)

                self.tables[-1].put(name, new_symbol)
            else:
                type1 = expr
                type2 = old_symbol.type

                if not type1:
                    error_type = "Assigning to an unknown variable"
                    raise Exception(error_type)
                
                if type1 == 'int' and type2 == 'int':
                    new_type = 'int'
                elif type1 == 'float' and type2 == 'int':
                    new_type = 'float'
                elif type1 == 'int' and type2 == 'float':
                    new_type =  'float'
                elif type1 == 'float' and type2 == 'float':
                    new_type = 'float'
                elif type1.startswith('matrix') and type2.startswith('matrix'):
                    dim1 = type1[6:]
                    dim2 = type2[6:]

                    if dim1 == dim2:
                        new_type = type1
                    elif dim1[0] == "1" and dim1[2] == dim2[2]:
                        new_type = type2
                    elif dim2[0] == "1" and dim1[2] == dim2[2]:
                        new_type = type1
                    else:
                        error_type = "Invalid dimensions for matrices " + \
                            node.pid.name + ' (' + dim1 + ')' + " and " + \
                            '(' + dim2 + ')'
                        raise Exception(error_type)
                elif type2.startswith('matrix') and type1 in ('int', 'float'):
                    error_type = "Invalid assigning with numerical value " + \
                        "and matrix"
                    raise Exception(error_type)
                else:
                    print(type1, type2)
                    error_type = "Invalid operations for assignment"
                    raise Exception(error_type)

                new_symbol = VariableSymbol(node.pid, new_type)
                self.tables[-1].put(name, new_symbol)
        except TypeError:
            error_type = "Type Error!"
            print("Line {0}: {1}".format(line_no, error_type))
        except Exception as error_type:
            print("Line {0}: {1}".format(line_no, error_type))

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op    = node.op
        line_no = node.line_no

        try:
            if not type1 or not type2:
                error_type = "Expression with an unknown variable"
                raise Exception(error_type)
            if op in ('.*', '.+', '.-', './'):
                if not type1.startswith('matrix'):
                    error_type = "Element-wise operation without a matrix"
                    raise Exception(error_type)
                elif type2 not in ('int', 'float'):
                    error_type = "Element-wise with not a int or float"
                    raise Exception(error_type)
                else:
                    return type1
            else:
                if type1 == 'int' and type2 == 'int':
                    return 'int'
                elif type1 == 'float' and type2 == 'int':
                    return 'float'
                elif type1 == 'int' and type2 == 'float':
                    return 'float'
                elif type1 == 'float' and type2 == 'float':
                    return 'float'
                elif type1.startswith('matrix') and type2.startswith('matrix'):
                    dim1 = type1[6:]
                    dim2 = type2[6:]

                    if dim1 == dim2:
                        return type1
                    elif dim1[0] == "1" and dim1[2] == dim2[2]:
                        return type2
                    elif dim2[0] == "1" and dim1[2] == dim2[2]:
                        return type1
                    else:
                        error_type = "Invalid dimensions for matrices " + \
                            ' (' + dim1 + ')' + " and " + \
                            '(' + dim2 + ')'
                        raise Exception(error_type)
                elif type1.startswith('matrix') and type2 in ('int', 'float'):
                    error_type = "Binary operations with numerical value " + \
                        "and matrix"
                    raise Exception(error_type)
                elif type2.startswith('matrix') and type1 in ('int', 'float'):
                    error_type = "Binary operations with numerical value " + \
                        "and matrix"
                    raise Exception(error_type)
                else:
                    error_type = "Invalid operations for assignment"
                    raise Exception(error_type)
        except Exception as error_type:
            print("Line {0}: {1}".format(line_no, error_type))

    def visit_Equality(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op    = node.op
        line_no = node.line_no

        return 'boolean'

    def visit_UnaryExpr(self, node):
        type1 = self.visit(node.expr)

    def visit_Matrix(self, node):
        len_vector = len(node.matrix[0])
        line_no = node.line_no

        for vector in node.matrix:
            if len(vector) != len_vector:
                error_type = "Incompatible size for matrix"
                print("Line {0}: {1}".format(line_no, error_type))
                break

        for vector in node.matrix:
            for elem in vector:
                elem_type = self.visit(elem)

                if elem_type not in ('float', 'int'):
                    error_type = "Wrong type in matrix"
                    print("Line {0}: {1}".format(line_no, error_type))
                    break

        row = len(node.matrix)
        column = len(node.matrix[0])

        dim = str(row) + 'x' + str(column)

        return 'matrix' + str(dim)

    def visit_Transpose(self, node):
        type1 = self.visit(node.expr)
        line_no = node.line_no

        try:
            if not type1.startswith('matrix'):
                error_type = 'Transpose operation with a non-matrix'
                raise Exception(error_type)

            dim = type1[6:][::-1]

            return 'matrix' + str(dim)
        except Exception as error_type:
            print("Line {0}: {1}".format(line_no, error_type))

    def visit_MatrixOperation(self, node):
        line_no = node.line_no

        try:
            for val in node.values:
                val_type = self.visit(val)

                if val_type != 'int':
                    error_type = "Invalid dimension values"
                    raise Exception(error_type)

            len_values = len(node.values)

            if len_values == 1:
                dim = str(node.values[0]) + 'x' + '1'
            else:
                dim = 'x'.join([str(d) for d in node.values])

            return 'matrix' + dim

        except Exception as error_type:
            print("Line {0}: {1}".format(line_no, error_type))

    def visit_IfCondition(self, node):
        line_no = node.line_no

        try:
            expr_type = self.visit(node.expr)

            if expr_type != 'boolean':
                error_type = "Condition is not a boolean"
                raise Exception(error_type)

            new_table = SymbolTable('New')
            new_table.symbol_table = self.tables[-1].symbol_table
            
            self.tables.append(new_table)
            self.visit(node.block)

            for elem in self.tables[-1].symbol_table:
                self.tables[-2].put(elem, self.tables[-1].get(elem))
            self.tables.pop()

            if node.else_block:
                self.visit(node.else_block)
            elif node.else_cond:
                self.visit(node.else_cond)
        except Exception as error_type:
            print("Line {0}: {1}".format(line_no, error_type))

    def visit_WhileCondition(self, node):
        line_no = node.line_no

        try:
            expr_type = self.visit(node.expr)

            if expr_type != 'boolean':
                error_type = "Condition is not a boolean"
                raise Exception(error_type)

            self.loop += 1
            new_table = SymbolTable('New')
            new_table.symbol_table = self.tables[-1].symbol_table
            self.tables.append(new_table)
            self.visit(node.block)

            self.loop -= 1

            for elem in self.tables[-1].symbol_table:
                self.tables[-2].put(elem, self.tables[-1].get(elem))

            self.tables.pop()

        except Exception as error_type:
            print("Line {0}: {1}".format(line_no, error_type))

    def visit_Range(self, node):
        line_no = node.line_no

        try:
            type1 = self.visit(node.start)
            type2 = self.visit(node.end)

            if type1 != 'int' or type2 != 'int':
                error_type = "Invalid range arguments"
                raise Exception(error_type)

            return 'int'
            
        except Exception as error_type:
            print("Line {0}: {1}".format(line_no, error_type))

    def visit_ForCondition(self, node):
        line_no = node.line_no

        try:
            self.loop += 1
            new_table = SymbolTable('New')
            new_table.symbol_table = self.tables[-1].symbol_table

            name = node.pid.name
            for_range = self.visit(node.for_range)
            new_symbol = VariableSymbol(node.pid, for_range)
            new_table.put(name, new_symbol)

            self.tables.append(new_table)
            self.visit(node.block)
            self.loop -= 1

            for elem in self.tables[-1].symbol_table:
                self.tables[-2].put(elem, self.tables[-1].get(elem))

            self.tables.pop()
            
        except Exception as error_type:
            print("Line {0}: {1}".format(line_no, error_type))
    
    def visit_Negation(self, node):
        line_no = node.line_no

        try:
            type1 = self.visit(node.value)
            print(type1)

            if type1 not in ('int', 'float') and not type1.startswith('matrix'):
                error_type = "Invalid arguments for negation"
                raise Exception(error_type)
            else:
                return type1
        except Exception as error_type:
            print("Line {0}: {1}".format(line_no, error_type))

    def visit_Instruction(self, node):
        line_no = node.line_no
        inst_type = node.instruction_type

        try:
            if self.loop <= 0 and inst_type not in ('print', 'return'):
                error_type = "Instruction outside a loop"
                raise Exception(error_type)

            if inst_type in ('print', 'return'):
                if node.value:
                    if type(node.value) == type(list()):
                        for val in node.value:
                            type1 = self.visit(val)

                            if not type1:
                                error_type = inst_type + \
                                    " operation with unknown variable"
                                raise Exception(error_type)
                    else:
                        type1 = self.visit(node.value)

                        if not type1:
                            error_type = inst_type + \
                                " operation with unknown variable"
                            raise Exception(error_type)

        except Exception as error_type:
            print("Line {0}: {1}".format(line_no, error_type))



