def constant(f):
    def fset(self, value):
        raise TypeError('constant: field is constant')
    def fget(self):
        return f()
    return property(fget, fset)




class _Messages(object):

    @constant
    def FORGOT_PASS_REQUEST_PROCESS_SUCCESS():
        return 'Forgot Password request processed successfully.'

    @constant
    def FORGOT_PASS_REQUEST_PROCESS_FAIL():
        return 'Invalid username/email.'    

    @constant
    def VALID_TOKEN():
        return 'Valid Token.'  

    @constant
    def INVALID_TOKEN():
        return 'Invalid or expired Token.'   

    @constant
    def RESET_PASSWORD_SUCCESS():
        return 'Password Reset Successfully.'

    @constant
    def REGISTERED_SUCCESS():
        return 'Successfully registered.'

    @constant
    def USERNAME_ALREADY_EXISTS():
        return 'Username already exists.'

    @constant
    def EMAIL_ALREADY_EXISTS():
        return 'Email already exists.'    

    @constant
    def FILE_NOT_FOUND():
        return 'File not found.'    

    @constant
    def FILE_UPLOADED_SUCCESS():
        return 'File uploaded successfully.'

    @constant
    def FILE_UPLOADED_FAIL():
        return 'An error occured during file uploading.'

    @constant
    def NO_SELECTED_FILE():
        return 'No selected file.'    

    @constant
    def ERROR_IN_FILE_READING():
        return 'An error occured in reading file.'

    @constant
    def INVALID_FILE_ACCESS_MODE():
        return 'Invalid file access mode.'

    @constant
    def ERROR_IN_FILE_WRITING():
        return 'An error occured in writing file.'    

    @constant
    def FILE_READ_SUCCESS():
        return 'File read successfully.'    

class _GlobalSettings(object):
    @constant
    def MAX_COOKIE_TIME():
        return 3000

    
    @constant
    def DEFAULT_PASSWORD():
        return '1234'



Messages = _Messages()
GlobalSettings=_GlobalSettings()