# -*- coding: utf-8 -*-
'''
Created on Jan 9, 2019

@author: odockal
'''

from enum import Enum
from builtins import staticmethod

class Labels(Enum):
    BUG = 0
    FEATURE = 1
    ENHANCEMENT = 2
    TASK = 3
    DOC = 4
    OTHER = 5
    
    @staticmethod
    def list():
        return list(map(lambda c: c.name.lower(), Labels))
    
    def __str__(self):
        return str(self.name()).lower()
    
    @staticmethod
    def isIn(toCompare):
        for enum_item in list():
            if toCompare.lower().equal(enum_item.lower()):
                return True
        return False
    
    @staticmethod
    def categorize(label):
        if label.lower() == Labels.BUG.name.lower():
            return 'Bugs'
        elif label.lower() in [obj.name.lower() for obj in [Labels.FEATURE, Labels.ENHANCEMENT]]:
            return 'Features'
        elif label.lower() == Labels.TASK.name.lower():
            return 'Tasks'
        else:
            return 'Others'