#!/usr/bin/env python3
"""
Generador de Railroad Diagrams para B-Minor+
Genera diagramas de sintaxis para todas las reglas importantes de la gramática
"""

import os
from railroad import *

# Crear directorio de salida
os.makedirs('out/svg', exist_ok=True)

# ============================================================
# PROGRAM
# ============================================================

def d_prog():
    """prog ::= decl_list 'EOF'"""
    return Diagram(
        Seq(
            N("decl_list"),
            T("EOF")
        )
    )

# ============================================================
# DECLARATIONS
# ============================================================

def d_decl_list():
    """decl_list ::= epsilon | decl decl_list"""
    return Diagram(
        ZM(N("decl"))
    )

def d_decl():
    """decl ::= ID : type ; | decl_init | class_decl"""
    return Diagram(
        Ch(
            Seq(T("ID"), T(":"), N("type_simple"), T(";")),
            Seq(T("ID"), T(":"), N("type_array_sized"), T(";")),
            Seq(T("ID"), T(":"), N("type_func"), T(";")),
            N("decl_init"),
            N("class_decl")
        )
    )

def d_decl_init():
    """decl_init ::= ID : type = expr ; | ..."""
    return Diagram(
        Ch(
            Seq(T("ID"), T(":"), N("type_simple"), T("="), N("expr"), T(";")),
            Seq(T("ID"), T(":"), N("type_array_sized"), T("="), T("{"), N("opt_expr_list"), T("}"), T(";")),
            Seq(T("ID"), T(":"), N("type_func"), T("="), T("{"), N("opt_stmt_list"), T("}"))
        )
    )

def d_class_decl():
    """class_decl ::= ID : CLASS = { class_body }"""
    return Diagram(
        Seq(
            T("ID"),
            T(":"),
            T("CLASS"),
            T("="),
            T("{"),
            N("class_body"),
            T("}")
        )
    )

def d_class_body():
    """class_body ::= epsilon | class_member class_body"""
    return Diagram(
        ZM(N("class_member"))
    )

def d_class_member():
    """class_member ::= field or method"""
    return Diagram(
        Ch(
            Seq(T("ID"), T(":"), N("type_simple"), T(";")),
            Seq(T("ID"), T(":"), N("type_array_sized"), T(";")),
            Seq(T("ID"), T(":"), N("type_func"), T("="), T("{"), N("opt_stmt_list"), T("}"))
        )
    )

# ============================================================
# STATEMENTS
# ============================================================

def d_stmt():
    """stmt ::= open_stmt | closed_stmt"""
    return Diagram(
        Ch(
            N("open_stmt"),
            N("closed_stmt")
        )
    )

def d_closed_stmt():
    """closed_stmt ::= if_stmt_closed | for_stmt_closed | while_stmt_closed | simple_stmt"""
    return Diagram(
        Ch(
            N("if_stmt_closed"),
            N("for_stmt_closed"),
            N("while_stmt_closed"),
            N("simple_stmt")
        )
    )

def d_open_stmt():
    """open_stmt ::= if_stmt_open | for_stmt_open | while_stmt_open"""
    return Diagram(
        Ch(
            N("if_stmt_open"),
            N("for_stmt_open"),
            N("while_stmt_open")
        )
    )

def d_if_stmt_closed():
    """if_stmt_closed ::= IF ( opt_expr ) closed_stmt ELSE closed_stmt"""
    return Diagram(
        Seq(
            T("IF"),
            T("("),
            N("opt_expr"),
            T(")"),
            N("closed_stmt"),
            T("ELSE"),
            N("closed_stmt")
        )
    )

def d_if_stmt_open():
    """if_stmt_open ::= IF ( opt_expr ) stmt | IF ( opt_expr ) closed_stmt ELSE if_stmt_open"""
    return Diagram(
        Ch(
            Seq(T("IF"), T("("), N("opt_expr"), T(")"), N("stmt")),
            Seq(T("IF"), T("("), N("opt_expr"), T(")"), N("closed_stmt"), T("ELSE"), N("open_stmt"))
        )
    )

