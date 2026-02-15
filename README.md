# B-Minor+ Grammar Extension
### Railroad Diagrams Atlas

---

## 📋 Descripción del Proyecto

Este proyecto presenta una **extensión completa del lenguaje B-Minor**, denominada **B-Minor+**, que añade nuevas construcciones de programación orientada a objetos y operadores modernos, manteniendo compatibilidad total con la gramática original.

El proyecto incluye:
- ✅ Gramática completa en formato BNF
- ✅ 39 diagramas de sintaxis (railroad diagrams) en SVG
- ✅ Visualizador web interactivo
- ✅ Documentación exhaustiva de diseño

---

## 🎯 Extensiones Implementadas

### 1. **Clases y Objetos**
Soporte completo para programación orientada a objetos:

```bminor
Sieve: class = {
    limit: integer;
    is_prime: array [100] boolean;
    
    init: function void (n:integer) = {
        limit = n;
    }
}

s: Sieve;
s = new Sieve(100);
s.init(50);
```

**Nuevas reglas:**
- `class_decl`: Declaración de clases
- `class_body`: Cuerpo de la clase
- `class_member`: Miembros (datos y métodos)
- `NEW`: Operador de construcción
- `.`: Acceso a miembros

### 2. **While Loop**
Bucle while con manejo correcto del dangling-else:

```bminor
while (i < 10) {
    print i;
    i++;
}
```

**Nuevas reglas:**
- `while_stmt_closed`
- `while_stmt_open`

### 3. **Operadores de Incremento/Decremento**
Pre y post incremento/decremento:

```bminor
i++;      // post-incremento
++i;      // pre-incremento
--count;  // pre-decremento
total--;  // post-decremento
```

**Reglas modificadas:**
- `expr8`: Pre-incremento/decremento
- `expr9`: Post-incremento/decremento

### 4. **Operadores de Asignación Compuesta**
Operadores compuestos para código más conciso:

```bminor
total += value;     // total = total + value
count -= 1;         // count = count - 1
product *= 2;       // product = product * 2
average /= n;       // average = average / n
```

**Reglas modificadas:**
- `expr1`: Asignación compuesta

### 5. **Operador Ternario**
Expresión condicional ternaria:

```bminor
result = (x > 0) ? x : -x;
print is_prime[i] ? i : 0;
```

**Nueva regla:**
- `expr1_5`: Operador ternario

---

## 📊 Precedencia y Asociatividad

| Nivel | Operadores | Asociatividad | Regla |
|-------|-----------|---------------|-------|
| 1 (menor) | `=` `+=` `-=` `*=` `/=` | Derecha | expr1 |
| 2 | `?:` | Derecha | expr1_5 |
| 3 | `\|\|` | Izquierda | expr2 |
| 4 | `&&` | Izquierda | expr3 |
| 5 | `==` `!=` `<` `<=` `>` `>=` | Izquierda | expr4 |
| 6 | `+` `-` | Izquierda | expr5 |
| 7 | `*` `/` `%` | Izquierda | expr6 |
| 8 | `^` | Izquierda | expr7 |
| 9 | `-` `!` `++` `--` (prefijo) | Derecha | expr8 |
| 10 (mayor) | `()` `[]` `.` `++` `--` (postfijo) | Izquierda | expr9 |

---

## 🚀 Estructura del Proyecto

```
bminor-plus/
├── grammar_bminor_plus.txt      # Gramática completa en BNF
├── railroad.py                   # Librería de railroad diagrams
├── generate_diagrams.py          # Generador de diagramas
├── out/
│   ├── svg/                      # 39 diagramas SVG
│   │   ├── prog.svg
│   │   ├── class_decl.svg
│   │   ├── while_stmt_closed.svg
│   │   ├── expr1_5.svg
│   │   └── ...
│   ├── index.html                # Visualizador web interactivo
│   └── index.md                  # Índice para Obsidian
└── README.md                     # Este archivo
```

---

## 🔧 Uso

### Generar los Diagramas

```bash
python3 generate_diagrams.py
```

Esto generará:
- 39 archivos SVG en `out/svg/`
- `out/index.html` - Visualizador web
- `out/index.md` - Índice markdown

### Visualizar los Diagramas

**Opción 1: Navegador Web**
```bash
# Abrir en navegador
open out/index.html
# o
firefox out/index.html
```

**Opción 2: Obsidian**
1. Abrir la carpeta `out/` en Obsidian
2. Abrir el archivo `index.md`

**Opción 3: Archivos SVG individuales**
```bash
# Ver un diagrama específico
open out/svg/while_stmt_closed.svg
```

