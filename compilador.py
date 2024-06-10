import sys
from abc import abstractmethod

class PrePro:
    def filter(code):
        filtered_lines = []
        output = ""
        for line in code.split('\n'):
            line = line.strip()
            if line and not line.startswith('--'):
                if line.find("--") != -1:
                    line = line[:line.find("--")]
                filtered_lines.append(line)
        for line in filtered_lines:
            output += line + "\n"
        return output

class Token():
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer():
    def __init__(self, source, position, next):
        self.source = source
        self.position = position
        self.next = next
        self.list = [
            "setup",
            "next",
            "plus",
            "minus",
            "display",
            "during_race",
            "verify",
            "other",
            "end_race",
            "end_vef",
            "end_other",
            "concat",
            "then",
            "is",
            "track_day",
            "end_trackday",
            "insert"
        ]

    def selectNext(self):
        if self.position >= len(self.source):
            self.next = None

        else:
            if self.source[self.position] == " ":
                self.position += 1
                self.selectNext()
            elif self.source[self.position] == "+":
                self.position += 1
                self.next = Token("PLUS_SIMPLE", "+")
            elif self.source[self.position] == "-":
                self.position += 1
                self.next = Token("MINUS_SIMPLE", "-")
            elif self.source[self.position] == "*":
                self.position +=1
                self.next = Token("TIMES", "*")
            elif self.source[self.position] == "/":
                self.position +=1
                self.next = Token("DIV", "/")
            elif self.source[self.position] == "(":
                self.position += 1
                self.next = Token("LPAREN", "(")
            elif self.source[self.position] == ")":
                self.position += 1
                self.next = Token("RPAREN", ")")
            elif self.source[self.position] == "\n":
                self.position += 1
                self.next = Token("NL", "\n")
            elif self.source[self.position] == "=" and self.source[self.position + 1] == "=":
                self.position += 2
                self.next = Token("EQ", "==")
            elif self.source[self.position] == ">":
                self.position += 1
                if self.position < len(self.source) and self.source[self.position] == "=":
                    self.position += 1
                    self.next = Token("GE", ">=")
                else:
                    self.next = Token("GT", ">")
            elif self.source[self.position] == "<":
                self.position += 1
                if self.position < len(self.source) and self.source[self.position] == "=":
                    self.position += 1
                    self.next = Token("LE", "<=")
                else:
                        self.next = Token("LT", "<")
            elif self.source[self.position] == ",":
                self.position += 1
                self.next = Token("COMMA", ",")
            elif self.source[self.position] == "\"":
                string = ""
                self.position += 1
                while self.position < len(self.source) and self.source[self.position] != "\"":
                    string += self.source[self.position]
                    self.position += 1
                if self.position == len(self.source):
                    sys.stderr.write("Erro de sintaxe. Aspas não fechadas. (1)")
                    sys.exit(1)
                self.position += 1
                self.next = Token("STR", string)
            elif self.source[self.position] == "!" and self.source[self.position + 1] == "=":
                self.position += 2
                self.next = Token("NE", "!=")
            elif self.source[self.position] == ":":
                self.position += 1
                self.next = Token("COLON", ":")
            elif self.source[self.position].isdigit():
                number = ""
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    number += self.source[self.position]
                    self.position += 1
                self.next = Token("NUMBER", number)
            elif self.source[self.position].isalpha():
                iden = ""
                while self.position < len(self.source) and self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == '_':
                    iden += self.source[self.position]
                    self.position += 1
                if iden in self.list:
                    self.next = Token(iden.upper(), iden)
                else:
                    self.next = Token("IDEN", iden)
            else:
                print("Erro de sintaxe. Caractere inválido. (1) -> ", self.source[self.position])
                sys.stderr.write("Erro de sintaxe. Caractere inválido. (1)")
                sys.exit(1)
                return


