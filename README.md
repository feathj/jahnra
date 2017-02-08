docker build .

docker-compose run --rm app python extract_lyrics.py
docker-compose run --rm app python jahnra.py