---

## 📐 Diseño de la Extensión

### Principio Fundamental: No Modificación

**Restricción clave:** No se modificó ninguna regla existente de la gramática original.

Todas las extensiones se realizaron mediante:
1. **Adición de alternativas**: Nuevas opciones en reglas existentes
2. **Nuevos no-terminales**: Reglas completamente nuevas
3. **Composición**: Las nuevas reglas componen con las existentes

### Ejemplos de Extensión No-Invasiva

#### ✅ Correcto: Añadir alternativa
```bnf
/* Original */
decl ::= 'ID' ':' type_simple ';'
    | 'ID' ':' type_array_sized ';'
    | decl_init

/* Extendido */
decl ::= 'ID' ':' type_simple ';'
    | 'ID' ':' type_array_sized ';'
    | decl_init
    | class_decl              /* NUEVA ALTERNATIVA */
```

#### ❌ Incorrecto: Modificar regla existente
```bnf
/* NO PERMITIDO */
decl ::= 'ID' ':' type_or_class ';'  /* Cambia regla original */
```

### Resolución del Dangling-Else

La gramática original ya resuelve el problema del dangling-else usando el patrón **open/closed statements**:

- **closed_stmt**: Statements completos (if-else completo, for, while)
- **open_stmt**: Statements incompletos (if sin else)

Este patrón se extendió consistentemente a `while`:
```bnf
while_stmt_closed ::= 'WHILE' '(' opt_expr ')' closed_stmt
while_stmt_open ::= 'WHILE' '(' opt_expr ')' open_stmt
```

### Transformación de Recursión Izquierda

Para los diagramas, las reglas con recursión izquierda se transformaron a forma iterativa:

**Original (recursión izquierda):**
```bnf
expr5 ::= expr5 '+' expr6
    | expr5 '-' expr6
    | expr6
```

**Transformada (para diagrama):**
```bnf
expr5 ::= expr6 (('+' | '-') expr6)*
```

Esta transformación es **solo para visualización**; la gramática BNF mantiene la forma original.

---

## 🎨 Leyenda de Diagramas

### Componentes Visuales

- **🟢 Verde (redondeado)**: Terminales (tokens, palabras clave)
  - Ejemplo: `WHILE`, `CLASS`, `+`, `;`

- **🔵 Azul (rectangular)**: No-terminales (reglas)
  - Ejemplo: `expr`, `stmt`, `type_simple`

- **●━━━●**: Puntos de inicio y fin del diagrama

- **Bifurcaciones**: Indican alternativas (OR)

- **Bucles**: Indican repetición (zero or more)

---

## 🆕 Nuevos Tokens Requeridos

Para implementar un scanner/lexer de B-Minor+, se requieren estos nuevos tokens:

| Token | Símbolo | Descripción |
|-------|---------|-------------|
| `CLASS` | `class` | Palabra clave para clases |
| `NEW` | `new` | Operador de construcción |
| `WHILE` | `while` | Palabra clave while |
| `PLUSEQ` | `+=` | Asignación con suma |
| `MINUSEQ` | `-=` | Asignación con resta |
| `TIMESEQ` | `*=` | Asignación con multiplicación |
| `DIVEQ` | `/=` | Asignación con división |
| `DOT` | `.` | Acceso a miembros |
| `QUESTION` | `?` | Operador ternario (condición) |
| `INC` | `++` | Incremento (ya existe) |
| `DEC` | `--` | Decremento (ya existe) |
| `COLON` | `:` | Dos puntos (ya existe) |

---

## 📝 Ejemplos de Código B-Minor+

### Ejemplo Completo: Criba de Eratóstenes

```bminor
Sieve: class = {
    limit: integer;
    is_prime: array [100] boolean;

    init: function void (n:integer) = {
        i: integer;
        limit = n;
        
        i = 0;
        while (i <= limit) {
            is_prime[i] = true;
            i++;
        }
        
        is_prime[0] = false;
        is_prime[1] = false;
    }

    run: function void () = {
        p: integer;
        multiple: integer;

        p = 2;
        while (p * p <= limit) {
            if (is_prime[p]) {
                multiple = p * p;
                while (multiple <= limit) {
                    is_prime[multiple] = false;
                    multiple += p;  // Operador compuesto
                }
            }
            p++;
        }
    }
    
    print_primes: function void () = {
        i: integer;
        i = 2;
        while (i <= limit) {
            // Operador ternario
            print is_prime[i] ? i : 0;
            i++;
        }
    }
}

main: function void () = {
    s: Sieve;
    s = new Sieve();  // Constructor
    s.init(100);       // Acceso a miembro
    s.run();
    s.print_primes();
}
```

