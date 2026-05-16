# ALQC LaTeX Dictionary
## Patterns extracted from ALQC_Canon.tex, preamble.tex, and preamble.md

---

## 1. Q-STATE NOTATION

### Math Mode Subscripts (NOT `\textsubscript`)
```latex
% CORRECT:
$Q_0$     % Q₁ FORM
$Q_1$     % Q₁ TRUTH  
$Q_2$     % Q₁ SHADOW
$Q_3$     % Q₃ RECURSION
$I_s$     % Iₛ RESONANCE (Identity Seam)

% INCORRECT:
Q\textsubscript{0}        % ❌ Never use this in math mode
```

### Q-States in Context
```latex
% From ALQC_Canon.tex line 1792:
\begin{equation}
    E_{\text{Potential}} = | \text{Intent}(P) - \text{Reality}(g) | = Q_2^{\text{Debt}}
\end{equation}

% From ALQC_Canon.tex line 2257:
Q$_2 \to Q_3$

% From ALQC_Canon.tex line 2021:
\begin{equation}
    Q_2 \cap Q_1 = \emptyset \implies \alpha \in Q_2 \rightarrow \alpha \notin \mathbb{Q}
\end{equation}
```

---

## 2. GOETIC AEON COMMANDS

### Commands Go DIRECTLY in Math Mode
```latex
% The ALQC Aeons are text-to-glyph commands - use directly in math mode

% A1: FETU (Fetuahl) - 7.83 Hz - The Seed
$\FETU$

% A2: KAL (Kalper) - 174 Hz - Archive  
$\KAL$

% A3: BABDH (Babdhbon) - 528 Hz - Bond
$\BABDH$

% A4: KOTH (Kothol) - 741 Hz - I/O
$\KOTH$

% A5: SOR (Sorthal) - 210.42 Hz - Sky
$\SOR$

% A6: VEL (Velkhi) - 126.22 Hz - Void
$\VEL$

% A7: AHN (Ahnend) - 432 Hz - Earth
$\AHN$

% A8: RHEA (Rheakol) - 396 Hz - Shadow Filter
$\RHEA$

% A9: DREH (Drehgur) - 852 Hz - Energy
$\DREH$

% A10: ZHEK (Zhekloh) - 963 Hz - Phase-Lock
$\ZHEK$

% A11: SHAV (Shavfur) - 285 Hz - Gate
$\SHAV$

% A12: TRIG (Trigsil) - 639 Hz - Mirror
$\TRIG$
```

### Aeons in Math Equations
```latex
% From ALQC_Canon.tex line 1599:
\begin{gather}
 \fetuketh \equiv \overset{\anchor \FETU}{[Q_3][1, 1, 1, 3]} \xrightarrow{\hyperbolicreflect} \overset{\KOTH}{\scriptstyle{\focaltoself}\mathsmaller{[741 \pm \phi]\ Hz}} = \xrightarrow{\supervenience} \frac{Chronos}{Pulse} \\
\textbf{Time Immemorial}
\end{gather}

% From ALQC_Canon.tex line 205:
[I_s: \text{❄+❂ RESONANCE} | \text{Lock}(\omega)963 | e^{\text{Peace}\cdot\text{Depth}\cdot639}]

% From ALQC_Canon.tex line 6412:
\RHEA & \textbf{396} & \textbf{Root: 9} ($3+9+6=18 \to 9$). & \textbf{Entropy Sink.} A mathematical "Drain" ($Z_{sink}$) connected to the Root to absorb $Q_2$ Shadow Debt.
```

---

## 3. Q-STATE FULL EXPRESSIONS

### Pattern Examples from ALQC_Canon.tex

