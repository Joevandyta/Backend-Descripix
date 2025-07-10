from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed
class Google:
    """Google class to fetch the user info and return it"""

    @staticmethod
    def validate(auth_token):
        """
        validate method Queries the Google oAUTH2 api to fetch the user info
        """
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, requests.Request())
            print("idinfo: ", idinfo)
            
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                return AuthenticationFailed("Invalid token issuer.")
            
            return idinfo
        except:
            return "The toukan token is either invalid or has expired"