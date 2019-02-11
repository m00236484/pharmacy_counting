import sys
import os
from itertools import islice
import csv
import time
import multiprocessing as mp,os

 
def processLine(fileName,drugs,  chunkStart, chunkSize):
    with open(fileName) as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        for line in lines:
            #process(line)
            #data = line.strip().split(',')
            if_drug_exist(line, drugs)


def readFile(fileName):
    
    print("Reading Input File: " + fileName)
    #drug = {}
    manager = mp.Manager()
    drug = manager.dict()    
    def chunkFile(fileName,size=1024*1024):
        fileEnd = os.path.getsize(fileName)
        with open(fileName,'r') as f:
            chunkEnd = f.tell()
            while True:
                chunkStart = chunkEnd
                f.seek(size,1)
                f.readline()
                chunkEnd = f.tell()
                yield chunkStart, chunkEnd - chunkStart
                if chunkEnd > fileEnd:
                    break
    #init objects
    cores = mp.cpu_count()
    pool = mp.Pool(cores)
    jobs = []

    #creaite jobs
    for chunkStart,chunkSize in chunkFile(fileName):
       jobs.append( pool.apply_async(processLine,(fileName, drug,chunkStart,chunkSize)) )

    #wait for all jobs to finish
    for job in jobs:
       job.get()

    #clean up
    print len(drug)
    get_output(drug)
    pool.close()
    '''
     lineCount = 0
   
       
        if lineCount == 0: 
            print("Warning : File is Empty, No Data to process!" )
        else:
            print("Total Found Raw Data : " + str(lineCount))
       
    '''
     
def get_output(drugs):
    print("Generating Output") 
    
    sortDrug = sorted(drugs.items(), key=lambda x: x[1], reverse=True)
    dirPath = os.path.dirname(os.getcwd())
    fileName = dirPath +'/output/top_cost_drug.txt'
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
    
    data = row.strip().split(",")
    if len(data) <   5  : return 
    id = data[0]
    drug_name = data[-2]
    drug_cost = data[-1]
    try:
       float(drug_cost)
    except ValueError:
        print drug_cost
        return
   
   
    client = set()
    drug_detail = []
        
    if drug_name in drugs:
        #print drug_name       
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
    dirPath = os.path.dirname(os.getcwd())
    fileName = dirPath +'/input/itcont.txt'
    print (fileName)
    if not os.path.exists(fileName):
        print ("Error : Input File doesn't Exist!")
        return 

    readFile(fileName)
    timeAfter = time.time()
    elapsed = timeAfter - timeBefore;
    print("Total Execution Time : " + str(long(elapsed))+ " Seconds")
    
if __name__ == '__main__':
    main()   
