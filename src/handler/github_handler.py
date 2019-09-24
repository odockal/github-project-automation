# -*- coding: utf-8 -*-
'''
Created on Jan 10, 2019

@author: odockal
'''

from config.app_config import AppConfig
from models.assets import ReleaseAsset
from utils.http_utils import sendHttpGetRequest, convertStrToJson, decodeHttpResponseAttribute, sendHttpPostRequest



class GHApiHandler:
    
    config = None
    
    def __init__(self, filename):
        self.config = AppConfig(filename)
        
    def getMilestones(self):
        return sendHttpGetRequest("{url}/milestones".format(url=self.config.getUrlAddress()), 
                                           params = (('state', 'all'),), 
                                           headers=self.config.getHeader())
    
    def getReleases(self):
        return sendHttpGetRequest("{}/releases".format(self.config.getUrlAddress()), 
                                              headers=self.config.getHeader())
    
    def getMilestoneNumberByTitle(self, title):
        milestones = self.getMilestones()
        for item in milestones.json():
            if item['title'] == title and item is not None:
                return item['number']
        else:
            raise ValueError(f"Given milestone title: '{title}' does not exist")
        
    def getResponseAttributeValueByKey(self, httpResponse, key, value, attribute):
        jsonData = httpResponse.json()
        for item in jsonData:
            if key in item and item.get(key) == value and item is not None:
                return item.get(attribute)
        else:
            raise ValueError(f"Given key: '{key}' with value: '{value}' does not exist")        
        
    
    def getReleaseUploadUrl(self, httpResponse):
        if hasattr(httpResponse, 'content'):
            uploadUrl = convertStrToJson(decodeHttpResponseAttribute(httpResponse, 'content'))['upload_url']
            index = uploadUrl.find("assets", 0, len(uploadUrl))
            url = uploadUrl[:index+len("assets")]
            return url
    
    def uploadReleaseAssets(self, assets):
        for asset in assets:
            with open(asset.getAssetLocation(), 'rb') as binary_file:
                parameters = asset.getHttpParams()
                uploadResponse = sendHttpPostRequest("{0}?name={1}".format(asset.getUrl, 
                                                                           asset.getAssetName()), 
                                                                           params=parameters.params, headers=parameters.header, files={'archive': (asset.getAssetName(), binary_file, 'application/zip')})
                print("Uploading the file returned the status_code: {}".format(uploadResponse.status_code)) 
        
    def getIssues(self, url, params, **kwargs):
        return sendHttpGetRequest(url, params, **kwargs)
        