# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 18:59:47 2022

@author: laksh
"""

from gnewsclient import gnewsclient

client = gnewsclient.NewsClient()

#See the default configurations
print(client.get_config())

#>>> {'location': 'United States', 'language': 'english', 'topic': 'Top Stories'}

#Default topics
print(client.topics)
#>>> ['Top Stories', 'World', 'Nation', 'Business', 'Technology', 'Entertainment', 'Sports', 'Science', 'Health']


# Updating some default value
client.location = 'India'
client.language = 'Hindi'
client.topic = 'Sports'

# to gets news urls 
print(client.get_news())

"""
>>> [
     {'title': 'South Africa vs India: विराट कोहली का छलका दर्द, बोले बल्लेबाजों की नाकामी पर कोई बहाना नही - Navbharat Times', 
      'link': 'https://news.google.com/__i/rss/rd/articles/CBMivAFodHRwczovL25hdmJoYXJhdHRpbWVzLmluZGlhdGltZXMuY29tL3Nwb3J0cy9jcmlja2V0L2luZGlhLWluLXNvdXRoLWFmcmljYS92aXJhdC1rb2hsaS1ub3QtaGFwcHktd2l0aC1iYXR0ZXJzLWFmdGVyLWluZGlhLWxvc3QtdGhlLXRlc3Qtc2VyaWVzLWFnYWluc3Qtc291dGgtYWZyaWNhL2FydGljbGVzaG93Lzg4ODk5Njk5LmNtc9IBAA?oc=5', 
      'media': None}, 
     {'title': 'Ind vs SA 3rd Test: केप टाउन टेस्ट हार टूटा भारत का द. अफ्रीका में पहली टेस्ट सीरीज जीतने का सपना - Hindustan', 
      'link': 'https://news.google.com/__i/rss/rd/articles/CBMipgFodHRwczovL3d3dy5saXZlaGluZHVzdGFuLmNvbS9jcmlja2V0L3N0b3J5LWluZGlhLXZzLXNvdXRoLWFmcmljYS0zcmQtdGVzdC1kYXktNGEtbWF0Y2gtcmVwb3J0LWluZC12cy1zYS0zcmQtdGVzdC1saXZlLXNjb3JlLXVwZGF0ZXMtYW5kLWhpbmRpLWNvbW1lbnRhcnktNTU3MjEzOC5odG1s0gEA?oc=5', 
      'media': None}, ...]
"""