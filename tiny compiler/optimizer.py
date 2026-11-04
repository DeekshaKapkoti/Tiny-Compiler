
import re
import operator


class Optimizer:

    def __init__(self, code_lines):
        self.code = code_lines
        self.optimized_code = []

    # PHASE 1: CONSTANT FOLDING
    def constant_folding(self, line):

        pattern = r'^\s*(t\d+)\s*=\s*(-?\d+)\s*([+\-*/])\s*(-?\d+)\s*$'
        match = re.match(pattern, line)

        if match:
            target, lhs, op, rhs = match.groups()

            lhs = int(lhs)
            rhs = int(rhs)

            operations = {
                '+': operator.add,
                '-': operator.sub,
                '*': operator.mul,
                '/': operator.floordiv
            }

            if op == '/' and rhs == 0:
                return line

            result = operations[op](lhs, rhs)

            return f"{target} = {result}"

        return line

    # PHASE 2: DEAD CODE ELIMINATION
    def dead_code_elimination(self):

        used_vars = set()

        for line in self.code:

            match = re.match(r'^\s*(\w+)\s*=\s*(.*)$', line)

            if match:
                expression = match.group(2)

                tokens = re.findall(r'\b[A-Za-z_]\w*\b', expression)

                used_vars.update(tokens)

            else:
                tokens = re.findall(r'\b[A-Za-z_]\w*\b', line)

                used_vars.update(
                    token for token in tokens
                    if token.startswith('t')
                )

        new_code = []

        for line in self.code:

            match = re.match(r'^\s*(t\d+)\s*=', line)

            if match:
                target = match.group(1)

                if target in used_vars:
                    new_code.append(line)

            else:
                new_code.append(line)

        self.code = new_code

    # MAIN OPTIMIZATION FUNCTION
    def optimize(self):

        # Step 1: Constant Folding
        self.code = [
            self.constant_folding(line)
            for line in self.code
        ]

        # Step 2: Dead Code Elimination
        self.dead_code_elimination()

        return self.code
