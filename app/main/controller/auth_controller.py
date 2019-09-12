from flask import request,make_response
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.dto import AuthDto
from ..service.auth_service import login,logout,forgotPassword,verifyToken,resetPassword

api = AuthDto.api
_login = AuthDto.login
_password_request = AuthDto.password_request
_reset_password=AuthDto.reset_password

@api.route('/login')
class Login(Resource):
    @api.doc('user_login')
    @api.expect(_login, validate=True)
    def post(self):
        """Verify valid login details"""

        if(request.json is not None):
            data = request.json
            _loginDto=_login
            _loginDto.email=data['email']
            _loginDto.username=data['username']
            _loginDto.password=data['password']            
            return login(_loginDto)
   

@api.route('/logout')
class Logout(Resource):
    @api.doc('user_logout')     
    def post(self):
        """User Logout from Api"""

        return logout()


@api.route('/checkAuth')
class Authentication(Resource):

    @jwt_required
    def get(self):
        """Check Authentication"""

        return make_response()   


@api.route('/forgetPassword')
@api.expect(_password_request, validate=True)
class ForgetPassword(Resource):          
    def post(self):
        """Forget Password"""
        data=request.json
        if(data is not None):
           _forgot_passwordDto=_password_request
           _forgot_passwordDto.email=data['email']
           _forgot_passwordDto.username=data['username']
           
           response_dto = forgotPassword(_forgot_passwordDto)                      
           return  response_dto.toJson(), response_dto.status_code



@api.route('/resetPassword')
@api.expect(_reset_password, validate=True)
class ResetPassword(Resource):

    def post(self):
        """Reset Password"""
        data = request.json
        if(data is not None):
            _reset_passwordDto=_reset_password
            _reset_passwordDto.token=data['token']
            _reset_passwordDto.new_password=data['new_password']
            
            response_dto = resetPassword(_reset_passwordDto)
            return response_dto.toJson(), response_dto.status_code     


@api.route('/verifyToken/<token>')
@api.param('token', '')
@api.response(404, 'Token not found.')
class VerifyToken(Resource):

    def get(self,token):
        """Verify Token before reseting password"""         
        if(token is not None):
           response_dto = verifyToken(token)
           return response_dto.toJson(), response_dto.status_code
                   


    