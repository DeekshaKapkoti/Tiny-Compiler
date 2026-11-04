from lexer import Token

# ---------- AST Node Classes ----------
class ASTNode:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children or []

    def __repr__(self):
        return self.label

# ---------- Parser Class ----------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        self.pos += 1

    def expect(self, token_type, value=None):
        token = self.peek()
        if not token:
            raise SyntaxError("Unexpected EOF")
        if token.type != token_type or (value and token.value != value):
            raise SyntaxError(f"Expected {token_type} {value}, got {token.type} {token.value}")
        self.advance()
        return token

    def match(self, token_type, value=None):
        token = self.peek()
        if token and token.type == token_type and (value is None or token.value == value):
            self.advance()
            return token
        return None

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        functions = []
        while self.peek():
            functions.append(self.parse_function())
        return ASTNode("Program", functions)

    def parse_function(self):
        self.expect("KEYWORD")        # return type
        name = self.expect("ID").value
        self.expect("LPAREN")
        self.expect("RPAREN")
        self.expect("LBRACE")

        body = []
        while self.peek() and self.peek().type != "RBRACE":
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)

        self.expect("RBRACE")
        return ASTNode(f"Function({name})", body)

    def parse_statement(self):
        token = self.peek()

        if token.type == "KEYWORD" and token.value in {"int", "float", "char"}:
            return self.parse_declaration()
        elif token.type == "ID":
            return self.parse_assignment()
        elif token.type == "KEYWORD" and token.value == "if":
            return self.parse_if_statement()
        elif token.type == "KEYWORD" and token.value == "while":
            return self.parse_while_statement()
        elif token.type == "KEYWORD" and token.value == "return":
            return self.parse_return()
        else:
            self.advance()
            return None

    def parse_declaration(self):
        var_type = self.expect("KEYWORD").value
        var_name = self.expect("ID").value
        self.expect("SEMI")
        return ASTNode("VarDecl", [ASTNode(var_type), ASTNode(var_name)])

    def parse_assignment(self):
        name = self.expect("ID").value
        self.expect("OP", "=")
        expr = self.parse_expression()
        self.expect("SEMI")
        return ASTNode("Assign", [ASTNode(name), expr])

    def parse_return(self):
        self.expect("KEYWORD", "return")
        expr = self.parse_expression()
        self.expect("SEMI")
        return ASTNode("Return", [expr])

    def parse_if_statement(self):
        self.expect("KEYWORD", "if")
        self.expect("LPAREN")
        condition = self.parse_expression()
        self.expect("RPAREN")
        self.expect("LBRACE")
        then_body = []
        while self.peek() and self.peek().type != "RBRACE":
            then_body.append(self.parse_statement())
        self.expect("RBRACE")

        else_body = []
        if self.peek() and self.peek().type == "KEYWORD" and self.peek().value == "else":
            self.expect("KEYWORD", "else")
            self.expect("LBRACE")
            while self.peek() and self.peek().type != "RBRACE":
                else_body.append(self.parse_statement())
            self.expect("RBRACE")

        children = [ASTNode("Condition", [condition]), ASTNode("Then", then_body)]
        if else_body:
            children.append(ASTNode("Else", else_body))
        return ASTNode("If", children)

    def parse_while_statement(self):
        self.expect("KEYWORD", "while")
        self.expect("LPAREN")
        condition = self.parse_expression()
        self.expect("RPAREN")
        self.expect("LBRACE")
        body = []
        while self.peek() and self.peek().type != "RBRACE":
            body.append(self.parse_statement())
        self.expect("RBRACE")
        return ASTNode("While", [ASTNode("Condition", [condition]), ASTNode("Body", body)])

    def parse_expression(self):
        left = self.parse_term()
        while self.peek() and self.peek().type == "OP":
            op = self.expect("OP").value
            right = self.parse_term()
            left = ASTNode(f"Op({op})", [left, right])
        return left

    def parse_term(self):
        token = self.peek()
        if token.type == "NUMBER":
            self.advance()
            return ASTNode(f"Number({token.value})")
        elif token.type == "ID":
            self.advance()
            return ASTNode(f"Var({token.value})")
        elif token.type == "LPAREN":
            self.expect("LPAREN")
            expr = self.parse_expression()
            self.expect("RPAREN")
            return expr
        else:
            raise SyntaxError(f"Unexpected token in expression: {token}")

# ---------- AST Tree Printer ----------

def print_ast_tree(node, indent=""):
    print(indent + str(node.label))
    for child in node.children:
        print_ast_tree(child, indent + "  ")

# ---------- Run Example ----------
if __name__ == "__main__":
    from lexer import Lexer

    code = """
    int main() {
        int x;
        x = 2 + 3;
        while (x < 5) {
            x = x + 1;
        }
        if (x == 5) {
            x = x + 5;
        } else {
            x = x - 1;
        }
        return x;
    }
    """

    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    print("==== AST TREE ====")
    print_ast_tree(ast)
