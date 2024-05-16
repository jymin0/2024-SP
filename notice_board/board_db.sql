CREATE DATABASE IF NOT EXISTS board_db DEFAULT CHARACTER SET UTF8;
USE board_db;

# 카테고리 추가
CREATE TABLE IF NOT EXISTS categories (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
) ENGINE=INNODB;


# 메인 게시판 데이터 추가
CREATE TABLE IF NOT EXISTS posts (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    # author VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    category_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
) ENGINE=INNODB;


# 카테고리 종목 추가 (중복되면 추가 X)
INSERT INTO categories (name)
SELECT * FROM (SELECT '공지게시판') AS tmp
WHERE NOT EXISTS (
    SELECT name FROM categories WHERE name = '공지게시판'
) LIMIT 1;

INSERT INTO categories (name)
SELECT * FROM (SELECT '자유게시판') AS tmp
WHERE NOT EXISTS (
    SELECT name FROM categories WHERE name = '자유게시판'
) LIMIT 1;

INSERT INTO categories (name)
SELECT * FROM (SELECT '홍보게시판') AS tmp
WHERE NOT EXISTS (
    SELECT name FROM categories WHERE name = '홍보게시판'
) LIMIT 1;

# posts 데이터 보기
SELECT * FROM posts;

# categories 데이터 보기
SELECT * FROM categories;
