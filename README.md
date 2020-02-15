# Manga K

Flask API to download and store manga

## Supported Sources

- Mangakakalot

- Manganel

## Database

Flask Sqlalchemy

## API

### GET _All mangas_

```bash
curl --location --request GET 'http://127.0.0.1:5000/mangas'
```

Used to get all the current mangas in the database

### GET _specific manga_

```bash
curl --location --request GET 'http://127.0.0.1:5000/manga/1'
```

#### NOTE

Update status of a chapter is marked by `update_status` key.
The first population of would not be marked as updates

### GET _thumbnail_

```bash
curl --location --request GET 'http://127.0.0.1:5000/thumbnail/1'
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
  "url": "https://mangakakalot.com/manga/1"
}
```

### POST _change manga settings_

```bash
curl --location --request POST 'http://127.0.0.1:5000/manga/2' \
--header 'Content-Type: application/json' \
--data-raw '{
    "manhwa": false,
    "favourite": true,
    "style": "rtl"
}'
```

Style refers to reading style
options:
* rtl (right to left)
* ltr (left to right)
* vertical
* webtoon

#### Headers

`Content-Type` application/json

#### Bodyraw _(application/json)_

```json
{
  "manhwa": false,
  "favourite": true,
  "style": "rtl"
}
```

### GET _specific chapter_

```bash
curl --location --request GET 'http://127.0.0.1:5000/chapter/1/5'
```

Provides information needed to create reader.

Pages have `link` if downloaded which when called sends image directly from server.

Calling this marks the chapter as read and is added to recents.

### GET _page list_

```bash
curl --location --request GET 'http://127.0.0.1:5000/pages/1/2'
```

Calling this marks the chapter as read and is added to recents.

### GET _page image_

```bash
curl --location --request GET 'http://127.0.0.1:5000/page/1/2/5'
```

Returns a jpeg image as attachment.

### GET _all favourites_

```bash
curl --location --request GET 'http://127.0.0.1:5000/favourites'
```

Returns all the mangas that have been favoured

### GET _all recents_

```bash
curl --location --request GET 'http://127.0.0.1:5000/recents'
```

`order` descending

returns the recently read list

### GET _all updates_

```bash
curl --location --request GET 'http://127.0.0.1:5000/updates'
```

`returns` The full update history in

`order` descending

### GET _manga updates_

```bash
curl --location --request GET 'http://127.0.0.1:5000/updates/1'
```

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
	"manga_id": 1,
    "chapter_ids": [1, 2]
}'
```

Returns information of chapters set to download

#### REQUIRES

manga_id id of the manga being added to download

chapter_ids list of ids belonging to chapters to be downloaded

#### Headers

`Content-Type` application/json

#### Bodyraw _(application/json)_

```json
{
  "manga_id": 1,
  "chapter_ids": [1, 2]
}
```

### POST _delete downloads_

```bash
curl --location --request POST 'http://127.0.0.1:5000/downloads/delete' \
--header 'Content-Type: application/json' \
--data-raw '{
    "ids": [1, 2]
}'
```

Returns information of chapters set to delete

#### REQUIRES

chapter ids to delete

#### Headers

`Content-Type` application/json

#### Bodyraw _(application/json)_

```json
{
    "ids": [1, 2]
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
