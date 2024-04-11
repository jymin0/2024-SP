from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route("/") #도메인
def index():
    return send_from_directory('THEME', 'index.html')

@app.route('/<path:name>') #도메인/css/b.scc
def start(name):
    return send_from_directory('THEME', name)

# from flask import Flask, send_from_directory, request, jsonify
# import pymysql, atexit, pymysql.cursors

# app = Flask(__name__)

# accepted_ip_list = ['192.168.0.1', '10.0.0.1', '127.0.0.1']  # 관리자 접근 허용된 IP 목록

# # MySQL 데이터베이스와 연결
# conn = pymysql.connect(
#     host='localhost',  #데이터베이스가 존재하는 IP
#     user='sourceplay',  #데이터베이스 사용자 아이디
#     password='sourceplay1134#@',  #데이터베이스 사용자 패스워드
#     db='myblog',    #db 이름
#     charset='utf8mb4',   #문자열 인코딩 종류
# )

# def check_ip(client_ip, ip_list):   #아이피 체크하기... 허용 IP에 포함된 경우는 True 반환
#     if client_ip in ip_list:
#         return True
#     else:
#         return False


# def exit_process():   #마지막에는 Mysql Connection 닫아주기 (메모리 반환하여 효율적)
#     conn.close();
#     conn = None

# atexit.register(exit_process)

# @app.route("/")  #메인 페이지로서 도메인만(예:localhost) 입력시 이곳으로 들어옴
# def index():
#     return send_from_directory('THEME', "index.html")  #도메인/THEME/index.html 내용을 클라이언트에 보내줌


# @app.route('/<path:name>')   #특정 파일 요청 시 그 경로에 맞는 파일을 보내줌. 
# def start(name):
#     return send_from_directory('THEME', name)  #예: 도메인/css/b.css를 요청하면..  도메인/THEME/css/b.css 내용을 보내줌

# @app.route('/save', methods=['POST'])  #게시글 저장
# def save_post():
#     if check_ip(request.remote_addr, accepted_ip_list) == False:  #허용되지 않은 IP라면 접근 막기
#         return jsonify({"error": "Error occurred."}), 500    


#     # POST 요청으로 받은 데이터를 변수에 저장
#     title = request.form['title']  #제목 받기
#     content = request.form['content']  #내용 받기

#     # 데이터 삽입 쿼리 실행
#     with conn.cursor() as cursor:
#         sql = "INSERT INTO post (title, content) VALUES (%s, %s)"   #받은 게시글을 Mysql에 넣기
#         cursor.execute(sql, (title, content))
#         conn.commit()

#     cursor.close()

#     return "OK"    

# @app.route('/get_posts', methods=['GET'])  #게시글 목록 가져오기
# def get_posts():
#     try:
#         page = request.args.get('page', 1, type=int)   #페이지 기반으로 가져옴
#         per_page = 10
#         start_index = (page - 1) * per_page

#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         # 총 게시물 수 구하기
#         cursor.execute("SELECT COUNT(*) as cnt FROM post")
#         total_count = cursor.fetchone()["cnt"]

#         # start_index + per_page = end_index
#         end_index = start_index + per_page
#         if end_index > total_count:
#             end_index = total_count

#         # 페이지에 해당하는 게시물 가져오기
#         cursor.execute(f"SELECT id, title, content, created_at FROM post ORDER BY created_at DESC LIMIT {start_index}, {end_index}")
#         rows = cursor.fetchall()

#         # 결과를 dict 형태로 변환하여 반환
#         result = {"total_count": total_count, "per_page": per_page, "page": page, "data": []}
#         for row in rows:
#             result['data'].append({"id": row["id"], "title": row["title"], "content": row["content"], "created_at": str(row["created_at"])})

#         cursor.close()

#         return jsonify(result), 200

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({"error": "Error occurred."}), 500

# @app.route('/check_adm', methods=['GET'])  #관리자 권한이 있는지 여부를 반환함
# def check_adm():
#     if check_ip(request.remote_addr, accepted_ip_list) == False:
#         return jsonify({"error": "Error occurred."}), 500      #없다면 에러 발생시키기
    
#     return "OK"


# @app.route('/delete_post', methods=['POST'])  #게시글 삭제하기
# def delete_post():
#     if check_ip(request.remote_addr, accepted_ip_list) == False:  #접근 권한이 있는지 여부를 IP 기반으로 확인함
#         return jsonify({"error": "Error occurred."}), 500    

#     post_id = request.form['post_id']  #게시글 코드 가져오기

#     # DB에서 해당 게시글 삭제
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM post WHERE id=%s", (post_id))  #해당 게시글 코드에 해당하는 글을 Mysql에서 삭제하기
#     conn.commit()
#     cursor.close()

#     return "OK"


# @app.route('/recent_posts', methods=['GET'])  #최근 게시글 가져오기
# def recent_posts():
#     try:
#         tot = request.args.get('tot', 1, type=int)  #가져올 글 개수

#         cursor = conn.cursor(pymysql.cursors.DictCursor)

#         # 페이지에 해당하는 게시물 가져오기
#         cursor.execute(f"SELECT id, title, content, DATE_FORMAT(created_at, '%Y-%m-%d') as created_at FROM post ORDER BY created_at DESC LIMIT {tot}")
#         rows = cursor.fetchall()

#         # 결과를 dict 형태로 변환하여 반환
#         result = []
#         for row in rows:
#             result.append({"id": row["id"], "title": row["title"], "content": row["content"], "created_at": str(row["created_at"])})

#         cursor.close()            

#         return jsonify(result), 200

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({"error": "Error occurred."}), 500    
    
# @app.route('/get_post_one/<int:post_id>', methods=['GET'])  #하나의 게시글 가져오기
# def get_post(post_id):
#     try:
#         cursor = conn.cursor(pymysql.cursors.DictCursor)

#         # post_id에 해당하는 글 select 쿼리 실행
#         sql = "SELECT id, title, content, DATE_FORMAT(created_at, '%%Y-%%m-%%d') as created_at FROM post WHERE id = %s"
#         cursor.execute(sql, post_id)
#         result = cursor.fetchone()

#         cursor.close();        
        
#         # 결과를 jsonify로 반환
#         return jsonify(result)
            
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({"error": "Error occurred."}), 500    