from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL 설정
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0000'
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM images")
    image_data = cur.fetchall()
    print("Image Data:", image_data)  # 디버깅을 위해 출력
    cur.execute("SELECT * FROM videos")
    video_data = cur.fetchall()
    print("Video Data:", video_data)  # 디버깅을 위해 출력
    return render_template('index.html', image_data=image_data, video_data=video_data)

@app.route('/search', methods=['POST'])
def search():
    search_keyword = request.form['searchInput'].lower()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM images WHERE title LIKE %s", ('%' + search_keyword + '%',))
    filtered_image_data = cur.fetchall()
    print("Filtered Image Data:", filtered_image_data)  # 디버깅을 위해 출력
    cur.execute("SELECT * FROM videos WHERE title LIKE %s", ('%' + search_keyword + '%',))
    filtered_video_data = cur.fetchall()
    print("Filtered Video Data:", filtered_video_data)  # 디버깅을 위해 출력
    return render_template('index.html', image_data=filtered_image_data, video_data=filtered_video_data)

if __name__ == '__main__':
    app.run(debug=True)
