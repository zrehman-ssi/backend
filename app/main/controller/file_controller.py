from flask import request,make_response
from flask_restplus import Resource
from flask_jwt_extended import jwt_required  

from app.main import db
from ..util.dto import ResponseDto
from ..util.enums import ResponseStatus
from ..util.constants import Messages

from ..util.dto import FileInfoDto
from ..service.file_service import saveFile,getFile

from ..util import parsers

_Messages=Messages

api = FileInfoDto.api
_file_info = FileInfoDto.file_info

@api.route('/saveFile')
class SaveFile(Resource):

    @api.doc('save file')
    @api.expect(parsers.file_upload, validate=True)
    
    def post(self):
        """Save File"""

        if request.files is None or 'file' not in request.files:
            #No file found
            response_object=ResponseDto()
            response_object.data=True,
            response_object.status = ResponseStatus.FAIL.value,
            response_object.message = _Messages.FILE_NOT_FOUND
            response_object.status_code=403      
            return response_object.toJson(),403
             
        else:
            args = parsers.file_upload.parse_args()             
            
            file = args['file']
            data = args ['data']
            if((file is not None and data is not None) and file.filename != ''):
                response = saveFile(args)
                response_object = response[0]
                return response_object.toJson() , response_object.status_code
            else:
                #No selected file
                response_object=ResponseDto()
                response_object.data=True,
                response_object.status = ResponseStatus.FAIL.value,
                response_object.message = _Messages.NO_SELECTED_FILE
                response_object.status_code=403      
                return response_object.toJson(),403                 

@api.route('/getFile')
class GetFile(Resource):

    @api.doc('Get file')
    @api.expect(_file_info, validate=True)
    
    def post(self):
        """Get File"""

        data = request.json
        if(data is not None):
            _file_infoDto=_file_info
            _file_infoDto.user_id=data['user_id']
            _file_infoDto.guid=data['guid']
            file = getFile(_file_infoDto.user_id,_file_infoDto.guid)
            if(file is not None and file.blob is not None):
                response_object=ResponseDto()
                response_object.data=True,
                response_object.status = ResponseStatus.SUCCESS.value,
                response_object.message = _Messages.FILE_READ_SUCCESS
                response_object.status_code=200      
                return response_object.toJson(),200
