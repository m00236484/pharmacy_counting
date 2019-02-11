import sys
import os
from itertools import islice
import csv
import time

def readFile(fileName, drug):
    print("Reading Input File: " + fileName)  
    
    lineCount = 0
    with open(fileName, 'r') as inputFile:
        next(inputFile) 
        for row in inputFile:
           lineCount += 1
           data = row.strip().split(',')
           if_drug_exist(row, drug) 
       
        if lineCount == 0: 
            print("Warning : File is Empty, No Data to process!" )
        else:
            print("Total Found Raw Data : " + str(lineCount))
       
        #if len(drug)>= 1 :  get_output(drug) 


def get_output(fileName, drugs):
    print("Generating Output") 
    sortDrug = sorted(drugs.items(), key=lambda x: x[1], reverse=True)
    dirPath = os.path.dirname(os.getcwd())
    #fileName = dirPath +'/output/top_cost_drug.txt'
    f = open(fileName, "w")
    # print sortDrug
    outRecord = 0
    f.write("drug_name,num_prescriber,total_cost" + '\n')  
    for drug, value  in sortDrug:
        outRecord += 1
        data = drug +',' + str(value[1]) + ',' + str(long(value[0])) + '\n' 
        f.write(data)
    print ("Count Of Drug output:" + str(outRecord) ) 
    print ("Ouput File:" + fileName ) 
        
          
            
def if_drug_exist(row, drugs):
    data = row.split(",")
    if len(data) <   5  : return 
    id = data[0]
    drug_name = data[-2]
    drug_cost = data[-1] 
    client = set()
    drug_detail = []
    if drug_name in drugs:
        drug_detail = drugs[drug_name]
        drug_detail[0] += float(drug_cost)
        client = drug_detail[2]
        if id not in client: 
            client.add(id)
            drug_detail[1] += 1
            drug_detail[2] = client    
        drugs[drug_name] = drug_detail
    else:
        drug_detail.append(float(drug_cost))
        client.add(id)
        drug_detail.append(1)
        drug_detail.append( client)
        drugs[drug_name] = drug_detail
        

def main():
    timeBefore = time.time() 
    print("App Started to Calculate Total Drug Cost" )
    total = len(sys.argv)
    cmdargs = str(sys.argv)
    inputFile = str(sys.argv[1])
    outPutFile = str(sys.argv[2])
    
    dirPath = os.path.dirname(os.getcwd())
    inDir = os.path.abspath(os.path.join(inputFile, os.pardir))
    fileName = os.path.basename(inputFile)
   
    if not os.path.exists(inputFile):
        print ("Error : Input File :" + fileName +"  doesn't Exist in This Directory " + inDir )
        return 
    inDir = os.path.abspath(os.path.join(inputFile, os.pardir))
    print inDir
    outDir = os.path.abspath(os.path.join(outPutFile, os.pardir))
    #print outDir 
    if not os.path.exists(outDir):
        print ("Error : Output Directory doesn't Exist!")
        return

    drugs = {}
    readFile(inputFile,drugs)
    if len(drugs)>= 1 :  get_output(outPutFile, drugs)

    timeAfter = time.time()
    elapsed = timeAfter - timeBefore;
    print("Total Execution Time : " + str(long(elapsed))+ " Seconds")
    
if __name__ == '__main__':
    main()   
