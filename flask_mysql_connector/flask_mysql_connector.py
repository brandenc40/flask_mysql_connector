from typing import Dict

import pandas as pd
from flask import Flask, current_app
from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import MySQLCursor

from .params import Params

try:
    from flask import _app_ctx_stack as _ctx_stack
except ImportError:
    from flask import _request_ctx_stack as _ctx_stack

# https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
# key = mysql connect arg key, value = flask config key
MYSQL_ARGS = {
    'user': Params.MYSQL_USER,
    'password': Params.MYSQL_PASSWORD,
    'database': Params.MYSQL_DATABASE,
    'host': Params.MYSQL_HOST,
    'port': Params.MYSQL_PORT,
    'unix_socket': Params.MYSQL_UNIX_SOCKET,
    'auth_plugin': Params.MYSQL_AUTH_PLUGIN,
    'use_unicode': Params.MYSQL_USE_UNICODE,
    'charset': Params.MYSQL_CHARSET,
    'collation': Params.MYSQL_COLLATION,
    'autocommit': Params.MYSQL_AUTOCOMMIT,
    'time_zone': Params.MYSQL_TIME_ZONE,
    'sql_mode': Params.MYSQL_SQL_MODE,
    'get_warnings': Params.MYSQL_GET_WARNINGS,
    'raise_on_warnings': Params.MYSQL_RAISE_ON_WARNINGS,
    'connection_timeout': Params.MYSQL_CONNECTION_TIMEOUT,
    'client_flags': Params.MYSQL_CLIENT_FLAGS,
    'buffered': Params.MYSQL_BUFFERED,
    'raw': Params.MYSQL_RAW,
    'consume_results': Params.MYSQL_CONSUME_RESULTS,
    'ssl_ca': Params.MYSQL_SSL_CA,
    'ssl_cert': Params.MYSQL_SSL_CERT,
    'ssl_disabled': Params.MYSQL_SSL_DISABLED,
    'ssl_key': Params.MYSQL_SSL_KEY,
    'ssl_verify_cert': Params.MYSQL_SSL_VERIFY_CERT,
    'ssl_verify_identity': Params.MYSQL_SSL_VERIFY_IDENTITY,
    'force_ipv6': Params.MYSQL_FORCE_IPV6,
    'dsn': Params.MYSQL_DSN,
    'pool_name': Params.MYSQL_POOL_NAME,
    'pool_size': Params.MYSQL_POOL_SIZE,
    'pool_reset_session': Params.MYSQL_POOL_RESET_SESSION,
    'compress': Params.MYSQL_COMPRESS,
    'converter_class': Params.MYSQL_CONVERTER_CLASS,
    'failover': Params.MYSQL_FAILOVER,
    'option_files': Params.MYSQL_OPTION_FILES,
    'allow_local_infile': Params.MYSQL_ALLOW_LOCAL_INFILE,
    'use_pure': Params.MYSQL_USE_PURE
}


class MySQL:
    def __init__(self, app: Flask = None, ctx_key: str = None, connection_args: Dict[str, str] = None):
        """
        :param flask.Flask app:
        :param str ctx_key: The unique key used for storing this mysql connection in the app context stack. This is
            useful if you are using two separate MySQL connections so they don't fight over the same ctx attribute.
                e.g.
                    mysql = MySQL(app, ctx_key="num1")
                    mysql2 = MySQL(app, ctx_key="num2")
        :param dict[str, str] connection_args: Args to be used in mysql.connector.connect(). Overrides any args found
            in the Flask app config.
        """
        self._arg_overrides = connection_args
        self._key = 'mysql_db_' + ctx_key if ctx_key else 'mysql_db'

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        app.teardown_request(self._teardown)

    def _connect(self) -> MySQLConnection:
        connect_args = {}
        config = self.app.config if self.app else current_app.config
        for k, v in MYSQL_ARGS.items():
            val = config.get(v)
            if val:
                connect_args[k] = val

        if self._arg_overrides:
            connect_args.update(self._arg_overrides)

        return connect(**connect_args)

    def _teardown(self, _):
        ctx = _ctx_stack.top
        if hasattr(ctx, self._key):
            getattr(ctx, self._key).close()

    @property
    def connection(self) -> MySQLConnection:
        ctx = _ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'mysql_db'):
                setattr(ctx, self._key, self._connect())
            return getattr(ctx, self._key)

    def new_cursor(self, **kwargs) -> MySQLCursor:
        conn = self.connection
        if conn:
            return conn.cursor(**kwargs)

    def execute_sql(self, sql: str, to_pandas: bool = False, dictionary: bool = False):
        """
        :param str sql:
        :param boolean to_pandas:
        :param boolean dictionary:
        :return pd.DataFrame|list:
        """
        cursor = self.new_cursor(dictionary=dictionary)
        cursor.execute(sql)
        if to_pandas:
            out = pd.DataFrame(cursor.fetchall(), columns=cursor.column_names)
        else:
            out = cursor.fetchall()
        cursor.close()
        return out
