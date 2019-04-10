# -*- coding: utf-8 -*-
'''
Created on Jan 9, 2019

@author: odockal
'''

from _collections import OrderedDict
from models.labels import Labels
from utils.http_utils import Print, sendHttpGetRequest

class Issues:
    
    issues = None
    handler = None
    
    def __init__(self, handler):
        self.handler = handler
        
    def inicializeDict(self):
        self.issues = OrderedDict([('Bugs', []),
                      ('Features', []),
                      ('Tasks', []),
                      ('Others', [])])
        
    def loadIssue(self, label, issue):
        self.issues.get(Labels.categorize(label)).append(issue)
        
    def processIssues(self, jsonData):
        for item in jsonData:
            Print("Processing {}".format(item['number']))
            prs = []
            if 'pull_request' in item:
                Print('This issue is PR: {}'.format(item['number']))
                prs.append(item)
                continue
            labels = sendHttpGetRequest("{0}/labels".format(item['url']), headers=self.handler.config.getHeader())
            labelData = labels.json()
            if len(labelData) > 0:
                for label in labelData:
                    if label['name'] in Labels.list():
                        self.loadIssue(label['name'], item)
            else:
                self.loadIssue('Others', item)
                
    def getIssues(self, jsonRawData):
        if self.issues is None:
            self.inicializeDict()
            self.processIssues(jsonRawData)
        return self.issues
    
