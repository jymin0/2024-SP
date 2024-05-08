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
@app.route('/api/timetable')
def get_timetable():
    try:
        with connection.cursor() as cursor:
            # timetable 테이블에서 데이터 가져오기
            sql = "SELECT * FROM timetable"
            cursor.execute(sql)
            timetable = cursor.fetchall()
            return jsonify({'timetable': timetable})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/api/update_timetable', methods=['POST'])
def update_timetable():
    try:
        data = request.get_json()
        timetable_id = data['id']
        day = data['day']
        new_value = data['value']
        with connection.cursor() as cursor:
            # timetable 테이블에서 해당 id와 day에 대한 값을 업데이트
            sql = f"UPDATE timetable SET {day} = %s WHERE id = %s"
            cursor.execute(sql, (new_value, timetable_id))
            connection.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/')
def index():
    return render_template('timetable.html')

if __name__ == '__main__':
    app.run(debug=True)