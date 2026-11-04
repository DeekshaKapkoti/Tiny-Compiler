class TACGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def generate(self, node):
        if node.label == "Program":
            for fn in node.children:
                self.generate(fn)
            return self.code

        elif node.label.startswith("Function"):
            self.code.append(f"\n# Function {node.label}")
            for stmt in node.children:
                self.generate(stmt)

        elif node.label == "VarDecl":
            return  # Declaration doesn't generate TAC

        elif node.label == "Assign":
            var_name = node.children[0].label
            expr_temp = self.generate(node.children[1])
            self.code.append(f"{var_name} = {expr_temp}")

        elif node.label == "Return":
            expr_temp = self.generate(node.children[0])
            self.code.append(f"RETURN {expr_temp}")

        elif node.label == "If":
            cond = self.generate(node.children[0].children[0])  # node['Condition']
            else_label = self.new_label()
            end_label = self.new_label()

            self.code.append(f"IF NOT {cond} GOTO {else_label}")
            for stmt in node.children[1].children:  # Then
                self.generate(stmt)
            self.code.append(f"GOTO {end_label}")
            self.code.append(f"{else_label}:")
            if len(node.children) == 3:  # Has Else block
                for stmt in node.children[2].children:
                    self.generate(stmt)
            self.code.append(f"{end_label}:")

        elif node.label == "While":
            start_label = self.new_label()
            end_label = self.new_label()
            self.code.append(f"{start_label}:")
            cond = self.generate(node.children[0].children[0])  # Condition
            self.code.append(f"IF NOT {cond} GOTO {end_label}")
            for stmt in node.children[1].children:  # Body
                self.generate(stmt)
            self.code.append(f"GOTO {start_label}")
            self.code.append(f"{end_label}:")

        elif node.label.startswith("Op("):
            op = node.label[3:-1]
            left = self.generate(node.children[0])
            right = self.generate(node.children[1])
            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {op} {right}")
            return temp

        elif node.label.startswith("Number("):
            return node.label[7:-1]

        elif node.label.startswith("Var("):
            return node.label[4:-1]

        else:
            for child in node.children:
                self.generate(child)
