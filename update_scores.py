import json, time, os, urllib.request, urllib.parse
from datetime import datetime

TMDB_KEY = os.environ.get("TMDB_API_KEY","")
FILM_LIST = [
    "Il Diavolo Veste Prada 2","Michael","È l'Ultima Battuta?",
    "Teresa - La Madre degli Ultimi","Super Mario Galaxy - Il Film",
    "Cena di Classe","The History of Sound - Sulle Note di un Amore",
    "Ella McCay - Perfettamente Imperfetta","Idoli - Fino all'ultima corsa",
    "L'Ultima Missione: Project Hail Mary","La Lezione","Un Bel Giorno",
    "Chopin, Notturno a Parigi","Rental Family - Nelle Vite degli Altri",
    "Domani Interrogo","Il Mago del Cremlino - Le Origini di Putin",
    "Cime Tempestose","HAMNET - Nel nome del Figlio","Le Cose non Dette",
    "2 Cuori e 2 Capanne","Marty Supreme","Sentimental Value","La Grazia",
    "Prendiamoci una Pausa","Song Sung Blue - Una Melodia d'Amore",
    "Ultimo Schiaffo","No Other Choice - Non c'è altra scelta",
    "Una di Famiglia","Buen Camino","Primavera","La Mia Famiglia a Taipei",
    "Norimberga","Gioia Mia","Un Inverno in Corea","L'Anno Nuovo che non arriva",
    "Eternity","Breve Storia d'Amore","Oi Vita Mia","Zootropolis 2",
    "Il Maestro","La Voce di Hind Rajab","The Life of Chuck",
    "Tutto Quello che Resta di Te","Duse","Springsteen: Liberami dal Nulla",
    "Per Te","Il Professore e il Pinguino","La Vita Va Così",
    "L'Isola di Andrea","Material Love","Enzo","L'Ultimo Turno","Afrodite",
    "Una Sconosciuta a Tunisi","Tre Amiche","Le Assaggiatrici",
    "La Vita da Grandi","Il Bambino di Cristallo","Il Nibbio","A Real Pain",
    "A Complete Unknown","FolleMente","Anora","Better Man",
    "Il Tempo che ci vuole","Martedì e Venerdì","Perfect Days",
    "Wonder: White Bird","Il Ragazzo e l'Airone","Conclave",
    "Una Notte a New York","Diamanti","The Substance","Francesca Cabrini",
    "Il Maestro che promise il Mare","L'Amore secondo Kafka","The Fabelmans",
    "C'è ancora domani","Oppenheimer","Killers of the Flower Moon",
    "Io Capitano","Comandante","THE QUIET GIRL","Close","La Stranezza",
    "Il Signore delle Formiche","ANATOMIA DI UNA CADUTA",
]

def tmdb_get(path, params={}):
    params["api_key"] = TMDB_KEY
    url = f"https://api.themoviedb.org/3{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent":"cinema/1.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def cerca(titolo):
    try:
        r = tmdb_get("/search/movie", {"query":titolo,"language":"it-IT","region":"IT"})
        results = r.get("results",[])
        if not results:
            r = tmdb_get("/search/movie", {"query":titolo})
            results = r.get("results",[])
        if not results: return None,None,None,None
        film = next((x for x in results[:3] if x.get("vote_count",0)>=5), results[0])
        poster = film.get("poster_path")          # path relativo, es. "/abc123.jpg"
        vote = film.get("vote_average",0)
        if vote==0 or film.get("vote_count",0)<3: return None,None,film.get("id"),poster
        v5 = round(vote/2, 1)
        return v5, v5, film.get("id"), poster
    except Exception as e:
        print(f"    ERRORE: {e}")
        return None,None,None,None

def load():
    try:
        with open("scores.json") as f: d=json.load(f)
        return {x["titolo"]:x for x in d.get("film",[])}
    except: return {}

def main():
    if not TMDB_KEY:
        print("ERRORE: TMDB_API_KEY mancante — uso solo struttura vuota")
    print(f"=== Aggiornamento {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    existing = load()
    film_finali = []
    for titolo in FILM_LIST:
        ex = existing.get(titolo,{})
        if ex.get("mym") and ex.get("cs"):
            film_finali.append(ex)
            print(f"  SKIP {titolo}")
            continue
        print(f"  CERCA {titolo}")
        if TMDB_KEY:
            mym,cs,tid,poster = cerca(titolo)
        else:
            mym,cs,tid,poster = None,None,None,None
        media = round((mym+cs)/2,1) if mym and cs else (mym or cs)
        # Mantieni poster_path esistente se il nuovo è None
        poster = poster or ex.get("poster_path")
        film_finali.append({"titolo":titolo,"mym":mym,"cs":cs,"media":media,"tmdb_id":tid,"poster_path":poster})
        if mym: print(f"    ✓ {mym}/5")
        else: print(f"    — non trovato")
        time.sleep(0.25)

    con_voto = sum(1 for f in film_finali if f.get("media"))
    output = {"aggiornato":datetime.now().strftime("%Y-%m-%d %H:%M"),
              "totale":len(film_finali),"con_voto":con_voto,"film":film_finali}
    with open("scores.json","w",encoding="utf-8") as f:
        json.dump(output,f,ensure_ascii=False,indent=2)
    print(f"\nCompletato: {con_voto}/{len(film_finali)} con voto")

if __name__=="__main__": main()
