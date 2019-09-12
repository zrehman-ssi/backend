from enum import Enum

class ResponseStatus(Enum):
    SUCCESS = 'success'
    FAIL = 'fail'

class FileAccessMode(Enum):
    NONE=''
    READ = 'r' 
    READ_ONLY_BINARY_MODE = 'rb'
    READ_AND_WRITE = 'r+'
    WRITE = 'w' 
    WRITE_ONLY_BINARY_MODE ='wb'
    WRITE_AND_READ = 'w+'
    WRITE_AND_READ_BINARY_MODE = 'wb+'    

class FileType(Enum):
    TEXT = '.txt'
    CSV = '.csv'
    EXCEL = '.xsl'    


# Don't change the enums given below, it belongs to database
class UserType(Enum):
    NONE = 0
    ADMIN = 1
    PATIENT = 2
    DOCTOR = 3      

class OrganizationType(Enum):
    NONE = 0
    STAKEHOLDER = 1
    PROVIDER = 2       