def d_for_stmt_closed():
    """for_stmt_closed ::= FOR ( opt_expr ; opt_expr ; opt_expr ) closed_stmt"""
    return Diagram(
        Seq(
            T("FOR"),
            T("("),
            N("opt_expr"),
            T(";"),
            N("opt_expr"),
            T(";"),
            N("opt_expr"),
            T(")"),
            N("closed_stmt")
        )
    )

def d_for_stmt_open():
    """for_stmt_open ::= FOR ( opt_expr ; opt_expr ; opt_expr ) open_stmt"""
    return Diagram(
        Seq(
            T("FOR"),
            T("("),
            N("opt_expr"),
            T(";"),
            N("opt_expr"),
            T(";"),
            N("opt_expr"),
            T(")"),
            N("open_stmt")
        )
    )

def d_while_stmt_closed():
    """while_stmt_closed ::= WHILE ( opt_expr ) closed_stmt"""
    return Diagram(
        Seq(
            T("WHILE"),
            T("("),
            N("opt_expr"),
            T(")"),
            N("closed_stmt")
        )
    )

def d_while_stmt_open():
    """while_stmt_open ::= WHILE ( opt_expr ) open_stmt"""
    return Diagram(
        Seq(
            T("WHILE"),
            T("("),
            N("opt_expr"),
            T(")"),
            N("open_stmt")
        )
    )

def d_simple_stmt():
    """simple_stmt ::= print | return | block | decl | expr ;"""
    return Diagram(
        Ch(
            N("print_stmt"),
            N("return_stmt"),
            N("block_stmt"),
            N("decl"),
            Seq(N("expr"), T(";"))
        )
    )

def d_print_stmt():
    """print_stmt ::= PRINT opt_expr_list ;"""
    return Diagram(
        Seq(
            T("PRINT"),
            N("opt_expr_list"),
            T(";")
        )
    )

def d_return_stmt():
    """return_stmt ::= RETURN opt_expr ;"""
    return Diagram(
        Seq(
            T("RETURN"),
            N("opt_expr"),
            T(";")
        )
    )

def d_block_stmt():
    """block_stmt ::= { stmt_list }"""
    return Diagram(
        Seq(
            T("{"),
            N("stmt_list"),
            T("}")
        )
    )

# ============================================================
# EXPRESSIONS - Transformadas para evitar recursión izquierda
# ============================================================

def d_expr():
    """expr ::= expr1"""
    return Diagram(N("expr1"))

def d_expr1():
    """expr1 ::= lval (= | += | -= | *= | /=) expr1 | expr1_5"""
    return Diagram(
        Ch(
            Seq(
                N("lval"),
                Ch(T("="), T("+="), T("-="), T("*="), T("/=")),
                N("expr1")
            ),
            N("expr1_5")
        )
    )

def d_expr1_5():
    """expr1_5 ::= expr2 ? expr1_5 : expr1_5 | expr2"""
    return Diagram(
        Ch(
            Seq(N("expr2"), T("?"), N("expr1_5"), T(":"), N("expr1_5")),
            N("expr2")
        )
    )

def d_expr2():
    """expr2 ::= expr3 (LOR expr3)*"""
    return Diagram(
        Seq(
            N("expr3"),
            ZM(Seq(T("||"), N("expr3")))
        )
    )

def d_expr3():
    """expr3 ::= expr4 (LAND expr4)*"""
    return Diagram(
        Seq(
            N("expr4"),
            ZM(Seq(T("&&"), N("expr4")))
        )
    )

def d_expr4():
    """expr4 ::= expr5 ((== | != | < | <= | > | >=) expr5)*"""
    return Diagram(
        Seq(
            N("expr5"),
            ZM(
                Seq(
                    Ch(T("=="), T("!="), T("<"), T("<="), T(">"), T(">=")),
                    N("expr5")
                )
            )
        )
    )

