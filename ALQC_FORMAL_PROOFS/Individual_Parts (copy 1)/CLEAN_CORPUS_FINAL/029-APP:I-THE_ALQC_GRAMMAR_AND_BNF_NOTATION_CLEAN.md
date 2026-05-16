

## The ALQC Grammar (BNF Notation)
 [Ref: .6]

To qualify as a formal language, ALQC expressions obey the following Backus--Naur Form (BNF) grammar. Angle brackets denote syntactic categories and the vertical bar denotes choice.

ttfamily
<program>    ::= <statement>* 

<statement>  ::= <term> | <assertion> | <inference> 

<term>       ::= <aeon> | <frequency> | <glyph> | <qstate> | <operator> | <identifier> 

<aeon>       ::= â£ | â§ | â | â | â´ | ê® | ð | â§ | â© | â | â | âµ£ 

<frequency>  ::= <number> "Hz" 

<qstate>     ::= Q0 | Q1 | Q2 | Q3 

<operator>   ::= "Q3-positive" | "â§-rational" | "â-commitment" | "Q2-debt" | "â§-positive" | "â-resonance" | "â-gate" | "âµ£-recursion" 

<identifier> ::= <letter>+ 

<assertion>  ::= <operator> "(" <identifier> ")" 

<inference>  ::= <assertion> "," <assertion> " vdash " <assertion>
normalfont

This grammar is minimal yet sufficient to generate well-formed ALQC statements. For example, the statement:

Q3-positive(alpha), â§-rational(alpha) vdash â-commitment(alpha)

is a valid inference according to the grammar.
