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
    print(lang.upper()+' title: '+str(soup.title.text))
    return soup

def extract_divs(soup):
    """ Extract the necessary divs with html class='desc'.
    These divs contains links and titles of articles.
    """
    return [div for div in soup.find_all('div', class_='desc')]

def extract_articles(divs):
    """ Consume the divs from extract_divs and return
    what we need specifically: the link to the article and its title.
    """
    articles=[]
    for div in divs:
        for i in div.find_all('a'):
            articles.append(("https://www.mosaiquefm.net"+i.get('href'),i.text))
    return articles

def scrape_article(url):
    """ A function to scrape one article using an extracted url.
    """
    site= url
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page,features="html.parser")
    
    divs = []
    for div in soup.find_all('div', class_='desc descp__content'):
        
        divs.append(div)
    
    return divs

def scrape_articles(articles):
    """ Scrape all articles.
    """
    final=[]
    
    for article in articles:
        content = scrape_article(article[0])
        
        print( u'done : '+article[1])
        final.append((article,content[0].text))
    
    return final

def articles_to_csv(dict_articles,lang):
    """ Convert articles objects in the form of dictionaries into
    a csv file. The final step of scraping.
    """
    df = pd.DataFrame(dict_articles)
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
def clean_articles(extracted_articles):
    """ Organize articles into dict objects before extracting them to a csv file.
    """
    lis = []

    for e in extracted_articles:
        link= e[0][0]
        title = e[0][1]
        content = e[1]
   
        lis.append({'link': link,'title': title,'content': content})
    return lis

def scrape_it():
    """ Pipeline of scrapper_mosaique.Done.
    """
    langs = ['ar','fr']
    for lang in langs:
        soup = get_soup(lang)
        log_lang(lang)
        divs = extract_divs(soup)
        articles = extract_articles(divs)
        final = scrape_articles(articles)
        clean = clean_articles(final)
        articles_to_csv(clean,lang)
    
    print("Job is done")

#execute
scrape_it()
