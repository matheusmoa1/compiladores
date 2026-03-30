from ast_nodes import Number, BinOp, Var, Decl, Programa, Assign, If, While, Compare


def verificar(programa):
    # Nossa 'tabela de símbolos' é um set simples com os nomes das variáveis
    declaradas = set()

    # 1. Primeiro, registramos quem nasceu no topo do programa
    for decl in programa.decls:
        # A expressão que inicializa a variável também precisa ser válida!
        verificar_expr(decl.expr, declaradas)
        declaradas.add(decl.name)

    # 2. Depois, conferimos se os comandos (if, while, atribuição) fazem sentido
    for cmd in programa.cmds:
        verificar_cmd(cmd, declaradas)

    # 3. Por fim, checamos a expressão de retorno lá no final
    verificar_expr(programa.result, declaradas)


def verificar_cmd(node, declaradas):
    if isinstance(node, Assign):
        # Regra de ouro: Não pode dar valor pra quem não foi declarado
        if node.name not in declaradas:
            raise NameError(f"Erro Semântico: Você tentou mudar a variável '{node.name}', mas ela nem foi declarada!")
        
        # O valor que você está atribuindo também precisa ser uma conta válida
        verificar_expr(node.expr, declaradas)

    elif isinstance(node, If):
        # No 'if', a condição tem que ser válida
        verificar_expr(node.cond, declaradas)
        # E todos os comandos dentro do 'then' e do 'else' também
        for c in node.then_cmds: verificar_cmd(c, declaradas)
        for c in node.else_cmds: verificar_cmd(c, declaradas)

    elif isinstance(node, While):
        # No 'while', a condição manda
        verificar_expr(node.cond, declaradas)
        # E o corpo do loop precisa estar limpo
        for c in node.cmds: verificar_cmd(c, declaradas)


def verificar_expr(node, declaradas):
    if isinstance(node, Number):
        # Número é número, não tem erro
        return

    elif isinstance(node, Var):
        if node.name not in declaradas:
            raise NameError(f"Erro Semântico: A variável '{node.name}' apareceu do nada! Você esqueceu de declarar?")

    elif isinstance(node, (BinOp, Compare)):
        # Se for conta (+, -, *) ou comparação (==, <, >), checa os dois lados
        verificar_expr(node.left, declaradas)
        verificar_expr(node.right, declaradas)

    else:
        # Se cair aqui, é porque o nó é algum tipo que a gente não esperava
        raise ValueError(f"Nó desconhecido na análise semântica: {type(node).__name__}")