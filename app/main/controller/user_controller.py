import json,os

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.dto import ResponseDto,UserDto,User
from ..service.user_service import saveNewUser, getAllUsers, getSingleUser,saveNewUsers
from ..service.file_service import saveFile,getFile,writeFile,readFile
from ..util.constants import Messages,GlobalSettings
from ..util.enums import ResponseStatus
from ..util.enums import FileAccessMode

from ..util import parsers
from ..util.parsers import CsvFileParser

from ..config import NetworkPath

api = UserDto.api
_user = UserDto.user 
_Global_Settings = GlobalSettings
_Messages=Messages


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    @jwt_required
    def get(self):
        """List all registered users"""
        return getAllUsers()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Register a new User """
        data = request.json
        if(data is not None):
            _userDto=_user
            _userDto.first_name=data['first_name']
            _userDto.last_name=data['last_name']
            _userDto.email=data['email']
            _userDto.username=data['username']
            _userDto.password=data['password']

            _userDto.created_by=data['username']
            _userDto.user_type=data['user_type']            
            _userDto.address1=data['address1']
            _userDto.address2=data['address2']
            _userDto.country=data['country']
            _userDto.state=data['state']
            _userDto.zip_code=data['zip_code']
            _userDto.provider_id=data['provider_id']
            _userDto.stakeholder_id=data['stakeholder_id']

            response_dto = saveNewUser(_userDto)            
            return  response_dto.toJson(), response_dto.status_code           
             


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = getSingleUser(public_id)
        if not user:
            api.abort(404)
        else:
            return user


@api.route('/registerUsers')
class RegisterUsers(Resource):

    @api.doc('users')
    @api.expect(parsers.file_upload, validate=True)
    
    def post(self):
        """Register users"""

        if request.files is None or 'file' not in request.files:
            #No file found
            response_object=ResponseDto()
            response_object.data=False,
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
                response_object=response[0]
                guid = response[1]
                if(response_object is not None and response_object.status_code == 200):
                    fileInfoData = json.loads(args['data'])                    
                    user_id =fileInfoData['user_id']
                    stakeholder_id = 0
                    provider_id = 0
                    created_by = ''
                    user_type=2

                    fileInfo = getFile(user_id , guid)
                    writeFile(fileInfo,NetworkPath,FileAccessMode.WRITE_ONLY_BINARY_MODE)                     
                    parsedData = CsvFileParser.parse(os.path.join(NetworkPath,file.filename))
                    users = []
                    if(parsedData is not None):
                        for row in parsedData.rows:                     
                            _user = User()
                            _user.first_name=row['First Name']
                            _user.last_name=row['Last Name']
                            _user.email=row['E-mail']
                            _user.address1 = row['Address1']
                            _user.address2 = row['Address2']
                            _user.country = row['Country']
                            _user.state = row['State']
                            _user.zip_code = row['Zip Code']
                            _user.password=_Global_Settings.DEFAULT_PASSWORD
                            _user.username=str.lower(_user.first_name)+'_'+str.lower(_user.last_name)                      
                            _user.created_by=created_by
                            _user.user_type = user_type
                            _user.provider_id = provider_id
                            _user.stakeholder_id = stakeholder_id

                            users.append(_user)

                        duplicate_users = saveNewUsers(users)

                else:
                        #No selected file
                        response_object=ResponseDto()
                        response_object.data=False,
                        response_object.status = ResponseStatus.FAIL.value,
                        response_object.message = _Messages.NO_SELECTED_FILE
                        response_object.status_code=403      
                        return response_object.toJson(),403                        