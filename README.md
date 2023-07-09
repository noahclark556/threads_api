# META Threads API
## Developed by Noah Clark
### https://qwertycode.org
### Donations at the above URL are very helpful 
### ! This API and its Development/Developer has no affiliation with META in any way !

# Introduction
___

This META Threads API allows the developer to easily pull and manipulate profile information from any Threads profile.

The API also includes AI capability that allows the developer to parse a profile into very readable OSINT information as well as pull out pertinent information from an infinite number of posts.

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
# Usage
___
Step 1. Clone this repository and place the 'threads_api' package in your python project.

Step 2. Import the library into your project:
```python
from threads_api import ThreadsApi
```

Step 3. Initialize the API:
```python
api = ThreadsApi('ANY-THREADS-USERNAME', 'OPENAI-ORGANIZATION', 'OPENAI-API-KEY')
```
_NOTE: If you are not using openAI, fill the openAI parameters with something random_

Step 4. Set the following optional parameters:
```python
api.aiRequestType = 'osint.profile'  # osint.character_prompt || osint.profile || osint.links || osint.mentions

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

print(api.bio)  # return users bio

print(api.name)  # return users name

print(api.posts)  # return posts in array format

print(api.links)  # return links, also includes mentions
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

```

# Other Notes
___
It should be mentioned that if the Selenium driver fails to pull profile data, you can do a few things to fix it. You can either increase the pageLoadWaitTime variable or edit the 'tag_references.py' and ensure they point to the correct paths.