### Uso de Nuevas Características

```bminor
// Operadores compuestos
total += value;
count -= 1;
product *= 2;
average /= n;

// Pre y post incremento
++i;
i++;
--count;
value--;

// Operador ternario
max = (a > b) ? a : b;
sign = (x >= 0) ? 1 : -1;

// While loop
while (i < n) {
    sum += arr[i];
    i++;
}

// Clases
Point: class = {
    x: integer;
    y: integer;
    
    distance: function float () = {
        return sqrt(x*x + y*y);
    }
}

p: Point;
p = new Point();
p.x = 10;
p.y = 20;
```

---

## 📚 Diagramas Importantes

### Declaraciones

- **class_decl**: Sintaxis completa de una clase
- **class_member**: Miembros de datos y métodos
- **decl**: Todas las formas de declaración

### Statements

- **while_stmt_closed/open**: Nueva estructura de control
- **stmt**: Jerarquía completa de statements
- **closed_stmt/open_stmt**: Manejo del dangling-else

### Expresiones

- **expr1**: Asignación y operadores compuestos
- **expr1_5**: Operador ternario
- **expr2-expr7**: Jerarquía de precedencia
- **expr8**: Operadores unarios (incluye pre-inc/dec)
- **expr9**: Operadores postfijo (incluye acceso a miembros)
- **lval**: L-values con acceso a miembros
- **group**: Expresiones primarias (incluye NEW)

### Tipos

- **type_simple**: Tipos básicos (extendido con ID para clases)
- **type_func**: Tipos de función

---

## ✅ Validación

El diseño fue validado contra el archivo de prueba `sieve.bp`, que utiliza todas las extensiones:

- ✅ Definición de clase `Sieve`
- ✅ Múltiples bucles `while`
- ✅ Operador compuesto `+=`
- ✅ Pre y post incremento `++`
- ✅ Operador ternario `?:`
- ✅ Operador `new`
- ✅ Acceso a miembros `.`

---

## 🎓 Resultados de Aprendizaje

Este proyecto demuestra:

1. **Extensibilidad de gramáticas**: Cómo extender un lenguaje sin romper compatibilidad
2. **Precedencia y asociatividad**: Diseño correcto de operadores
3. **Resolución de ambigüedades**: Manejo del dangling-else
4. **Visualización de sintaxis**: Railroad diagrams como herramienta pedagógica
5. **Transformación de gramáticas**: Conversión de recursión izquierda
6. **Diseño de lenguajes**: Principios de POO aplicados a gramáticas

---

## 📦 Entregables

1. ✅ Gramática completa (`grammar_bminor_plus.txt`)
2. ✅ 39 diagramas SVG en `out/svg/`
3. ✅ Visualizador HTML (`out/index.html`)
4. ✅ Índice Markdown (`out/index.md`)
5. ✅ Código fuente del generador (`generate_diagrams.py`)
6. ✅ Librería de diagramas (`railroad.py`)
7. ✅ Documentación completa (este README)

---

## 🔍 Notas Técnicas

### Librería Railroad Diagrams

Se implementó una versión simplificada de `railroad-diagrams` que genera SVG puro, con:

- **Terminal**: Cajas verdes redondeadas
- **NonTerminal**: Cajas azules rectangulares
- **Sequence**: Concatenación de elementos
- **Choice**: Alternativas (ramificaciones)
- **Optional**: Elemento opcional (puede omitirse)
- **ZeroOrMore**: Repetición (cero o más veces)

### Generación de Diagramas

El proceso es completamente reproducible:

1. `railroad.py` define las primitivas de diagramas
2. `generate_diagrams.py` define cada regla como función
3. Cada función construye el diagrama usando las primitivas
4. Los SVG se generan en `out/svg/`
5. El HTML/Markdown embebe los SVG

---

## 👨‍🎓 Autor

Proyecto desarrollado para el curso de **Compiladores / Lenguajes de Programación**

**Taller:** Extensión de Gramática B-Minor  
**Año:** 2025

---

## 📄 Licencia

Este proyecto es material académico para fines educativos.

---

## 🙏 Agradecimientos

- Gramática base B-Minor
- Inspiración en railroad-diagrams de Tab Atkins Jr.
- Comunidad de diseño de lenguajes de programación

---

**¡Explora los diagramas y entiende visualmente la sintaxis de B-Minor+!** 🚂
