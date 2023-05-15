from app import create_app
from os import getenv

"""The way Flask works the application needs to be instantiated outside the main block"""
app = create_app(getenv('ENVIRONMENT'))

if __name__ == '__main__':  
    app.run()