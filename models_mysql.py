import mysql.connector

def init_db():
    conn = mysql.connector.connect(
        host="localhost",      # hoặc IP server MySQL
        user="root",           # tài khoản MySQL
        password="",  # để trống nếu không có password, hoặc nhập password thực tế
        database="video_crawler"  # tên database bạn muốn dùng
    )
    c = conn.cursor()

    # Tạo bảng Authors
    c.execute("""
    CREATE TABLE IF NOT EXISTS Authors (
        authorID VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255),
        avatar TEXT
    );
    """)

    # Tạo bảng Videos
    c.execute("""
    CREATE TABLE IF NOT EXISTS Videos (
        videoID BIGINT PRIMARY KEY,
        authorID VARCHAR(255),
        textContent TEXT,
        duration INT,
        createTime DATETIME,
        webVideoUrl TEXT,
        FOREIGN KEY (authorID) REFERENCES Authors(authorID)
    );
    """)

    # Tạo bảng VideoInteractions
    c.execute("""
    CREATE TABLE IF NOT EXISTS VideoInteractions (
        interactionID INT AUTO_INCREMENT PRIMARY KEY,
        videoID BIGINT,
        diggCount INT,
        playCount BIGINT,
        shareCount INT,
        commentCount INT,
        collectCount INT,
        timeLog DATETIME,
        FOREIGN KEY (videoID) REFERENCES Videos(videoID)
    );
    """)

    conn.commit()
    conn.close()
    print("Database và bảng đã được khởi tạo thành công.")

if __name__ == "__main__":
    init_db()
