from flask import Flask
from flask_mysql_connector import MySQL

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE'] = 'sys'
mysql = MySQL(app)

_example_sql = 'select * from sys.user_summary'


@app.route('/new_cursor')
def new_cursor():
    cur = mysql.new_cursor(dictionary=True)
    cur.execute(_example_sql)
    output = cur.fetchall()
    return str(output)


@app.route('/connection')
def connection():
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute(_example_sql)
    output = cur.fetchall()
    return str(output)


@app.route('/easy_execute')
def easy_execute():
    df = mysql.execute_sql(_example_sql, to_pandas=True)
    return str(df.to_dict())


if __name__ == '__main__':
    app.run(debug=True)