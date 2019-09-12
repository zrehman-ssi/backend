import os
import uuid
import datetime
import json
import base64
import pathlib
from pathlib import Path


from app.main import db
from ..util.dto import ResponseDto,FileInfoDto
from ..util.enums import ResponseStatus,FileAccessMode
from ..util.constants import Messages,GlobalSettings
from ..util.parsers import CsvFileParser

from app.main.model.file_info import FileInfo

from ..config import NetworkPath

_Messages=Messages
_Global_Settings=GlobalSettings

_file_InfoDto=FileInfoDto.file_info

def saveFile(args):
    if(args is not None):
        try:

            infoData = json.loads(args['data'])
            file = args['file']
            extension = getFileExtension(file.filename)
            _file_InfoDto.user_id = infoData['user_id']
            fullPath=os.path.join(NetworkPath, file.filename)
            if(os.path.isdir(NetworkPath)==False):
                os.mkdir(NetworkPath)
            isExist = os.path.isfile(fullPath)
            if(isExist==True):
                os.remove(fullPath) 
            file.save(fullPath)
            
            blob =  readFile(fullPath,FileAccessMode.READ_ONLY_BINARY_MODE)
            file_info = FileInfo(
                user_id=_file_InfoDto.user_id,
                guid=str(uuid.uuid4()),
                blob=blob,
                fileName=file.filename
            )
            guid = file_info.guid
            data = saveChanges(file_info)
            response_object=ResponseDto()
            response_object.data=True,
            response_object.status = ResponseStatus.SUCCESS.value,
            response_object.message = _Messages.FILE_UPLOADED_SUCCESS
            response_object.status_code=200       
            return response_object,guid
        except Exception as e:
            print(e)
            response_object=ResponseDto()
            response_object.data=False,
            response_object.status = ResponseStatus.FAIL.value,
            response_object.message = _Messages.FILE_UPLOADED_FAIL
            response_object.status_code=403       
            return response_object,''


def getFile(userId,fileGuid):
    try:
        file = FileInfo.query.filter_by(guid=fileGuid).filter_by(user_id=userId).first()
        if (file is not None):             
            return file

    except Exception as e:
        print(e)
        response_object=ResponseDto()
        response_object.data=True,
        response_object.status = ResponseStatus.FAIL.value,
        response_object.message = _Messages.ERROR_IN_FILE_READING
        response_object.status_code=403       
        return response_object    



def getFileExtension(fileName):
    file_extension = pathlib.PurePosixPath(fileName).suffix
    return file_extension

def getFileNameWithExtension(filePath):
    file_Name = Path(filePath).stem
    return file_Name



def readFile(filePath,fileAccessMode=FileAccessMode.NONE):
    try:

        if(fileAccessMode == FileAccessMode.NONE):
            return Messages.INVALID_FILE_ACCESS_MODE
        elif(fileAccessMode == FileAccessMode.READ):
            file = open(filePath,'r')
            data = file.read()
            return data
        elif(fileAccessMode == FileAccessMode.READ_ONLY_BINARY_MODE):
            with open(filePath,'rb') as file:
                blob = base64.b64encode(file.read())
                return blob    


    except Exception as e:
         print(e)
         return   _Messages.ERROR_IN_FILE_READING  


def writeFile(fileInfo,filePath,fileAccessMode=FileAccessMode.NONE):
    try:

        if(fileAccessMode == FileAccessMode.NONE):
            return Messages.INVALID_FILE_ACCESS_MODE
        elif(fileAccessMode == FileAccessMode.WRITE):
            pass
        elif(fileAccessMode == FileAccessMode.WRITE_ONLY_BINARY_MODE):
            file = base64.b64decode(fileInfo.blob)
            if(os.path.isdir(filePath)==False):
                os.mkdir(filePath)
            filePath = filePath + fileInfo.fileName
            isExist = os.path.isfile(filePath)
            if(isExist==True):
                os.remove(filePath)
            file_writer = open(filePath,'wb')
            file_writer.write(file)
            file_writer.close()        

    except Exception as e:
         print(e)
         return   _Messages.ERROR_IN_FILE_READING
  
        
def saveChanges(data):
    db.session.add(data)
    db.session.commit()
    return data  