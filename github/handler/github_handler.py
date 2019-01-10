# -*- coding: utf-8 -*-
'''
Created on Jan 10, 2019

@author: odockal
'''

import configparser
from github.utils.http_utils import sendHttpGetRequest, testHttpResponse, sendHttpPostRequest

class AppConfig:
    
    configuration = None
    urlAddress = None
    header = None
    
    def __init__(self, fileName):
        self.configuration = self.readConfigFile(fileName)
        default = self.configuration['DEFAULT']
        baseUrl = default.get('baseUrlAddress')
        owner = default.get('owner')
        repository = default.get('repository')
        self.urlAddress = u"{0}/{1}/{2}".format(baseUrl, owner, repository)
        authentication = None
        if 'AUTHENTICATION' in self.configuration:
            authentication = self.configuration['AUTHENTICATION']
        self.header = {'Authorization': "token {}".format(authentication.get('token'))} 
    
    def readConfigFile(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
        return config
    
    def getConfiguration(self):
        return self.configuration
    
    def getUrlAddress(self):
        return self.urlAddress
    
    def getHeader(self):
        return self.header

class GHApiHandler:
    
    config = None
    
    def __init__(self, filename):
        self.config = AppConfig(filename)
        
    def getMilestones(self):
        return self.sendGetRequest("{url}/milestones".format(url=self.config.getUrlAddress()), 
                                           params = (('state', 'all'),), 
                                           headers=self.config.getHeader())
    
    def getReleases(self):
        return self.sendGetRequest("{}/releases".format(self.config.getUrlAddress()), 
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
        
    def sendGetRequest(self, url, status=None, params=None, **kwargs):
        response = sendHttpGetRequest(url, params, **kwargs)
        status_code = 200 if status is None else status
        testHttpResponse(response, status_code)
        return response
    
    def sendPostRequest(self, url, status=None, params=None, **kwargs):
        response = sendHttpPostRequest(url, params, **kwargs)
        status_code = 200 if status is None else status
        testHttpResponse(response, status_code)
        return response
        
    def getIssues(self, url, params, **kwargs):
        return self.sendGetRequest(url, 200, params, **kwargs)
        