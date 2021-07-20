import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="51be9cd513d140b09aef34eb4b658bc6",
                                                           client_secret="dabedd95010148fdb93a6de230728812"))

song  = "Aries (feat. Peter Hook and Georgia)"
artist = "Gorillaz Feat. Peter Hook Feat. Georgia"


results = sp.search(q=song, type='track', limit=1)

for track in (results['tracks']['items']):
    # print (results['tracks']['items'])
    print(track['name'],"\t"+track['album']['name'])
    artists = ""
    
    for i in range(len(track['album']['artists'])):
        artists += track['album']['artists'][i]['name']