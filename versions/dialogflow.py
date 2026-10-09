# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 18:26:54 2022

@author: laksh
"""

import os
# os.environ["Google_Application_Credentials"] = "path_of.json"   # Which is obtain after the service account is created on the google cloud

import dialogflow_v2 as dialogflow

dialogflow_session_client = dialogflow.SessionClient()
project_id = "newsextractor-tjiy"


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(text = text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result


response = detect_intent_from_text("Tell me business news of India", 176237)

#To print the name of intent created for bot on Dialogflow
response.intent.display_name

#Printing the tags it detected for the passed query
dict(response.parameters)


def get_reply(query, chat_id):
    response = detect_intent_from_text(query, chat_id)
    
    if response.intent.display_name == 'get_news':  #get_news is the Intent name that we created on Dialogflow for our chatbot
        return "get_news", dict(response.parameters)
    else:
        return "small_talk", response.fulfillment_text
    
#%% Fetching news

from gnewsclient import gnewsclient
client = gnewsclient.NewsClient()

def fetch_news(parameters):
    client.location = parameters.get('geo-country')
    client.language = parameters.get('language')
    client.topic = parameters.get('topic')
    
    return client.get_news()
    