#!/usr/bin/env python
# -*- coding: utf-8 -*-
# most look like r"\\blah":r"\blah{}" but some use r"\\\blah":r"\\blah"

latexKeywords = [
    #(r"\{",r'{}'),
    #(r"\}",r'}'),
    #(r"\[",r'[]'),
    #(r"\]",r']'),
    (r"\\alpha\{",r"\alpha"),
    (r"\\approx",r'\approx'),
    (r"\\author\{",r'\author{}'),
    (r"\\begin\{",r'\begin{}'),
    (r"\\bar\{",r'\bar{}'),
    (r"\\big",r'\big{}'),
    (r"\\bibliographystyle{",r'\bibliographystyle{}'),
    (r"\\bibliography{",r'\bibliography{}'),
    (r"\\bigg",r'\bigg{}'),
    (r"\\Big",r'\Big{}'),
    (r"\\Bigg",r'\Bigg{}'),
    (r"\\beta",r'\beta'),
    (r"\\Beta",r'\Beta'),
    (r"\\bm{",r'\bm{}'),
    (r"\\caption{",r'\caption{}'),
    (r"\\cong",r'\cong'),
    (r"\\cap\{",r'\cap'),
    (r"\\centering",r'\centering'),
    (r"\\cite{",r'\\cite{}'),
    (r"\\cup{",r'\cup'),
    (r"\\date\{",r'\date{}'),
    (r"\\delta",r'\delta{}'),
    (r"\\definecolor{",r'\definecolor{}{}{}'),
    (r"\\def{",r'\def{}'),
    (r"\\Delta",r'\Delta{}'),
    (r"\\documentclass",r'\documentclass{}'),
    (r"\\end\{",r'\end{}'),
    (r"\\epsilon",r'\epsilon'),
    (r"\\equiv",r'\equiv'),
    (r"\\footnotesize",r'\footnotesize'),
    (r"\\frac{",r'\frac{}{}'),
    (r"\\hline",r'\hline{}'),
    (r"\\hypersetup\{",r'\hypersetup{}'),
    (r"\\in",r'\in'),
    (r"\\includegraphics\{",r'\includegraphics{}'),
    (r"\\item{",r'\item'),
    (r"\\ldots",r'\ldots'),
    (r"\\leq",r'\leq'),
    (r"\\label{",r'\label{}'),
    (r"\\left",r'\left'),
    (r"\\\maketitle",r'\\maketitle'),
    (r"\\mathbf{",r'\mathbf{}'),
    (r"\\mathcal{",r'\mathcal{}'),
    (r"\\mu",r'\mu'),
    (r"\\newcommand{",r'\newcommand{}{}'),
    (r"\\newline",r'\newline'),
    (r"\\noindent",r'\noindent'),
    (r"\\neq",r'\neq'),
    (r"\\normalsize",r'\normalsize'),
    (r"\\paragraph\{",r'\paragraph{}'),
    (r"\\paragraph\*{",r'\paragraph*{}'),
    (r"\\pm",r'\pm'),
    (r"\\pi",r'\pi'),
    (r"\\phi",r'\phi'),
    (r"\\Phi",r'\Phi'),
    (r"\\perp",r'\perp'),
    (r"\\prod",r'\prod^{}_{}'),
    (r"\\right",r'\right'),
    (r"\\ref{",r'\ref'),
    (r"\\section\{",r'\section{}'),
    (r"\\section\*\{",r'\section*{}'),
    (r"\\setlength",r'\setlength{}{}'),
    (r"\\sqrt{",r'\sqrt{}'),
    (r"\\sigma",r'\sigma'),
    (r"\\sim",r'\sim'),
    (r"\\subsection{",r'\subsection{}'),
    (r"\\subsection\*\{",r'\subsection*{}'),
    (r"\\subsubsection\{",r'\subsubsection{}'),
    (r"\\subsubsection*\{",r'\subsubsection*{}'),
    (r"\\sum",r'\sum'),
    (r"\\scriptsize",r'\scriptsize'),
    (r"\\textrm",r'\textrm{}'),
    (r"\\times",r'\times'),
    (r"\\textbf",r'\textbf{}'),
    (r"\\textcolor",r'\textcolor{}'),
    (r"\\textit",r'\textit{}'),
    (r"\\textsl",r'\textsl{}'),
    (r"\\texttt",r'\texttt{}'),
    (r"\\title",r'\title{}'),
    (r"\\tiny",r'\tiny'),
    (r"\\today",r'\today'),
    (r"\\usepackage",r'\\usepackage{}'),
    (r"\\vdots",r'\vdots'),
    #(r"\\",r'\\'),
]