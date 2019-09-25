'''
Created on Jan 14, 2019

@author: odockal
'''
import configparser

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
    
    def getDefaultSection(self):
        return self.configuration['DEFAULT']
    
    def getConfiguration(self):
        return self.configuration
    
    def getUrlAddress(self):
        return self.urlAddress
    
    def getHeader(self):
        return self.header