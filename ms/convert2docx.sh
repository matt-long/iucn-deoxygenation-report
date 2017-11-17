#!/bin/bash


#htlatex future-chapter.tex "html,word" "symbol/! -cmozhtf" "-coo -cvalidate"

# see https://github.com/citation-style-language/styles
pandoc  future-chapter.tex --number-sections --bibliography=references.bib --csl=agu.csl  -smart -o future-chapter.docx
