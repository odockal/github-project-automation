# github-project-automation
### Python project for github release automation

Is uses GitHub REST API v3 to communicate with github. It is tailored to create new release for github project with list of resolved issues for particular milestone. 

These information has to be set up in resources/config.ini file, some other resources are hard coded so far. This should change in future to be fully configurable. Also, future version should be using GitHub GraphQL API v4.

### Requirements
* Python 3.7

### Usage
Simply fork the project, get the content to your disk with
		
	git clone https://github.com/user/github-project-automation.git
	
Now you have to configure resources/config.ini file, you need to set your repository owner, project name and milestone it aim to build, also you can provide url of binary or archive you want to upload for that release. Then,
	
	cd github-project-automation
	
	python3 github/main.py

It produces new release for given owner/repo and also uses hard coded file name and tag defined in `main.py`. Should be changed in future.
 
