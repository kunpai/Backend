# Code Foo Backend Project
For Code Foo IGN
Using the .csv file given, I created a Backend server on Flask using SQLite as the database

## Usage of Backend Server

All responses will have the form

```json
{
    "media_type" : row[1],
    "name" : row[2],
    "short_description" : row[5],
    "long_description" : row[4],
    "genres" : row[11],
    "ratings" : row[9],
    "review_url" : row[8],
    "slug" : row[10],
    "published_by" : row[13],
    "franchise": row[14]
}
```
where row is the extraction from the SQLite Database.


Here are the endpoints on the API and what they do:

1. **Definition**

`GET`, `POST`

**/api/details**

This endpoint takes in a title, converts it into a slug, and checks if any entry in the database fulfils the query.

`POST`:

```json
    {
        "slug" : slug
    }
```
Any string entered is converted into a slug using the string function ```.lower().replace(' ','-')```

`GET` :
- `200 OK`

```json
[
    {
        "media_type" : row[1],
        "name" : row[2],
        "short_description" : row[5],
        "long_description" : row[4],
        "genres" : row[11],
        "ratings" : row[9],
        "review_url" : row[8],
        "slug" : row[10],
    },
]
```

2. **Definition**

`GET`, `POST`

**/api/recommend**

This endpoint takes in a type of media (Movie, Game, etc.) and a Genre, and returns media that fulfils both categories.

`POST`:

```json
    {
        "media_type" : media_type,
        "genres" : genre
    }
```
Any string entered is converted into the correct format using the string function ```.title()```

`GET` :
- `200 OK`

```json
[
    {
        "media_type" : row[1],
        "name" : row[2],
        "short_description" : row[5],
        "long_description" : row[4],
        "genres" : row[11],
        "ratings" : row[9],
        "review_url" : row[8],
        "slug" : row[10],
    },
]
```

3. **Definition**

`GET`, `POST`

**/api/publisher**

This endpoint takes in a type of media (Movie, Game, etc.) and a Publisher, and returns media that fulfils both categories.

`POST`:

```json
    {
        "media_type" : media_type,
        "published_by" : publisher
    }
```
Any string entered is converted into the correct format using the string function ```.title()```

`GET` :
- `200 OK`

```json
[
    {
        "media_type" : row[1],
        "name" : row[2],
        "short_description" : row[5],
        "long_description" : row[4],
        "genres" : row[11],
        "ratings" : row[9],
        "review_url" : row[8],
        "slug" : row[10],
        "published_by" : row[13]
    },
]
```

4. **Definition**

`GET`, `POST`

**/api/franchise**

This endpoint takes in a Franchise, and returns media that fulfils that category.

`POST`:

```json
    {
        "franchise" : franchise
    }
```
Any string entered is converted into the correct format using the string function ```.title()```

`GET` :
- `200 OK`

```json
[
    {
        "media_type" : row[1],
        "name" : row[2],
        "short_description" : row[5],
        "long_description" : row[4],
        "genres" : row[11],
        "ratings" : row[9],
        "review_url" : row[8],
        "slug" : row[10],
        "franchise" : row[14]
    },
]
```

5. **Definition**

`GET`, `POST`

**/api/mediafranchise**

This endpoint takes in a type of media (Movie, Game, etc.) and a Publisher, and returns media that fulfils both categories.

`POST`:

```json
    {
        "media_type" : media_type,
        "franchise" : franchise
    }
```
Any string entered is converted into the correct format using the string function ```.title()```

`GET` :
- `200 OK`

```json
[
    {
        "media_type" : row[1],
        "name" : row[2],
        "short_description" : row[5],
        "long_description" : row[4],
        "genres" : row[11],
        "ratings" : row[9],
        "review_url" : row[8],
        "slug" : row[10],
        "franchise" : row[14]
    },
]
```


## Usage of Discord Bot

As an application of the backend server, I designed a Discord bot that uses the database and slash commands to become a media searcher and recommender. I also implemented a wishlist where users can add the media they like and view them later (Watch Later?).

1. **Definition**

**/search**

This command converts an entered string into a slug, and uses ```/api/details``` to get the results from the database.

![Alt text](https://github.com/kunpai/Backend/blob/main/BotScreenshots/Search.png?raw=true "search")

2. **Definition**

**/recommend**

This command converts an entered media type and genre into a title, and uses ```/api/recommend``` to get the results from the database.

![Alt text](https://github.com/kunpai/Backend/blob/main/BotScreenshots/Recommend.png?raw=true "recommend")

3. **Definition**

**/publisher**

This command converts an entered media type and publisher into a title, and uses ```/api/publisher``` to get the results from the database.

![Alt text](https://github.com/kunpai/Backend/blob/main/BotScreenshots/Publisher.png?raw=true "publisher")

4. **Definition**

**/franchise**

This command converts an entered media type and franchise into a title, and uses ```/api/mediafranchise``` to get the results from the database.

![Alt text](https://github.com/kunpai/Backend/blob/main/BotScreenshots/Franchises.png?raw=true "franchises")

