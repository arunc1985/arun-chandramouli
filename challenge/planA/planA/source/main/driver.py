'''
    Driver module for start-up
'''
from api import BMIProcessor,ESDataParser

class BmiDriver:

    @staticmethod
    def upload(bmiUsersJsonFile,bmiCatJsonFile,esHost,esPort,esIndex):
        '''
            Parse Records & Upload to Elasticsearch Index(Bulk Upload)
        '''
        procesor_ins=BMIProcessor(bmiUsersJsonFile,bmiCatJsonFile)
        procesor_ins.getFileContents()
        procesor_ins.getBMIValues()
        es_processor_ins=ESDataUploader(esHost='localhost',esPort='9200')     
        es_processor_ins.getEsConnection()
        es_processor_ins.setRecordsBulk(es_index='bmi',records=list(procesor_ins.getBMIValues()))
        return True

if __name__ == "__main__":
    '''
        unset bmiUsersJsonFile
        unset bmiCatJsonFile
        unset esHost
        unset esPort
        unset esIndex
        unset bmiCAT
        export bmiCatJsonFile=/home/intucell/tests/arun-chandramouli/challenge/planA/files/bmi_cat.json
        export bmiUsersJsonFile=/home/intucell/tests/arun-chandramouli/challenge/planA/files/sample2.json
        export esHost=localhost
        export esPort=9200
        export esIndex='bmi'
        export bmiCAT="OverWeight"
    '''
    bmiUsersJsonFile=os.environ['bmiUsersJsonFile']
    bmiCatJsonFile=os.environ['bmiCatJsonFile']
    esHost=os.environ['esHost']    
    esPort=os.environ['esPort']    
    esIndex=os.environ['esIndex'] 
    # Upload Records
    BmiDriver.upload(bmiUsersJsonFile,bmiCatJsonFile,esHost,esPort,esIndex)

    es_processor_ins_parser=ESDataParser(esHost='localhost',esPort='9200')
    es_processor_ins_parser.getEsConnection()
    results=es_processor_ins_parser.getRecordsFromIndex(es_index='bmi',query={'bmi.cat':'ModerateObese'})
    print("results :: ",results)
