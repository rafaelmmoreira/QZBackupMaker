import requests
import time
from bs4 import BeautifulSoup
import os
import json

forums = {#'Queen - General Discussion': 10,
          #'Queen - Serious Discussion': 1,
          'Queen collecting and trading': 13,
          'Queen + Adam Lambert': 9,
          'Sharing The Music - Request': 12,
          'Sharing The Music - Announce': 4,
          'Fan mixes': 11,
          'Personal': 3,
          'Queenzone.com': 7,
          'Queen News': 8}
mainURL = 'http://queenzone.com/forums/forum_view.aspx?Q='



for forum in forums:
    fpage = 1
    os.mkdir(forum)
    while True:
        forumReq = requests.get(mainURL + str(forums[forum]) + '&page=' + str(fpage))
        if forumReq.status_code == 200:
            forumHTML = BeautifulSoup(forumReq.text, 'html.parser')
            # get all threads on current forum page:
            table = forumHTML.find_all('tr', class_=['qzTableData','qzTableDataAlternate']) 
            if table == [] or table == None:
                break
            for row in table:
                # get thread info:
                #print(row.text)
                cols = row.find_all('td')
                thread = {}
                thread['title'] = cols[1].find('a').text.strip()
                thread['url'] = cols[1].find('a')['href']
                thread['author'] = cols[2].text.strip()
                # get thread content:
                page = 1
                threadContent = []
                print(forum, '|| page = ', fpage, '\n--', thread['title'])
                while True:
                    print('---page =', page)
                    pageReq = requests.get('http://queenzone.com' + thread['url'] + '?page=' + str(page))
                    pageHTML = BeautifulSoup(pageReq.text, 'html.parser')
                    threadTable = pageHTML.find_all('tr', class_=['qzTableData','qzTableDataAlternate']) 
                    if threadTable == [] or threadTable == None:
                        break                
                    for post in threadTable:
                        postDict = {}
                        author = post.find('a', class_='author').text
                        content = post.find('div', class_='forumContent').text
                        timestamp = post.find('span', class_='small').text
                        signature = post.find('div', class_='sigDiv')
                        if signature != None:
                            content = content.replace(signature.text, '')
                        # find quotes and adjust Queenzone quote syntax:
                        quotes = post.find_all('div', class_='quote')
                        for quote in quotes:
                            newquote = quote.text
                            authorswrote = quote.find_all('b') + post.find_all('strong')
                            for a in authorswrote:
                                newquote = newquote.replace(a.text, '[b]'+a.text+'[/b]')
                            newquote = '[QUOTE]'+newquote+'[/QUOTE]'                                               
                            content = content.replace(quote.text, newquote)
                            
                        postDict['author'] = author.strip()
                        postDict['timestamp'] = timestamp.replace('\\r', '').replace('\\n', '').replace('Posted:', '').strip()
                        postDict['content'] = content.replace(timestamp, '').strip()
                        
                        threadContent.append(postDict)
                    page += 1
                thread['posts'] = threadContent
                filename = thread['url'][7:].replace('/', '_').replace('.aspx', '.json')
                with open(os.path.join(forum, filename), 'w') as output:
                    json.dump(thread, output, indent=1)
        fpage += 1
