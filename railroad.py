"""
Simple Railroad Diagram Generator
Genera diagramas de sintaxis en formato SVG para gramáticas BNF
"""

class Component:
    def __init__(self):
        self.width = 0
        self.height = 0
        
    def to_svg(self, x, y):
        return ""

class Terminal(Component):
    def __init__(self, text):
        super().__init__()
        self.text = text
        padding = 10
        self.width = len(text) * 8 + padding * 2
        self.height = 30
        
    def to_svg(self, x, y):
        rx = 10
        svg = f'<rect x="{x}" y="{y}" width="{self.width}" height="{self.height}" '
        svg += f'rx="{rx}" ry="{rx}" fill="#90EE90" stroke="#000" stroke-width="2"/>\n'
        svg += f'<text x="{x + self.width/2}" y="{y + self.height/2 + 5}" '
        svg += f'text-anchor="middle" font-family="monospace" font-size="14" font-weight="bold">{self.text}</text>\n'
        return svg

class NonTerminal(Component):
    def __init__(self, text):
        super().__init__()
        self.text = text
        padding = 10
        self.width = len(text) * 8 + padding * 2
        self.height = 30
        
    def to_svg(self, x, y):
        svg = f'<rect x="{x}" y="{y}" width="{self.width}" height="{self.height}" '
        svg += f'fill="#87CEEB" stroke="#000" stroke-width="2"/>\n'
        svg += f'<text x="{x + self.width/2}" y="{y + self.height/2 + 5}" '
        svg += f'text-anchor="middle" font-family="monospace" font-size="14">{self.text}</text>\n'
        return svg

class Sequence(Component):
    def __init__(self, *items):
        super().__init__()
        self.items = items
        self.width = sum(item.width for item in items) + (len(items) - 1) * 20
        self.height = max(item.height for item in items) if items else 30
        
    def to_svg(self, x, y):
        svg = ""
        current_x = x
        for i, item in enumerate(self.items):
            y_offset = y + (self.height - item.height) / 2
            svg += item.to_svg(current_x, y_offset)
            current_x += item.width
            
            # Línea de conexión
            if i < len(self.items) - 1:
                y_mid = y + self.height / 2
                svg += f'<line x1="{current_x}" y1="{y_mid}" x2="{current_x + 20}" y2="{y_mid}" '
                svg += f'stroke="#000" stroke-width="2"/>\n'
                current_x += 20
        
        return svg

class Choice(Component):
    def __init__(self, *items):
        super().__init__()
        self.items = items
        self.width = max(item.width for item in items) + 100
        self.height = sum(item.height for item in items) + (len(items) - 1) * 20 + 20
        
    def to_svg(self, x, y):
        svg = ""
        current_y = y + 10
        
        for i, item in enumerate(self.items):
            # Calcular posición centrada
            item_x = x + (self.width - item.width) / 2
            
            # Dibujar el item
            svg += item.to_svg(item_x, current_y)
            
            # Líneas de entrada
            if i == 0:
                # Primera opción - línea directa
                svg += f'<line x1="{x}" y1="{y + self.height/2}" x2="{item_x}" y2="{current_y + item.height/2}" '
                svg += f'stroke="#000" stroke-width="2" fill="none"/>\n'
            else:
                # Otras opciones - curva desde arriba
                svg += f'<path d="M {x} {y + self.height/2} Q {x + 20} {current_y + item.height/2} {item_x} {current_y + item.height/2}" '
                svg += f'stroke="#000" stroke-width="2" fill="none"/>\n'
            
            # Líneas de salida
            svg += f'<line x1="{item_x + item.width}" y1="{current_y + item.height/2}" '
            svg += f'x2="{x + self.width}" y2="{y + self.height/2}" '
            svg += f'stroke="#000" stroke-width="2" fill="none"/>\n'
            
            current_y += item.height + 20
        
        return svg

