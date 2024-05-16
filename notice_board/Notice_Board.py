from flask import Flask, request, redirect
import pymysql

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='root',
                       db='board_db',
                       charset='utf8',
                       cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

def template(content, categories, posts, post_id=None):
    categories_options = ''.join(
        [f'<option value="{category["id"]}">{category["name"]}</option>' for category in categories])
    posts_list = ''.join([f'<li><a href="/read/{post["id"]}/">{post["title"]}</a></li>' for post in posts])

    context_ui = ''
    if post_id is not None:
        context_ui = f'''
            <li><a href="/update/{post_id}/">글 수정</a></li>
            <li><form action="/delete/{post_id}/" method="POST"><input type="submit" value="글 삭제"></form></li>
        '''

    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">게시판</a></h1>
            <form action="/" method="GET">
                <select name="category">
                    <option value="">모든 카테고리</option>
                    {categories_options}
                </select>
                <input type="submit" value="필터">
            </form>
            <ul>
                {posts_list}
            </ul>
            {content}
            <ul>
                <li><a href="/create/">글 쓰기</a></li>
                {context_ui}
            </ul>
        </body>
    </html>
    '''


@app.route('/')
def index():
    category = request.args.get('category')
    cursor = conn.cursor()

    if category:
        cursor.execute("SELECT * FROM posts WHERE category_id=%s", (category,))
    else:
        cursor.execute("SELECT * FROM posts")

    posts = cursor.fetchall()
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    return template('<h2>게시판입니다</h2>욕설, 비방글은 자제해주세요.', categories, posts)


@app.route('/read/<int:id>/')
def read(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id=%s", (id,))
    post = cursor.fetchone()

    content = f'<h2>{post["title"]}</h2>{post["content"]}'
    return template(content, [], [post], id)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()

        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="제목"></p>
                <p><textarea name="content" placeholder="내용"></textarea></p>
                <p><select name="category">
                    {}
                </select></p>
                <p><input type="submit" value="올리기"></p>
            </form>
        '''.format(
            ''.join([f'<option value="{category["id"]}">{category["name"]}</option>' for category in categories]))

        return template(content, categories, [])
    elif request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category')

        if not title or not content or not category_id:
            return "모든 필드를 입력해주세요.", 400

        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (title, content, category_id) VALUES (%s, %s, %s)",
                       (title, content, category_id))
        conn.commit()

        return redirect('/')


@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts WHERE id=%s", (id,))
        post = cursor.fetchone()

        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()

        content = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="title" value="{post["title"]}" placeholder="제목"></p>
                <p><textarea name="content" placeholder="내용">{post["content"]}</textarea></p>
                <p><select name="category">
                    {get_categories_options(categories, post["category_id"])}
                </select></p>
                <p><input type="submit" value="수정"></p>
            </form>
        '''
        return template(content, categories, [post], id)
    elif request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category')

        cursor = conn.cursor()
        cursor.execute("UPDATE posts SET title=%s, content=%s, category_id=%s WHERE id=%s",
                       (title, content, category_id, id))
        conn.commit()

        return redirect(f'/read/{id}/')


@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id=%s", (id,))
    conn.commit()

    return redirect('/')

def get_categories_options(categories, selected_id):
    options = ''
    for category in categories:
        selected = 'selected' if category['id'] == selected_id else ''
        options += f'<option value="{category["id"]}" {selected}>{category["name"]}</option>'
    return options


if __name__ == "__main__":
    app.run(debug=True)
