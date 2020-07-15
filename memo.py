from flask import Flask, request
from functools import wraps
from flaskext.mysql import MySQL
import json

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'memo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


def json_formatted_request_body(f):
    @wraps(f)
    def validate(*args, **kwargs):
        try:
            request.json
        except Exception as e:
            print(e)
            return 'invalid json format', 400

        return f(*args, **kwargs)

    return validate


def login_required(f):
    @wraps(f)
    def authorize(*args, **kwargs):
        if 'name' in request.headers and 'password' in request.headers:
            try:
                name = request.headers['name']
                password = request.headers['password']

                conn = mysql.connect()
                cursor = conn.cursor()

                cursor.execute('SELECT COUNT(*) FROM user WHERE name = %s and password = %s', (name, password))
                count = cursor.fetchone()[0]

                if count > 0:
                    return f(*args, **kwargs)

            except Exception as e:
                print(e)
                return 'unauthorized', 401

        return 'unauthorized', 401

    return authorize


@app.route('/memo/write', methods=['POST'])
@json_formatted_request_body
@login_required
def memo_write():
    try:
        name = request.headers['name']
        password = request.headers['password']

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM user WHERE name = %s and password = %s', (name, password))
        user_id = int(cursor.fetchone()[0])

        if 'title' in request.json and 'body' in request.json:
            title = request.json['title']
            body = request.json['body']

            cursor.execute('INSERT INTO memo (author_id, title, body) VALUE (%s, %s, %s)', (int(user_id), title, body))
            conn.commit()

        else:
            return 'bad request', 400

        return 'ok', 201

    except Exception as e:
        print(e)
        return 'server error', 500


@app.route('/memo/update', methods=['POST'])
@json_formatted_request_body
@login_required
def memo_update():
    try:
        name = request.headers['name']
        password = request.headers['password']

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM user WHERE name = %s and password = %s', (name, password))
        user_id = int(cursor.fetchone()[0])

        if 'memo_id' in request.json and 'title' in request.json and 'body' in request.json:
            title = request.json['title']
            body = request.json['body']
            memo_id = request.json['memo_id']

            cursor.execute('SELECT COUNT(*) FROM memo WHERE author_id = %s and id = %s', (int(user_id), int(memo_id)))
            count = int(cursor.fetchone()[0])

            if count <= 0:
                return 'bad request', 401

            cursor.execute('UPDATE memo SET title=%s, body=%s where id=%s', (title, body, int(memo_id)))
            conn.commit()

        else:
            return 'bad request', 400

        return 'ok', 200

    except Exception as e:
        print(e)
        return 'server error', 500


@app.route('/memo/list', methods=['POST'])
@json_formatted_request_body
@login_required
def memo_list():
    try:
        name = request.headers['name']
        password = request.headers['password']

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM user WHERE name = %s and password = %s', (name, password))
        user_id = int(cursor.fetchone()[0])

        cursor.execute('SELECT * FROM memo WHERE author_id = %s and active = 1', int(user_id))
        memos = cursor.fetchall()

        responses = [{
            'created': str(iter[1]),
            'updated': str(iter[2]),
            'title': iter[4],
            'body': iter[5]
        } for iter in memos]

        print(json.dumps(responses))

        return json.dumps(responses), 200

    except Exception as e:
        print(e)
        return 'server error', 500


@app.route('/user/signin', methods=['POST'])
@login_required
def signin():
    return '', 204


@app.route('/user/signup', methods=['POST'])
@json_formatted_request_body
def signup():
    if 'name' in request.json and 'password' in request.json:
        try:
            data = request.json
            name = data['name']
            password = data['password']

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM user WHERE name = %s', name)
            count = cursor.fetchone()[0]

            if count > 0:
                return 'name already exists', 403

            cursor.execute('INSERT INTO user (name, password) VALUE (%s, %s)', (name, password))
            conn.commit()
            return 'signup success', 201

        except Exception as e:
            print(e)
            return 'server error', 500

    return 'bad request', 400


if __name__ == '__main__':
    app.debug = True
    app.run()
