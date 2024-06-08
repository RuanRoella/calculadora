from configparser import ConfigParser
from pathlib import Path

import re

KEYBOARD = [["%", "CE", "C", "\u232B"],
            ["¹/\u02E3", "\u02E3²", "²\u221A\u02E3", "\u00F7"],
            ["7", "8", "9", 'x'],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["←", "0", ",", "="]]



class Calculator:
    
    def get_x_element(self, value: int, expression: str):

        if expression:
            
            calc = None
            preview = None
            match expression:
                case "¹/\u02E3": # 1/x
                    calc = 1 / float(value)
                    preview = "1/(%s)" % value
                case "\u02E3²": # x²
                    calc = float(value) ** 2
                    preview = "sqr(%s)" % value
                case "²\u221A\u02E3": # Raiz
                    calc = float(value) ** (1/2)
                    preview = "\u221A(%s)" % value

            if calc.is_integer():
                return {"display": int(calc), 'preview': preview}
            
            point = len(str(calc).split('.')[-1] )
            result = "%.{0}f".format(point if point <= 14 else 14) % calc
            
            return {"display": result.replace('.', ','), 'preview': preview}

    #TODO Semantic Error
    #Fix somes result is returning wrong values
    def get_porcent(self, calc):
        
        _all = calc[:1]
        _part = calc[-1]
        
        if _all.isnumeric():
            # % = (Parte / Todo) x 100
            porc = (float(_part) * float(_all)) / 100

        new_expression = str(porc).replace('.', ',')

        return {"display": new_expression, "preview": "%s%s" % (calc[:-1], porc)}
        
    def eval(self, calc):
        
        try:
            value = self._normalizate_expression(calc)
        except ZeroDivisionError:
            value = "Error"
        finally:
            return value
        

    def _normalizate_expression(self, expression: str):
        
        operators = ['+', '-', 'x', '÷']

        exp = re.compile('|'.join('(?:{})'.format(re.escape(i)) for i in sorted(operators, reverse=True, key=len)))
        
        _split_exp = ""
        _new_exp = ""
        find_op = exp.findall(expression)
        if len(find_op) > 0:
            for op in find_op:
                _split_exp = expression.split(op)
                if op == "÷":
                    _op = "/"
                elif op == "x":
                    _op = "*"
                else:
                    _op = op
                _new_exp = "%s%s%s" % (_split_exp[0], _op, _split_exp[1])
        
        
        result = eval(_new_exp)
        point = len(str(result).split('.')[-1] )

        if isinstance(result, int):
            return result
        
        value = "%.{0}f".format(point if point <= 14 else 14) % result
        return value.replace('.', ',')



class Dict(dict):
    def __init__(self, *args, **kwargs):
        super(Dict, self).__init__(*args, **kwargs)
        self.__dict__ = self
    
    def __getattribute__(self, name: str):
        try:
            if isinstance(name, str):
                return super().__getattribute__(name)
        except AttributeError:
            pass

class Settings:
    data = Path(r'app\DATA.ini')

    config = ConfigParser(dict_type=Dict)

    config.read(data)

    def __new__(cls):
        return cls.config._sections
