from requests import get
from urllib import quote_plus
from bs4 import BeautifulSoup as bs
from csv import DictWriter as dw

root_url = 'http://lyrics.wikia.com/'
band_filename = 'RSTOP100'

visited = {}

with open(band_filename, 'r') as band_file, open('db.csv', 'w+') as csv_file:
    writer = dw(csv_file, fieldnames=['genre', 'band', 'song', 'lyrics'])
    writer.writeheader()

    for line in band_file:
        band, genre = line.partition(' - ')[::2]

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
            if url in visited:
                print 'skipping duplicate: ', url
                continue
            visited[url] = 1

            print 'Getting lyrics for: ', url
            r = get(url)
            if r.status_code != 200:
                print 'Failed to grab song: ', url
                continue

            lyricbox = bs(r.text, 'html.parser').select('.lyricbox')
            if len(lyricbox) != 1:
                continue

            clean_lyrics = '\n'.join(lyricbox[0].stripped_strings)

            writer.writerow({
                'genre': genre.strip().encode('utf-8'),
                'band': band.strip().encode('utf-8'),
                'song': url.encode('utf-8'),
                'lyrics': clean_lyrics.encode('utf-8')
                })
        exit()
