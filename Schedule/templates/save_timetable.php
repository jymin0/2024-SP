<?php
// MySQL 데이터베이스 연결
$servername = "localhost:3306"; // MySQL 서버 주소
$username = "root"; // MySQL 사용자 이름
$password = "seo1005404@"; // MySQL 비밀번호
$dbname = "timetable"; // 사용할 데이터베이스 이름

// MySQL 데이터베이스에 연결
$conn = new mysqli($servername, $username, $password, $dbname);

// 연결 확인
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// POST 요청에서 JSON 데이터 가져오기
$data = json_decode(file_get_contents('php://input'), true);

// 시간표 데이터를 MySQL 데이터베이스에 저장
$stmt = $conn->prepare("INSERT INTO timetable (time, monday, tuesday, wednesday, thursday, friday) VALUES (?, ?, ?, ?, ?, ?)");
$stmt->bind_param("ssssss", $time, $monday, $tuesday, $wednesday, $thursday, $friday);

foreach ($data as $row) {
    $time = $row[0];
    $monday = $row[1];
    $tuesday = $row[2];
    $wednesday = $row[3];
    $thursday = $row[4];
    $friday = $row[5];
    $stmt->execute();
}

$stmt->close();
$conn->close();

echo "시간표가 성공적으로 저장되었습니다.";
?>
