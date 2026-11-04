def simulate_return(tac_code):
    print("\n" + "=" * 31)
    print("FINAL OUTPUT (Simulated Return)")
    print("=" * 31)

    variables = {}

    def eval_expr(expr):
        tokens = expr.split()
        if len(tokens) == 1:
            return variables.get(tokens[0], int(tokens[0]) if tokens[0].isdigit() else None)
        elif len(tokens) == 3:
            a, op, b = tokens
            a_val = variables.get(a, int(a) if a.isdigit() else None)
            b_val = variables.get(b, int(b) if b.isdigit() else None)
            if a_val is not None and b_val is not None:
                try:
                    return eval(f"{a_val} {op} {b_val}")
                except:
                    return None
        return None

    for line in tac_code:
        if "=" in line and not line.startswith("IF") and not line.startswith("GOTO"):
            parts = line.split("=", 1)
            if len(parts) == 2:
                left, right = map(str.strip, parts)
                result = eval_expr(right)
                if result is not None:
                    variables[left] = result
        elif line.startswith("RETURN"):
            ret_var = line.split()[1]
            value = variables.get(ret_var, f"<unknown value of {ret_var}>")
            print(f"Return Value: {value}")
