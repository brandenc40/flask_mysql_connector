from flask import Flask
import sys
sys.path.append('../')
from flask_mysql_connector import MySQL

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE'] = 'sys'
mysql = MySQL(app)

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
    conn = mysql.connection
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