class Node():
    def __init__ (self, value:int, children=None):
        self.value = value
        self.children = children if children is not None else []

    @abstractmethod
    def Evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st, ft):
        if self.value == "CONCAT":
            return ["STR", str(self.children[0].Evaluate(st, ft)[1]) + str(self.children[1].Evaluate(st, ft)[1])]
        elif self.value == "NEXT":
            result =  ["INT", int(self.children[0].Evaluate(st, ft)[1] + 1)]
            st.set(self.children[0].value, result[1], result[0])
            return result
        elif self.value == "+" or self.value == "-" or self.value == "*" or self.value == "/" or self.value == "NEXT" or self.value == "+=" or self.value == "-=":
            if self.children[0].Evaluate(st, ft)[0] == "INT" and self.children[1].Evaluate(st, ft)[0] == "INT":
                if self.value == "+":
                    return ["INT", int(self.children[0].Evaluate(st, ft)[1]) + int(self.children[1].Evaluate(st, ft)[1])]
                elif self.value == "-":
                    return ["INT", int(self.children[0].Evaluate(st, ft)[1]) - int(self.children[1].Evaluate(st, ft)[1])]
                elif self.value == "*":
                    return ["INT", int(self.children[0].Evaluate(st, ft)[1]) * int(self.children[1].Evaluate(st, ft)[1])]
                elif self.value == "/":
                    return ["INT", int(self.children[0].Evaluate(st, ft)[1]) // int(self.children[1].Evaluate(st, ft)[1])]
                elif self.value == "+=":
                    result = ["INT", int(self.children[0].Evaluate(st, ft)[1] + self.children[1].Evaluate(st, ft)[1])]
                    st.set(self.children[0].value, result[1], result[0])
                    return result
                elif self.value == "-=":
                    result = ["INT", int(self.children[0].Evaluate(st, ft)[1] - self.children[1].Evaluate(st, ft)[1])]
                    st.set(self.children[0].value, result[1], result[0])
                    return result
            else:
                sys.stderr.write("Tipo dos operadores inválido.")
                sys.exit(1)
                return
        elif self.value == "==" or self.value == ">" or self.value == "<" or self.value == "!=" or self.value == ">=" or self.value == "<=":
            if self.children[0].Evaluate(st, ft)[0] == self.children[1].Evaluate(st, ft)[0]:
                if self.value == "==":
                    if self.children[0].Evaluate(st, ft)[0] == "STR":
                        return [self.children[0].Evaluate(st, ft)[0], int(self.children[0].Evaluate(st, ft)[1] == self.children[1].Evaluate(st, ft)[1])]
                    return [self.children[0].Evaluate(st, ft)[0], int(int(self.children[0].Evaluate(st, ft)[1]) == int(self.children[1].Evaluate(st, ft)[1]))]
                elif self.value == ">":
                    if self.children[0].Evaluate(st, ft)[0] == "STR":
                        return [self.children[0].Evaluate(st, ft)[0], int(self.children[0].Evaluate(st, ft)[1] > self.children[1].Evaluate(st, ft)[1])]
                    return [self.children[0].Evaluate(st, ft)[0], int(int(self.children[0].Evaluate(st, ft)[1]) > int(self.children[1].Evaluate(st, ft)[1]))]
                elif self.value == "<":
                    if self.children[0].Evaluate(st, ft)[0] == "STR":
                        return [self.children[0].Evaluate(st, ft)[0], int(self.children[0].Evaluate(st, ft)[1] < self.children[1].Evaluate(st, ft)[1])]
                    return [self.children[0].Evaluate(st, ft)[0], int(int(self.children[0].Evaluate(st, ft)[1]) < int(self.children[1].Evaluate(st, ft)[1]))]
                elif self.value == "!=":
                    if self.children[0].Evaluate(st, ft)[0] == "STR":
                        return [self.children[0].Evaluate(st, ft)[0], int(self.children[0].Evaluate(st, ft)[1] != self.children[1].Evaluate(st, ft)[1])]
                    return [self.children[0].Evaluate(st, ft)[0], int(int(self.children[0].Evaluate(st, ft)[1]) != int(self.children[1].Evaluate(st, ft)[1]))]
                elif self.value == ">=":
                    if self.children[0].Evaluate(st, ft)[0] == "STR":
                        return [self.children[0].Evaluate(st, ft)[0], int(self.children[0].Evaluate(st, ft)[1] >= self.children[1].Evaluate(st, ft)[1])]
                    return [self.children[0].Evaluate(st, ft)[0], int(int(self.children[0].Evaluate(st, ft)[1]) >= int(self.children[1].Evaluate(st, ft)[1]))]
                elif self.value == "<=":
                    if self.children[0].Evaluate(st, ft)[0] == "STR":
                        return [self.children[0].Evaluate(st, ft)[0], int(self.children[0].Evaluate(st, ft)[1] <= self.children[1].Evaluate(st, ft)[1])]
                    return [self.children[0].Evaluate(st, ft)[0], int(int(self.children[0].Evaluate(st, ft)[1]) <= int(self.children[1].Evaluate(st, ft)[1]))]
            else:
                sys.stderr.write("Tipo dos operadores inválido.")
                sys.exit(1)
                return
        else:
            sys.stderr.write("Tipo da operação inválido.")
            sys.exit(1)
            return


class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def Evaluate(self, st, ft):
        if self.children[0].Evaluate(st, ft)[0] == "INT":
            if self.value == "+":
                return ["INT", int(self.children[0].Evaluate(st, ft)[1])]
            elif self.value == "-":
                return ["INT", int(-self.children[0].Evaluate(st, ft)[1])]
            elif self.value == "not":
                return ["INT", int(not self.children[0].Evaluate(st, ft)[1])]
        else:
            sys.stderr.write("Tipo dos operadores inválido para UnOp")
            sys.exit(1)
            return

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def Evaluate(self, st, ft):
        return ["INT", int(self.value)]

class StrVal(Node):
    def __init__(self, value):
        super().__init__(value, [])

    def Evaluate(self, st, ft):
        return ["STR", self.value]

class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])

    def Evaluate(self, st, ft):
        pass

