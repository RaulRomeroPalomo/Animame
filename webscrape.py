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
        sinopsis = soup.find("span",{"itemprop":"description"})
        if sinopsis:
            sinopsis=sinopsis.get_text()
        else:
            sinopsis="No existe sinopsis"
        print sinopsis
        popularity = soup.find("span",{"class":"numbers popularity"}).strong.get_text().replace("#","")
        print popularity
        lateral = soup.find("td",{"class":"borderClass"})
        nombrejapo = lateral.findAll("div",{"class":"spaceit_pad"})
        original = "No disponible"
        if len(nombrejapo) > 1:
            original = nombrejapo[1].get_text().split(":")[1].strip()
            
        print original
        otherInfo=soup.findAll("div",{"class":"spaceit"})
        lanzamiento = "No hay fecha"
        for info in otherInfo:
            text =info.get_text()
            if "Aired:" in text:
                info.span.clear()
                lanzamiento = info.get_text().strip()
            
        genres = "Sin generos"
        
                          
        print lanzamiento
        genres = soup.find("div",{"id":"content"}).find("div",{"class":"js-scrollfix-bottom"}).find("script",{"type":"text/javascript"})
        if genres:
            listgenres= str(genres).split("genres")[1].split("])")[0].replace('\"',"")[3:].strip().split(",")
            for g in listgenres:
                print g
    
    except AttributeError as e:
        print e
        
            
if __name__=="__main__":
    principal()