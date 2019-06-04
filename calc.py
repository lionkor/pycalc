"""
calc.py

Copyright (c) 2019 Lion Kortlepel

supported features:
    - addition, subtraction, division, multiplication, exponent
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
    "e"  : "2.718281828459045235360287471352",
}

DEBUG = True
FLOG = True

def log (s):
    if DEBUG:
        print (s)
    if FLOG:
        with open ("log.txt", "a") as f:
            f.write (str (s) + "\n")

def evaluate (s : str): # float
    # ignore any whitespace that may be left
    s = s.replace (" ", "").replace ("\n", "").replace (",", ".")

    for _str, _repl in specials.items ():
        s = s.replace (_str, _repl)

    # if number before minus, turn into "+-"
    if '-' in s:
        _index = s.find ('-') - 1
        if _index != -1:
            if s[_index] in "1234567890)":
                s = s[:s.find ('-')] + "+" + s[s.find ('-'):]
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
        _paren_count = 0
        end_index = 0
        for i in range (start_index + 1, len (s)):
            if s[i] == ')':
                if _paren_count == 0:
                    end_index = i
                else:
                    _paren_count -= 1
            elif s[i] == '(':
                _paren_count += 1
        _expr = s[start_index + 1:end_index].strip ()
        log (f"expression in parentheses is {_expr}")
        if len (_expr) > 0:
            # replacing parentheses with the evaluated value for their content
            s = s[:start_index] + str (evaluate (_expr)) + s[end_index + 1:]
            log (f"s: {s}")

    for _o in ["==", "!=", ">=", "<=", "<", ">", "and", "or", "xor", "<<", ">>", "+", "/", "*", "%", "^"]: # sorted by precedence, ascending
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