def d_expr5():
    """expr5 ::= expr6 ((+ | -) expr6)*"""
    return Diagram(
        Seq(
            N("expr6"),
            ZM(
                Seq(
                    Ch(T("+"), T("-")),
                    N("expr6")
                )
            )
        )
    )

def d_expr6():
    """expr6 ::= expr7 ((* | / | %) expr7)*"""
    return Diagram(
        Seq(
            N("expr7"),
            ZM(
                Seq(
                    Ch(T("*"), T("/"), T("%")),
                    N("expr7")
                )
            )
        )
    )

def d_expr7():
    """expr7 ::= expr8 (^ expr8)*"""
    return Diagram(
        Seq(
            N("expr8"),
            ZM(Seq(T("^"), N("expr8")))
        )
    )

def d_expr8():
    """expr8 ::= (- | ! | ++ | --)? expr9"""
    return Diagram(
        Seq(
            Opt(Ch(T("-"), T("!"), T("++"), T("--"))),
            N("expr9")
        )
    )

def d_expr9():
    """expr9 ::= group (++ | -- | . ID)*"""
    return Diagram(
        Seq(
            N("group"),
            ZM(
                Ch(
                    T("++"),
                    T("--"),
                    Seq(T("."), T("ID"))
                )
            )
        )
    )

def d_group():
    """group ::= ( expr ) | ID ( opt_expr_list ) | NEW ID ( opt_expr_list ) | ID index | factor"""
    return Diagram(
        Ch(
            Seq(T("("), N("expr"), T(")")),
            Seq(T("ID"), T("("), N("opt_expr_list"), T(")")),
            Seq(T("NEW"), T("ID"), T("("), N("opt_expr_list"), T(")")),
            Seq(T("ID"), N("index")),
            N("factor")
        )
    )

def d_lval():
    """lval ::= ID | ID index | lval . ID"""
    return Diagram(
        Ch(
            T("ID"),
            Seq(T("ID"), N("index")),
            Seq(N("lval"), T("."), T("ID"))
        )
    )

def d_index():
    """index ::= [ expr ]"""
    return Diagram(
        Seq(T("["), N("expr"), T("]"))
    )

def d_factor():
    """factor ::= ID | INTEGER_LITERAL | FLOAT_LITERAL | CHAR_LITERAL | STRING_LITERAL | TRUE | FALSE"""
    return Diagram(
        Ch(
            T("ID"),
            T("INTEGER_LITERAL"),
            T("FLOAT_LITERAL"),
            T("CHAR_LITERAL"),
            T("STRING_LITERAL"),
            T("TRUE"),
            T("FALSE")
        )
    )

# ============================================================
# TYPES
# ============================================================

def d_type_simple():
    """type_simple ::= INTEGER | FLOAT | BOOLEAN | CHAR | STRING | VOID | ID"""
    return Diagram(
        Ch(
            T("INTEGER"),
            T("FLOAT"),
            T("BOOLEAN"),
            T("CHAR"),
            T("STRING"),
            T("VOID"),
            T("ID")
        )
    )

def d_type_array():
    """type_array ::= ARRAY [] type_simple | ARRAY [] type_array"""
    return Diagram(
        Seq(
            T("ARRAY"),
            T("["),
            T("]"),
            Ch(N("type_simple"), N("type_array"))
        )
    )

def d_type_array_sized():
    """type_array_sized ::= ARRAY index type_simple | ARRAY index type_array_sized"""
    return Diagram(
        Seq(
            T("ARRAY"),
            N("index"),
            Ch(N("type_simple"), N("type_array_sized"))
        )
    )

def d_type_func():
    """type_func ::= FUNCTION type ( opt_param_list )"""
    return Diagram(
        Seq(
            T("FUNCTION"),
            Ch(N("type_simple"), N("type_array_sized")),
            T("("),
            N("opt_param_list"),
            T(")")
        )
    )

