import mysql.connector
import pandas as pd
from flask import _app_ctx_stack, current_app


class MySQL(object):
    def __init__(self, app=None, connection_args=None):
        """
        :param flask.Flask app:
        :param dict[str, str] connection_args: Args to be used in mysql.connector.connect(). Overrides any args found
            in the Flask app config.
        """
        self.connection_args = connection_args
        self.app = app
        if app:
            app.teardown_appcontext(self._teardown)

    def _connect(self):
        connect_args = {}

        # https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        if current_app.config.get('MYSQL_USER'):
            connect_args['user'] = current_app.config['MYSQL_USER']
        if current_app.config.get('MYSQL_PASSWORD'):
            connect_args['password'] = current_app.config['MYSQL_PASSWORD']
        if current_app.config.get('MYSQL_DATABASE'):
            connect_args['database'] = current_app.config['MYSQL_DATABASE']
        if current_app.config.get('MYSQL_HOST'):
            connect_args['host'] = current_app.config['MYSQL_HOST']
        if current_app.config.get('MYSQL_PORT'):
            connect_args['port'] = current_app.config['MYSQL_PORT']
        if current_app.config.get('MYSQL_UNIX_SOCKET'):
            connect_args['unix_socket'] = current_app.config['MYSQL_UNIX_SOCKET']
        if current_app.config.get('MYSQL_AUTH_PLUGIN'):
            connect_args['auth_plugin'] = current_app.config['MYSQL_AUTH_PLUGIN']
        if current_app.config.get('MYSQL_USE_UNICODE'):
            connect_args['use_unicode'] = current_app.config['MYSQL_USE_UNICODE']
        if current_app.config.get('MYSQL_CHARSET'):
            connect_args['charset'] = current_app.config['MYSQL_CHARSET']
        if current_app.config.get('MYSQL_COLLATION'):
            connect_args['collation'] = current_app.config['MYSQL_COLLATION']
        if current_app.config.get('MYSQL_AUTOCOMMIT'):
            connect_args['autocommit'] = current_app.config['MYSQL_AUTOCOMMIT']
        if current_app.config.get('MYSQL_TIME_ZONE'):
            connect_args['time_zone'] = current_app.config['MYSQL_TIME_ZONE']
        if current_app.config.get('MYSQL_SQL_MODE'):
            connect_args['sql_mode'] = current_app.config['MYSQL_SQL_MODE']
        if current_app.config.get('MYSQL_GET_WARNINGS'):
            connect_args['get_warnings'] = current_app.config['MYSQL_GET_WARNINGS']
        if current_app.config.get('MYSQL_RAISE_ON_WARNINGS'):
            connect_args['raise_on_warnings'] = current_app.config['MYSQL_RAISE_ON_WARNINGS']
        if current_app.config.get('MYSQL_CONNECTION_TIMEOUT'):
            connect_args['connection_timeout'] = current_app.config['MYSQL_CONNECTION_TIMEOUT']
        if current_app.config.get('MYSQL_CLIENT_FLAGS'):
            connect_args['client_flags'] = current_app.config['MYSQL_CLIENT_FLAGS']
        if current_app.config.get('MYSQL_BUFFERED'):
            connect_args['buffered'] = current_app.config['MYSQL_BUFFERED']
        if current_app.config.get('MYSQL_RAW'):
            connect_args['raw'] = current_app.config['MYSQL_RAW']
        if current_app.config.get('MYSQL_CONSUME_RESULTS'):
            connect_args['consume_results'] = current_app.config['MYSQL_CONSUME_RESULTS']
        if current_app.config.get('MYSQL_SSL_CA'):
            connect_args['ssl_ca'] = current_app.config['MYSQL_SSL_CA']
        if current_app.config.get('MYSQL_SSL_CERT'):
            connect_args['ssl_cert'] = current_app.config['MYSQL_SSL_CERT']
        if current_app.config.get('MYSQL_SSL_DISABLED'):
            connect_args['ssl_disabled'] = current_app.config['MYSQL_SSL_DISABLED']
        if current_app.config.get('MYSQL_SSL_KEY'):
            connect_args['ssl_key'] = current_app.config['MYSQL_SSL_KEY']
        if current_app.config.get('MYSQL_SSL_VERIFY_CERT'):
            connect_args['ssl_verify_cert'] = current_app.config['MYSQL_SSL_VERIFY_CERT']
        if current_app.config.get('MYSQL_SSL_VERIFY_IDENTITY'):
            connect_args['ssl_verify_identity'] = current_app.config['MYSQL_SSL_VERIFY_IDENTITY']
        if current_app.config.get('MYSQL_FORCE_IPV6'):
            connect_args['force_ipv6'] = current_app.config['MYSQL_FORCE_IPV6']
        if current_app.config.get('MYSQL_DSN'):
            connect_args['dsn'] = current_app.config['MYSQL_DSN']
        if current_app.config.get('MYSQL_POOL_NAME'):
            connect_args['pool_name'] = current_app.config['MYSQL_POOL_NAME']
        if current_app.config.get('MYSQL_POOL_SIZE'):
            connect_args['pool_size'] = current_app.config['MYSQL_POOL_SIZE']
        if current_app.config.get('MYSQL_POOL_RESET_SESSION'):
            connect_args['pool_reset_session'] = current_app.config['MYSQL_POOL_RESET_SESSION']
        if current_app.config.get('MYSQL_COMPRESS'):
            connect_args['compress'] = current_app.config['MYSQL_COMPRESS']
        if current_app.config.get('MYSQL_CONVERTER_CLASS'):
            connect_args['converter_class'] = current_app.config['MYSQL_CONVERTER_CLASS']
        if current_app.config.get('MYSQL_FAILOVER'):
            connect_args['failover'] = current_app.config['MYSQL_FAILOVER']
        if current_app.config.get('MYSQL_OPTION_FILES'):
            connect_args['option_files'] = current_app.config['MYSQL_OPTION_FILES']
        if current_app.config.get('MYSQL_ALLOW_LOCAL_INFILE'):
            connect_args['allow_local_infile'] = current_app.config['MYSQL_ALLOW_LOCAL_INFILE']
        if current_app.config.get('MYSQL_USE_PURE'):
            connect_args['use_pure'] = current_app.config['MYSQL_USE_PURE']

        # overrides any args from config
        if self.connection_args:
            connect_args.update(self.connection_args)

        return mysql.connector.connect(**connect_args)

    def _teardown(self, _):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'mysql_db'):
            ctx.mysql_db.close()

    @property
    def connection(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'mysql_db'):
                ctx.mysql_db = self._connect()
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
        cursor.close()
        return out
