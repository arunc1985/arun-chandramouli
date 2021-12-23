'''
    This module contains all the required main APIs for processing and publications
'''
import os
from utils import JsonOperator,ESOperator,BMICalculator

# Define the main processor class for BMI operations. This class object will serve as entrypoint
class BMIProcessor:

    def __init__(self,bmiUsersJsonFile,bmiCatJsonFile):
        self.bmiUsersJsonFile=bmiUsersJsonFile
        self.bmiCatJsonFile=bmiCatJsonFile

    def getFileContents(self):
        self.bmiUsersJsonFileContents=JsonOperator.readJson(json_file=self.bmiUsersJsonFile)
        self.bmiCatJsonFileContents=JsonOperator.readJson(json_file=self.bmiCatJsonFile)
        print(self.bmiCatJsonFileContents)

    def getBMIValues(self):
        for data in BMICalculator.calculateBmi(self.bmiUsersJsonFileContents,self.bmiCatJsonFileContents):
            print(data)

if __name__ == "__main__":
    bmiUsersJsonFile = os.environ['bmiUsersJsonFile']
    bmiCatJsonFile = os.environ['bmiCatJsonFile']
    procesor_ins=BMIProcessor(bmiUsersJsonFile,bmiCatJsonFile)
    procesor_ins.getFileContents()
    procesor_ins.getBMIValues()
