# Code Foo Backend Project
For Code Foo IGN
Using the .csv file given, I created a Backend server on Flask using SQLite as the database

## Usage

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


