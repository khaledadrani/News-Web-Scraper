
import bs4 as bs
import urllib.request as url_req
import numpy as np
import pandas as pd




def scrape_article(url):
    sauce = url_req.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    
    divs = []
    for div in soup.find_all('div', class_='desc descp__content'):
        
        divs.append(div)
    
    return divs

def scrape_articles(articles):
    final=[]
    
    for art in articles:
        content = scrape_article(art[1])
        
        print( u'done : '+art[0])
        final.append((art,content[0].text))
    
    return final

def log_lang(lang):
    if lang=='ar':
        print('note: if you are not seeing the arabic characters'+ 
        ' in the right form in the IO, it means there"s a problem with your terminal.'+
        ' still trying to fix it...')
        print('note: check the saved files and you will see the characters are fine.')

def scrape_lang(lang): #ar or fr
    #https://www.mosaiquefm.net/ar/
    print('scraping the '+lang+' version...')
    sauce = url_req.urlopen('https://www.mosaiquefm.net/'+lang+'/').read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    log_lang(lang)
    divs = []
    for div in soup.find_all('div', class_='desc'):
        divs.append(div)

    articles=[]

    for div in divs:
        for i in div.find_all('a'):
            articles.append((i.text,"https://www.mosaiquefm.net"+i.get('href')))
    
    result = scrape_articles(articles)

    
    lis = []

    for e in result:
        link= e[0][1]
        title = e[0][0]
        content = e[1]
   
        lis.append({'link': link,'title': title,'content': content})


    df = pd.DataFrame(lis)
    print(lang+' version done.')
    df.to_csv('mosaique_'+lang+'.csv',encoding='utf-8-sig')

print('scraping mosaique fm...')
scrape_lang('ar')
scrape_lang('fr')
print('scraping is done!')




