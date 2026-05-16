import os
import re
import sys

# ==============================================================================
# 1. THE STANDARD LIBRARY (STATIC MAPS)
# ==============================================================================
STANDARD_MAP = {
    # --- CELESTIAL BODIES ---
    r"\mercury": "â¿", r"\venus": "â", r"\earth": "â", r"\mars": "â",
    r"\jupiter": "â", r"\saturn": "â", r"\uranus": "â¢", r"\neptune": "â",
    r"\pluto": "â", r"\sun": "â", r"\moon": "â¾", 
    r"\ascnode": "â", r"\descnode": "â", r"\comet": "â",

    # --- ZODIAC ---
    r"\aries": "â", r"\taurus": "â", r"\gemini": "â", r"\cancer": "â",
    r"\leo": "â", r"\virgo": "â", r"\libra": "â", r"\scorpio": "â",
    r"\sagittarius": "â", r"\capricorn": "â", r"\aquarius": "â", r"\pisces": "â",

    # --- ALQC SPECIFIC ---
    r"\LoI": "â", r"\loid": "â¾", r"\sloid": "â½", r"\sloig": "â",
    r"\axiomyrid": "á³", r"\axiomyr": "â", r"\maresun": "â",
    r"\loivector": "â¤", r"\loibias": "â", 
    r"\kleinbottle": "ð", r"\triquatraseal": "ð", r"\TManifold": "ð¯"
}

# ==============================================================================
# 2. THE MATHEMATICS ENGINE
# ==============================================================================
MATH_MAP = {
    # --- GREEK ---
    r"\alpha": "Î±", r"\beta": "Î²", r"\gamma": "Î³", r"\delta": "Î´",
    r"\epsilon": "Îµ", r"\zeta": "Î¶", r"\eta": "Î·", r"\theta": "Î¸",
    r"\iota": "Î¹", r"\kappa": "Îº", r"\lambda": "Î»", r"\mu": "Î¼",
    r"\nu": "Î½", r"\xi": "Î¾", r"\pi": "Ï", r"\rho": "Ï",
    r"\sigma": "Ï", r"\tau": "Ï", r"\upsilon": "Ï", r"\phi": "Ï",
    r"\chi": "Ï", r"\psi": "Ï", r"\omega": "Ï",
    r"\Delta": "Î", r"\Gamma": "Î", r"\Lambda": "Î", r"\Phi": "Î¦",
    r"\Psi": "Î¨", r"\Omega": "Î©", r"\Sigma": "Î£", r"\Theta": "Î",
    
    # --- OPERATORS ---
    r"\nabla": "â", r"\partial": "â", r"\sum": "â", r"\prod": "â",
    r"\int": "â«", r"\oint": "â®", r"\infty": "â", r"\sqrt": "â",
    r"\approx": "â", r"\equiv": "â¡", r"\neq": "â ", r"\leq": "â¤",
    r"\geq": "â¥", r"\to": "â", r"\rightarrow": "â", r"\Rightarrow": "â", 
    r"\iff": "â", r"\in": "â", r"\notin": "â", r"\subset": "â",
    r"\forall": "â", r"\exists": "â", r"\neg": "Â¬",
    r"\times": "Ã", r"\cdot": "Â·", r"\circ": "â", r"\otimes": "â", 
    r"\oplus": "â", r"\pm": "Â±", r"\mp": "â", r"\div": "Ã·",
    
    # --- SETS & FONTS ---
    r"\mathbb\{R\}": "â", r"\mathbb\{C\}": "â", r"\mathbb\{Z\}": "â¤",
    r"\mathbb\{N\}": "â", r"\mathbb\{Q\}": "â", r"\mathbb\{I\}": "ð",
    r"\mathbb\{K\}": "ð", r"\mathbb\{P\}": "â", r"\mathbb\{S\}": "ð",
    r"\mathcal\{T\}": "ð¯", r"\mathcal\{H\}": "â", r"\mathcal\{L\}": "â",
    r"\mathcal\{M\}": "â³", r"\mathcal\{R\}": "â", r"\mathcal\{F\}": "â±",
    r"\mathfrak\{P\}": "ð", r"\mathfrak\{C\}": "â­",

    # --- NOISE REMOVAL ---
    r"\underbrace": "", r"\xrightarrow": "â", r"\left": "", r"\right": "",
    r"\text": "", r"\mathrm": "", r"\mathbf": "", r"\mathit": ""
}

