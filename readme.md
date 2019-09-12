Code Format :
Methods : testMethod
Property-class :test_property
Property-py:_test_property
Class:TestClass
Constants:TEST_CONSTANT
Enums:TESTING_ENUM


Before running this following environment variables needs to be set first.
    'SIB_ENV' possible values are 'dev', 'test', 'prod'. The default that will be used is 'dev'
    'SIB_SECRET_KEY' any random string value.

In order to run the project run following command.
    py manage.py run

For all the db related command run following
    py manage.py db 'the db command'
in above command replace 'the db command' with your respective command.



// Command to create the new virtual enviornment
py -m venv venv


// Command to install all the dependencies from the text files to virtual enviornment.
pip install -r requirement.txt


// Command to add the dependencies in requirement.txt file after adding new package.
pip freeze > requirement.txt


// Command of Migrations
python manage.py db init 
python manage.py db migrate -m "Name of migration"
python manage.py db upgrade