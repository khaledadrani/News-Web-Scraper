import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def get_soup(lang): 
    """ This function will get the html extracted from the targeted
    page of mosaiquefm depending on the lang argument(language).
    """
    site= "https://www.mosaiquefm.net/"+lang+"/"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page,features="html.parser")
    #print(lang.upper()+' title: '+str(soup.title.text))
    return soup


def extract_divs(soup):
    divs=[]
    classes=['col-xs-6 col-sm-6 col-md-4 news','col-xs-6 col-sm-6 col-md-6 news','col-xs-5 col-sm-4 col-md-5 thumb']
    for cla in classes:
        for div in soup.find_all('div', class_=cla):
            divs.append(div)
    return divs

def thumbs_desc(divs):
    thumbs=[]
    desc=[]
    nb = [i for i in range(100)]
    for lis in divs:
        for c in nb:
            l = [d.text for d in lis.find_all('span', class_='categorie bg_'+str(c))]  
            if(len(l)!=0):
                thumbs.extend(l)


    for x in divs:    
        f = [d for d in x.find_all('div', class_='desc')]
        if(len(f)!=0):
            desc.extend(f)
    
    return thumbs, desc

def extract_links(desc):
    links=[]
    for div in desc:
        for i in div.find_all('a'):
            links.append({"link":"https://www.mosaiquefm.net"+i.get('href'),"title":i.text})
    return links


def to_jamil(links,thumbs):
    return list(zip(links,thumbs))

def scrape_article(url):
    site= url
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page,features="html.parser")
    
    divs = []
    for div in soup.find_all('div', class_='desc descp__content'):
        
        divs.append(div)
    
    return divs

def scrape_articles(jamil):
    final=[]
    
    for j in jamil:
        content = scrape_article(j[0]['link'])
        #print( u'done : '+j[0]['title'])
        final.append({"link": j[0]['link'], "title": j[0]['title'], "type": j[1], "content": content[0].text})
    
    return final

def articles_to_csv(job,lang):
    df = pd.DataFrame(job)
    print(lang+' version done.')
    df.to_csv('mosaique_'+lang+'.csv',encoding='utf-8-sig')


def log_lang(lang):
    """ Some information about the IO settings.
    """
    if lang=='ar':
        print('note: if you are not seeing the arabic characters'+ 
        ' in the right form in the IO, it means there"s a problem with your terminal.'+
        ' still trying to fix it...')
        print('note: check the saved files and you will see the characters are fine.')

def scrape_it():
    """ Pipeline of scrapper_mosaique.Done.
    """
    print('Job begins.')
    langs = ['ar','fr']
    for lang in langs:
        
        soup = get_soup(lang)
        #log_lang(lang)
        divs = extract_divs(soup)
        thumbs,desc = thumbs_desc(divs)
        links = extract_links(desc)
        jamil = to_jamil(links,thumbs)
        final = scrape_articles(jamil)
        articles_to_csv(final,lang)
        
    
    print("Job is done.")

#execute
scrape_it()
