'''
Created on Jan 14, 2019

@author: odockal
'''
import os
from utils.http_utils import sendHttpPostRequest

class ReleaseAsset:
    
    assetLocation = None
    assetName = None
    httpParameters = None
    uploadUrl = None
    
    def __init__(self, assetLocation, url, name, files = None, params = None, header = None):
        self.assetLocation = assetLocation
        self.uploadUrl = url
        self.assetName = name
        self.sha265sum = None # TODO
        self.httpParameters.files = files
        self.httpParameters.header = header
        self.httpParameters,params = params
        
    def getAssetLocation(self):
        if os.path.exists(self.assetLocation):
            return self.assetLocation
        else:
            raise FileNotFoundError("File asset location '{}' does not exist".format(self.assetLocation))
        
    def getUrl(self):
        return self.uploadUrl
    
    def getHttpParameters(self):
        return self.httpParameters
    
    def getAssetName(self):
        return self.assetName
    
    def uploadAsset(self):
        with open(self.getAssetLocation(), 'rb') as binary_file:
            parameters = self.getHttpParams()
            uploadResponse = sendHttpPostRequest("{0}?name={1}".format(self.getUrl, 
                                                                       self.getAssetName()), 
                                                                       params=parameters.params, headers=parameters.header, files={'archive': (self.getAssetName(), binary_file, 'application/zip')})
            print("Uploading the file returned the status_code: {}".format(uploadResponse.status_code))        
    
    