class Block(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st, ft):
        for child in self.children:
            child.Evaluate(st, ft)

class Identifier(Node):
    def _init_(self, value):
        super()._init_(value, [])

    def Evaluate(self, st, ft):
        try:
            try:
                true = (st.get(self.value))[0].isalpha()
                return ["STR", st.get(self.value)[0]]
            except:
                return ["INT", st.get(self.value)[0]]
        except:
            sys.stderr.write("Variável sendo usada sem ser declarada [ " + self.value + " ]")
            sys.exit(1)

class Assign(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st, ft):
        st.set(self.children[0].value, self.children[1].Evaluate(st, ft)[1], self.children[1].Evaluate(st, ft)[0])

class VarDec(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st, ft):
        if self.children[1] is not None:
            st.create(self.children[0].value)
            st.set(self.children[0].value, self.children[1].Evaluate(st, ft)[1], self.children[1].Evaluate(st, ft)[0])
        else:
            st.create(self.children[0].value)

class Return(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st, ft):
        return self.children[0].Evaluate(st, ft)

class Print(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st, ft):
        var = self.children[0].Evaluate(st, ft)
        if var[0] == "STR":
            sys.stdout.write(str(var[1]) + "\n")
        elif var[0] == "INT":
            sys.stdout.write(str(var[1]) + "\n")

class If(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st, ft):
        if self.children[0].Evaluate(st, ft)[1]:
            for child in self.children[1]:
                child.Evaluate(st, ft)
        elif len(self.children) == 3:
            for child in self.children[2]:
                child.Evaluate(st, ft)

class While(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st, ft):
        while self.children[0].Evaluate(st, ft)[1] == 1:
            for child in self.children[1]:
                child.Evaluate(st, ft)

