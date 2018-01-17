#encoding: utf-8
from bs4 import BeautifulSoup
from django.core.management import call_command
import requests

from principal.models import Anime, Genero, Tipo, Estudio, Usuario


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
    result = "?"
    message = soup.find("h1",{"class","h1"})
    if message and "404" in message.get_text():
        result = "No existe el usuario"
    else:
        allgenres = []
        allstudios = []
        url = soup.find("div",{"class":"user-image mb8"})
        if url.img:
            url=url.img['src']
        else:
            url = ""
        query = Usuario.objects.filter(usuario=nombre)
        if query:
            query.delete()
        user = Usuario.objects.create(usuario=nombre,image=url)
        
        user.topestudios.clear()
        user.topgeneros.clear()
        favanime = soup.find("ul",{"class":"favorites-list anime"})
        if favanime:
            favanime = favanime.findAll("li",{"class":"list di-t mb8"})
            for fav in favanime:
                prefs = getDataAnime(fav.findAll("a")[1]['href'])
                allstudios.append(prefs[0])
                allgenres.append(prefs[1])
            topstudios = getTop(allstudios)
            for estudio in topstudios:
                s = Estudio.objects.get_or_create(nombre=estudio) 
                user.topestudios.add(s[0])            
            topgenres = getTop(allgenres)
            for genero in topgenres:
                g = Genero.objects.get_or_create(nombre=genero)
                user.topgeneros.add(g[0])
            
            result = user
        else:
            result = nombre+" no tiene animes favoritos, por lo que no podemos hacer ninguna recomendación."
    
    print result
    return result


def getTop(lists):
    flatten = sum(lists,[])
    ranking = {}
    for element in flatten:
        if element not in ranking.keys():
            ranking[element]=1
        else:
            ranking.update({element:ranking[element]+1})
    
    return sorted(ranking, key=ranking.get, reverse=True)[:3]


def getDataAnime(url):
    prefs =[]
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"lxml")      
    side = soup.find("div",{"id":"content"}).find("div",{"class":"js-scrollfix-bottom"})
    estudios = side.findAll("a")
    studies = []
    generos = []
    for ts in estudios:
        if "/producer" in ts["href"]:
            studies.append(ts.get_text())        
    genres=side.find("script",{"type":"text/javascript"})
    if genres:
        listgenres= str(genres).split("genres")[1].split("])")[0].replace('\"',"")[3:].strip().split(",")
        for g in listgenres:
            if g is not "":
                generos.append(g)    
    
    prefs.append(studies)
    prefs.append(generos)
    return prefs
    
    
    
       
if __name__=="__main__":
    getUsuario("Yunekow")
    
    