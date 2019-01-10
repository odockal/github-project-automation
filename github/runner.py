# -*- coding: utf-8 -*-
'''
Created on Jan 3, 2019



@author: odockal
'''
import os
import sys
from github.handler.github_handler import GHApiHandler
from github.issues import Issues

print("Running {}".format(sys.argv[0]))

debug=0
version = '2.4.0'
tag = '2.4.0.RC1'
labelList = ('bug', 'enhancement', 'feature', 'task', 'doc')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def printPartInMarkDown(issues):
    print(createMarkDownString(issues))
            
def createMarkDownString(issues):
    output = str("")
    for key in issues:
        output += f"## {key}\r\n"
        for item in issues[key]:
            output += f"#{item['number']} - {item['title']}\r\n"
    return output

def retrieveIssuesFromMilestone(handler, milestone):
    params = (
        ('per_page', '100/'),
        ('milestone', '{}/'.format(handler.getMilestoneNumberByTitle(milestone))),
        ('state', 'closed'),
    )
    issuesObj = Issues(handler)
    
    issuesResponse = handler.getIssues("{}/issues".format(handler.config.getUrlAddress()), 
                                       params=params, 
                                       headers=handler.config.getHeader())
    
    issues = issuesObj.getIssues(issuesResponse.json())
    return issues

def createRelease(handler, url, version, params=None, **kwargs):
    try:
        handler.getResponseAttributeValueByKey(handler.getReleases(), 'name', version , 'id')
        raise ValueError("Release {} already exists".format(version))
    except ValueError as err:
        if str(err).__contains__("does not exist"):
            return handler.sendPostRequest(url, 200, params, **kwargs)
        raise err

if __name__ == '__main__':
    handler = GHApiHandler("{}/resources/config.ini".format(ROOT_DIR))
    issues = retrieveIssuesFromMilestone(handler, version)
    MDString = createMarkDownString(issues)
    # releases = handler.getReleases()
    # releaseID = handler.getResponseAttributeValueByKey(releases, 'name', version , 'id')
    # release = handler.sendRequestGetResponse("{0}/releases/{1}".format(handler.config.getUrlAddress(), releaseID), headers=handler.config.getHeader())
    # print(release.json()['body'])
    params = {
        "tag_name": tag,
        "name": version,
        "body": MDString,
        "draft": True,
        "prerelease": False,
    }
    response = createRelease(handler, "{0}/releases".format(handler.config.getUrlAddress()), version, params, headers=handler.config.getHeader())
    print(response.json())
    pass