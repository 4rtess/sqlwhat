# sqlwhat

[![Build Status](https://travis-ci.org/datacamp/sqlwhat.svg?branch=master)](https://travis-ci.org/datacamp/sqlwhat)

Reference
---------

* API Docs: https://sqlwhat.readthedocs.io
* AST viewer: https://sqlwhat-viewer.herokuapp.com
* Example DataCamp Course: https://github.com/datacamp/courses-sql-test

Raising issues with how SQL is parsed
-------------------------------------

Please raise an issue on the respsective parser repo:

* [antlr-tsql](https://github.com/datacamp/antlr-tsql)
* [antlr-psql](https://github.com/datacamp/antlr-plsql)

Setup ANTLR grammar
-------------------

```
docker run -it -v ${PWD}:/output $CONTAINER\_ID /bin/bash
# inside container
cd /output
antlr4 -Dlanguage=Python3 $GRAMMAR_FILE.g4
```

Running unit tests
------------------

In order to install psycopg2 in a virtualenv, I [needed to run](http://stackoverflow.com/a/39244687/1144523)..

```
env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install --no-cache psycopg2
```
