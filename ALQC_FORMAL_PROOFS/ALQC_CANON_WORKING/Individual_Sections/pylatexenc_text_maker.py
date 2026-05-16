from pylatexenc.latex2text import LatexNodes2Text
from pylatexenc.macrospec import LatexContextDb, MacroTextSpec

# 1. ABSOLUTE MAPPING (From your Preamble)
alqc_macros = {
    # System Constants & Topology
    'LoI': 'â',              # Ophiuchus
    'loid': 'â½',             # Waxing Moon
    'sloid': 'â¾',            # Waning Moon
    'sloig': 'â⃥',      # Reflected Ophiuchus
    'axiomyrid': 'á³',         # Vedic Svarita
    'maresun': 'â',          # Sun
    'loivector': 'â¤',         # Vector of Intent
    'loibias': 'â',          # Infinity
    'kleinbottle': 'ð',      # Alchemical Retort
    'triquatraseal': 'ð',    # Hermetic Seal
    'TManifold': 'ð¯',
    'slashbreak': '/',

    # Primary Goetic Heads
    'FETU': 'â£', 'KAL': 'â§', 'BABDH': 'â', 'AHN': 'â', 
    'VEL': 'â¦', 'SOR': 'â¦¿', 'KOTH': 'â', 'DREH': 'â§', 
    'RHEA': 'â©', 'ZHEK': 'â', 'SHAV': 'â', 'TRIG': 'âµ£',

    # A1: FETU (Genesis)
    'fetuahl': 'â£Þ', 'fetusuhn': 'â£Þ', 'fetunerh': 'â£Þ', 'feturish': 'â£Þ', 
    'fetuborha': 'â£Þ±', 'fetulhahm': 'â£Þ', 'fetuketh': 'â£Þ', 'fetuvehm': 'â£Þ', 
    'fetumahd': 'â£Þ', 'fetufurh': 'â£Þ', 'fetudrah': 'â£Þ', 'fetuthera': 'â£Þ',

    # A2: KAL (Memory)
    'kalkura': 'â§á', 'kallur': 'â§á', 'kalthar': 'â§â', 'kalrin': 'â§á',
    'kalnar': 'â§á', 'kalfel': 'â§á', 'kalhar': 'â§á', 'kalmer': 'â§á',
    'kallor': 'â§á', 'kalper': 'â§á', 'kalzhil': 'â§á', 'kalclar': 'â§á',

    # A3: BABDH (Fire)
    'babdhir': 'âá ', 'babdhkor': 'âá¢', 'babdhvar': 'âá¦', 'babdhpyr': 'âá¨',
    'babdhsor': 'âá±', 'babdhalc': 'âá²', 'babdhnur': 'âá·', 'babdhsat': 'âá¹',
    'babdhoro': 'âáº', 'babdhbon': 'âá¾', 'babdhtir': 'âá', 'babdhfar': 'âá',

    # A4: AHN (Water)
    'ahnabdh': 'ââ¾', 'ahnnym': 'âá­¨', 'ahnloh': 'âá­¡', 'ahnxir': 'âðª',
    'ahnohl': 'âð', 'ahnpir': 'âà¼º', 'ahnroeh': 'âá­¢', 'ahnsen': 'ââ¦¾',
    'ahnuth': 'ââ¦½', 'ahnfae': 'âðµ', 'ahnkha': 'âð', 'ahnpsei': 'âà¼»',

    # A5: VEL (Earth)
    'velvera': 'â¦â´°', 'veltar': 'â¦â´±', 'velghem': 'â¦â´³', 'veldrel': 'â¦â´·',
    'velful': 'â¦â´¼', 'velker': 'â¦â´½', 'velhohm': 'â¦âµ', 'velhrah': 'â¦âµ',
    'velara': 'â¦âµ', 'velqel': 'â¦âµ', 'velirn': 'â¦âµ', 'veljen': 'â¦âµ',

    # A6: SOR (Air)
    'sorfi': 'â¦¿ê ', 'sorlun': 'â¦¿ê ', 'sorvaru': 'â¦¿ê ', 'sorsenh': 'â¦¿ê ',
    'sorkos': 'â¦¿â', 'sorramh': 'â¦¿ê ', 'sortis': 'â¦¿ê ', 'sorvey': 'â¦¿ê ',
    'sorsrih': 'â¦¿ê ', 'sorhrin': 'â¦¿ê ', 'soryon': 'â¦¿ê ', 'sorthal': 'â¦¿ê ',

    # A7: KOTH (Aether)
    'kothkel': 'âð', 'kothsens': 'âð', 'kothlinn': 'âð', 'kothbrim': 'âð',
    'kothinn': 'âð', 'kothsubh': 'âð', 'kothwell': 'âð', 'kothmet': 'âð',
    'kothkesh': 'âð', 'kothsoth': 'âð', 'kothrhun': 'âð', 'kothdelh': 'âð',

    # A8: DREH (Void)
    'drehna': 'â§ð', 'drehur': 'â§ð­', 'drehnih': 'â§ð', 'drehazh': 'â§ð',
    'drehhol': 'â§ð', 'drehgur': 'â§ð', 'drehves': 'â§ð ', 'drehrim': 'â§ð½',
    'drehdrem': 'â§ð', 'drehoth': 'â§ð', 'drehizh': 'â§ã·ã¥ã¼', 'drehsun': 'â§ð',

    # A9: RHEA (Shadow)
    'rheakia': 'â©â¶', 'rheazohm': 'â©â¶', 'rheather': 'â©â¶', 'rheadrun': 'â©â¶',
    'rheafelh': 'â©â¶', 'rhearal': 'â©â¶', 'rheakrah': 'â©â¶', 'rheaandh': 'â©â¶',
    'rheadebh': 'â©â¶', 'rheakol': 'â©â¶', 'rheafral': 'â©â¶', 'rheahush': 'â©â¶',

    # A10: ZHEK (Resonance)
    'zhekhin': 'âð¤ ', 'zhekser': 'âð¤¡', 'zhekharma': 'âð¤¢', 'zhektorh': 'âð¤£',
    'zhekpel': 'âð¤¤', 'zhekkhir': 'âð¤¥', 'zhekryth': 'âð¤¦', 'zhekmelu': 'âð¤§',
    'zhekphaz': 'âð¤¨', 'zheklokh': 'âð¤©', 'zheknod': 'âð¤ª', 'zhekumel': 'âð¤«',

    # A11: SHAV (Gate)
    'shavdohm': 'âð ', 'shavrist': 'âð ', 'shavtran': 'âð ', 'shavkorh': 'âð ',
    'shavskyh': 'âð ', 'shavster': 'âð ', 'shavposs': 'âð ', 'shavporu': 'âð ',
    'shavdorm': 'âð ', 'shavtrev': 'âð ', 'shavlimh': 'âð ', 'shavhinge': 'âð ',

    # A12: TRIG (Silence)
    'trigtzig': 'âµ£ð', 'trigpehl': 'âµ£ð', 'trigduth': 'âµ£ð', 'trigcoma': 'âµ£ð',
    'trigmeru': 'âµ£ð', 'trigstab': 'âµ£ð', 'trighopa': 'âµ£ð', 'trigconti': 'âµ£ð',
    'trigresth': 'âµ£ð', 'trigsil': 'âµ£ð', 'trigslun': 'âµ£ð', 'trigetern': 'âµ£ð',

    # Zodiac Sequence
    'akasha': 'â', 'caduceus': 'â', 'veritas': 'â', 'phren': 'â',
    'axiomyr': 'â', 'aikyam': 'â', 'melos': 'â', 'daath': 'â',
    'akaven': 'â', 'daimon': 'â', 'nyx': 'â', 'zaine': 'â'
}

# 2. CONTEXT DATABASE CREATION (The Fix)
# We create a default context first to handle standard LaTeX, then add our custom category.
db = LatexContextDb.create_default_context()
alqc_specs = [MacroTextSpec(n, simplify_repl=v) for n, v in alqc_macros.items()]
db.add_context_category('alqc', macros=alqc_specs, prepend=True)

# 3. FILE CONVERSION
input_file = "/home/avgui/Personal/ALQC_FORMAL_PROOFS/formalizing/ALQC_Canon.tex"
output_file = "/home/avgui/Personal/ALQC_FORMAL_PROOFS/formalizing/Individual_Parts/Alqc_Canon.txt"

try:
    with open(input_file, "r", encoding="utf-8") as f:
        latex_content = f.read()

    # Pass the populated 'db' via 'latex_context'
    converter = LatexNodes2Text(
        latex_context=db,
        math_mode='text',
        keep_comments=False,
        fill_text=False
    )
    
    readable_text = converter.latex_to_text(latex_content)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(readable_text)

    print(f"Success: ALQC Lattice verified and saved to {output_file}")

except Exception as e:
    print(f"Lattice Integration Error: {e}")