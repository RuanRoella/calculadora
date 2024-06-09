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
    
    def get_x_element(self, value: str, expression: str):
        

        value = float(value.replace(',', '.'))
        if expression:
            
            calc = None
            preview = None
            result = None
            match expression:
                case "¹/\u02E3": # 1/x
                    calc = 1 / value
                    preview = "1/"
                case "\u02E3²": # x²
                    calc = value ** 2
                    preview = "sqr"
                case "²\u221A\u02E3": # Raiz
                    calc = value ** (1/2)
                    preview = "\u221A"

            if value.is_integer():
                prev = "%s( %s )" % (preview, str(int(value)))
            else:
                prev = "%s( %s )" % (preview, str(value).replace('.', ','))
            
            
            if calc.is_integer():
                result = {"display": int(calc), 'preview': prev}
            else:
                point = len(str(calc).split('.')[-1] )
                format = "%.{0}f".format(point if point <= 14 else 14) % calc

                result = {"display": format.replace('.', ','), 'preview': prev}
            
            return result

    def get_porcent(self, display, preview):
        
        result = "0"
        new_expression = "0"
        if preview:

            operators = ['+', '-', 'x', '÷']

            exp = re.compile('|'.join('(?:{})'.format(re.escape(i)) for i in sorted(operators, reverse=True, key=len)))
            op = exp.search(preview).group()
            
            _all = preview.split(op)[0].strip()
            _part = display.replace(',', '.')

            # % = (Parte / Todo) x 100
            porc = (float(_part) * float(_all)) / 100

            result = str(porc).replace('.', ',')
            new_expression = "%s%s" % (preview, porc)

        return { "display": result, "preview": new_expression }
        
    def eval(self, display, preview):

        try:
            value = self._normalizate_expression(display, preview)
        except ZeroDivisionError:
            value = "Error"
        finally:
            return value
        
    def _normalizate_expression(self, display: str, preview: str):
        
        operators = ['+', '-', 'x', '÷']

        exp = re.compile('|'.join('(?:{})'.format(re.escape(i)) for i in sorted(operators, reverse=True, key=len)))
        
        _split_exp = ""
        _new_exp = ""
        find_op = exp.findall(preview)
        if len(find_op) > 0:
            for op in find_op:
                _split_exp = preview.split(op)
                if op == "÷":
                    _op = "/"
                elif op == "x":
                    _op = "*"
                else:
                    _op = op
                _new_exp = "%s%s%s" % (_split_exp[0].strip(), _op, display)
        
        result = eval(_new_exp)
        point = len(str(result).split('.')[-1] )
#
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
