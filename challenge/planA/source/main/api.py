'''
    This module contains all the required main APIs for processing and publications
'''
import os
from utils import JsonOperator,ESOperator,BMICalculator

# Define the main processor class for BMI operations. This class object will serve as entrypoint
class BMIProcessor:
    '''
        This class deals with following tasks;
            1. Get JSON input files from Users
            2. Load JSON records into memory
            3. Find BMI Values - BMI, Category, HealthRisk
            4. Update the existing records with new columns
    '''

    def __init__(self,bmiUsersJsonFile,bmiCatJsonFile):
        '''
            Initialize the files attributes
            :param bmiUsersJsonFileContents: File that contains user-data such as Gender, Height, Weight
            :param bmiCatJsonFileContents: 
                File that contains category,healthRisk such as UnderWeight,OverWeight etc..Contains Ranges of weighs
        '''
        self.bmiUsersJsonFile=bmiUsersJsonFile
        self.bmiCatJsonFile=bmiCatJsonFile

    def getFileContents(self):
        '''
            Using Utils read the *JSON* files and load
        '''
        self.bmiUsersJsonFileContents=JsonOperator.readJson(json_file=self.bmiUsersJsonFile)
        self.bmiCatJsonFileContents=JsonOperator.readJson(json_file=self.bmiCatJsonFile)

    def getBMIValues(self):
        '''
            Given the JSON set of records from step -getFileContents,
            find out the BMI Index, Category, HealthRisk etc and yield the records.
        '''
        for data in BMICalculator.calculateBmi(self.bmiUsersJsonFileContents,self.bmiCatJsonFileContents):
            print(data)

    def findSpecificCat(self):
        '''
            Given a Set of Records in millions from previous step - getBMIValues,
            find out people of specific category such as OverWeight, ModerateWeight etc...
        '''

class ESProcessor:
    '''
        This class deals with following tasks;
        1. Create ES re-usable connections
        2. Push records to ES Index
        3. Read records from ES Index
        4. Delete Indexes
    '''

    def __init__(self,**esConnParams):
        '''
            Initialize the ElasticSearch attributes
            :param esConnParams: ElasticSearch Hostname and PORT
        '''
        self.esConnParams=esConnParams

    def getEsConnection(self):
        '''
            Return an ES connection
        '''
        self.esConnObj=ESOperator.esConnection(self.esConnParams['esHost'],self.esConnParams['esPort'])
        return self.esConnObj

    def setRecordsBulk(self,es_index,records):
        '''
            Push records in BULK into ElasticSearch
        '''
        return ESOperator.bulkUploadJson(es_conn_object=self.esConnObj,es_index=es_index,json_file_contents=records)

    def getRecordsFromIndex(self,es_index):
        '''
            Get Records from an Index and return
        '''
        return ESOperator.bulkReadJson(es_conn_object=self.esConnObj,es_index=es_index)

if __name__ == "__main__":
    '''
        export bmiCatJsonFile=/home/intucell/tests/arun-chandramouli/challenge/planA/files/bmi_cat.json
        export bmiUsersJsonFile=/home/intucell/tests/arun-chandramouli/challenge/planA/files/sample1.json
        export bmiCAT="OverWeight"
    '''
    bmiUsersJsonFile = os.environ['bmiUsersJsonFile']
    bmiCatJsonFile = os.environ['bmiCatJsonFile']
    procesor_ins=BMIProcessor(bmiUsersJsonFile,bmiCatJsonFile)
    procesor_ins.getFileContents()
    procesor_ins.getBMIValues()
