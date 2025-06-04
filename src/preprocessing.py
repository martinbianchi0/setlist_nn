import requests
import pandas as pd
from datetime import datetime

API_KEY = 'CLninVzk2hduoK_avKOO-mxHnM9zrJ_JXdHX'
HEADERS = {'Accept': 'application/json', 'x-api-key': API_KEY}

def get_setlists(artist, pages=10):
    all_data = []
    for p in range(1, pages + 1):
        params = {'artistName': artist, 'p': p}
        r = requests.get('https://api.setlist.fm/rest/1.0/search/setlists', headers=HEADERS, params=params)
        if r.status_code != 200:
            break
        data = r.json().get('setlist', [])
        for s in data:
            try:
                date = datetime.strptime(s['eventDate'], '%d-%m-%Y')
                venue = s['venue']['name']
                city = s['venue']['city']['name']
                country = s['venue']['city']['country']['code']
                coords = s['venue']['city'].get('coords', {})
                lat = coords.get('lat', None)
                long = coords.get('long', None)
                tour = s.get('tour', {}).get('name', None)
                songs = []
                for set_block in s.get('sets', {}).get('set', []):
                    for song in set_block.get('song', []):
                        songs.append(song.get('name'))
                if songs:
                    all_data.append({
                        'date': date,
                        'venue': venue,
                        'city': city,
                        'country': country,
                        'lat': lat,
                        'long': long,
                        'tour': tour,
                        'songs': songs
                    })
            except Exception:
                continue
    return pd.DataFrame(all_data)

# HICE ESTO PARA GUARDAR LA INFO EN UN CSV Y Q SEA MAS FACIL DE VER
if __name__ == "__main__":
    artist = "The Rolling Stones" # Cambia por el artista que quieras
    df = get_setlists(artist, pages=10)
    df.to_csv(f"{artist}_setlists.csv", index=False)
    print(f"Archivo {artist}_setlists.csv guardado correctamente.")