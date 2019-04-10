# -*- coding: utf-8 -*-
'''
Created on Jan 9, 2019

@author: odockal
'''

import requests
import json
import sys
import os.path
from builtins import getattr

debug = 0

def Print(string):
    if debug:
        print(string)
        
def sendHttpGetRequest(url, params=None, **kwargs):
    httpResponse = requests.get(url, params=params, **kwargs)
    httpResponse.raise_for_status()
    return httpResponse

def sendHttpPostRequest(url, params=None, **kwargs):
    httpResponse = requests.post(url, json=params, **kwargs)
    httpResponse.raise_for_status()
    return httpResponse

def sendDeleteRequest(url, params=None, **kwargs):
    httpResponse = requests.delete(url, params=params, **kwargs)
    httpResponse.raise_for_status()
    return httpResponse

def downloadFile(filename, url, overwriteLocally=False, params=None, **kwargs):
    contentResponse = sendHttpGetRequest(url, params=params, **kwargs)
    data = None
    if hasattr(contentResponse, 'content'):
        data = contentResponse.content
    if not os.path.exists(filename) or overwriteLocally:
        with open(filename, "wb") as binaryFile:
            binaryFile.write(data)
        return filename
    else:
        raise Exception("File '{}' already exists, wont overwrite it".format(filename))
    raise Exception("File was not downloaded properly")
    
def decodeHttpResponseAttribute(httpObject, attribute):
    if hasattr(httpObject, attribute):
        return getattr(httpObject, attribute).decode('UTF-8')
    else:
        raise NameError(f"HTTP response object does not have attribute with name {attribute}")
            
def convertStrToJson(chain):
    if isinstance(chain, (str)):
        try:
            jsonObj = json.loads(chain)
            return jsonObj
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
    else:
        raise ValueError('Given object {} is not a string'.format(chain))
    
def testHttpResponse(response, expectedStatusCodeCategory):
    category = str(expectedStatusCodeCategory)[:1]
    if str(response.status_code)[:1] is not category:
        content = decodeHttpResponseAttribute(response, 'content')
        message = convertStrToJson(content)['message']
        raise ValueError(u"Http response to '{1}' is '{0}' with message: '{2}'".format(response.status_code, response.url, message)) 