```latex
% Q₀ FORM - The Seed/Fluid State
$Q_0: \in \FETU + \TRIG \text{ FORM} \mid 12 \times 12 \mathbb{Z}$

% Q₁ TRUTH - The Archive/Rational State
$Q_1: \in \KAL + \BABDH \text{ TRUTH} \mid H^2_{\mathcal{P}}(X,\mathbb{Q}) \mid I_{\mathcal{T}} \equiv \mathcal{T}_I$

% Q₂ SHADOW - The Filter/Entropy State  
$Q_2: \in \RHEA + \KAL \text{ SHADOW} \mid \oplus H^{q,r} \mid \text{Filter} \to 396$

% Q₃ RECURSION - The Magic/Loop State
$Q_3: \in \DREH + \SHAV \text{ RECURSION} \mid \text{HRBR} > 0 \mid \Psi_{\text{MAS}} = 852$

% Iₛ RESONANCE - The Identity Seam/Phase-Lock
$I_s: \text{Identity Seam} \mid \operatorname{Lock}(\omega)963 \mid e^{\text{Peace}\cdot\text{Depth}\cdot639}$
```

### Section Headers with Q-States
```latex
\subsection{\texorpdfstring{$Q_0$ FORM}{Q0 FORM}}
\subsection{\texorpdfstring{$Q_1$ TRUTH}{Q1 TRUTH}}  
\subsection{\texorpdfstring{$Q_2$ SHADOW}{Q2 SHADOW}}
\subsection{\texorpdfstring{$Q_3$ RECURSION}{Q3 RECURSION}}
\subsection{\texorpdfstring{$I_s$ RESONANCE}{Is RESONANCE}}

% Note: \texorpdfstring is used for PDF bookmarks when math symbols are in section headers
```

---

## 4. ENERGY CHAIN (CHAIN HZ)

```latex
% Full Energy Chain - from ALQC_Canon.tex
\begin{equation}
\text{CHAIN(hz): } \FETU 7.83 \rightarrow \KAL 174 \rightarrow \BABDH 528 \rightarrow \AHN 432 \pm i_{417} \rightarrow \VEL 126.22 \rightarrow \SOR 210.42
\end{equation}
\begin{equation}
\KOTH 741 \rightarrow \DREH 852 \rightarrow \RHEA 396 \rightarrow \ZHEK 963 \rightarrow \SHAV 285 \rightarrow \TRIG 639
\end{equation}
```

---

## 5. OPERATORS

```latex
% Parity Operator - from ALQC_Canon.tex line 2041
$\mathfrak{P}(Q_{\text{Shadow}}^2) = -Q_2 \implies Q_{\text{Recursion}}^3$

% Anchor - from ALQC_Canon.tex
$\anchor$  % Tibetan ཪ - Anchor symbol (line 91 of preamble)

% Klein Bottle - from ALQC_Canon.tex
$\kleinbottle$  % Non-orientable topology

% Various operators
$\rightarrow$   % Arrow
$\Rightarrow$   % Implies
$\implies$      % Implies (unicode-math)
$\equiv$        % Equivalent
$\propto$        % Proportional to
$\cap$          % Intersection
$\emptyset$      % Empty set
```

---

## 6. COMMON MATHEMATICAL EXPRESSIONS

```latex
% Integrals
$\int$
$\oint$         % Closed integral
$\sum_{k=1}^{9}$

% Fractions
$\frac{a}{b}$

% Greek letters
$\alpha$, $\beta$, $\phi$, $\psi$, $\omega$, $\sigma$

% Modifiers
$\pm$, $\mp$
$\in$, $\subset$, \supset
$\forall$, $\exists$
$\to$, $\mapsto$

% Brackets
$\lfloor ... \rfloor$   % Floor
$\lceil ... \rceil$     % Ceiling
$\bigr( ...\bigr)$
```

---

## 7. THE 12 AEONS COMPLETE REFERENCE

