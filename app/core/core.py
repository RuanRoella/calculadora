from typing import Union
import re

def format_number(num: str) -> Union[int, bool]:

    num = float(num.replace(',', '.'))

    if num % 1 == 0:
        return int(num)
    else:
        point = len(str(num).split('.')[-1])
        value = "%.{0}f".format(point if point <= 12 else 12) % num
        return float(value)

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
                format = "%.{0}f".format(point if point <= 12 else 12) % calc

                result = {"display": format.replace('.', ','), 'preview': prev}

            return result

    def get_porcent(self, display, preview):
        
        result = "0"
        new_expression = "0"
        if preview:

            operators = ['+', '-', 'x', '÷']

            exp = re.compile('|'.join('(?:{})'.format(re.escape(i)) for i in sorted(operators, reverse=True, key=len)))
            op = exp.search(preview).group()
            
            _all = preview.split(op)[0].strip().replace(',', '.')
            _part = display.replace(',', '.')

            # % = (Parte / Todo) x 100
            porc = (float(_part) * float(_all)) / 100

            result = str(porc).replace('.', ',')
            new_expression = "%s%s" % (preview, result)

        return { "display": result, "preview": new_expression }
        
    def eval(self, display, preview):
        
        try:
            value = self._normalizate_expression(display, preview)
        except ZeroDivisionError:
            value = "Error"
        finally:
            return value
        
    def _normalizate_expression(self, display: str, preview: str):

        if preview == "":
            return

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
                _new_exp = "%s%s%s" % (_split_exp[0].strip().replace(',', '.'), _op, display.replace(',', '.'))

        _calc = eval(_new_exp)
        value = format_number(str(_calc))

        prev = format_number(display)
        return { "display": str(value).replace('.', ','), "preview": str(prev).replace('.', ',') }

