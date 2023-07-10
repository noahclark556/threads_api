# -----------------------
# Developed by Noah Clark
# https://qwertycode.org
# July 9, 2023
# Enjoy!
# -----------------------

import time
from bs4 import BeautifulSoup
from selenium import webdriver
from threads_api.profile_object import Profile
from threads_api.tag_references import TagReferences
from selenium.webdriver import ChromeOptions
from ast import literal_eval
import os
import openai


class ThreadsApi:

    def __init__(self, userId, openAIOrg, openAIKey, statusPrintingEnabled=True):
        self.openAIOrg = openAIOrg
        self.openAIKey = openAIKey
        self.statusPrintingEnabled = statusPrintingEnabled
        self.aiRequestType = 'osint.character_prompt'
        self.maxPosts = 10
        self.profile = userId
        self.pageLoadWaitTime = 5
        self.gptModel = 'gpt-4' # gpt-4 or gpt-3.5-turbo recommended
        self.usingAI = True
        self.posts = []
        self.links = []
        self.bio = ''
        self.name = ''
        self.userId = ''
        self.followers = ''
        self.linkedInstagram = ''
        self.aiResponse = ''

        openai.organization = self.openAIOrg
        openai.api_key = self.openAIKey

    def getType(self, user_profile):
        request = []
        if self.aiRequestType == 'osint.character_prompt':
            request = [
                {"role": "system",
                 "content": "You are going to receive some information from a Meta Threads profile. The posts will be shown to you in an array. Using this information, build a character prompt that best describes the individual who owns this profile. Only return the character prompt, do not include anything else such as intros or leading sentences."},
                {"role": "user",
                 "content": f"Users name: {user_profile.name}. Users bio {user_profile.bio}. Users posts: {user_profile.posts}"}
            ]
        elif self.aiRequestType == 'osint.profile':
            request = [
                {"role": "system",
                 "content": "You are going to receive some information from a Meta Threads profile. The posts will be shown to you in an array. Using this information, build a brief bulleted summary of the individual who owns this profile. Include all important information used for OSINT. Such as birthday, location, age, ethnicity and anything else you can find."},
                {"role": "user",
                 "content": f"Users name: {user_profile.name}. Users bio {user_profile.bio}. Users posts: {user_profile.posts}"}
            ]
        elif self.aiRequestType == 'osint.links':
            request = [
                {"role": "system",
                 "content": "You are going to receive some information from a Meta Threads profile. The posts will be shown to you in an array. Using this information, return all mentioned links to other webpages in an array format."},
                {"role": "user",
                 "content": f"Users name: {user_profile.name}. Users bio {user_profile.bio}. Users posts: {user_profile.links}"}
            ]
        elif self.aiRequestType == 'osint.mentions':
            request = [
                {"role": "system",
                 "content": "You are going to receive some information from a Meta Threads profile. The posts will be shown to you in an array. Using this information, return all mentions of other accounts. Other accounts are normally mentioned using a @ symbol. Return this information in array format."},
                {"role": "user",
                 "content": f"Users name: {user_profile.name}. Users bio {user_profile.bio}. Users posts: {user_profile.links}"}
            ]
        return request

    def startAi(self, user_profile):
        if user_profile.name != 'N/A' and user_profile.bio != 'N/A':
            request = self.getType(user_profile)
            response = openai.ChatCompletion.create(
                model=self.gptModel,
                messages=request
            )
            if self.aiRequestType == 'osint.links' or self.aiRequestType == 'osint.mentions':
                return literal_eval(response.choices[0].message.content)
            return response.choices[0].message.content
        else:
            if self.statusPrintingEnabled:
                print("Unable to locate profile information. Try increasing the pageLoadWaitTime.")
            return "N/A"

    def getUserId(self, soup):
        soupStr = str(soup)
        startIndex = soupStr.find('"user_id"') + 11
        i = 0
        newId = ""
        while i < 30:
            if soupStr[startIndex + i].isdigit():
                newId += soupStr[startIndex + i]
            else:
                break
            i += 1
        return newId

    def parsePageData(self, soup):
        # dom = etree.HTML(str(soup))
        # self.name = dom.xpath(TagReferences().name)[0].text
        try:
            self.name = soup.select_one(TagReferences().name).text
        except Exception:
            self.name = 'N/A'
        # self.bio = dom.xpath(TagReferences().bio)[0].text
        try:
            self.bio = soup.select_one(TagReferences().bio).text
        except Exception:
            self.bio = 'N/A'

        try:
            self.followers = soup.select_one(TagReferences().followers).text
        except Exception:
            self.followers = 'N/A'

        try:
            self.linkedInstagram = soup.select_one(TagReferences().linkedInstagram)['href']
        except Exception:
            self.linkedInstagram = 'N/A'

        try:
            self.userId = self.getUserId(soup)
        except Exception:
            self.userId = 'N/A'

        if self.name == 'N/A' and self.bio == 'N/A':
            if self.statusPrintingEnabled:
                print("Unable to locate profile information. Try increasing the pageLoadWaitTime.")

        # try:
        posts = soup.select(TagReferences().posts)
        links = soup.select(TagReferences().links)
        # except Exception:
        #     posts = ['None']

        counter = 0
        for post in posts:
            if counter >= self.maxPosts:
                break
            self.posts.append(post.text)
            counter += 1

        counter = 0
        for link in links:
            if counter >= self.maxPosts:
                break
            self.links.append(link.text)
            counter += 1

        return Profile(self.name, self.bio, self.posts, self.links)

    def getSoup(self, url):
        options = ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--incognito')
        options.add_argument('--ignore-certificate-errors')
        browser = webdriver.Chrome(options)
        browser.get(url)
        time.sleep(self.pageLoadWaitTime)
        html = browser.page_source
        return BeautifulSoup(html, "html.parser")

    def start(self):
        os.system('clear')
        if self.statusPrintingEnabled:
            print("Donations to development are greatly appreciated and are very helpful, please visit https://qwertycode.org to donate.\n")
            print("To disable this message and all others, set statusPrintingEnabled=False in the inital API instance. This will disable some error messages. \n\n")
        if self.statusPrintingEnabled:
            print("Please wait, executing API functions..")
        soup = self.getSoup(f"https://www.threads.net/@{self.profile}")
        user_profile = self.parsePageData(soup)
        if self.usingAI:
            self.aiResponse = self.startAi(user_profile)
        else:
            self.aiResponse = "api.usingAI is set to false. Please set this to true to enable AI, otherwise the openAI request will be skipped."
