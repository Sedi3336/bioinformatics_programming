#!/bin/bash

#This is Sedi's reply to the first homework of the Bioinformatics programming course

white="winequality-white.csv"
red="winequality-red.csv"
url="http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/"

if [ ! -e "./download/" ];then
	mkdir download
fi
cd download

if [ ! -e $white ];then
	wget $url$white
fi
if [ ! -e $red ];then
	wget $url$red
fi

if [ ! -e "../data" ];then
	mkdir ../data
fi
cd ../data

sed 's/;/,/g' ../download/$white > ./$white
sed 's/;/,/g' ../download/$red > ./$red

awk -F "," 'NR==1 {print $3 "," $5 "," $9 "," $11} ; $12>5 {print $3 "," $5 "," $9 "," $11}' $white > white_wine_good.csv
awk -F "," 'NR==2 {print $3 "," $5 "," $9 "," $11} ; $12<=5 {print $3 "," $5 "," $9 "," $11}' $white > white_wine_poor.csv
awk -F "," 'NR==1 {print $3 "," $5 "," $9 "," $11} ; $12>5 {print $3 "," $5 "," $9 "," $11}' $red > red_wine_good.csv
awk -F "," 'NR==2 {print $3 "," $5 "," $9 "," $11} ; $12<=5 {print $3 "," $5 "," $9 "," $11}' $red > red_wine_poor.csv


csv_wines=("white_wine_good.csv" "white_wine_poor.csv" "red_wine_good.csv" "red_wine_poor.csv")

cd ..
python3 HW2.py ${csv_wines[@]}
