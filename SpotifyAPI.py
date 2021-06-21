import json
import time
import pandas as pd
import requests
import base64

class SpotifyAPI:
    def __init__(self, clientid, clientsec):
        self.clientid = clientid
        self.clientsec = clientsec
        self.getToken()

    def getToken(self):
        creds = f"{self.clientid}:{self.clientsec}"
        creds = (base64.b64encode(creds.encode())).decode()
        r = requests.post("https://accounts.spotify.com/api/token", data={"grant_type": "client_credentials"}, headers={"Authorization": f"Basic {creds}"})
        if r.status_code != 200:
            print("Error when requesting access token:", r.json())
            exit(1)
        r = r.json()
        self.access_token = r["access_token"]
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.expires_in = r["expires_in"]
        self.last_renewed = time.time()
    
    def search(self, **kwargs):
        endpoint = "https://api.spotify.com/v1/search?"
        for key, val in kwargs.items():
            endpoint = endpoint + f'{key}={val}&'
        endpoint = endpoint[:-1]

        elapsed = time.time() - self.last_renewed
        print(elapsed, self.expires_in)
        if  elapsed > (self.expires_in - 100):
            print(f"Token expired after {elapsed} Attempting to renew.")
            self.getToken()

        r = requests.get(endpoint, headers=self.headers)

        while(r.status_code == 429):
            retry_after = int(r.headers["Retry-After"])
            print(f"Rate limited. Set to sleep for {retry_after}")
            time.sleep(retry_after)
            r = requests.get(endpoint, headers=self.headers)

        if r.status_code != 200:
            print("Something went wrong, dumping response.")
            print(json.dumps(r.json(), indent=2))
        else:
            print("Success.")

        r = r.json()

        try: 
            spotify_id = [d['id'] for d in r['tracks']['items']][0]
            spotify_href = [d['href'] for d in r['tracks']['items']][0]
            spotify_name = [d['name'] for d in r['tracks']['items']][0]
        except:
            print(f"Error getting data for query {endpoint} dumping response.")
            print(json.dumps(r, indent=2))
            spotify_id = 'null'
            spotify_href = 'null'
            spotify_name = 'null'

        return spotify_id, spotify_href, spotify_name
        

if __name__ == "__main__":
    df = pd.read_csv("UMG_Raw_Song_Data.csv")

    handler = SpotifyAPI("831cc784a86e40f7a94913a7760911c1", "9ec69ad406ef4de69d0c52b0becf9eb8")

    isrc = df['isrc'].values
    names = df['song_name'].values
    new_values = []
    for i, v in enumerate(isrc):
        spotify_id, spotify_href, spotify_name = handler.search(q=f"isrc:{v}", type="track")
        entry = {'isrc': v, 'song_name': names[i], 'spotify_id': spotify_id, 'spotify_href': spotify_href, 'spotify_name': spotify_name}
        new_values.append(entry)
    
    df_spotify = pd.DataFrame(new_values)
    df_spotify.to_csv('Spotify_Data.csv', index=False)

    
