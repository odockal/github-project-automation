# -*- coding: utf-8 -*-
'''
Created on Jan 3, 2019



@author: odockal
'''
import os
import sys
from handler.github_handler import GHApiHandler
from models.issues import Issues
from utils.http_utils import sendHttpPostRequest,\
    decodeHttpResponseAttribute, convertStrToJson, downloadFile,\
    sendDeleteRequest

print("Running {}".format(sys.argv[0]))
print("Passed program arguments: {}".format(sys.argv))

debug=0
overwrite=0
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
            return sendHttpPostRequest(url, params, **kwargs)
        raise err

def main():
    handler = GHApiHandler("{}/../resources/config.ini".format(ROOT_DIR))
    tag = handler.config.getDefaultSection().get('tag') if not None else '2.6.0.RC2'
    version = handler.config.getDefaultSection().get('version') if not None else '2.6.0'
    fileName = handler.config.getDefaultSection().get('fileName') if not None else 'org.eclipse.reddeer-2.6.0.zip'
    header = handler.config.getHeader()
    issues = retrieveIssuesFromMilestone(handler, version)
    MDString = createMarkDownString(issues)
    params = {
        "tag_name": tag,
        "name": version,
        "body": MDString,
        "draft": True,
        "prerelease": False,
    }
    paramsUploadAsset = {
        "content_type": "application/zip"
    }
    contentUrl = handler.config.configuration['DEFAULT'].get('assetUrl')
    dFile = downloadFile(fileName, contentUrl, True)
    try:
        response = createRelease(handler, "{0}/releases".format(handler.config.getUrlAddress()), version, params, headers=header)
    except ValueError as err:
        if overwrite:
            if str(err).__contains__("already exists"):
                print("Deleting existing release - for testing purposes only")
                releaseID = handler.getResponseAttributeValueByKey(handler.getReleases(), 'name', version , 'id')
                sendDeleteRequest("{0}/releases/{1}".format(handler.config.getUrlAddress(), releaseID), headers=header)
                response = createRelease(handler, "{0}/releases".format(handler.config.getUrlAddress()), version, params, headers=header)
            else:
                raise err
        else:
            raise err
    if hasattr(response, 'content'):
        uploadUrl = convertStrToJson(decodeHttpResponseAttribute(response, 'content'))['upload_url']
        print(uploadUrl)
        index = uploadUrl.find("assets", 0, len(uploadUrl))
        print(index)
        url = uploadUrl[:index+len("assets")]
        print(url)
    if uploadUrl:
        if dFile is not None:
            with open(dFile, 'rb') as binary_file:
                pass
                uploadResponse = sendHttpPostRequest("{0}?name={1}".format(url, fileName), params=paramsUploadAsset, headers=header, files={'archive': (fileName, binary_file, 'application/zip')})
                print("Uploading the file returned the status_code: {}".format(uploadResponse.status_code))    

if __name__ == '__main__':
    main()