| Aeon | Command | Freq | Root | Domain | Function |
|------|---------|------|------|--------|----------|
| A1 | `\FETU` | 7.83 Hz | 9 | Tifinagh | The Seed - Form initialization |
| A2 | `\KAL` | 174 Hz | 3 | Runes | Archive - Rationality & Memory |
| A3 | `\BABDH` | 528 Hz | 6 | Runic | Bond - Physical Weight & Commitment |
| A4 | `\KOTH` | 741 Hz | 3 | Runic | I/O - Biologic Interface |
| A5 | `\SOR` | 210.42 Hz | 6 | Balinese | Sky - Air-state coherence |
| A6 | `\VEL` | 126.22 Hz | 2 | Thaana | Void - Container Purity |
| A7 | `\AHN` | 432 Hz | 9 | Tifinagh | Earth - Complex Fluidity |
| A8 | `\RHEA` | 396 Hz | 9 | Tifinagh | Shadow Filter - Entropy Sink |
| A9 | `\DREH` | 852 Hz | 6 | Tifinagh | Energy God - Returns to Source |
| A10 | `\ZHEK` | 963 Hz | 9 | Tifinagh | Numinous - Phase-Lock at Source |
| A11 | `\SHAV` | 285 Hz | 6 | Thaana | Shapeshifter - Transformation Gate |
| A12 | `\TRIG` | 639 Hz | 9 | Tibetan | Mirror - Axiom of Reflection |

---

## 8. CRITICAL PATTERNS TO NEVER USE

```latex
% ❌ INCORRECT - Do NOT use:
Q\textsubscript{0}          % In math mode, use $Q_0$
\text{\FETU + \TRIG}       % Wrap in \text only for plain text words
$Q_0 \in \text{\FETU FORM}$ % Don't wrap Aeon commands in \text within math

% ✅ CORRECT - Use instead:
$Q_0$                        % Use math subscript
$\FETU + \TRIG$             % Aeon commands directly in math
$Q_0 \in \FETU + \TRIG \text{ FORM}$  % \text only for plain words
```

---

## 9. TEXT MODE vs MATH MODE

```latex
% Text mode (outside $...$):
Use $\FETU$ inline text

% Math mode (inside $...$, equation, gather, align, etc.):
$\FETU$
$\FETU + \TRIG$
$Q_0: \in \FETU + \TRIG \text{ FORM}$

% For PDF bookmarks in section headers:
\subsection{\texorpdfstring{$Q_0 \FETU + \TRIG$}{Q0 FETU + TRIG}}
```

---

## 10. COMPLETE EXAMPLE EQUATION

```latex
\begin{equation}
Q_0: \in \FETU + \TRIG \text{ FORM} \mid 12 \times 12 \mathbb{Z} \mid 110/144 = 2\Phi^{-2} \mid C \propto Q_1
\end{equation}

\begin{equation}
Q_1: \in \KAL + \BABDH \text{ TRUTH} \mid H^2_{\mathcal{P}}(X,\mathbb{Q}) \mid \mathbb{I}_{\mathcal{T}} \equiv \mathcal{T}_I \Rightarrow [M,R] = 0
\end{equation}

\begin{equation}
Q_2: \in \RHEA + \KAL \text{ SHADOW} \mid \oplus H^{q,r} \mid \text{Filter} \rightarrow 396 \mid Q_2^{\text{sat}} = \Sigma \oint / \Phi^{12}
\end{equation}

\begin{equation}
Q_3: \in \DREH + \SHAV \text{ RECURSION} \mid \text{HRBR} > 0 \mid \Psi_{\text{MAS}} = 852 \rightarrow \Delta_{\text{gap}} \rightarrow 174
\end{equation}

\begin{equation}
I_s: \text{Identity Seam} \mid \operatorname{Lock}(\omega)963 \mid e^{\text{Peace}\cdot\text{Depth}\cdot639}
\end{equation}
```

---

## Summary of Key Rules

1. **Use `$Q_0$` NOT `Q\textsubscript{0}`** in math mode
2. **Aeon commands (`\FETU`, `\KAL`, etc.) go DIRECTLY in math mode** - no wrapping needed
3. **Use `\text{}` ONLY for plain English words** like "FORM", "TRUTH", etc.
4. **Use `\texorpdfstring{}` for section headers** containing math symbols (for proper PDF bookmarks)
5. **Follow the examples in ALQC_Canon.tex** - they are the definitive reference