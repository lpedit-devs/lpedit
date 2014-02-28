#!/usr/bin/env python

"""
(1) takes an outfile (i.e. out.txt) and using the original file 
    combines the results into a single reST document.

inFileName is a file path to a *.rst | *.Rnw file
outFileName is a file path to a out file (i.e. out.txt)

USAGE:
   
    $ python ParsePython.py -i foo.rst -o out.txt

NOTE: this script preserves the order of the code chunks
"""

import getopt,sys,os,re

## parse inputs 
if len(sys.argv) < 5:
    print "INPUT ERROR", sys.argv[0] + " -i inFileName -o outFileName"
    sys.exit()

try:
    optlist, args = getopt.getopt(sys.argv[1:],'i:o:l:')
except getopt.GetoptError:
    print getopt.GetoptError
    print "INPUT ERROR:", sys.argv[0] + "-i inFileName -o outFileName -l language"
    sys.exit()

inFileName = None
outFileName = None

for o, a in optlist:
    if o == '-i':
        inFileName = a
    if o == '-o':
        outFileName = a
    if o == '-l':
        language = a

## error checking
if os.path.exists(inFileName) == False:
    print "INPUT ERROR:", sys.argv[0], inFileName, "does not exist"
    sys.exit()

if not re.search("\.rst",inFileName,flags=re.IGNORECASE):
    print "INPUT ERROR:", sys.argv[0], inFileName, "in file not of type *.rst"
    sys.exit()

if language.lower() == 'r':
    highlightLang = 'none'
elif language.lower() == 'python':
    highlightLang = 'python'
else:
    print "ERROR: AssembpleOutRst was provided with an invalid language arg"
    sys.exit()

## read the outfile results into a dictionary
outResultsHandle = open(outFileName,'r')
outResults = {}
chunk = 0

def get_label(_linja,chunk):
    linja = re.sub('"',"",_linja)
    linja = re.sub("\[\d+\]\s+","",linja)
    if re.search('^<<.+>>=',linja):
        chunk+=1
        label = re.sub("\s+","",linja)
        label = re.sub("[<<|>>|(=$)]","",label)

        if label == None or label == '' or label == 'chunk':
            label = 'chunk'+str(chunk)
        return label

    if re.search('^@',linja):
        return 'end'

    return None

for linja in outResultsHandle:
    label = get_label(linja,chunk)

    ## remove leading spaces in R output
    if re.search("^\s\[[0-9]+\]",linja):
        linja = linja[1:]

    if label == 'end':
        chunkLabel = None
    elif label != None:
        chunkLabel = label
        continue

    if chunkLabel != None:
        if outResults.has_key(chunkLabel) == False:
            outResults[chunkLabel] = ''
        outResults[chunkLabel] += re.sub("\n","\n  ",linja) 

## open a file
rstFileName = re.sub("\.rst",".rst.tmp",inFileName,flags=re.IGNORECASE)
outFileHandle = open(rstFileName,'w')
inFileHandle = open(inFileName,'r')
chunk = 0
chunkLabel = None

for linja in inFileHandle:
    label = get_label(linja,chunk)
    
    ## grab and highlight the included code
    if label == 'end':
        if chunkLabel != None:
            oldLabel = chunkLabel
        chunkLabel = None
    elif label != None:
        chunkLabel = label
        outFileHandle.write("\n.. rubric:: %s"%(chunkLabel))
        outFileHandle.write("\n\n.. code-block:: %s \n\n"%(language))
    
    if label == 'end' or label != None:
        pass
    elif chunkLabel == None:
        outFileHandle.write(linja)
    else:
        outFileHandle.write("  "+linja)

    ## add any results from included code
    if label == 'end':
        outFileHandle.write("\n\n%s \n\n  %s \n\n"%('.. code-block:: none',outResults[oldLabel]))
        
print 'assemble complete.'