SUPERSCRIPTS = {
    '0': 'â°', '1': 'Â¹', '2': 'Â²', '3': 'Â³', '4': 'â´', 
    '5': 'âµ', '6': 'â¶', '7': 'â·', '8': 'â¸', '9': 'â¹',
    '+': 'âº', '-': 'â»', '=': 'â¼', '(': 'â½', ')': 'â¾',
    'n': 'â¿', 'i': 'â±', 'a': 'áµ', 'b': 'áµ', 'c': 'á¶'
}

SUBSCRIPTS = {
    '0': 'â', '1': 'â', '2': 'â', '3': 'â', '4': 'â', 
    '5': 'â', '6': 'â', '7': 'â', '8': 'â', '9': 'â',
    '+': 'â', '-': 'â', '=': 'â', '(': 'â', ')': 'â',
    'a': 'â', 'e': 'â', 'o': 'â', 'x': 'â', 'h': 'â', 'k': 'â', 
    'l': 'â', 'm': 'â', 'n': 'â', 'p': 'â', 's': 'â', 't': 'â'
}

def transmute_math_structure(content):
    # 1. Fractions: rac{a}{b} -> (a/b)
    for _ in range(3): 
        content = re.sub(r"\frac\{([^{}]+)\}\{([^{}]+)\}", r"(/)", content)

    # 2. Square Roots: \sqrt{x} -> â(x)
    content = re.sub(r"\sqrt\{([^{}]+)\}", r"â()", content)

    # 3. Superscripts: ^2 or ^{12}
    def replace_sup(match):
        txt = match.group(1)
        return "".join([SUPERSCRIPTS.get(c, c) for c in txt])
    
    content = re.sub(r"\^\{([a-zA-Z0-9\+\-\=\(\)]+)\}", replace_sup, content)
    content = re.sub(r"\^([a-zA-Z0-9])", replace_sup, content)

    # 4. Subscripts: _2 or _{12}
    def replace_sub(match):
        txt = match.group(1)
        return "".join([SUBSCRIPTS.get(c, c) for c in txt])
        
    content = re.sub(r"_\{([a-zA-Z0-9\+\-\=\(\)]+)\}", replace_sub, content)
    content = re.sub(r"_([a-zA-Z0-9])", replace_sub, content)

    return content

# ==============================================================================
# 3. DYNAMIC PREAMBLE PARSER
# ==============================================================================
def parse_preamble(file_path):
    print(f"[SYSTEM] Parsing {file_path} for Glyph Definitions...")
    
    if not os.path.exists(file_path):
        print(f"[ERROR] {file_path} not found. Using Standard Maps only.")
        return {}

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    glyph_map = {}

    # Simple Commands (
