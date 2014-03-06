.. sweave


Importing a CSV File
==========================

Some practices when we carry out analyses simply do not feel reproducible or they lend themselves too easily to human error.  Copy and paste for example.  Taking two columns from a spreadsheet and making a new one is fairly easy, but would you make a mistake after 100 times?  People have `lost their jobs <http://www.economist.com/node/21528593>`_ and worse because of carelessness in spreadsheet manipulation.

So let the computer do it for you.

Download: :download:`ExampleInDataFile.csv <../ExampleInDataFile.csv>`

<<import-csv-example>>=
# (1) read in a csv file where one field is a date
# (2) write a new csv file with a new field added as a column
# NOTE: The new col will consist of days from some date

library(stats)

## read in the automated results
inFileName <- "ExampleInDataFile.csv"
inFilePath <- paste(getwd(),inFileName,sep="/")
inData <- read.table(inFilePath,header=T,sep=",")
header <- names(inData)

## prepare the outfile
outfileName <- "ExampleOutDataFile.csv" 
newHeader <- paste('group','value','date','time','daysFrom',sep=",")
cat(newHeader,file=outfileName,append=F,fill=T)

## create a function to play with the columns
dayOne <- as.Date("1979-11-19")
process_file <- function(x, outfile) {
    group <- x[1] 
    value <- x[2]
    date  <- x[3]
    time  <- x[4]
    daysFrom <- as.Date(date) - dayOne
    rowToOutput <- paste(group, value, date, time, daysFrom, sep=",")
    print(paste(group, value, date, time, sep=","))
    cat(rowToOutput,file=outfile,append=T,fill=T)
}

## write the data to file
apply(inData, 1, process_file,outfile=outfileName)
@

Exercises
^^^^^^^^^^^^^^

  1. Create a Sweave document that breaks this code up at each of the comments

So now lets read in the file and play with it:
<<import-csv-example>>=
x <- read.csv("ExampleInDataFile.csv")
attach(x)
print(names(x))
print(mean(x$value))
@