class Read(Node):
    def _init_(self, children):
        super()._init_(None, children)

    def Evaluate(self, st, ft):
        return ["INT", self.value]

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parseExpression(tok):
        resultado = Parser.parseTerm(tok)
        while (1):
            if tok.next is not None and tok.next.type == "PLUS_SIMPLE":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS_SIMPLE" and tok.next.type != "MINUS_SIMPLE" and tok.next.type != "IDEN":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (6 0 1)")
                    sys.exit(1)
                else:
                    resultado = BinOp("+", [resultado, Parser.parseTerm(tok)])
            elif tok.next is not None and tok.next.type == "MINUS_SIMPLE":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS_SIMPLE" and tok.next.type != "MINUS_SIMPLE" and tok.next.type != "IDEN":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (6 1 )")
                    sys.exit(1)
                else:
                    resultado = BinOp("-", [resultado, Parser.parseTerm(tok)])
            elif tok.next is not None and tok.next.type == "CONCAT":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS_SIMPLE" and tok.next.type != "MINUS_SIMPLE" and tok.next.type != "IDEN" and tok.next.type != "STR":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (6 2 )")
                    sys.exit(1)
                else:
                    resultado = BinOp("CONCAT", [resultado, Parser.parseTerm(tok)])
            else:
                return resultado

    def parseTerm(tok):
        resultado = Parser.parseFactor(tok)
        while (1):
            if tok.next is not None and tok.next.type == "TIMES":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS_SIMPLE" and tok.next.type != "MINUS_SIMPLE" and tok.next.type != "IDEN":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (7)")
                    sys.exit(1)
                else:
                    resultado = BinOp("*", [resultado, Parser.parseFactor(tok)])

            elif tok.next is not None and tok.next.type == "DIV":
                tok.selectNext()
                if tok.next.type != "NUMBER" and tok.next.type != "LPAREN" and tok.next.type != "PLUS_SIMPLE" and tok.next.type != "MINUS_SIMPLE" and tok.next.type != "IDEN":
                    sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (7)")
                    sys.exit(1)
                else:
                    resultado = BinOp("/", [resultado, Parser.parseFactor(tok)])
            else:
                return resultado

    def parseFactor(tok):
        if tok.next.type == "NUMBER":
            numero = tok.next.value
            tok.selectNext()
            return IntVal(numero)
        elif tok.next is not None and tok.next.type == "PLUS_SIMPLE":
            tok.selectNext()
            numero = UnOp("+", [Parser.parseFactor(tok)])
            return numero
        elif tok.next is not None and tok.next.type == "MINUS_SIMPLE":
            tok.selectNext()
            numero = UnOp("-", [Parser.parseFactor(tok)])
            return numero
        elif tok.next is not None and tok.next.type == "LPAREN":
            tok.selectNext()
            resultado = Parser.parseBoolExp(tok)
            if tok.next.type != "RPAREN":
                sys.stderr.write("Erro de sintaxe. ')' esperado. (9)")
                sys.exit(1)
            else:
                tok.selectNext()
                return resultado
        elif tok.next.type == "IDEN":
            id_saida = tok.next.value
            tok.selectNext()
            return Identifier(value=id_saida)
        elif tok.next.type == "INSERT":
            tok.selectNext()
            if tok.next.type != "LPAREN":
                sys.stderr.write("Erro de sintaxe. '(' esperado. (10)")
                sys.exit(1)
            else:
                tok.selectNext()
                if tok.next.type != "RPAREN":
                    sys.stderr.write("Erro de sintaxe. ')' esperado. (11)")
                    sys.exit(1)
                else:
                    tok.selectNext()
                    return Read(value=int(input()))
        elif tok.next.type == "STR":
            string = tok.next.value
            tok.selectNext()
            return StrVal(value=string)
        else:
            sys.stderr.write("Erro de sintaxe. Número ou '(' esperado. (10)")
            sys.exit(1)

    def parseStatement(tok):
        if tok.next.type == "IDEN":
            iden = tok.next.value
            tok.selectNext()
            if tok.next.type == "IS":
                tok.selectNext()
                saida = Parser.parseBoolExp(tok)
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. New Line esperado. (11)")
                    sys.exit(1)
                else:
                    tok.selectNext()
                    return Assign(value="is",children=[Identifier(iden), saida])
            elif tok.next.type == "NEXT":
                tok.selectNext()
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. New Line esperado. (12)")
                    sys.exit(1)
                else:
                    tok.selectNext()
                    return BinOp(value="NEXT", children=[Identifier(iden)])
            elif tok.next.type == "PLUS":
                tok.selectNext()
                saida = Parser.parseBoolExp(tok)
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. New Line esperado. (13)")
                    sys.exit(1)
                else:
                    tok.selectNext()
                    return BinOp(value="+=", children=[Identifier(iden), saida])
            elif tok.next.type == "MINUS":
                tok.selectNext()
                saida = Parser.parseBoolExp(tok)
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. New Line esperado. (14)")
                    sys.exit(1)
                else:
                    tok.selectNext()
                    return BinOp(value="-=", children=[Identifier(iden), saida])
            else:
                sys.stderr.write("Erro de sintaxe. '=' esperado. (31)")
                sys.exit(1)
        elif tok.next.type == "DISPLAY":
            tok.selectNext()
            if tok.next.type != "LPAREN":
                sys.stderr.write("Erro de sintaxe. '(' esperado. (4)")
                sys.exit(1)
            else:
                tok.selectNext()
                saida = Parser.parseBoolExp(tok)
                if tok.next.type != "RPAREN":
                    sys.stderr.write("Erro de sintaxe. ')' esperado. (5)")
                    sys.exit(1)
                tok.selectNext()
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. Nova linha esperada após RPAREN. (6)")
                    sys.exit(1)
                tok.selectNext()
                return Print(value="DISPLAY", children=[saida])
        elif tok.next.type == "VERIFY":
            tok.selectNext()
            if tok.next.type != "LPAREN":
                sys.stderr.write("Erro de sintaxe. '(' esperado. (5)")
                sys.exit(1)
            tok.selectNext()
            condicao = Parser.parseBoolExp(tok)
            if tok.next.type != "RPAREN":
                sys.stderr.write("Erro de sintaxe. ')' esperado. (6)")
                sys.exit(1)
            tok.selectNext()
            if tok.next.type != "THEN":
                sys.stderr.write("Erro de sintaxe. 'then' esperado. (7)")
                sys.exit(1)
            tok.selectNext()
            if tok.next.type != "COLON":
                sys.stderr.write("Erro de sintaxe. ':' esperado. (8)")
                sys.exit(1)
            tok.selectNext()
            if tok.next.type != "NL":
                sys.stderr.write("Erro de sintaxe. Nova linha esperada após THEN. (8)")
                sys.exit(1)
            tok.selectNext()
            bloco1 = []
            while tok.next.type != "END_VEF":
                bloco1.append(Parser.parseStatement(tok))
            tok.selectNext()
            if tok.next.type != "NL":
                sys.stderr.write("Erro de sintaxe. Nova linha esperada após END. (8)")
                sys.exit(1)
            tok.selectNext()
            if tok.next.type == "OTHER":
                tok.selectNext()
                if tok.next.type != "COLON":
                    sys.stderr.write("Erro de sintaxe. ':' esperado. (8)")
                    sys.exit(1)
                tok.selectNext()
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. Nova linha esperada após ELSE. (9)")
                    sys.exit(1)
                tok.selectNext()
                bloco2 = []
                while tok.next.type != "END_OTHER":
                    bloco2.append(Parser.parseStatement(tok))
                tok.selectNext()
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. Nova linha esperada após END. (9)")
                    sys.exit(1)
                tok.selectNext()
                return If(value="VERIFY", children=[condicao, bloco1, bloco2])
            else:
                return If(value="VERIFY", children=[condicao, bloco1])
        elif tok.next.type == "DURING_RACE":
            tok.selectNext()
            if tok.next.type != "LPAREN":
                sys.stderr.write("Erro de sintaxe. '(' esperado. (7)")
                sys.exit(1)
            tok.selectNext()
            condicao = Parser.parseBoolExp(tok)
            if tok.next.type != "RPAREN":
                sys.stderr.write("Erro de sintaxe. ')' esperado. (8)")
                sys.exit(1)
            tok.selectNext()
            if tok.next.type != "NL":
                sys.stderr.write("Erro de sintaxe. Nova linha esperada após DO. (11)")
                sys.exit(1)
            tok.selectNext()
            lista_statements = []
            while (tok.next.type != "END_RACE"):
                lista_statements.append(Parser.parseStatement(tok))
            tok.selectNext()
            if tok.next.type != "NL":
                sys.stderr.write("Erro de sintaxe. Nova linha esperada após END. (12)")
                sys.exit(1)
            tok.selectNext()
            whi =  While(value="during_race", children=[condicao, lista_statements])
            return whi
        elif tok.next.type == "SETUP":
            tok.selectNext()
            if tok.next.type != "IDEN":
                sys.stderr.write("Erro de sintaxe. Identificador esperado. (12)")
                sys.exit(1)
            iden = tok.next.value
            tok.selectNext()
            if tok.next.type == "IS":
                tok.selectNext()
                saida = Parser.parseBoolExp(tok)
                if tok.next.type != "NL":
                    sys.stderr.write("Erro de sintaxe. Nova linha esperada após NL. (13)")
                    sys.exit(1)
                tok.selectNext()
                return VarDec(value="is", children=[Identifier(iden), saida])
            elif tok.next.type == "NL":
                tok.selectNext()
                return VarDec(value="is", children=[Identifier(iden), None])
            else:
                sys.stderr.write("Erro de sintaxe. Erro após LOCAL. (14)")
                sys.exit(1)
        elif tok.next.type == "END_TRACKDAY":
            tok.selectNext()
            if tok.next.type != "NL":
                sys.stderr.write("Erro de sintaxe. Nova linha esperada após END_TRACKDAY. (15)")
                sys.exit(1)
            tok.selectNext()
            return NoOp()
        else:
            sys.stderr.write("Erro de sintaxe. '=' esperado. (3)")
            sys.exit(1)

    def parseBoolExp(tok):
        return Parser.parseBoolTerm(tok)

    def parseBoolTerm(tok):
        return Parser.parseRelExp(tok)

    def parseRelExp(tok):
        resultado = Parser.parseExpression(tok)
        if tok.next.type == "GT":
            tok.selectNext()
            return BinOp(">", [resultado, Parser.parseExpression(tok)])
        elif tok.next.type == "LT":
            tok.selectNext()
            return BinOp("<", [resultado, Parser.parseExpression(tok)])
        elif tok.next.type == "EQ":
            tok.selectNext()
            return BinOp("==", [resultado, Parser.parseExpression(tok)])
        elif tok.next.type == "NE":
            tok.selectNext()
            return BinOp("!=", [resultado, Parser.parseExpression(tok)])
        elif tok.next.type == "GE":
            tok.selectNext()
            return BinOp(">=", [resultado, Parser.parseExpression(tok)])
        elif tok.next.type == "LE":
            tok.selectNext()
            return BinOp("<=", [resultado, Parser.parseExpression(tok)])
        else:
            return resultado

    def parseBlock(tok):
        saida = Block([])
        if tok.next is None or tok.next.type != "TRACK_DAY":
            sys.stderr.write("Erro de sintaxe. TRACK_DAY esperado. (1)")
            sys.exit(1)
        tok.selectNext()
        if tok.next.type != "NL":
            sys.stderr.write("Erro de sintaxe. Nova linha esperada após TRACK_DAY. (1)")
            sys.exit(1)
        tok.selectNext()
        while tok.next.type != "END_TRACKDAY":
            saida.children.append(Parser.parseStatement(tok))
        tok.selectNext()
        if tok.next.type != "NL":
            sys.stderr.write("Erro de sintaxe. Nova linha esperada após END_TRACKDAY. (1)")
            sys.exit(1)
        tok.selectNext()
        return saida

    def run(code):
        code_filtrado = PrePro.filter(code=code)
        tokenizer = Tokenizer(code_filtrado, 0, None)
        tokenizer.selectNext()
        ast = Parser.parseBlock(tokenizer)
        st = SymbolTable()
        ft = SymbolTable()
        resultado = ast.Evaluate(st, ft)
        # Verifica se não há código após o END_TRACKDAY
        if tokenizer.next is not None:
            sys.stderr.write("Código após END_TRACKDAY")
            sys.exit(1)
        else:
            return resultado


class SymbolTable:
    def __init__(self):
        self.table = {}

    def set(self, key, value, type):
        if key in self.table:
            self.table[key] = [value, type]
        else:
            sys.stderr.write("Variável sendo definida sem ser declarada [ " + key + " ]")
            sys.exit(1)

    def get(self, key):
        return self.table[key]

    def create(self, key):
        if key not in self.table:
            self.table[key] = None
        else:
            sys.stderr.write("Variável sendo redefinida [ " + key + " ]")
            sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <file>")
        print("  |-> EXEMPLO: python main.py teste.ps")
        return

    file = sys.argv[1]
    if file[-3:] != ".ps":
        print("Erro: Arquivo inválido. Deve ser do tipo .ps")
        sys.stderr.write("Erro: Arquivo inválido. Deve ser do tipo .ps")
        sys.exit(1)
        return
    with open(file, "r") as f:
        file = f.read()

    left, right = 0, 0
    for char in file:
        if char == '(':
            left += 1
        if char == ')':
            right += 1

    if left != right:
        print("Erro: Número de parênteses inválido.")
        sys.stderr.write("Erro de sintaxe. Número de parênteses inválido.")
        sys.exit(1)
        return

    else:
        Parser.run(file)

if __name__ == "__main__":
    main()