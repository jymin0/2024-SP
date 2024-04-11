from flask import Flask, request, redirect
 
app = Flask(__name__)
 
 
nextId = 4
topics = [
    {'id': 1, 'title': '오늘 추천 메뉴좀', 'body': '돈까스 VS 제육복음 선택좀'},
    {'id': 2, 'title': '휴강 안하나', 'body': '오늘은 집에서 쉬고싶다'},
    {'id': 3, 'title': '시험 날짜 나옴?', 'body': 'ㅇㅇ수업 시험날짜 나옴?'}
]
 
 
def template(contents, content, id=None):
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li><a href="/update/{id}/">글 수정</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="글 삭제"></form></li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">게시판</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">글 쓰기</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''
 
 
def getContents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags
 
 
@app.route('/')
def index():
    return template(getContents(), '<h2>게시판입니다</h2>욕설, 비방글은 자제해주세요.')
 
 
@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break
    return template(getContents(), f'<h2>{title}</h2>{body}', id)
 
 
@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET': 
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="제목"></p>
                <p><textarea name="body" placeholder="내용"></textarea></p>
                <p><input type="submit" value="올리기"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id': nextId, 'title': title, 'body': body}
        topics.append(newTopic)
        url = '/read/'+str(nextId)+'/'
        nextId = nextId + 1
        return redirect(url)
 
 
@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET': 
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break
        content = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="title" placeholder="title" value="{title}"></p>
                <p><textarea name="body" placeholder="body">{body}</textarea></p>
                <p><input type="submit" value="수정"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = '/read/'+str(id)+'/'
        return redirect(url)
 
 
@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')
 
 
app.run(debug=True)