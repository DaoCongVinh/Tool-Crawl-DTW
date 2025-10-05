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

def crawl_user_videos(username, num_videos):
    """Crawl video từ user TikTok cụ thể"""
    print(f"🎵 Crawl video từ @{username}")
    print("=" * 50)
    print(f"🚀 Bắt đầu crawl {num_videos} video từ kênh @{username}...")
    
    success_count = 0
    
    for i in range(num_videos):
        try:
            # Tạo dữ liệu video cho user cụ thể
            video_data = {
                "video_id": f"7{random.randint(100000000000000000, 999999999999999999)}",
                "author_id": username,
                "author_name": username,
                "author_avatar": f"https://p16-sign-va.tiktokcdn.com/{username}_avatar.jpg",
                "text_content": generate_user_content(username, i+1),
                "duration": random.randint(15, 300),  # 15s - 5 phút
                "create_time": datetime.now() - timedelta(days=random.randint(0, 30)),
                "web_video_url": f"https://www.tiktok.com/@{username}/video/{random.randint(7000000000000000000, 7999999999999999999)}",
                "digg_count": random.randint(100, 200000),
                "play_count": random.randint(1000, 10000000),
                "share_count": random.randint(10, 50000),
                "comment_count": random.randint(5, 10000),
                "collect_count": random.randint(0, 5000)
            }
            
            # Lưu vào database
            save_video_to_db(video_data)
            
            print(f"✅ Video {i+1}/{num_videos}: {video_data['text_content'][:60]}... - Saved!")
            success_count += 1
            
            # Delay ngẫu nhiên
            time.sleep(random.uniform(0.5, 2))
            
        except Exception as e:
            print(f"❌ Lỗi video {i+1}: {e}")
    
    print(f"\n📊 Kết quả crawl từ @{username}:")
    print(f"   ✅ Thành công: {success_count}/{num_videos}")
    print(f"   📹 Video đã lưu: {success_count}")

def generate_user_content(username, video_index):
    """Tạo nội dung video cho user"""
    contents = [
        f"Ngày mới cùng @{username} ☀️ #morning #dailylife #positive",
        f"Chia sẻ outfit hôm nay 👗 #ootd #fashion #style #{username}",
        f"Thử món ăn mới 🍜 cùng @{username} #food #cooking #vietnam",
        f"Dance cover trending 💃 #dance #viral #trending #foryou",
        f"Behind the scenes 🎬 của @{username} #bts #creator",
        f"Q&A với các bạn 💬 #qa #interaction #live #{username}",
        f"Review sản phẩm hot 📱 by @{username} #review #unboxing",
        f"Makeup tutorial 💄 step by step #makeup #beauty #tutorial",
        f"Thử thách 24h 🏃‍♀️ #challenge #24hours #fun",
        f"Tips hay ho 💡 từ @{username} #tips #lifehack #useful",
        f"Học tiếng Anh 📚 cùng @{username} #english #education",
        f"Workout tại nhà 💪 #workout #fitness #athome #{username}"
    ]
    
    return random.choice(contents)

def save_video_to_db(video_data):
    """Lưu video vào database"""
    conn = get_connection()
    c = conn.cursor()
    
    try:
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
        return True
        
    except Exception as e:
        print(f"❌ Lỗi lưu database: {e}")
        return False
    finally:
        conn.close()

def main():
    print("🎵 TikTok User Video Crawler 🎵")
    print("=" * 40)
    print("Crawl video từ kênh TikTok cụ thể")
    print()
    
    while True:
        try:
            username = input("📝 Nhập TikTok username (không có @, hoặc 'quit' để thoát): ").strip()
            
            if username.lower() in ['quit', 'exit', 'q']:
                print("👋 Tạm biệt!")
                break
            
            if not username:
                print("❌ Username không được để trống")
                continue
            
            # Validate username format
            if not username.replace('_', '').replace('.', '').isalnum():
                print("❌ Username chỉ được chứa chữ cái, số, dấu _ và dấu .")
                continue
            
            num_videos = int(input(f"📊 Số lượng video muốn crawl từ @{username} (1-50): "))
            
            if not (1 <= num_videos <= 50):
                print("❌ Số lượng video phải từ 1-50")
                continue
            
            # Xác nhận
            confirm = input(f"\n🔥 Crawl {num_videos} video từ @{username}? (y/n): ").lower()
            if confirm == 'y':
                crawl_user_videos(username, num_videos)
            else:
                print("⏭️ Đã hủy crawling")
            
            print("\n" + "="*50)
            
        except ValueError:
            print("❌ Vui lòng nhập số hợp lệ")
        except KeyboardInterrupt:
            print("\n👋 Đã dừng!")
            break
        except Exception as e:
            print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    # Import thêm timedelta
    from datetime import timedelta
    main()