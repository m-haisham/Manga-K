# Manga K

Flask API to download and store manga

## Supported Sources

- Mangakakalot

- Manganel

## API

### GET _All mangas_

```bash
curl --location --request GET 'http://127.0.0.1:5000/mangas'
```

Used to get all the current mangas in the database

### GET _specific manga_

```bash
curl --location --request GET 'http://127.0.0.1:5000/manga/Goblin_Slayer'
```

#### KEYS

chapters all chapters including the updates

#### NOTE

With every call to this Uri updates are added to database, so a second call to this would not give the updates. If you need to get updates more than once goto **manga updates**.

### GET _thumbnail_

```bash
curl --location --request GET 'http://127.0.0.1:5000/manga/Goblin_Slayer/thumbnail'
```

Employs a caching mechanism so it is recommended to use this over direct url.

### POST _new manga_

```bash
curl --location --request POST 'http://127.0.0.1:5000/mangas' \
--header 'Content-Type: application/json' \
--data-raw '{
	"url": "https://mangakakalot.com/manga/martial_peak"
}'
```

#### Headers

`Content-Type` application/json

#### Bodyraw _(application/json)_

```json
{
  "url": "https://mangakakalot.com/manga/martial_peak"
}
```

### POST _change manga settings_

```bash
curl --location --request POST 'http://127.0.0.1:5000/manga/Fukushuu_o_Koinegau_Saikyou_Yuusha_wa,_Yami_no_Chikara_de_Senmetsu_Musou_Suru' \
--header 'Content-Type: application/json' \
--data-raw '{
    "manhwa": false,
    "favourite": true
}'
```

#### Headers

`Content-Type` application/json

#### Bodyraw _(application/json)_

```json
{
  "manhwa": false,
  "favourite": true
}
```

### GET _specific chapter_

```bash
curl --location --request GET 'http://127.0.0.1:5000/manga/Martial_Peak/Chapter_3'
```

Provides information needed to create reader.

Pages have `link` if downloaded which when called sends image directly from server.

Calling this marks the chapter as read and is added to recents.

### GET _page list_

```bash
curl --location --request GET 'http://127.0.0.1:5000/manga/Martial_Peak/Chapter_3/pages'
```

Calling this marks the chapter as read and is added to recents.

### GET _page image_

```bash
curl --location --request GET 'http://127.0.0.1:5000/manga/Martial_Peak/Chapter_3/1'
```

Returns a jpeg image as attachment.

### GET _all favourites_

```bash
curl --location --request GET 'http://127.0.0.1:5000/favourites'
```

Returns all the mangas that have been favourited

### GET _all recents_

```bash
curl --location --request GET 'http://127.0.0.1:5000/recents'
```

returns the recently read list

### GET _manga updates_

```bash
curl --location --request GET 'http://127.0.0.1:5000/manga/Goblin_Slayer/updates'
```

updates arent added to the database chapter list, so consecutive calls will give the same result.

### POST search

```bash
curl --location --request POST 'http://127.0.0.1:5000/search/1' \
--header 'Content-Type: application/json' \
--data-raw '{
	"word": "tomo"
}'
```

`word` is used a keyword for search

#### Headers

`Content-Type` application/json

#### Bodyraw (application/json)

```json
{
  "word": "tomo"
}
```

### GET _popular_

```bash
curl --location --request GET 'http://127.0.0.1:5000/popular'
```

### GET _latest_

```bash
curl --location --request GET 'http://127.0.0.1:5000/latest'
```

### GET _all downloads_

```bash
curl --location --request GET 'http://127.0.0.1:5000/downloads'
```

Returns all the current downloads

### GET _specific download_

```bash
curl --location --request GET 'http://127.0.0.1:5000/download/0'
```

Where 0 is the index of download.

### POST _add downloads_

```bash
curl --location --request POST 'http://127.0.0.1:5000/downloads' \
--header 'Content-Type: application/json' \
--data-raw '{
	"manga_url": "https://mangakakalot.com/manga/martial_peak",
    "urls": [
    	"https://mangakakalot.com/chapter/martial_peak/chapter_3"
    ]
}'
```

Returns information of chapters set to download

#### REQUIRES

manga_url url of the manga being added to download

urls list of urls belonging to chapters to be downloaded

#### Headers

`Content-Type` application/json

#### Bodyraw _(application/json)_

```json
{
  "manga_url": "https://mangakakalot.com/manga/martial_peak",
  "urls": ["https://mangakakalot.com/chapter/martial_peak/chapter_3"]
}
```

### POST _delete downloads_

```bash
curl --location --request POST 'http://127.0.0.1:5000/downloads/delete' \
--header 'Content-Type: application/json' \
--data-raw '{
	"manga_url": "https://mangakakalot.com/manga/martial_peak",
    "urls": [
    	"https://mangakakalot.com/chapter/martial_peak/chapter_3"
    ]
}'
```

Returns information of chapters set to delete

#### REQUIRES

manga_url url of the manga being added to download

urls list of urls belonging to chapters to be downloaded

#### Headers

`Content-Type` application/json

#### Bodyraw _(application/json)_

```json
{
  "manga_url": "https://mangakakalot.com/manga/martial_peak",
  "urls": ["https://mangakakalot.com/chapter/martial_peak/chapter_3"]
}
```

### GET _get flags_

```bash
curl --location --request GET 'http://127.0.0.1:5000/downloads/status'
```

Returns the download flags

### POST _set flags_

```bash
curl --location --request POST 'http://127.0.0.1:5000/download/status' \
--header 'Content-Type: application/json' \
--data-raw '{
	"clear": true
}'
```

set `pause` to control downloads.

set `clear` to true to clear the queue.

clear flag resets after clearing the queue.

### Headers

`Content-Type` application/json

#### Bodyraw _(application/json)_

```json
{
  "pause": true,
  "clear": false
}
```
