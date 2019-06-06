"""
calc.py

Copyright (c) 2019 Lion Kortlepel

supported features:
    - addition, subtraction, division, multiplication, exponent
    - functions, like sqrt (x), sin (x), cos (x)
    - bitwise operations, like XOR, AND, OR, <<, >>
    - equality / relational operators
    - floating point operands, example: 3.1415926 * 2.01
    - unary negation, examples: 2 * -5
    - whitespace is ignored, formatting of big numbers using whitespace is
       completely safe, example: 1 000 000 000 * 0.000354221
    - parentheses, example: 10 / (2 / 4)
    - nested parentheses, example: 2 * (5 - 2 * (4 / (8.33 / 2)))
    - implicit multiplication for parentheses, so that: 2 (3 / 6) == 2 * (3 / 6)
"""

specials : dict = {
    "pi" : "3.141592653589793238462643383279",
}

import math

def is_prime (_x : str): # bool
    x = int (_x)
    for i in range (2, int (math.sqrt (x)) + 1):
        if x % i == 0:
            return int (False)
    return int (True)

functions : dict = {
    "sqrt" : math.sqrt,
    "cos" : math.cos,
    "sin" : math.sin,
    "fact" : math.factorial,
    "abs" : math.fabs,
    "fabs" : math.fabs,
    "degrees" : math.degrees,
    "radians" : math.radians,
    "prime" : is_prime,
}

DEBUG = True
FLOG = True

def log (s):
    if DEBUG:
        print (s)
    if FLOG:
        with open ("log.txt", "a") as f:
            f.write (str (s) + "\n")

# 2*((1-((1+1)*0))*5)

def find_matching_parentheses (s : str, _start : int = 0): # int
    _paren_count = 0
    end_index = 0
    for i in range (_start, len (s)):
        if s[i] == ')':
            if _paren_count == 0:
                end_index = i
            else:
                _paren_count -= 1
        elif s[i] == '(':
            _paren_count += 1
    return end_index

def evaluate (s : str): # float
    # ignore any whitespace that may be left
    s = s.replace (" ", "").replace ("\n", "").replace (",", ".").replace ("()", "")

    # if number before minus, turn into "+-"
    for i in range (0, len (s)):
        if s[i] == '-':
            _index = i - 1
            if _index != -1:
                if s[_index] in "1234567890)":
                    s = s[:i] + "+" + s[i:]
                log (f"replaced with {s}")

    for i in range (0, len (s)):
        # implicit multiplication in 'x (y)' or '(x) y' cases
        if s[i] == '(':
            if i == 0: continue
            if s[i - 1] in "0123456789)":
                s = s[:i] + "*" + s[i:]
        elif s[i] == ')':
            if i == len (s) - 1: continue
            if s[i + 1] in "0123456789(":
                s = s[:i + 1] + "*" + s[i + 1:]

    # parentheses have high precedence
    while '(' in s and ')' in s:
        start_index = s.find ('(')
        end_index = find_matching_parentheses (s, start_index + 1)
        _expr = s[start_index + 1:end_index].strip ()

        log (f"expression in parentheses is {_expr}")
        if len (_expr) > 0:
            handled = False
            # looking for function names if parentheses are present
            for _name, _func in functions.items ():
                if s[start_index - len (_name):start_index] == _name:
                    log (f"calling function {_name} with args {{{_expr}}}")
                    # replacing function call with returned value
                    s = s[:start_index - len (_name)] + str (float (_func (evaluate (_expr)))) + s[end_index + 1:]
                    handled = True
                    break
            if not handled:
                # replacing parentheses with the evaluated value for their content
                s = s[:start_index] + str (evaluate (_expr)) + s[end_index + 1:]
            log (f"replaced s: {s}")

    for _str, _repl in specials.items ():
        # TODO check right and left
        s = s.replace (_str, _repl)

    for _o in ["==", "!=", ">=", "<=", "<", ">", "and", "xor", "or", "<<", ">>", "+", "/", "*", "%", "^"]: # sorted by precedence, ascending
        _in = s.find (_o)
        # log (f"_o: {_o}, _in: {_in}")
        if _in != -1:
            op0 = s[:_in]
            op1 = s[_in + 1:]

            if s[_in:_in+2] == "==":
                op1 = s[_in + 2:]
                log (f"evaluated {op0} == {op1}")
                return int (evaluate (op0) == evaluate (op1))

            if s[_in:_in+2] == "!=":
                op1 = s[_in + 2:]
                log (f"evaluated {op0} != {op1}")
                return int (evaluate (op0) != evaluate (op1))

            if s[_in:_in+2] == ">=":
                op1 = s[_in + 2:]
                log (f"evaluated {op0} >= {op1}")
                return int (evaluate (op0) >= evaluate (op1))

            if s[_in:_in+2] == "<=":
                op1 = s[_in + 2:]
                log (f"evaluated {op0} <= {op1}")
                return int (evaluate (op0) <= evaluate (op1))

            if _o == '<' and s[_in+1] != '<': # extra check to discern from "<<"
                log (f"evaluated {op0} < {op1}")
                return int (evaluate (op0) < evaluate (op1))

            if _o == '>' and s[_in+1] != '>': # extra check to discern from ">>"
                log (f"evaluated {op0} > {op1}")
                return int (evaluate (op0) > evaluate (op1))

            if s[_in:_in + 3] == "and":
                op1 = s[_in + 3:]
                log (f"evaluated {op0} and {op1}")
                return int (evaluate (op0)) & int (evaluate (op1))

            if s[_in:_in + 2] == "or":
                op1 = s[_in + 2:]
                log (f"evaluated {op0} or {op1}")
                return int (evaluate (op0)) | int (evaluate (op1))

            if s[_in:_in + 3] == "xor":
                op1 = s[_in + 3:]
                log (f"evaluated {op0} xor {op1}")
                return int (evaluate (op0)) ^ int (evaluate (op1))

            if s[_in:_in + 2] == "<<":
                op1 = s[_in + 2:]
                log (f"evaluated {op0} << {op1}")
                return int (evaluate (op0)) << int (evaluate (op1))

            if s[_in:_in + 2] == ">>":
                op1 = s[_in + 2:]
                log (f"evaluated {op0} >> {op1}")
                return int (evaluate (op0)) >> int (evaluate (op1))

            if _o == '+':
                log (f"evaluated {op0} + {op1}")
                return evaluate (op0) + evaluate (op1)

            if _o == '/':
                log (f"evaluated {op0} / {op1}")
                return evaluate (op0) / evaluate (op1)

            if _o == '*':
                log (f"evaluated {op0} * {op1}")
                return evaluate (op0) * evaluate (op1)

            if _o == '%':
                log (f"evaluated {op0} % {op1}")
                return evaluate (op0) % evaluate (op1)

            if _o == '^':
                log (f"evaluated {op0} ^ {op1}")
                return evaluate (op0) ** evaluate (op1)

    return float (s)


def main ():
    while True:
        try:
            expr = input ("c ")
            if "exit" in expr:
                print ("Bye!")
                break
            print (evaluate (expr))
        except Exception as e:
            print ("Oops! Something went wrong:", e)

if __name__ == "__main__":
    main ()
