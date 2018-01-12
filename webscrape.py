#encoding: utf-8
import sqlite3

from bs4 import BeautifulSoup
import requests
from types import NoneType


def principal():
    url = "https://myanimelist.net/topanime.php?type=upcoming"
    r=requests.get(url)
    data = r.text
        
    soup = BeautifulSoup(data, "lxml")
    body = soup.find("table",{"class":"top-ranking-table"})
    ranking = body.findAll("tr",{"class":"ranking-list"})
    for r in ranking:
        titulo = r.find("a",{"class":"hoverinfo_trigger fl-l fs14 fw-b"})
        url = titulo["href"]
        getAnime(url)


def getAnime(url):
    r = requests.get(url)
    try:
        soup = BeautifulSoup(r.text,"lxml")
        name = soup.find("span",{"itemprop":"name"}).get_text()
        print name
        lateral = soup.find("td",{"class":"borderClass"})
        cosas = lateral.findAll("div",{"class":"spaceit_pad"})
        if len(cosas) > 1:
            print cosas[1].get_text().split(":")[1]

            
    except AttributeError:
        print "Fallico"
        
            
if __name__=="__main__":
    principal()