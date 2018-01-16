#encoding: utf-8
from bs4 import BeautifulSoup
from django.core.management import call_command
import requests

from principal.models import Anime, Genero, Tipo, Estudio


def principal():
    call_command('flush',interactive=False)
    call_command('syncdb',interactive=False)

    url = "https://myanimelist.net/topanime.php?type=upcoming"

    i=0
    while i <= 250:    
        r=requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, "lxml")
        body = soup.find("table",{"class":"top-ranking-table"})
        ranking = body.findAll("tr",{"class":"ranking-list"})
        for r in ranking:
            titulo = r.find("a",{"class":"hoverinfo_trigger fl-l fs14 fw-b"})
            url = titulo["href"]
            getAnime(url)
        i+=50
        url = "https://myanimelist.net/topanime.php?type=upcoming&limit="+str(i)


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

        print lanzamiento
        
        
        side = soup.find("div",{"id":"content"}).find("div",{"class":"js-scrollfix-bottom"})
        typeStudio = side.findAll("a")
        tipo = "No type"
        studio = []
        for ts in typeStudio:
            if "?type" in ts["href"]:
                tipo = ts.get_text()
            otipo =Tipo.objects.get_or_create(nombre=tipo)
            if "/producer" in ts["href"]:
                studio.append(ts.get_text())
        if not studio:
            studio=["Unknown"]
                
        anime = Anime.objects.create(titulo=name,original=original,sinopsis=sinopsis,lanzamiento=lanzamiento,
                             popularidad=int(popularity),tipo=otipo[0])
        
        for s in studio:
            print s
            os = Estudio.objects.get_or_create(nombre=s)
            anime.estudios.add(os[0])
            
        genres=side.find("script",{"type":"text/javascript"})
        if genres:
            listgenres= str(genres).split("genres")[1].split("])")[0].replace('\"',"")[3:].strip().split(",")
            for g in listgenres:
                if g is not "":
                    genero=Genero.objects.get_or_create(nombre=g)
                    anime.generos.add(genero[0])
        
        print tipo
        
    except AttributeError as e:
        print e
        
         

def getUsuario(nombre):
    url="https://myanimelist.net/profile/"+nombre
    r=requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    
       
       
       
       
if __name__=="__main__":
    principal()