import uuid
import datetime

from app.main import db
from ..util.dto import ResponseDto
from ..util.enums import ResponseStatus
from ..util.constants import Messages,GlobalSettings

from flask import make_response,abort
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, set_access_cookies, unset_jwt_cookies)
from ..service.user_service import saveNewUser, getAllUsers, getSingleUser, getUserByEmail,getUserById,getUserByUsername
from app.main.model.password_requests import PasswordRequests
from app.main.model.file_info import FileInfo

_Messages=Messages
_Global_Settings=GlobalSettings

def login(loginDto):
    users = getAllUsers()
    isAuthenticated = False
    access_token = ''
    for user in users:
        if(user is not None and ((user.email == loginDto.email or user.username == loginDto.username ) and user.check_password(loginDto.password)==True)):
            isAuthenticated=True
            access_token=create_access_token(identity=loginDto.email)
            break

    if(isAuthenticated):
        return setCookie(token=access_token)    

    else:
        return abort(401)
    

def logout():
    return deleteCookie()

def forgotPassword(forgotPasswordDto):
    user=getUserByEmail(forgotPasswordDto.email)
    if(user is None):
        user=getUserByUsername(forgotPasswordDto.username)

    if(user is not None):
        forgot_password=PasswordRequests(
            token=str(uuid.uuid4()),
            created_on=datetime.datetime.utcnow(),
            user_id=user.id)
        saveChanges(forgot_password)

        response_object=ResponseDto()
        response_object.data=True,
        response_object.status = ResponseStatus.SUCCESS.value,
        response_object.message = _Messages.FORGOT_PASS_REQUEST_PROCESS_SUCCESS
        response_object.status_code=200       
        return response_object
    else:
        response_object=ResponseDto()
        response_object.data=False,
        response_object.status = ResponseStatus.FAIL.value,
        response_object.message = _Messages.FORGOT_PASS_REQUEST_PROCESS_FAIL 
        response_object.status_code=403       
        return response_object     
        

def verifyToken(token):
    password_req = PasswordRequests.query.filter_by(token=token).first()
    if(password_req is not None):
        response_object=ResponseDto()
        response_object.data=True,
        response_object.status = ResponseStatus.SUCCESS.value,
        response_object.message = _Messages.VALID_TOKEN 
        response_object.status_code=200       
        return response_object

    else:
        response_object=ResponseDto()
        response_object.data=False,
        response_object.status = ResponseStatus.FAIL.value,
        response_object.message = _Messages.INVALID_TOKEN  
        response_object.status_code=403       
        return response_object        
            

def resetPassword(resetPasswordDto):
    password_req = PasswordRequests.query.filter_by(token=resetPasswordDto.token).first()
    if(password_req is not None):         
        user = getUserById(password_req.user_id)
        user.password = resetPasswordDto.new_password
        user.modified_on = datetime.datetime.utcnow()
        user.modified_by = user.username       
        password_req.token = None
                 
        db.session.commit()

        response_object=ResponseDto()
        response_object.data=True,
        response_object.status = ResponseStatus.SUCCESS.value,
        response_object.message = _Messages.RESET_PASSWORD_SUCCESS  
        response_object.status_code=200       
        return response_object

    else:
        response_object=ResponseDto()
        response_object.data=False,
        response_object.status = ResponseStatus.FAIL.value,
        response_object.message = _Messages.INVALID_TOKEN  
        response_object.status_code=403       
        return response_object            


def deleteCookie():
    resp = make_response()
    unset_jwt_cookies(resp)
    return resp

def setCookie(token):
    resp=make_response()
    set_access_cookies(resp,token,max_age=_Global_Settings.MAX_COOKIE_TIME)
    return resp

def saveChanges(data):
    db.session.add(data)
    db.session.commit()
    return data  