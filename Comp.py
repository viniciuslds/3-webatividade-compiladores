def appendFile(file, text) -> None:
    "Adiciona informações ao arquivo tokens.csv, é usado para a exportação"
    arq = open(file,"a")
    arq.write(text)
    arq.close()

def clearFiles() -> None:
    "Limpa os arquivos de saída, é usado antes da exportação"
    files = ["tokens.csv","simbolos.csv"]
    
    for i in files:
        arq = open(i,"w")
        arq.write("")
        arq.close()

class Token:
    """
    Cria um novo tipo de dado chamado Token, um lexema
    É iniciado recebendo o seu token propriamente, a sua identificação e a sua posição
    A classe por si só calcula seu tamanho
    """
    def __init__(self, token, identification, position) -> object:
        self.token          = token
        self.identification = identification
        self.position       = position
        self.size           = len(token)
    
class Program:
    """
    Cria um novo tipo de dado chamado Program
    Tudo o que é relacionado ao programa a ser analisado está aqui
    É iniciado recebendo apenas as instruções
    A classe por si só calcula seu tamanho, inicializa a lista de tokens e cria sua tabela de índices
    """
    def __init__(self, instructions) -> object:
        self.instructions   = instructions
        self.size           = 0
        self.tokens         = []
        self.simbols        = {}

    def printscreen(self) -> None:
        "Apenas mostra em tela as instruções do programa"
        print(self.instructions)

    def export(self) -> None:
        """
        Realiza a exportação da tabela de símbolos do programa analisado
        O método Scan deve ser executando antes da exportação
        """
        clearFiles()
        appendFile("tokens.csv","Token;Identificação;Tamanho;Posição\n")
        for i in self.tokens:
            appendFile("tokens.csv",f"{i.token};{str(i.identification)};{i.size};{str(i.position)}\n")

        appendFile("simbolos.csv","Índice;Símbolo\n")
        for i in self.simbols:
            appendFile("simbolos.csv",f"{i};{self.simbols[i]}\n")
   

    def scan(self) -> None:
        """
        Realiza a identificação, um a um, dos Tokes dentro do Program
        Apresenta possíveis erros nas instruções do programa
        """
        tempToken = ""

        for element in self.instructions:
            '''if element == ";":
                token = Token(";", "Terminador", (0, (self.size - 1)))
                self.tokens.append(token)'''
            
            if element != " " and element != ".":
                tempToken += element
            
            else:
                identification = self.checkIdentification(tempToken)
                if identification != "Char Desconhecido":
                    if identification == "Constante" or identification == "Identificador":
                        self.checkSimbol(tempToken)
                        token = Token(tempToken, (identification, self.simbols[tempToken]), (0, (self.size - len(tempToken))))
                    else:
                        token = Token(tempToken, identification, (0, (self.size - len(tempToken))))
                    
                    self.tokens.append(token)

                else:
                    raise ValueError("Caractere desconhecido = ("+tempToken+") na posição "+str(self.size))

                tempToken = ""

            if element == ".":
                tempToken = "."
                token = Token(".", "Terminador", (0, (self.size)))
                self.tokens.append(token)

            self.size += 1
        
        if tempToken != ".":
           raise ValueError("O último caractere deve ser o terminador (.)")

    def checkSimbol(self, token):
        "Verifica se já contém os símbolo na tabela de símbolos"
        if token not in self.simbols:
            self.simbols[token] = len(self.simbols)

    def checkIdentification(self, token) -> str:
        "Verifica o token e retorna a sua identificação"
        if token == "<" or token == "=" or token == "+":
            return "Operador"

        elif token == "while" or token == "do":
            return "Palavra"

        elif token == "i" or token == "j":
            return "Identificador"
        
        elif token == "100":
            return "Constante"

        elif token == ".":
            return "Terminador"
        
        else:
            return "Char Desconhecido"

# Cria a instância de um programa
program = Program("while i < 100 do i = i + j.")
# Faz a varredura em busca de erros léxicos
program.scan()
# Exporta a tabela de Tokens em .csv
program.export()