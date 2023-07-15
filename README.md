# META Threads API
## Developed by Noah Clark
### https://qwertycode.org
### Donations at the above URL are very helpful 
### ! This API and its Development/Developer has no affiliation with META in any way !

# Introduction
___

This META Threads API allows the developer to easily pull and manipulate profile information from any Threads profile.

The API also includes AI capability that allows the developer to parse a profile into very readable OSINT information as well as pull out pertinent information from an infinite number of posts.

A demo video is located here: https://youtu.be/55a9mEaP-ao

# Requirements
___

'Selenium' is used in this package. Please ensure you have Chrome installed, if you do not want to install Chrome, you can adjust the API code to use a web driver executable. The code to adjust would be located in 'threads_api.py' under the getSoup function.

Please execute the following pip installs:
```python
pip install beautifulsoup4
pip install selenium
pip install openai
```
In order to use AI functions, you will need to get an OpenAI API Key as well as an OpenAI organization identifier. Although AI is not a requirement to use this package.

# Change Notes
___

### July 15, 2023 @ 5:00 PM (update)
- AI credentials are no longer a required parameter. Use api.openAIOrg="YOUR-ORG" and api.openAIKey="YOUR_KEY" to enable AI capability
- These values are required to use AI. An error will be returned if they are not set and api.usingAI is set to True

### July 15, 2023 @ 4:45 PM (update)
- api.replies() has been added, retrieve all replies from account
- api.replyLinks() has been added, retrieve all links from all replies on account

### July 9, 2023 @ 6:45 PM (update)
- Update pushed to github, developers can now retrieve the url of the account owners instagram account using 'api.linkedInstagram'
- Fixed 'api.name' issues. Only the name is now returned, rather than the entire title

### July 9, 2023 @ 6:30 PM (update)
- Update pushed to github, developers can now retrieve the numeric user_id variable from selected profiles using 'api.userId'

### July 9, 2023 @ 10:00 AM (release)
- Package published to github with described capability

### July 8, 2023 (prep)
- Initial package finalized and prepped for release

# Usage
___
Step 1. Clone this repository and place the 'threads_api' package in your python project.

Step 2. Import the library into your project:
```python
from threads_api import ThreadsApi
```

Step 3. Initialize the API:
```python
api = ThreadsApi('ANY-THREADS-USERNAME')
```
_NOTE: If you are not using openAI, fill the openAI parameters with something random_

Step 4. Set the following optional parameters:
```python
api.aiRequestType = 'osint.profile'  # osint.character_prompt || osint.profile || osint.links || osint.mentions

api.openAIOrg = 'OPENAI-ORGANIZATION' # your OpenAI Api organization identifier

api.openAIKey = 'OPENAI-API-KEY' # your OpenAI Api Key 

api.gptModel = 'gpt-4'  # 'gpt-4' or 'gpt-3.5-turbo' recommended

api.maxPosts = 50  # max number of posts to scrape

api.pageLoadWaitTime = 3  # time to wait for page to load (change according to internet speed)

api.usingAI = True  # set to False to completely skip AI functionality

api.statusPrintingEnabled = True  # set to False to disable print statements from API

```

Step 5. Start the execution process:
```python
api.start()
```

Step 6. Retrieve and manipulate the API data:
```python
print(api.aiResponse)  # return AI request response

print(api.userId)  # return numeric user_id of account

print(api.bio)  # return users bio

print(api.name)  # return users name

print(api.posts)  # return posts in array format

print(api.links)  # return links, also includes mentions

print(api.linkedInstagram)  # return linked instagram account url

print(api.replies)  # return all replies

print(api.replyLinks)  # return all links contained in replies

print(api.followers)  # return follower count
```

Final product should look like this:
```python
from threads_api.threads_api import ThreadsApi

api = ThreadsApi('THREADS-USERNAME', 'OPENAI-ORGANIZATION', 'OPENAI-API-KEY')

api.aiRequestType = 'osint.profile'  # osint.character_prompt || osint.profile || osint.links || osint.mentions

api.gptModel = 'gpt-4'  # 'gpt-4' or 'gpt-3.5-turbo' recommended

api.maxPosts = 50  # max number of posts to scrape

api.pageLoadWaitTime = 3  # time to wait for page to load (change according to internet speed)

api.usingAI = True  # set to False to completely skip AI functionality

api.statusPrintingEnabled = True  # set to False to disable print statements from API


api.start()


print(api.aiResponse)  # return AI request response

print(api.bio)  # return users bio

print(api.name)  # return users name

print(api.posts)  # return posts in array format

print(api.links)  # return links, also includes mentions

print(api.linkedInstagram)  # return linked instagram account url

print(api.replies)  # return all replies

print(api.replyLinks)  # return all links contained in replies

print(api.followers)  # return follower count
```

# Other Notes
___
It should be mentioned that if the Selenium driver fails to pull profile data, you can do a few things to fix it. You can either increase the pageLoadWaitTime variable or edit the 'tag_references.py' and ensure they point to the correct paths.