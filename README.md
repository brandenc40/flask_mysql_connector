# Flask-MySQL-Connector

### Easy to use MySQL client for Flask apps.

#### Install

```
pip install flask-mysql-connector
```

#### Example Usage

```python
from flask import Flask
from flask_mysql_connector import MySQL, Params

app = Flask(__name__)

# params used for all connections
app.config[Params.MYSQL_USER] = 'root'
app.config[Params.MYSQL_DATABASE] = 'sys'

mysql = MySQL(app)

mysql2 = MySQL(
    app, 
    # creates key `mysql_db_2` instead of default of `mysql_db`
    ctx_key="2", 
    # params used for only this connection to override default
    connection_args={Params.MYSQL_DATABASE: "another_db"}
)

EXAMPLE_SQL = 'select * from sys.user_summary'


@app.route('/')
def new_cursor():
    cur = mysql.new_cursor(dictionary=True)
    cur.execute(EXAMPLE_SQL)
    output = cur.fetchall()
    response = app.response_class(
        response=str(output),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/connection')
def connection():
    conn = mysql2.connection
    cur = conn.cursor()
    cur.execute(EXAMPLE_SQL)
    output = cur.fetchall()
    response = app.response_class(
        response=str(output),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/easy_execute')
def easy_execute():
    df = mysql.execute_sql(EXAMPLE_SQL, to_pandas=True)
    response = app.response_class(
        response=str(df.to_dict()),
        status=200,
        mimetype='application/json'
    )
    return response


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
