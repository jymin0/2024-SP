from flask import Flask, render_template, request

app = Flask(__name__)

# 뉴스 데이터를 리스트 형태로 저장합니다.
news_data = [
    { "title": "뉴스 제목 1", "image": "news1.jpg", "instagram_link": "https://www.instagram.com/p/C5k-EXcylyJ/?img_index=1" },
    { "title": "뉴스 제목 2", "image": "news2.jpg", "instagram_link": "https://www.instagram.com/p/C5kZacvysEY/" }
    # 추가적인 뉴스 데이터
]

@app.route('/')
def index():
    return render_template('index.html', news_data=news_data)

@app.route('/search', methods=['POST'])
def search():
    search_keyword = request.form['searchInput'].lower()
    filtered_news = [news for news in news_data if search_keyword in news['title'].lower()]
    return render_template('index.html', news_data=filtered_news)

if __name__ == '__main__':
    app.run(debug=True)
