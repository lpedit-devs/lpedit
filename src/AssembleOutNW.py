#!/usr/bin/env python

"""
(1) takes an outfile (i.e. out.txt) and using the original file 
    combines the results into a single latex document.

inFileName is a file path to a *.rst | *.Rnw file
outFileName is a file path to a out file (i.e. out.txt)

USAGE:
   
    $ python AssembleOutNW.py -i out.txt -o outfile.txt

NOTE: this script preserves the order of the code chunks
"""

import getopt,sys,os,re

## parse inputs 
if len(sys.argv) < 5:
    print "INPUT ERROR", sys.argv[0] + " -i inFileName -o outFileName"
    sys.exit()

try:
    optlist, args = getopt.getopt(sys.argv[1:],'i:o:')
except getopt.GetoptError:
    print getopt.GetoptError
    print "INPUT ERROR:", sys.argv[0] + "-i inFileName -o outFileName"
    sys.exit()

inFileName = None
outFileName = None

for o, a in optlist:
    if o == '-i':
        inFileName = a
    if o == '-o':
        outFileName = a

## error checking
if os.path.exists(inFileName) == False:
    print "INPUT ERROR:", sys.argv[0], inFileName, "does not exist"
    sys.exit()

if not re.search("\.nw",inFileName,flags=re.IGNORECASE):
    print "INPUT ERROR:", sys.argv[0], inFileName, "in file not of type *.nw"
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

## write the results of each chunk to a dictionary
for linja in outResultsHandle:
    label = get_label(linja,chunk)

    if label == 'end':
        chunkLabel = None
    elif label != None:
        chunkLabel = label
        continue

    if chunkLabel != None:
        if outResults.has_key(chunkLabel) == False:
            outResults[chunkLabel] = ''
        toWrite = re.sub("^[\s+]\[[\d|\d\d]\]\s+","",linja) 
        toWrite = re.sub("\n\s+","\n",toWrite) 
        toWrite = re.sub("\n[\s]+\[[\d|\d\d]\]","",toWrite)
        outResults[chunkLabel] += toWrite

## open an outfile
texFileName = re.sub("\.nw",".tex",inFileName,flags=re.IGNORECASE)
outFileHandle = open(texFileName,'w')
inFileHandle = open(inFileName,'r')

for linja in inFileHandle:
    label = get_label(linja,chunk)

    ## handle end label
    if label == 'end':
        if chunkLabel != None:
            oldLabel = chunkLabel
        chunkLabel = None
    elif label != None:
        chunkLabel = label

    ## code start
    if label != 'end' and label != None:
        outFileHandle.write("\n\\begin{verbatim}\n")

    ## write the document text
    if label == 'end' or label != None:
        pass
    elif chunkLabel == None:
        outFileHandle.write(linja) # text 
    else:
        outFileHandle.write(linja) # code

    ## add any results from included code
    if label == 'end':
        outFileHandle.write("\n\end{verbatim}\n")
        outFileHandle.write("\\begin{verbatim}\n\n%s"%outResults[oldLabel])
        outFileHandle.write("\n\end{verbatim}\n")
