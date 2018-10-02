# Article parser

This script creats a json represented model of an pure html content belongs to the article.

## Install dependencies

Use [pipenv](https://pipenv.readthedocs.io/en/latest/) for installing dependencies.

## Usage

`article_parser.py [-h] -p PORTAL -t HTML_TEXT`

Accepted values for PORTAL: [index, origo, nnn, nynyny, ps]. Find the portal url for those values in the table below:

| potals | portal url |
|--------|:-----------|
| index  |  index.hu  | 
| origo  |  origo.hu  | 
| nnn    |  444.hu    | 
| nynyny |  888.hu    | 
| ps     | pestisracok.hu |

example usage:

`python article_parser.py -p index -t "$(< /path/to/index/article.html)"`

## Articel model

Every article shares the same structure (independently from its source), like:

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

## Samples

You can try out the parser with samples (replace \<portal\>):

usage:

```find samples/<portal> -exec sh -c 'python article_parser.py -p <portal> -t "$(<$1)"' -- {} \; ```

exapmle:

```find samples/index -exec sh -c 'python article_parser.py -p index -t "$(<$1)"' -- {} \; ```



# Article model cleaner

This script "cleans" the article models so it fix invalid data such as missing values. One example is the missing publication time that sometimes can be extracted from the url.

usage:

`article_model_cleaner.py [-h] -a ARTICLE_CONTENT`

example:

`python article_model_cleaner.py -a "$(< path/to/an/article.model )"`

# Count missing data

This script counts the percentage of missing data by keys so it helps validate the "cleaness level" of your data.

usage:

`missing_data_counter.py [-h] -m MODEL_FILES [MODEL_FILES ...]`

example:

`python missing_data_counter.py -m $(ls . | grep txt | tr '\n' ' ')`

example result:

`{'content': 0, 'published_time': 0, 'url': 0, 'author': 13, 'title': 0, 'description': 4, 'category': 0}`

