from flask import Flask, jsonify, render_template, request
import pymysql

app = Flask(__name__)

# MySQL 연결 설정
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='seo1005404@',
                             database='timetb',
                             cursorclass=pymysql.cursors.DictCursor)

# Flask 엔드포인트 설정
@app.route('/api/timetable', methods=['GET'])
def get_timetable():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM timetable")
        result = cursor.fetchall()
    return jsonify({'timetable': result})

@app.route('/api/update_timetable', methods=['POST'])
def update_timetable():
    try:
        data = request.json
        with connection.cursor() as cursor:
            sql = "UPDATE timetable SET {} = %s WHERE id = %s".format(data['day'].lower())
            cursor.execute(sql, (data['value'], data['id']))
        connection.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/notes', methods=['GET'])
def get_notes():
    with connection.cursor() as cursor:
        cursor.execute("SELECT notes FROM notes_table WHERE id = 1")
        result = cursor.fetchone()
    return jsonify({'notes': result['notes']})

@app.route('/api/save_notes', methods=['POST'])
def save_notes():
    try:
        data = request.json
        with connection.cursor() as cursor:
            sql = "UPDATE notes_table SET notes = %s WHERE id = 1"
            cursor.execute(sql, (data['notes'],))
        connection.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/')
def index():
    return render_template('timetable.html')

if __name__ == '__main__':
    app.run(debug=True)