ewcommand{\FETU}{...\symbol{"23E3"}})
    hex_pattern = re.compile(r'\(?:newcommand|def)\s*\{\(\w+)\}.*?\(?:symbol|char)\s*\{?"([0-9A-Fa-f]+)\}?')
    for match in hex_pattern.finditer(content):
        glyph_map["\" + match.group(1)] = chr(int(match.group(2), 16))

    # Compound Commands (
ewcommand{etuahl}{\FETU...\symbol{"0787}})
    compound_pattern = re.compile(r'\(?:newcommand|def)\s*\{\(\w+)\}\s*\{\(\w+).*?\(?:symbol|char)\s*\{?"([0-9A-Fa-f]+)\}?')
    for match in compound_pattern.finditer(content):
        child = "\" + match.group(1)
        parent = "\" + match.group(2)
        hex_code = match.group(3)
        if parent in glyph_map:
            glyph_map[child] = glyph_map[parent] + chr(int(hex_code, 16))

    print(f"[SUCCESS] Extracted {len(glyph_map)} Dynamic Definitions.")
    return glyph_map

# ==============================================================================
# 4. CLEANING ENGINE
# ==============================================================================
def clean_file(filepath, dynamic_map):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # --- PHASE 1: MATH TRANSLATION (Symbols & Structure) ---
    # Convert \Psi -> Î¨ FIRST so structural regexes see cleaner text
    full_map = {**STANDARD_MAP, **dynamic_map, **MATH_MAP}
    sorted_cmds = sorted(full_map.keys(), key=len, reverse=True)

    for cmd in sorted_cmds:
        glyph = full_map[cmd]
        pattern = re.escape(cmd) + r"(?![a-zA-Z])" 
        content = re.sub(pattern, glyph, content)

    content = transmute_math_structure(content)

    # --- PHASE 2: TABLE & STRUCTURE SURGERY (Critical Step) ---
    
    # 1. Handle Multicolumn: \multicolumn{6}{p{14cm}}{TEXT} -> > TEXT
    # We use a robust regex that handles the complex arguments including nested braces in p{...}
    # Matches: \multicolumn {NUM} {TYPE} {TEXT}
    # We strip the first two args and keep the third.
    content = re.sub(r"\multicolumn\s*\{[^}]+\}\s*\{(?:[^{}]|\{[^}]*\})*\}\s*\{((?:[^{}]|\{[^}]*\})*)\}", r"> ", content)

    # 2. Handle Addlinespace: ddlinespace[1ex] -> Newline
    content = re.sub(r"\addlinespace(?:\[.*?\])?", "
", content)

    # 3. Table Borders -> Markdown Separators
    content = re.sub(r"\(toprule|midrule|bottomrule|hline)", "---", content)
    
    # 4. Table Headers & Rows
    content = re.sub(r"\endhead", "", content)
    content = re.sub(r"\endfirsthead", "", content)
    content = re.sub(r"\endfoot", "", content)
    content = re.sub(r"\endlastfoot", "", content)

    # --- PHASE 3: ENVIRONMENT DISSOLUTION ---
    
    # Remove egin{...} and \end{...} tags but keep content
    content = re.sub(r"\begin\{[^}]*\}", "", content)
    content = re.sub(r"\end\{[^}]*\}", "", content)

    # Labels & References
    content = re.sub(r"\label\{[a-zA-Z]*:?([^}]*)\}", r" [Ref: ]", content)
    content = re.sub(r"\ref\{([^}]*)\}", r"", content)

    # Text Formatting
    content = re.sub(r"\textbf\{((?:[^{}]|{[^{}]*})*)\}", r"****", content)
    content = re.sub(r"\textit\{((?:[^{}]|{[^{}]*})*)\}", r"**", content)
    content = re.sub(r"\emph\{((?:[^{}]|{[^{}]*})*)\}", r"**", content)
    
    # Headers
    content = re.sub(r"\section\*?\{([^}]*)\}", r"
# 
", content)
    content = re.sub(r"\subsection\*?\{([^}]*)\}", r"
## 
", content)
    content = re.sub(r"\subsubsection\*?\{([^}]*)\}", r"
### 
", content)
    
    # Lists
    content = re.sub(r"\item\[(.*?)\]", r"
* **** ", content)
    content = re.sub(r"\item", r"
* ", content)
    
    # Table Cells & Rows
    content = content.replace("&", " | ")
    content = content.replace("\\", "
")
    content = re.sub(r"\tabularnewline", "
", content)

    # --- PHASE 4: FINAL POLISH ---
    
    # Strip Math Delimiters (content is already Unicode)
    content = content.replace("$", " ") 
    content = content.replace("\[", "
").replace("\]", "
")

    # Remove Comments
    content = re.sub(r"(?<!\)%.*", "", content) 
    content = re.sub(r"\slash", "/", content)
    content = re.sub(r"\,", " ", content)
    content = re.sub(r"\ ", " ", content)
    
    # NOW we can safely strip stray braces
    content = re.sub(r"\{|\}", "", content) 
    
    # Collapse Whitespace
    content = re.sub(r"
{3,}", "

", content) 

    return content

# ==============================================================================
# 5. MAIN EXECUTION
# ==============================================================================
def main():
    print("IGNITION: ALQC FINAL TRANSMUTER (Math-Aware + Tables)")
    
    preamble_path = "PREABMLE.txt"
    dynamic_map = parse_preamble(preamble_path)
    output_dir = "CLEAN_CORPUS_FINAL"
    os.makedirs(output_dir, exist_ok=True)
    
    count = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith((".tex", ".txt", ".md")):
                if output_dir in root: continue
                if file == "PREABMLE.txt": continue
                if "CLEAN" in file: continue 
                
                input_path = os.path.join(root, file)
                output_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}_CLEAN.md")
                
                print(f"Processing: {file}...")
                try:
                    cleaned_text = clean_file(input_path, dynamic_map)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_text)
                    count += 1
                except Exception as e:
                    print(f"Error: {e}")

    print(f"COMPLETE: {count} files transmuted to {output_dir}/")

if __name__ == "__main__":
    main()