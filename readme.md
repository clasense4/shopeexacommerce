# Shopee X Acommerce

Example repositories how to integrate between [Shopee API](https://partner.shopeemobile.com) and [Acommerce API](https://acommerce.atlassian.net/wiki/spaces/PA/pages). Api Mock is using [mockable.io](mockable.io).

## Installation

Make sure you have this requirement :

- Python 2.7.14
- Virtualenv
- Virtualenvwrapper (optional)

```shell
virtualenv -p /usr/local/bin/python2.7 ~/Envs/shopeexacommerce
# If virtualenvwrapper is installed
workon shopeexacommerce

# If virtualenvwrapper not installed
source ~/Envs/shopeexacommerce/bin/activate

pip install -r requirements.txt
```

## Configuration

Change necessary value at `src/settings.py`.

## Run

```
$> python shopeexacommerce.py
```
The script will return dictionary which has :
- code : `201`
- data : `Python Dict`

## Test

### No Coverage

```
$> nosetests test/test_*

.cat: token.txt: No such file or directory
.cat: token.txt: No such file or directory
...cat: token.txt: No such file or directory
.cat: token.txt: No such file or directory
....................
----------------------------------------------------------------------
Ran 26 tests in 15.637s
```

### With Coverage

```
$> nosetests test/test_* --cover-package=src --with-coverage --cover-html

..cat: token.txt: No such file or directory
...cat: token.txt: No such file or directory
.cat: token.txt: No such file or directory
....................
Name                        Stmts   Miss  Cover
-----------------------------------------------
src/__init__.py                 0      0   100%
src/acommerce_api.py           53      0   100%
src/settings.py                 8      0   100%
src/shopee_api.py              38      0   100%
src/shopee_transformer.py      64      0   100%
-----------------------------------------------
TOTAL                         163      0   100%
----------------------------------------------------------------------
Ran 26 tests in 15.742s

OK
```

New directory called `cover` is located at main project directory.