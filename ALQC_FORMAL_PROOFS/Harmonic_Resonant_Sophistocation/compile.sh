#!/bin/bash
# Compilation script for Hyperspatial_Constant_of_Semantic_Reference.tex

# Try different LaTeX engines in order of preference
ENGINES=("xelatex" "lualatex" "pdflatex")

echo "Searching for compatible LaTeX engine..."

for engine in "${ENGINES[@]}"; do
    if command -v $engine &> /dev/null; then
        echo "Found $engine"
        echo "Compiling with $engine..."
        
        cd ALQC_FORMAL_PROOFS/Harmonic_Resonant_Sophistocation
        
        $engine Hyperspatial_Constant_of_Semantic_Reference.tex
        
        if [ $? -eq 0 ]; then
            echo ""
            "================================================"
            "Compilation successful with $engine!"
            "PDF output:" Hyperspatial_Constant_of_Semantic_Reference.pdf
            "================================================"
            exit 0
        else
            echo "$engine failed with exit code $?"
        fi
    fi
done

echo ""
echo "================================================"
echo "No compatible LaTeX engine found."
echo "Please install xelatex or lualatex to compile."
echo "================================================"
echo ""
echo "Alternative: Compile without visual elements using:"
echo "  xelatex -no-shell-escape -interaction=batchmode Hyperspatial_Constant_of_Semantic_Reference.tex"
echo ""
echo "For more detailed error output, run:"
echo "  xelatex -interaction=errormode Hyperspatial_Constant_of_Semantic_Reference.tex"