#!/usr/bin/env python
# -*- coding: utf-8 -*-

text1 = r"""
%A minimial Python in LaTeX template
\documentclass[a4paper]{article}
\usepackage{amsmath,pgf,graphicx,textcomp}
\usepackage[utf8]{inputenc}

\title{Title of Document}
\author{Author Name}

\begin{document}
\maketitle

\section{Section title}
We show in this example how to create a matrix of random numbers.
The matrix has $N$ rows and $M$ columns.

<<label=chunk1>>=
import numpy as np
N = 4
M = 5
mat = np.random.normal(0,1,(N,M))
print(mat)
@

\end{document}
"""
