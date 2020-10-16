#!/bin/bash

#This is Sedi's reply to the second homework of the Bioinformatics programming and scripting course

white="winequality-white.csv"
red="winequality-red.csv"
url="http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/"
# A directory called download is created and we change our directory to download
if [ ! -e "./download/" ];then
	mkdir download
fi
cd download
#wget is used to download the data (white and red) in the download directory.
if [ ! -e $white ];then
	wget $url$white
fi
if [ ! -e $red ];then
	wget $url$red
fi
#a directory called data is created and we change our current directory to data and replace all the ; to , and save changes in the data directory
if [ ! -e "../data" ];then
	mkdir ../data
fi
cd ../data

sed 's/;/,/g' ../download/$white > ./$white
sed 's/;/,/g' ../download/$red > ./$red
# awk is used to keep only the 4 columns with the variables of interest and quality is used to subset the data.

awk -F "," 'NR==1 {print $3 "," $5 "," $9 "," $11} ; NR==1 { next } $12>5 {print $3 "," $5 "," $9 "," $11}' $white > white_wine_good.csv
awk -F "," 'NR==1 {print $3 "," $5 "," $9 "," $11} ; NR==1 { next } $12<=5 {print $3 "," $5 "," $9 "," $11}' $white > white_wine_poor.csv
awk -F "," 'NR==1 {print $3 "," $5 "," $9 "," $11} ; NR==1 { next } $12>5 {print $3 "," $5 "," $9 "," $11}' $red > red_wine_good.csv
awk -F "," 'NR==1 {print $3 "," $5 "," $9 "," $11} ; NR==1 { next } $12<=5 {print $3 "," $5 "," $9 "," $11}' $red > red_wine_poor.csv

# a list of wine paths and a directory called results are created here. At the end, we run the python  which will perform the analysis on the csv_wines
csv_wines=("white_wine_good.csv" "white_wine_poor.csv" "red_wine_good.csv" "red_wine_poor.csv")
cd ..
if [ ! -e "./results/" ];then
        mkdir results
fi
python3 HW2.py ${csv_wines[@]}
