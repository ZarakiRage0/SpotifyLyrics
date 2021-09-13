import spotipy
import spotipy.util as util
from dotenv import load_dotenv
import os

load_dotenv()


def set_up_spotify():
    spotify_username = os.getenv("SPOTIFY_USERNAME")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    scope = os.getenv("SCOPE")
    redirect = os.getenv("REDIRECT")

    token = util.prompt_for_user_token(spotify_username, scope, client_id=client_id, client_secret=client_secret,
                                       redirect_uri=redirect)
    spotify = spotipy.Spotify(auth=token)
    return spotify


def get_song(spotify):
    current_track = spotify.current_user_playing_track()
    if current_track is None:
        print("Spotify isn't playing any songs right now.")
        exit(-1)
    artists = current_track["item"]["artists"]
    song = current_track["item"]["name"]
    album = current_track["item"]["album"]["uri"]
    image = current_track["item"]["album"]["images"][0]

    return song, artists, album, image


if __name__ == '__main__':
    spotify_client = set_up_spotify()

    while True:
        print(get_song(spotify_client)[0])
