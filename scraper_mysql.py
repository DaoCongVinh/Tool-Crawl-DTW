import mysql.connector
import json

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="video_crawler"
    )

def save_to_mysql(data):
    conn = get_connection()
    c = conn.cursor()

    author = data["video"]["Author"]
    video = data["video"]
    interactions = video["Interactions"]

    # --- Authors ---
    c.execute("""
        INSERT INTO Authors (authorID, name, avatar)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE name = VALUES(name), avatar = VALUES(avatar)
    """, (author["AuthorID"], author["Name"], author["Avatar"]))

    # --- Videos ---
    c.execute("""
        INSERT INTO Videos (videoID, authorID, textContent, duration, createTime, webVideoUrl)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            textContent = VALUES(textContent),
            duration = VALUES(duration),
            createTime = VALUES(createTime),
            webVideoUrl = VALUES(webVideoUrl)
    """, (
        video["VideoID"],
        author["AuthorID"],
        video["TextContent"],
        video["Duration"],
        video["CreateTime"],
        video["WebVideoUrl"]
    ))

    # --- VideoInteractions ---
    c.execute("""
        INSERT INTO VideoInteractions (videoID, diggCount, playCount, shareCount, commentCount, collectCount, timeLog)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        video["VideoID"],
        interactions["DiggCount"],
        interactions["PlayCount"],
        interactions["ShareCount"],
        interactions["CommentCount"],
        interactions["CollectCount"],
        interactions["TimeLog"]
    ))

    conn.commit()
    conn.close()
    print(f"Đã lưu video {video['VideoID']} vào MySQL thành công!")

if __name__ == "__main__":
    with open("sample_video.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        save_to_mysql(data)
