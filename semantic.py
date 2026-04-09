from ast_nodes import Number, BinOp, Var, Decl, Programa, Assign, If, While, Compare, FunDecl, Call, Return

def verificar(programa):
    ambiente_global = {} 
    
    for decl in programa.decls:
        if isinstance(decl, Decl):
            verificar_expr(decl.expr, ambiente_global, None)
            ambiente_global[decl.name] = {'tipo': 'var'}
        elif isinstance(decl, FunDecl):
            # Registra função no ambiente global
            ambiente_global[decl.name] = {'tipo': 'fun', 'params': len(decl.params)}
            
            ambiente_local = set(decl.params)
            
            for f_decl in decl.decls:
                verificar_expr(f_decl.expr, ambiente_global, ambiente_local)
                ambiente_local.add(f_decl.name)
            
            for cmd in decl.cmds:
                verificar_cmd(cmd, ambiente_global, ambiente_local)

    for cmd in programa.cmds:
        verificar_cmd(cmd, ambiente_global, None)

def verificar_cmd(node, ambiente_global, ambiente_local):
    if isinstance(node, Assign):
        esta_em_local = ambiente_local and node.name in ambiente_local
        esta_em_global = node.name in ambiente_global and ambiente_global[node.name]['tipo'] == 'var'
        if not (esta_em_local or esta_em_global):
            raise NameError(f"Erro Semântico: Variável '{node.name}' não declarada!")
        verificar_expr(node.expr, ambiente_global, ambiente_local)

    elif isinstance(node, If):
        verificar_expr(node.cond, ambiente_global, ambiente_local)
        for c in node.then_cmds: verificar_cmd(c, ambiente_global, ambiente_local)
        for c in node.else_cmds: verificar_cmd(c, ambiente_global, ambiente_local)

    elif isinstance(node, While):
        verificar_expr(node.cond, ambiente_global, ambiente_local)
        for c in node.cmds: verificar_cmd(c, ambiente_global, ambiente_local)

    elif isinstance(node, Return):
        verificar_expr(node.expr, ambiente_global, ambiente_local)

def verificar_expr(node, ambiente_global, ambiente_local):
    if isinstance(node, Number):
        return

    elif isinstance(node, Var):
        esta_em_local = ambiente_local and node.name in ambiente_local
        esta_em_global = node.name in ambiente_global and ambiente_global[node.name]['tipo'] == 'var'
        if not (esta_em_local or esta_em_global):
            raise NameError(f"Erro Semântico: A variável '{node.name}' não foi declarada!")

    elif isinstance(node, Call):
        if node.name not in ambiente_global or ambiente_global[node.name]['tipo'] != 'fun':
            raise NameError(f"Erro Semântico: A função '{node.name}' não foi declarada!")
        
        qtd_esperada = ambiente_global[node.name]['params']
        if len(node.args) != qtd_esperada:
            raise TypeError(f"Erro Semântico: Função '{node.name}' espera {qtd_esperada} argumentos, mas recebeu {len(node.args)}.")
            
        for arg in node.args:
            verificar_expr(arg, ambiente_global, ambiente_local)

    elif isinstance(node, (BinOp, Compare)):
        verificar_expr(node.left, ambiente_global, ambiente_local)
        verificar_expr(node.right, ambiente_global, ambiente_local)

    else:
        raise ValueError(f"Nó desconhecido na análise semântica: {type(node).__name__}")