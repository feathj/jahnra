from requests import get
from urllib import quote_plus
from bs4 import BeautifulSoup as bs

root_url = 'http://lyrics.wikia.com/'
band_filename = 'RSTOP100'

genre_to_lyrics = {}


def serialize_lyrics(g2l):
    for genre, lyrics in g2l.iteritems():
        with open("./db/{0}".format(genre.replace(' ', '_')), 'w+') as f:
            for lyric in lyrics:
                f.write(lyric.encode('utf8') + '\n')

with open(band_filename, 'r') as f:
    for line in f:
        band, genres = line.partition(' - ')[::2]
        genres = genres.split(',')

        safe_band = band.replace(' ', '_')
        safe_band = quote_plus(safe_band)

        url = '{0}/wiki/{1}'.format(root_url, band.replace(' ', '_'))
        r = get(url)

        if r.status_code != 200:
            print 'Failed to grab band: ', url
            continue

        body = bs(r.text, 'html.parser').find(id='WikiaArticle')
        lyric_links = body.select('ol > li > b > a')

        for lyric_link in lyric_links:
            if lyric_link.get('class', '') == 'new':
                continue
            if safe_band not in lyric_link['href']:
                continue
            if 'redlink' in lyric_link['href']:
                continue

            url = '{0}{1}'.format(root_url, lyric_link['href'])
            print 'Getting lyrics for: ', url
            r = get(url)
            if r.status_code != 200:
                print 'Failed to grab song: ', url
                continue

            lyricbox = bs(r.text, 'html.parser').select('.lyricbox')
            if len(lyricbox) != 1:
                continue
            for lyric in lyricbox[0].stripped_strings:
                for genre in genres:
                    if genre.strip() not in genre_to_lyrics:
                        genre_to_lyrics[genre.strip()] = []
                    genre_to_lyrics[genre.strip()].append(lyric)
        #break
print 'Serializing Lyrics Database'
serialize_lyrics(genre_to_lyrics)
