from flask import Flask, render_template, request

app = Flask(__name__)

# 이미지 데이터를 리스트 형태로 저장합니다.
image_data = [
    { 
        "title": f"이미지 제목 {i}", 
        "image": f"image{i}.jpg", 
        "instagram_link": f"https://www.instagram.com/p/image{i}/" 
    }
    for i in range(1, 11)
]

# 비디오 데이터를 리스트 형태로 저장합니다.
video_data = [
    { 
        "title": f"비디오 제목 {i}", 
        "video": f"video{i}.mp4", 
        "instagram_link": f"https://www.instagram.com/p/video{i}/" 
    }
    for i in range(1, 11)
]

@app.route('/')
def index():
    return render_template('index.html', image_data=image_data, video_data=video_data)

@app.route('/search', methods=['POST'])
def search():
    search_keyword = request.form['searchInput'].lower()
    filtered_image_data = [news for news in image_data if search_keyword in news['title'].lower()]
    filtered_video_data = [news for news in video_data if search_keyword in news['title'].lower()]
    return render_template('index.html', image_data=filtered_image_data, video_data=filtered_video_data)

if __name__ == '__main__':
    app.run(debug=True)
