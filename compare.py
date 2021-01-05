#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import external modules
from bs4 import BeautifulSoup
import sys
import re
import os
import datetime
import glob

# retrieve data from files
fileOrigin = open("origin.html", "r")
fileGenerated = open("generated.html", "r")

# parse the files
soupOrigin = BeautifulSoup(fileOrigin, 'lxml')
soupGenerated = BeautifulSoup(fileGenerated, 'lxml')

def removeBlankSpace(sentence):
    pattern=r"\s+"
    return re.sub(pattern, "", sentence)

def formatData(myListDataSource,myListDataFinal):
    # myListDataFinal=[]
    for x in myListDataSource:
        myVal=x.text.replace("\n"," ")
        if len(myVal)>1:
            myListDataFinal.append(myVal.strip())

def createFile(myList,myFilename):
    f=open(myFilename, 'w')
    for rec in myList:
        f.writelines(rec + "\n")
    f.close()

# display the values of the classs implemented inside the file
def extractClassValue():
    classes = []
    setOfClass=()
    for x in [soupOrigin,soupGenerated]:
        for element in x.find_all(class_=True):
            classes.extend(element["class"])
        setOfClass=set(classes)
        if x==soupOrigin:
            print(f"Available classes within the origin file {setOfClass}")
        else :
            print(f"Available classes within the generated file {setOfClass}")

def purge(dir):
    files = os.listdir(dir)
    ext = ('.txt')
    for file in files:
        if file.endswith(ext):
            os.remove(os.path.join(dir,file))

def compareTwoList():

    # user input
    print("Please insert the class targeted!!!")
    myClass=input()

    now = datetime.datetime.now()
    now=str(now.strftime("%Y-%m-%d %H:%M:%S")).replace(" ","").replace("-","")

    # creating the file
    f=open("results" + now +".txt", 'w')

    # retrieve the p tag
    originListP=soupOrigin.find_all("p",class_=myClass)
    generatedListP=soupGenerated.find_all("p",class_=myClass)

    originListPF=[]
    generatedListPF=[]

    # format the data
    formatData(originListP,originListPF)
    formatData(generatedListP,generatedListPF)

    # generate the data extracted from html and save it into a txt file
    createFile(originListPF,"dataOrigin.txt")
    createFile(generatedListPF,"dataGenerated.txt")

    # sort the data 
    list1=sorted(originListPF)
    list2=sorted(generatedListPF)

    print("")
    print("-------------- Details of the comparison -------------------------------")
    print("")
    f.write("\n")
    f.write("\n-------------- Details of the comparison -------------------------------")
    f.write("\n")
    
    # origin has more contents

    if len(list1)>len(list2):
        referenceList=set(list1)
        print("Origin file has more contents than generated file")
        print("")
        f.write("\nOrigin file has more contents than generated file")
        f.write("\n")

    if len(list1)<len(list2):
        referenceList=set(list2)
        print("Generated file has more contents than origin file")
        print("")
        f.write("\nGenerated file has more contents than origin file")
        f.write("\n")

    if len(list1)==len(list2):
        referenceList=set(list2)
        print("Generated file has the same number of content with origin file")
        print("")
        f.write("\nGenerated file has the same number of content with origin file")
        f.write("\n")

    for ele in referenceList:
        occurLs1=0
        occurLs2=0

        eleBis=removeBlankSpace(ele)

        # count the occurence in list1
        for ls1 in list1:
            ls1Bis=removeBlankSpace(ls1)
            if ls1Bis==eleBis:
                occurLs1+=1

        # count the occurence in list2
        for ls2 in list2:
            ls2Bis=removeBlankSpace(ls2)
            if ls2Bis==eleBis:
                occurLs2+=1

        # display results
        if occurLs1-occurLs2 !=0 :
            print(f"Element to compare :  {ele}")
            print(f"Occurence(s) in Origin file : {occurLs1}")
            print(f"Occurence(s) in Generated file : {occurLs2}")
            print(f"Difference : {abs(occurLs1-occurLs2)}")
            
            print(f"--------------------------------------------")
            f.write(f"\nElement to compare :  {ele}")
            f.write(f"\nOccurence(s) in Origin file : {occurLs1}")
            f.write(f"\nOccurence(s) in Generated file : {occurLs2}")
            f.write(f"\nDifference : {abs(occurLs1-occurLs2)}")
            f.write(f"\n--------------------------------------------")

    # close the file
    f.close()

    # final message
    print(f"Files generated here : {os.getcwd()}")

def displayMenu():
    print("")
    print("---------------------------------------------------------------------")
    print("-------------- COMPARE ITPP HTML GENERATED FILES --------------------")
    print("---------------------------------------------------------------------")
    print("")
    print("Option  1 :-> List the available classes  ")
    print("Option  2 :-> Show the Global stats abouts the P <Tag>  ")
    print("Option  3 :-> Comparison Process between origin and generated html files  ")
    print("Option  4 :-> Close the app  ")
    print("")

def showGlobalStats():
    originNbrP=len(soupOrigin.find_all('p'))
    generatedNbrP=len(soupGenerated.find_all('p'))
    print("")
    print("-------------- Global Stats -----------------------------------------")
    print("")
    print(f"Origin file, number of paragraphs : {originNbrP}")
    print(f"Generated file, number of paragraphs : {generatedNbrP}")
    print(f"Diff number of paragraphs : {abs(generatedNbrP-originNbrP)}")
    print("")

def main():
    # remove existing .txt files 
    purge(os.getcwd())

    while True :

        displayMenu()

        print("Please insert your option : ")
        
        userChoice=int(input())

        # management of the user's choice

        if userChoice ==1 :
            extractClassValue()

        if userChoice ==2 :
            showGlobalStats()

        if userChoice ==3 :
            compareTwoList()
        
        if userChoice ==4 :
            sys.exit()
            break

        if userChoice not in [1,2,3,4] :
            print("Please check your input!!!")


if __name__ == "__main__":
    main()