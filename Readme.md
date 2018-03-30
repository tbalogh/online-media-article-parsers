# Usage

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