class Optional(Component):
    def __init__(self, item):
        super().__init__()
        self.item = item
        self.width = item.width + 100
        self.height = item.height + 40
        
    def to_svg(self, x, y):
        svg = ""
        item_x = x + 50
        item_y = y + 20
        
        # Dibujar item
        svg += self.item.to_svg(item_x, item_y)
        
        # Línea que pasa por el item
        y_mid = item_y + self.item.height / 2
        svg += f'<line x1="{x}" y1="{y_mid}" x2="{item_x}" y2="{y_mid}" stroke="#000" stroke-width="2"/>\n'
        svg += f'<line x1="{item_x + self.item.width}" y1="{y_mid}" x2="{x + self.width}" y2="{y_mid}" stroke="#000" stroke-width="2"/>\n'
        
        # Línea que evita el item (arriba)
        svg += f'<path d="M {x} {y_mid} Q {x + 25} {y} {x + 50} {y} L {item_x + self.item.width - 50} {y} Q {item_x + self.item.width - 25} {y} {item_x + self.item.width} {y_mid}" '
        svg += f'stroke="#000" stroke-width="2" fill="none"/>\n'
        
        return svg

class ZeroOrMore(Component):
    def __init__(self, item):
        super().__init__()
        self.item = item
        self.width = item.width + 100
        self.height = item.height + 60
        
    def to_svg(self, x, y):
        svg = ""
        item_x = x + 50
        item_y = y + 30
        
        # Dibujar item
        svg += self.item.to_svg(item_x, item_y)
        
        # Línea principal
        y_mid = item_y + self.item.height / 2
        svg += f'<line x1="{x}" y1="{y_mid}" x2="{item_x}" y2="{y_mid}" stroke="#000" stroke-width="2"/>\n'
        svg += f'<line x1="{item_x + self.item.width}" y1="{y_mid}" x2="{x + self.width}" y2="{y_mid}" stroke="#000" stroke-width="2"/>\n'
        
        # Línea de bypass (arriba)
        svg += f'<path d="M {x} {y_mid} Q {x + 25} {y + 10} {x + 50} {y + 10} L {item_x + self.item.width - 50} {y + 10} Q {item_x + self.item.width - 25} {y + 10} {item_x + self.item.width} {y_mid}" '
        svg += f'stroke="#000" stroke-width="2" fill="none"/>\n'
        
        # Línea de repetición (abajo)
        svg += f'<path d="M {item_x + self.item.width} {y_mid} Q {item_x + self.item.width + 25} {y + self.height - 10} {item_x + self.item.width - 50} {y + self.height - 10} L {x + 50} {y + self.height - 10} Q {x + 25} {y + self.height - 10} {x + 50} {y_mid}" '
        svg += f'stroke="#000" stroke-width="2" fill="none"/>\n'
        
        return svg

class Diagram:
    def __init__(self, *items):
        if len(items) == 1:
            self.root = items[0]
        else:
            self.root = Sequence(*items)
        
        self.width = self.root.width + 60
        self.height = self.root.height + 40
        
    def to_svg(self):
        svg = f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">\n'
        svg += '<style>\n'
        svg += 'text { font-family: monospace; }\n'
        svg += '</style>\n'
        
        # Línea de entrada
        y_mid = 20 + self.root.height / 2
        svg += f'<circle cx="10" cy="{y_mid}" r="5" fill="#000"/>\n'
        svg += f'<line x1="10" y1="{y_mid}" x2="30" y2="{y_mid}" stroke="#000" stroke-width="2"/>\n'
        
        # Diagrama principal
        svg += self.root.to_svg(30, 20)
        
        # Línea de salida
        svg += f'<line x1="{30 + self.root.width}" y1="{y_mid}" x2="{self.width - 10}" y2="{y_mid}" stroke="#000" stroke-width="2"/>\n'
        svg += f'<circle cx="{self.width - 10}" cy="{y_mid}" r="5" fill="#000"/>\n'
        
        svg += '</svg>'
        return svg
    
    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(self.to_svg())

# Funciones de ayuda
def T(text):
    """Terminal"""
    return Terminal(text)

def N(text):
    """NonTerminal"""
    return NonTerminal(text)

def Seq(*items):
    """Sequence"""
    return Sequence(*items)

def Ch(*items):
    """Choice"""
    return Choice(*items)

def Opt(item):
    """Optional"""
    return Optional(item)

def ZM(item):
    """Zero or More"""
    return ZeroOrMore(item)
