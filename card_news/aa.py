from flask import Flask, render_template, request, redirect
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
    sort_by = request.args.get('sort_by', 'created_at')  # Default sorting by created_at
    sort_order = request.args.get('sort_order', 'desc')  # Default descending order

    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM images ORDER BY {sort_by} {sort_order}")
    image_data = cur.fetchall()
    cur.execute(f"SELECT * FROM videos ORDER BY {sort_by} {sort_order}")
    video_data = cur.fetchall()
    return render_template('index.html', image_data=image_data, video_data=video_data, sort_by=sort_by, sort_order=sort_order)

@app.route('/search', methods=['POST'])
def search():
    search_keyword = request.form['searchInput'].lower()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM images WHERE title LIKE %s", ('%' + search_keyword + '%',))
    filtered_image_data = cur.fetchall()
    cur.execute("SELECT * FROM videos WHERE title LIKE %s", ('%' + search_keyword + '%',))
    filtered_video_data = cur.fetchall()
    return render_template('index.html', image_data=filtered_image_data, video_data=filtered_video_data)

@app.route('/increment_view/<int:item_id>')
def increment_view(item_id):
    cur = mysql.connection.cursor()
    # Determine if the item is an image or video based on its ID
    cur.execute("SELECT * FROM images")
    image_data = cur.fetchall()
    if item_id <= len(image_data):
        cur.execute("UPDATE images SET view_count = view_count + 1 WHERE id = %s", (item_id,))
    else:
        cur.execute("SELECT * FROM videos")
        video_data = cur.fetchall()
        video_id = item_id - len(image_data)
        cur.execute("UPDATE videos SET view_count = view_count + 1 WHERE id = %s", (video_id,))
    mysql.connection.commit()
    cur.close()
    # Redirect to the Instagram link associated with the item
    if item_id <= len(image_data):
        return redirect(image_data[item_id - 1][2])
    else:
        return redirect(video_data[video_id - 1][2])

if __name__ == '__main__':
    app.run(debug=True)
