# ALQC Canon Diagrams - Integration Instructions

## File Structure
```
ALQC_FORMAL_PROOFS/
  ALQC_CANON_WORKING/
    diagrams/
      tripartite_core_diagram.tex      # Diagram 1
      frequency_chain_diagram.tex      # Diagram 2
      qstate_flow_diagram.tex          # Diagram 3
      dcomp_evolution_diagram.tex      # Diagram 4
      shared_styles.tex                # Common styles
      plan.md                          # Original plan
      plan_updated.md                  # Updated plan with user feedback
      README.md                        # This file
```

## Quick Integration

### Option 1: Individual Diagram Insertion

Each diagram can be independently inserted into your main document:

```latex
% In your main .tex file (e.g., ALQC_Canon_Formalized.tex)

\begin{figure}[htbp]
  \centering
  \input{diagrams/tripartite_core_diagram.tex}
  \caption{Tripartite Core Structure: Pilot≡Ship≡Hull in sacred geometry with AXIOMYR[LOCUS(0,0,0)] at the center}
  \label{fig:tripartite_core}
\end{figure}

\begin{figure}[htbp]
  \centering
  \input{diagrams/frequency_chain_diagram.tex}
  \caption{Harmonic Frequency Chain: Full celestial chart showing 13 frequencies, Q-State assignments, Φ return loop (963→Q₃→Q₁), Lissajous curves, Chladni patterns, and Faraday wave elements}
  \label{fig:frequency_chain}
\end{figure}

\begin{figure}[htbp]
  \centering
  \input{diagrams/qstate_flow_diagram.tex}
  \caption{Q-State Flow Relationships: State space diagram showing Q₀→Q₁→Q₂→Q₃, Φ return loop, Mirror Axiom, C_local flows, Lissajous phase space, and Ennead Equation}
  \label{fig:qstate_flow}
\end{figure}

\begin{figure}[htbp]
  \centering
  \input{diagrams/dcomp_evolution_diagram.tex}
  \caption{D-Comp Evolution Through Aevum States: Sacred staircase showing 8-phase reduction from maximum D-COMP to perfect zero at Phase Lock}
  \label{fig:dcomp_evolution}
\end{figure}
```

### Option 2: Inline Insertion (Without Caption)

For inline insertion within a section:

```latex
% Without figure environment
\centering
\input{diagrams/tripartite_core_diagram.tex}
```

## Prerequisites

All diagrams require the following TikZ libraries:

```latex
\usepackage{tikz}
\usetikzlibrary{arrows.meta, shapes.geometric, positioning, calc}
\usetikzlibrary{decorations.pathmorphing, fadings, patterns}
\usetikzlibrary{decorations.text, decorations.markings}
\usetikzlibrary{shadows.blur, shadows, backgrounds}
\usetikzlibrary{decorations.pathreplacing}
```

These should already be present in your main document from [`preamble.tex`](../ALQC-CANON_WORKING/preamble.tex).

## Color Definitions

Each diagram includes local color definitions for standalone compilation. These match the ALQC standard colors:

- `voidblack` #050505
- `electricblue` #00F0FF
- `sovereignfire` #FF4500
- `shadowsilver` #C0C0C0
- `deepvoid` #000010
- `glyphwhite` #E0E0E0
- `phigold` #D4AF37
- `goldflow` #FFA500

## Glyph Usage

The diagrams use ALQC glyphs. Your main document should have proper unicode glyph mapping defined in [`preamble.tex`](../ALQC-CANON_WORKING/preamble.tex):

- ⏣ (FETU)
- ⬡ (KAL)
- ✡ (BABDH)
- ⚝ (KOTH)
- ⋆ (VEL)
- ☿ (SOR)
- 🜂 (KOTH - alternate)
- ⧗ (DREH)
- ⊛ (RHEA)
- ❄ (ZHEK)
- ⚛ (SHAV)
- ⌬ (TRIG)
- ⧉, ⌖, ⟁ (Q-State glyphs)
- ♾ (TSP/LOI infinity symbol)

## Compilation

### Using LuaLaTeX (Recommended)

