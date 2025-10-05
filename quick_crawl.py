import mysql.connector
import json
import time
import random
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="video_crawler"
    )

def quick_crawl_demo(num_videos):
    """Demo nhanh crawl video TikTok"""
    print(f"🚀 Bắt đầu crawl {num_videos} video từ TikTok...")
    
    success_count = 0
    
    for i in range(num_videos):
        try:
            # Tạo dữ liệu mẫu video TikTok
            video_data = {
                "video_id": f"7{random.randint(100000000000000000, 999999999999999999)}",
                "author_id": f"tiktok_user_{i+1}",
                "author_name": f"TikToker_{i+1}",
                "author_avatar": f"https://tiktok.com/avatar_{i+1}.jpg",
                "text_content": f"Video TikTok số {i+1} - Nội dung thú vị 🎵 #trending",
                "duration": random.randint(15, 180),
                "create_time": datetime.now(),
                "web_video_url": f"https://www.tiktok.com/@tiktok_user_{i+1}/video/{random.randint(7000000000000000000, 7999999999999999999)}",
                "digg_count": random.randint(100, 10000),
                "play_count": random.randint(1000, 100000),
                "share_count": random.randint(10, 1000),
                "comment_count": random.randint(5, 500),
                "collect_count": random.randint(0, 200)
            }
            
            # Lưu vào database
            conn = get_connection()
            c = conn.cursor()
            
            # Authors
            c.execute("""
                INSERT INTO Authors (authorID, name, avatar)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE name = VALUES(name), avatar = VALUES(avatar)
            """, (video_data["author_id"], video_data["author_name"], video_data["author_avatar"]))
            
            # Videos
            c.execute("""
                INSERT INTO Videos (videoID, authorID, textContent, duration, createTime, webVideoUrl)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    textContent = VALUES(textContent),
                    duration = VALUES(duration),
                    createTime = VALUES(createTime),
                    webVideoUrl = VALUES(webVideoUrl)
            """, (
                video_data["video_id"],
                video_data["author_id"],
                video_data["text_content"],
                video_data["duration"],
                video_data["create_time"],
                video_data["web_video_url"]
            ))
            
            # VideoInteractions
            c.execute("""
                INSERT INTO VideoInteractions (videoID, diggCount, playCount, shareCount, commentCount, collectCount, timeLog)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                video_data["video_id"],
                video_data["digg_count"],
                video_data["play_count"],
                video_data["share_count"],
                video_data["comment_count"],
                video_data["collect_count"],
                datetime.now()
            ))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Video {i+1}: {video_data['author_name']} - {video_data['text_content'][:40]}... - Saved!")
            success_count += 1
            
            # Delay ngắn
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Lỗi video {i+1}: {e}")
    
    print(f"\n📊 Kết quả: {success_count}/{num_videos} video đã lưu thành công!")

if __name__ == "__main__":
    print("🎵 TikTok Quick Crawler 🎵")
    print("=" * 30)
    
    try:
        num = int(input("Nhập số lượng video muốn crawl (1-50): "))
        if 1 <= num <= 50:
            quick_crawl_demo(num)
        else:
            print("❌ Số lượng phải từ 1-50")
    except ValueError:
        print("❌ Vui lòng nhập số hợp lệ")
    except KeyboardInterrupt:
        print("\n👋 Đã dừng crawling!")