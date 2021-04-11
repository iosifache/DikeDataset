#!/usr/bin/env bash
#
# Script for downloading the samples

# Process the malicious OLE file by download, unarchiving, extension
# filtering, renaming and extension replacement
for year in 2020 2021; 
do
    for month in $(seq -f "%02g" 1 12);
        do
            url="https://mb-api.abuse.ch/downloads/$year-$month-15.zip"; 
            wget "$url"; 
    done;
done
unzip -P infected "*.zip"
mkdir keeped
for ext in doc docx docm xls xlsx xlsm ppt pptx pptm;
do
    mv ./*.$ext keeped;
done
find . -type f -maxdepth 1 -exec rm {} \;
mv keeped/* .
for i in *;
do
    sum=$(sha256sum "$i");
    mv -- "$i" "${sum%% *}.${i##*.}";
done
rename.ul -o .xlsx .ole ./*.xlsx
for ext in doc docx docm xls xlsx xlsm ppt pptx pptm;
do
    rename.ul -o .$ext .ole ./*.$ext;
done
find . -type f -exec basename {} .ole \; > hashes.txt

# Process the benign and malicious PE files by downloading, unarchiving,
# moving and renaming
wget https://ndownloader.figshare.com/files/12149696
unrar x Dataset.rar
mkdir benign
mkdir malware
find Dataset/Benign -type f -exec cp {} benign \;
find Dataset/Virus -type f -exec cp {} malware \;
rm -rf Dataset
for i in benign/*;
do
    sum=$(sha256sum "$i");
    mv -- "$i" "${sum%% *}.${i##*.}";
done
for i in malware/*;
do
    sum=$(sha256sum "$i");
    mv -- "$i" "${sum%% *}.${i##*.}";
done