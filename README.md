# github-project-automation
### Python project for github release automation

Application uses GitHub REST API v3 to communicate with github. It is tailored to create new release for github project with list of resolved issues for particular milestone. 

These information has to be set up in resources/config.ini file, some other resources are hard coded so far. This should change in future to be fully configurable. Also, future version should be using GitHub GraphQL API v4.

### Requirements
* Python 3.7

### Usage
Simply fork the project, get the content to your disk with
		
	git clone https://github.com/user/github-project-automation.git
	
Now you have to configure resources/config.ini file, you need to set your repository owner, repository or project name, version or milestone, tag and filename of the asset you want to upload for that release. Then,
	
	cd github-project-automation
	
	python3 src/main.py

It produces new release draft for given owner/repo, uploads the artifacts, creates a list of issues based on labels bug, task, enhancement, feature and doc.
 
