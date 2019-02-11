import sys
import os
from itertools import islice
import csv


def readFile(fileName):
    numberOfLines = 1000
    # dirPath = os.path.dirname(os.getcwd())
    #print(dirPath)
    drug = {}
    lincount = 0 
    with open(fileName, 'r') as inputFile:
        fileReader = islice(inputFile,1,None, numberOfLines)
        #cvsReader = csv.reader(fileName)
        #header = cvsReader.next()
        # print header
        for row in fileReader:
           #print row
           #if lincount ==  0: continue
           lincount += 1
           data = row.strip().split(',')
           
           #id,prescriber_last_name,prescriber_first_name,drug_name,drug_cost = data
           #if drug_name == 'NOVOLOG':
           #    print drug_cost
           if_drug_exist(row, drug) 
        print lincount 
        get_output(drug) 


def get_output(drugs):
    sortDrug = sorted(drugs.items(), key=lambda x: x[1], reverse=True)
    dirPath = os.path.dirname(os.getcwd())
    fileName = dirPath +'/output/output.txt'
    f = open(fileName, "w")
    # print sortDrug  
    for drug, value  in sortDrug:
        data = drug +',' + str(value[1]) + ',' + str(value[0]) + '\n' 
        f.write(data)
        
          
            
def if_drug_exist(data, drugs):
    #print data
    #return
    #print data 
    
    if len(data) <   5  : return 

    id = data[0]
    if id == '24525861': print "Got It"
    drug_name = data[-2]
    drug_cost = data[-1] 
    
    # prescriber_last_name,prescriber_first_name,
    drug_name = data[3]
    drug_cost = data[4]
    client = set()
    drug_detail = []
    if drug_name in drugs:
        #print (drug_name)
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
    dirPath = os.path.dirname(os.getcwd())
    fileName = dirPath +'/input/input.txt'
    # fileName = '/Users/unifi/Google Drive File Stream/My Drive/insight/pharmacy_counting/input/input.tx'
    readFile(fileName)


if __name__ == '__main__':
    main()   
