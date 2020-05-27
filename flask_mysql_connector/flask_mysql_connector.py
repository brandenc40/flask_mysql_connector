import pandas as pd
from flask import _app_ctx_stack, current_app
from mysql.connector import MySQLConnection


class MySQL(object):
    def __init__(self, app=None, connection_args=None):
        """
        :param flask.Flask app:
        :param dict[str, str] connection_args: Args to be used in MySQLConnection. Overrides any args found 
            in the Flask app config. 
        """
        self.connection_args = connection_args
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        :param flask.Flask app:
        """
        # https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        app.config.setdefault('MYSQL_USER', None)
        app.config.setdefault('MYSQL_PASSWORD', None)
        app.config.setdefault('MYSQL_DATABASE', None)
        app.config.setdefault('MYSQL_HOST', '127.0.0.1')
        app.config.setdefault('MYSQL_PORT', 3306)
        app.config.setdefault('MYSQL_UNIX_SOCKET', None)
        app.config.setdefault('MYSQL_AUTH_PLUGIN', None)
        app.config.setdefault('MYSQL_USE_UNICODE', True)
        app.config.setdefault('MYSQL_CHARSET', 'utf8')

        # todo version
        app.config.setdefault('MYSQL_COLLATION', 'utf8mb4_general_ai_ci')
        app.config.setdefault('MYSQL_AUTOCOMMIT', False)
        app.config.setdefault('MYSQL_TIME_ZONE', None)
        app.config.setdefault('MYSQL_SQL_MODE', None)
        app.config.setdefault('MYSQL_GET_WARNINGS', False)
        app.config.setdefault('MYSQL_RAISE_ON_WARNINGS', False)
        app.config.setdefault('MYSQL_CONNECTION_TIMEOUT', None)
        app.config.setdefault('MYSQL_CLIENT_FLAGS', None)
        app.config.setdefault('MYSQL_BUFFERED', False)
        app.config.setdefault('MYSQL_RAW', False)
        app.config.setdefault('MYSQL_CONSUME_RESULTS', False)
        app.config.setdefault('MYSQL_SSL_CA', None)
        app.config.setdefault('MYSQL_SSL_CERT', None)
        app.config.setdefault('MYSQL_SSL_DISABLED', False)
        app.config.setdefault('MYSQL_SSL_KEY', None)
        app.config.setdefault('MYSQL_SSL_VERIFY_CERT', False)
        app.config.setdefault('MYSQL_SSL_VERIFY_IDENTITY', False)
        app.config.setdefault('MYSQL_FORCE_IPV6', False)
        app.config.setdefault('MYSQL_DSN', None)
        app.config.setdefault('MYSQL_POOL_NAME', None)
        app.config.setdefault('MYSQL_POOL_SIZE', 5)
        app.config.setdefault('MYSQL_POOL_RESET_SESSION', True)
        app.config.setdefault('MYSQL_COMPRESS', False)
        app.config.setdefault('MYSQL_CONVERTER_CLASS', None)
        app.config.setdefault('MYSQL_FAILOVER', None)
        app.config.setdefault('MYSQL_OPTION_FILES', None)
        option_groups = ['client', 'connector_python']
        app.config.setdefault('MYSQL_OPTION_GROUPS', option_groups)
        app.config.setdefault('MYSQL_ALLOW_LOCAL_INFILE', True)
        app.config.setdefault('MYSQL_USE_PURE', False)  # todo version

        app.teardown_appcontext(self.teardown)

    def connect(self):
        connect_args = {
            'user': current_app.config['MYSQL_USER'],
            'password': current_app.config['MYSQL_PASSWORD'],
            'database': current_app.config['MYSQL_DATABASE'],
            'host': current_app.config['MYSQL_HOST'],
            'port': current_app.config['MYSQL_PORT'],
            'unix_socket': current_app.config['MYSQL_UNIX_SOCKET'],
            'auth_plugin': current_app.config['MYSQL_AUTH_PLUGIN'],
            'use_unicode': current_app.config['MYSQL_USE_UNICODE'],
            'charset': current_app.config['MYSQL_CHARSET'],
            'collation': current_app.config['MYSQL_COLLATION'],
            'autocommit': current_app.config['MYSQL_AUTOCOMMIT'],
            'time_zone': current_app.config['MYSQL_TIME_ZONE'],
            'sql_mode': current_app.config['MYSQL_SQL_MODE'],
            'get_warnings': current_app.config['MYSQL_GET_WARNINGS'],
            'raise_on_warnings': current_app.config['MYSQL_RAISE_ON_WARNINGS'],
            'connection_timeout': current_app.config['MYSQL_CONNECTION_TIMEOUT'],
            'client_flags': current_app.config['MYSQL_CLIENT_FLAGS'],
            'buffered': current_app.config['MYSQL_BUFFERED'],
            'raw': current_app.config['MYSQL_RAW'],
            'consume_results': current_app.config['MYSQL_CONSUME_RESULTS'],
            'ssl_ca': current_app.config['MYSQL_SSL_CA'],
            'ssl_cert': current_app.config['MYSQL_SSL_CERT'],
            'ssl_disabled': current_app.config['MYSQL_SSL_DISABLED'],
            'ssl_key': current_app.config['MYSQL_SSL_KEY'],
            'ssl_verify_cert': current_app.config['MYSQL_SSL_VERIFY_CERT'],
            'ssl_verify_identity': current_app.config['MYSQL_SSL_VERIFY_IDENTITY'],
            'force_ipv6': current_app.config['MYSQL_FORCE_IPV6'],
            'dsn': current_app.config['MYSQL_DSN'],
            'pool_name': current_app.config['MYSQL_POOL_NAME'],
            'pool_size': current_app.config['MYSQL_POOL_SIZE'],
            'pool_reset_session': current_app.config['MYSQL_POOL_RESET_SESSION'],
            'compress': current_app.config['MYSQL_COMPRESS'],
            'converter_class': current_app.config['MYSQL_CONVERTER_CLASS'],
            'failover': current_app.config['MYSQL_FAILOVER'],
            'option_files': current_app.config['MYSQL_OPTION_FILES'],
            'option_groups': current_app.config['MYSQL_OPTION_GROUPS'],
            'allow_local_infile': current_app.config['MYSQL_ALLOW_LOCAL_INFILE'],
            'use_pure': current_app.config['MYSQL_USE_PURE']
        }

        # overrides any args from config
        connect_args.update(self.connection_args)

        return MySQLConnection(**connect_args)

    def teardown(self, _):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'mysql_db'):
            ctx.mysql_db.close()

    @property
    def connection(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'mysql_db'):
                ctx.mysql_db = self.connect()
            return ctx.mysql_db

    def new_cursor(self, **kwargs):
        conn = self.connection
        if conn:
            return conn.cursor(**kwargs)

    def execute_sql(self, sql, to_pandas=False, dictionary=False):
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
        return out
