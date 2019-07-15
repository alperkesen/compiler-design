#!/usr/bin/python


class Symbol(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class VariableSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)


class SymbolTable(object):
    def __init__(self, name):
        self.name = name
        self.symbol_table = dict()

    def put(self, name, symbol):
        self.symbol_table[name] = symbol

    def get(self, name):
        return self.symbol_table.get(name, None)
        

