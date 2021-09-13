#!/usr/bin/python
import requests
from bs4 import BeautifulSoup


class Song:
    def __init__(self):
        self._valid_search = False
        self._link_list = None
        self._song_title = None
        self._lyrics = None
        self._album = None
        self._album_cover = None

    def get_lyrics(self):
        return self._lyrics

    def get_song_title(self):
        return self._song_title

    def get_album_uri(self):
        return self._album

    def is_valid(self):
        return self._valid_search

    def set_songs_links(self, search_title: str):
        self._song_title = search_title
        search_url = "https://search.azlyrics.com/search.php?q=" + search_title
        page = requests.get(search_url)
        text = page.text
        soup = BeautifulSoup(text, "html.parser")
        soup = soup.find('table', class_="table table-condensed")
        if soup is None:
            self._valid_search = False
        else:
            self._valid_search = True
            link_list = [link.get('href') for link in soup.find_all('a', href=True)]
            link_list[:] = [link for link in link_list if "https" in link]
            print(link_list)
            self._link_list = link_list

    def set_lyrics(self):
        song_url = self._link_list[0]
        page = requests.get(song_url)
        text = page.text
        soup = BeautifulSoup(text, "html.parser")
        soup = soup.find('div', class_="col-xs-12 col-lg-8 text-center")
        divs = soup.find_all('div')
        self._lyrics = divs[5].get_text()

    def search_lyrics(self, search_title: str, album, image):
        self.set_songs_links(search_title=search_title)
        self._album = album
        self._album_cover = image
        if not self._valid_search:
            self._lyrics = "Error in Search"
        else:
            self.set_lyrics()

    def title_compare(self, title: str):
        return self._song_title == title


if __name__ == '__main__':
    song = Song()
    while True:
        search = input()
        song.search_lyrics(search_title=search)
        print(song.get_lyrics())