```bash
cd ALQC_FORMAL_PROOFS/ALQC_CANON_WORKING
lualatex -output-directory=ALQC_CANON_WORKING/ALQC_Canon_Formalized.tex
```

### Standalone Diagram Testing

To test a single diagram independently:

```bash
cd ALQC_FORMAL_PROOFS/ALQC_CANON_WORKING/diagrams

# Create a test file for a diagram
cat > test_diagram1.tex << 'EOF'
\documentclass[tikz,border=1cm]{standalone}
\usepackage{fontspec}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, shapes.geometric, positioning, calc}
\usetikzlibrary{decorations.pathmorphing, fadings, patterns}
\usetikzlibrary{decorations.text, decorations.markings}
\usetikzlibrary{shadows.blur, shadows, backgrounds}
\usetikzlibrary{decorations.pathreplacing}

\input{tripartite_core_diagram.tex}
\end{document}
EOF

lualatex test_diagram1.tex
```

## Design Philosophy Integration

The diagrams incorporate:

1. **Lissajous Figures** - Graceful, looping oscillations showing Q-State transitions
2. **Chladni Patterns** - 2D standing wave nodal lines at harmonic positions
3. **Faraday Waves** - Nonlinear standing wave surfaces
4. **Sacred Geometry** - Triquatra, vesica piscis, flower of life elements
5. **Poetic Elements** - Verses from THE CANON integrated with mathematical notation
6. **Metaphysical/Esoteric** - Spiritual essence not separated from technical precision

## Troubleshooting

### Missing Glyphs
If glyphs don't display, ensure your [`preamble.tex`](../ALQC-CANON_WORKING/preamble.tex) includes:
```latex
\usepackage{fontspec}
\newfontfamily\symbolafont{Symbola}[Scale=MatchUppercase]
\newunicodechar{⏣}{{\symbolafont ⏣}}
% ... (other glyph mappings)
```

### Color Issues
If colors don't render, ensure XeLaTeX or LuaLaTeX is used (not PDFLaTeX).

### Compilation Speed
Complex diagrams with many decorations may compile slowly. This is normal for:
- Lissajous curves with many samples
- Chladni patterns with many node points
- Faraday wave decorations

## Customization

### Adjusting Size

Add `scale=` to the tikzpicture environment:

```latex
\begin{tikzpicture}[scale=1.5] {...}\end{tikzpicture}
```

### Modifying Colors

Each diagram uses local definitions. To change colors globally, modify the definitions at the top of each diagram file.

### Adding/Removing Elements

Each diagram is structured in numbered sections with comments:

```latex
% ======================================================================
% 1. BACKGROUND: Void with Stars
% ======================================================================
```

Comment out sections or add new ones as needed.

## Shared Styles

The [`shared_styles.tex`](shared_styles.tex) file contains:
- Color definitions
- Common TikZ styles for nodes and arrows
- Helper functions for Lissajous curves
- Chladni pattern generators
- Faraday wave elements
- Sacred geometry functions

To use in custom diagrams:

```latex
\input{diagrams/shared_styles.tex}
```

## Reference to Main Document

The diagrams reference and align with:
- [`ALQC_Canon_Formalized.tex`](../ALQC-CANON_WORKING/ALQC_Canon_Formalized.tex)
- The ALQC Canon specification
- Tripartite Core Axioms
- Harmonic Frequency Chain specification
- Q-State Flow relationships
- D-Comp Evolution formulas

## Aevum Integration

The D-Comp diagram specifically illustrates the journey through Aevum states:

1. Initiation (Phase 1)
2. Foundation (Phase 2)
3. Shadow Integration (Phase 3)
4. Dimensional Compression (Phase 4)
5. Geometric Lift (Phase 5)
6. Debt Saturation (Phase 6)
7. **Phase Lock** (Phase 7 - crucial transition)
8. Total Symmetry - D-COMP = 0 (Phase 0)

## Support

For issues or questions:
- Check that all TikZ libraries are loaded
- Verify glyph mappings in preamble
- Ensure LuaLaTeX/XeLaTeX is being used
- Review individual diagram comments for context