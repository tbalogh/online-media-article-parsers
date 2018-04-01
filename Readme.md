# Article parser

This script creats a json represented model of an pure html content belongs to the article.

## Usage

`usage: article_parser.py [-h] -p PORTAL -t HTML_TEXT`

| potals | portal url |
|--------|:-----------|
| index  |  index.hu  | 
| origo  |  origo.hu  | 
| nnn    |  444.hu    | 
| nynyny |  888.hu    | 
| ps     | pestisracok.hu |

example usage:

`python article_parser.py -p index -t "$(< an_index_article.html)"`

## Articel model

Every article independently it's source shares the same structure, like:

```
"
{
    "id": ...,
    "portal": ...,
    "url": ...,
    "published_time": ...,
    "title": ...,
    "content": ...,
    "description": ..., #optional
    "author": ..., #optional
    "category": ..., #optional
    "tags": ..., #optional
    "description": ..., #optional
}
"
```

# Article model cleaner

This script "cleans" the article models so it fix invalid data such as missing values. One example is the missing publication time that sometimes can be extracted from the url.

`usage: article_model_cleaner.py [-h] -a ARTICLE_CONTENT`

example usage:

`python article_model_cleaner.py -a "$(< example_article_model.txt )"`

# Count missing data

This script counts the percentage of missing data by keys so it helps validate the "cleaness level" of your data.

`usage: missing_data_counter.py [-h] -m MODEL_FILES [MODEL_FILES ...]`

example usage:

`python missing_data_counter.py -m $(ls . | grep txt | tr '\n' ' ')`

example result:

`{'content': 0, 'published_time': 0, 'url': 0, 'author': 13, 'title': 0, 'description': 4, 'category': 0}`

