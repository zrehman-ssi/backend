import werkzeug
from flask_restplus import reqparse

import csv,os

from ..util.constants import Messages
from ..util.enums import FileAccessMode
from ..util.dto import FileInfo

_Messages=Messages

file_upload = reqparse.RequestParser()
file_upload.add_argument('file',  
                         type=werkzeug.datastructures.FileStorage, 
                         location='files', 
                         required=True, 
                         help='Upload file')
file_upload.add_argument('data',                          
                         required=True, 
                         help='data')


class CsvFileParser(object):

    @staticmethod
    def parse(filePath):        
        rows=[]
        try: 
            with open(filePath,'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                for row in csv_reader:
                    rows.append(row)
                
                fileInfo = FileInfo()
                fileInfo.rows = rows                

                return fileInfo

        except Exception as e:
            print(e)
            return   _Messages.ERROR_IN_FILE_READING  


