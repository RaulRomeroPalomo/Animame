#encoding:utf-8
from whoosh.fields import *
from whoosh.index import *
from whoosh.qparser.default import QueryParser

from principal.models import Anime, Genero, Tipo, Estudio


dirindex="Index"

def inicia_indice():
    if not os.path.exists(dirindex):
        os.mkdir(dirindex)
    schema = Schema(titulo=TEXT(stored=True),sinopsis=TEXT(stored=True), lanzamiento=TEXT(stored=True)) #importante poner stored si vas a listar
    ix = create_in(dirindex,schema)
    return ix

def setIndice(anime, ix):
    writer = ix.writer()
    print anime.titulo
    writer.add_document(titulo=unicode(anime.titulo).strip(), sinopsis=unicode(anime.sinopsis).strip(), lanzamiento=unicode(anime.lanzamiento).strip())
    writer.commit()  
    

def buscar(pattern, texto):
    ix=open_dir(dirindex)
    with ix.searcher() as searcher:
        query = QueryParser(pattern,ix.schema).parse(unicode(texto))
        results= searcher.search(query)
        for r in results:
            print r['titulo']
            print r['sinopsis']
            

if __name__=="__main__":
    buscar('titulo', 'Boku')