# ============================================================
# GENERACIÓN DE TODOS LOS DIAGRAMAS
# ============================================================

diagrams = {
    # Program
    'prog': d_prog,
    
    # Declarations
    'decl_list': d_decl_list,
    'decl': d_decl,
    'decl_init': d_decl_init,
    'class_decl': d_class_decl,
    'class_body': d_class_body,
    'class_member': d_class_member,
    
    # Statements
    'stmt': d_stmt,
    'closed_stmt': d_closed_stmt,
    'open_stmt': d_open_stmt,
    'if_stmt_closed': d_if_stmt_closed,
    'if_stmt_open': d_if_stmt_open,
    'for_stmt_closed': d_for_stmt_closed,
    'for_stmt_open': d_for_stmt_open,
    'while_stmt_closed': d_while_stmt_closed,
    'while_stmt_open': d_while_stmt_open,
    'simple_stmt': d_simple_stmt,
    'print_stmt': d_print_stmt,
    'return_stmt': d_return_stmt,
    'block_stmt': d_block_stmt,
    
    # Expressions
    'expr': d_expr,
    'expr1': d_expr1,
    'expr1_5': d_expr1_5,
    'expr2': d_expr2,
    'expr3': d_expr3,
    'expr4': d_expr4,
    'expr5': d_expr5,
    'expr6': d_expr6,
    'expr7': d_expr7,
    'expr8': d_expr8,
    'expr9': d_expr9,
    'group': d_group,
    'lval': d_lval,
    'index': d_index,
    'factor': d_factor,
    
    # Types
    'type_simple': d_type_simple,
    'type_array': d_type_array,
    'type_array_sized': d_type_array_sized,
    'type_func': d_type_func,
}

print("Generando railroad diagrams...")
for name, func in diagrams.items():
    diagram = func()
    filename = f'out/svg/{name}.svg'
    diagram.save(filename)
    print(f"  ✓ {filename}")

print(f"\n✅ {len(diagrams)} diagramas generados en out/svg/")

# Generar índice en Markdown
print("\nGenerando índice...")
with open('out/index.md', 'w') as f:
    f.write("# B-Minor+ Grammar - Railroad Diagrams\n\n")
    f.write("## Program Structure\n\n")
    f.write("### prog\n![[svg/prog.svg]]\n\n")
    
    f.write("## Declarations\n\n")
    for name in ['decl_list', 'decl', 'decl_init', 'class_decl', 'class_body', 'class_member']:
        f.write(f"### {name}\n![[svg/{name}.svg]]\n\n")
    
    f.write("## Statements\n\n")
    stmt_rules = ['stmt', 'closed_stmt', 'open_stmt', 
                  'if_stmt_closed', 'if_stmt_open',
                  'for_stmt_closed', 'for_stmt_open',
                  'while_stmt_closed', 'while_stmt_open',
                  'simple_stmt', 'print_stmt', 'return_stmt', 'block_stmt']
    for name in stmt_rules:
        f.write(f"### {name}\n![[svg/{name}.svg]]\n\n")
    
    f.write("## Expressions\n\n")
    expr_rules = ['expr', 'expr1', 'expr1_5', 'expr2', 'expr3', 'expr4', 
                  'expr5', 'expr6', 'expr7', 'expr8', 'expr9',
                  'group', 'lval', 'index', 'factor']
    for name in expr_rules:
        f.write(f"### {name}\n![[svg/{name}.svg]]\n\n")
    
    f.write("## Types\n\n")
    for name in ['type_simple', 'type_array', 'type_array_sized', 'type_func']:
        f.write(f"### {name}\n![[svg/{name}.svg]]\n\n")

print("✅ Índice generado en out/index.md")
print("\n🎉 ¡Listo! Todos los diagramas han sido generados.")
