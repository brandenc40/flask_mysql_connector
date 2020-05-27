# Flask-MySQL-Connector

### Easy to use MySQL client for Flask apps.

#### Install

```
pip install flask-mysql-connector
```

#### Example Usage

```python
from flask import Flask
from flask_mysql_connector import MySQL

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE'] = 'sys'
mysql = MySQL(app)

EXAMPLE_SQL = 'select * from sys.user_summary'


# using the new_cursor() method
@app.route('/new_cursor')
def new_cursor():
    cur = mysql.new_cursor(dictionary=True)
    cur.execute(EXAMPLE_SQL)
    output = cur.fetchall()
    return str(output)


# using the connection property
@app.route('/connection')
def connection():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(EXAMPLE_SQL)
    output = cur.fetchall()
    return str(output)


# using the execute_sql() method to easily
# select sql and optionally output to Pandas
@app.route('/easy_execute')
def easy_execute():
    df = mysql.execute_sql(EXAMPLE_SQL, to_pandas=True)
    return str(df.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
```

#### Availble Config Params

| Param                     | Default Value |
| ------------------------- | ------------- |
| MYSQL_USER                |               |
| MYSQL_PASSWORD            |               |
| MYSQL_DATABASE            |               |
| MYSQL_HOST                | 127.0.0.1     |
| MYSQL_PORT                | 3306          |
| MYSQL_UNIX_SOCKET         |               |
| MYSQL_AUTH_PLUGIN         |               |
| MYSQL_USE_UNICODE         | TRUE          |
| MYSQL_CHARSET             | utf8          |
| MYSQL_COLLATION           |               |
| MYSQL_AUTOCOMMIT          | FALSE         |
| MYSQL_TIME_ZONE           |               |
| MYSQL_SQL_MODE            |               |
| MYSQL_GET_WARNINGS        | FALSE         |
| MYSQL_RAISE_ON_WARNINGS   | FALSE         |
| MYSQL_CONNECTION_TIMEOUT  |               |
| MYSQL_CLIENT_FLAGS        |               |
| MYSQL_BUFFERED            | FALSE         |
| MYSQL_RAW                 | FALSE         |
| MYSQL_CONSUME_RESULTS     | FALSE         |
| MYSQL_SSL_CA              |               |
| MYSQL_SSL_CERT            |               |
| MYSQL_SSL_DISABLED        | FALSE         |
| MYSQL_SSL_KEY             |               |
| MYSQL_SSL_VERIFY_CERT     | FALSE         |
| MYSQL_SSL_VERIFY_IDENTITY | FALSE         |
| MYSQL_FORCE_IPV6          | FALSE         |
| MYSQL_DSN                 |               |
| MYSQL_POOL_NAME           |               |
| MYSQL_POOL_SIZE           | 5             |
| MYSQL_POOL_RESET_SESSION  | TRUE          |
| MYSQL_COMPRESS            | FALSE         |
| MYSQL_CONVERTER_CLASS     |               |
| MYSQL_FAILOVER            |               |
| MYSQL_OPTION_FILES        |               |
| MYSQL_OPTION_GROUPS       |               |
| MYSQL_ALLOW_LOCAL_INFILE  | TRUE          |
| MYSQL_USE_PURE            |               |
