import mysql.connector
import requests
import json
import time
import random
from datetime import datetime
from urllib.parse import urlparse

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="video_crawler"
    )

def save_to_mysql(video_data):
    """Lưu dữ liệu video vào MySQL"""
    conn = get_connection()
    c = conn.cursor()

    try:
        # --- Authors ---
        c.execute("""
            INSERT INTO Authors (authorID, name, avatar)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE name = VALUES(name), avatar = VALUES(avatar)
        """, (
            video_data["author_id"], 
            video_data["author_name"], 
            video_data["author_avatar"]
        ))

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
            video_data["video_id"],
            video_data["author_id"],
            video_data["text_content"],
            video_data["duration"],
            video_data["create_time"],
            video_data["web_video_url"]
        ))

        # --- VideoInteractions ---
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
        print(f"✅ Đã lưu video {video_data['video_id']} vào MySQL thành công!")
        return True
    except Exception as e:
        print(f"❌ Lỗi khi lưu video {video_data.get('video_id', 'Unknown')}: {e}")
        return False
    finally:
        conn.close()

def scrape_tiktok_videos(num_videos=10):
    """
    Scrape videos từ TikTok trending/discover
    Đây là một ví dụ mô phỏng - trong thực tế bạn cần sử dụng API hoặc tools chuyên dụng
    """
    print(f"🚀 Bắt đầu crawl {num_videos} video từ TikTok...")
    
    scraped_count = 0
    success_count = 0
    
    for i in range(num_videos):
        try:
            # Mô phỏng delay giữa các request
            time.sleep(random.uniform(1, 3))
            
            # Tạo dữ liệu mẫu (trong thực tế sẽ crawl từ TikTok API)
            video_data = generate_sample_video_data(i + 1)
            
            print(f"📹 Video {i+1}/{num_videos}: {video_data['author_name']} - {video_data['text_content'][:50]}...")
            
            # Lưu vào database
            if save_to_mysql(video_data):
                success_count += 1
            
            scraped_count += 1
            
        except Exception as e:
            print(f"❌ Lỗi khi crawl video {i+1}: {e}")
            continue
    
    print(f"\n📊 Kết quả crawl:")
    print(f"   - Tổng số video đã crawl: {scraped_count}")
    print(f"   - Lưu thành công: {success_count}")
    print(f"   - Thất bại: {scraped_count - success_count}")

def generate_sample_video_data(index):
    """
    Tạo dữ liệu mẫu cho video TikTok
    Trong thực tế, đây sẽ là dữ liệu được crawl từ TikTok API
    """
    base_timestamp = int(time.time()) - random.randint(0, 86400 * 7)  # Trong 7 ngày qua
    
    sample_authors = [
        {"id": f"author_{index}", "name": f"tiktoker_{index}", "avatar": f"https://tiktok.com/avatar_{index}.jpg"},
        {"id": f"creator_{index}", "name": f"creator_vn_{index}", "avatar": f"https://tiktok.com/creator_{index}.jpg"},
        {"id": f"user_{index}", "name": f"user_vietnam_{index}", "avatar": f"https://tiktok.com/user_{index}.jpg"}
    ]
    
    sample_texts = [
        "Thử thách dance mới cực hot 🔥 #dance #trending",
        "Mẹo nấu ăn siêu hay mà ít người biết 👨‍🍳 #cooking",
        "Outfit hôm nay của tôi 💅 #ootd #fashion",
        "Thử makeup trend viral 💄 #makeup #beauty",
        "Cuộc sống hàng ngày của tôi ✨ #daily #life",
        "Review sản phẩm hot trend 📱 #review",
        "Học tiếng Anh qua TikTok 📚 #english #education",
        "Thử thách 24h không dùng điện thoại 📵 #challenge"
    ]
    
    author = random.choice(sample_authors)
    
    return {
        "video_id": f"7{random.randint(100000000000000000, 999999999999999999)}",
        "author_id": author["id"],
        "author_name": author["name"],
        "author_avatar": author["avatar"],
        "text_content": random.choice(sample_texts),
        "duration": random.randint(15, 180),  # 15s - 3 phút
        "create_time": datetime.fromtimestamp(base_timestamp),
        "web_video_url": f"https://www.tiktok.com/@{author['name']}/video/{random.randint(7000000000000000000, 7999999999999999999)}",
        "digg_count": random.randint(100, 50000),
        "play_count": random.randint(1000, 1000000),
        "share_count": random.randint(10, 5000),
        "comment_count": random.randint(5, 2000),
        "collect_count": random.randint(0, 1000)
    }

def crawl_tiktok_by_hashtag(hashtag, num_videos=10):
    """
    Crawl video theo hashtag cụ thể
    """
    print(f"🏷️ Crawl {num_videos} video với hashtag: #{hashtag}")
    # Implementation sẽ tương tự như scrape_tiktok_videos
    # nhưng filter theo hashtag
    scrape_tiktok_videos(num_videos)

def crawl_tiktok_by_user(username, num_videos=10):
    """
    Crawl video từ user cụ thể
    """
    print(f"👤 Crawl {num_videos} video từ user: @{username}")
    print(f"🚀 Bắt đầu crawl video từ kênh @{username}...")
    
    scraped_count = 0
    success_count = 0
    
    for i in range(num_videos):
        try:
            # Mô phỏng delay giữa các request
            time.sleep(random.uniform(1, 3))
            
            # Tạo dữ liệu mẫu cho user cụ thể
            video_data = generate_user_video_data(username, i + 1)
            
            print(f"📹 Video {i+1}/{num_videos}: @{username} - {video_data['text_content'][:50]}...")
            
            # Lưu vào database
            if save_to_mysql(video_data):
                success_count += 1
            
            scraped_count += 1
            
        except Exception as e:
            print(f"❌ Lỗi khi crawl video {i+1}: {e}")
            continue
    
    print(f"\n📊 Kết quả crawl từ @{username}:")
    print(f"   - Tổng số video đã crawl: {scraped_count}")
    print(f"   - Lưu thành công: {success_count}")
    print(f"   - Thất bại: {scraped_count - success_count}")

def generate_user_video_data(username, index):
    """
    Tạo dữ liệu mẫu cho video từ user cụ thể
    """
    base_timestamp = int(time.time()) - random.randint(0, 86400 * 30)  # Trong 30 ngày qua
    
    # Các loại nội dung phổ biến trên TikTok
    sample_contents = [
        f"Một ngày trong cuộc sống của @{username} ✨ #dailylife #vietnam",
        f"Thử thách makeup mới 💄 cùng @{username} #makeup #beauty #tutorial",
        f"Review sản phẩm hot trend 📱 by @{username} #review #unboxing",
        f"Dance cover siêu hot 🔥 #dance #trending #viral #foryou",
        f"Mẹo nấu ăn hay ho 👨‍🍳 chia sẻ từ @{username} #cooking #food #tips",
        f"Outfit của ngày hôm nay 💅 #ootd #fashion #style #outfit",
        f"Học tiếng Anh cùng @{username} 📚 #english #education #learning",
        f"Thử thách 24h 📵 cùng @{username} #challenge #24hours #funny",
        f"Behind the scenes 🎬 của @{username} #bts #creator #content",
        f"Q&A với fans 💬 @{username} trả lời #qa #fans #interaction"
    ]
    
    return {
        "video_id": f"7{random.randint(100000000000000000, 999999999999999999)}",
        "author_id": username,
        "author_name": username,
        "author_avatar": f"https://p16-sign-va.tiktokcdn.com/{username}_avatar.jpg",
        "text_content": random.choice(sample_contents),
        "duration": random.randint(15, 180),  # 15s - 3 phút
        "create_time": datetime.fromtimestamp(base_timestamp),
        "web_video_url": f"https://www.tiktok.com/@{username}/video/{random.randint(7000000000000000000, 7999999999999999999)}",
        "digg_count": random.randint(100, 100000),  # User cụ thể có thể có tương tác cao hơn
        "play_count": random.randint(1000, 5000000),
        "share_count": random.randint(10, 10000),
        "comment_count": random.randint(5, 5000),
        "collect_count": random.randint(0, 2000)
    }

def main():
    print("🎵 TikTok Video Scraper 🎵")
    print("=" * 40)
    
    while True:
        print("\nChọn chức năng:")
        print("1. Crawl video trending")
        print("2. Crawl video theo hashtag")
        print("3. Crawl video theo user")
        print("4. Thoát")
        
        choice = input("\nNhập lựa chọn (1-4): ").strip()
        
        if choice == "1":
            try:
                num_videos = int(input("Nhập số lượng video muốn crawl (1-100): "))
                if 1 <= num_videos <= 100:
                    scrape_tiktok_videos(num_videos)
                else:
                    print("❌ Số lượng video phải từ 1-100")
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ")
        
        elif choice == "2":
            hashtag = input("Nhập hashtag (không có #): ").strip()
            if hashtag:
                try:
                    num_videos = int(input("Nhập số lượng video (1-50): "))
                    if 1 <= num_videos <= 50:
                        crawl_tiktok_by_hashtag(hashtag, num_videos)
                    else:
                        print("❌ Số lượng video phải từ 1-50")
                except ValueError:
                    print("❌ Vui lòng nhập số hợp lệ")
            else:
                print("❌ Hashtag không được để trống")
        
        elif choice == "3":
            username = input("Nhập TikTok username (không có @): ").strip()
            if username:
                # Kiểm tra format username
                if not username.replace('_', '').replace('.', '').isalnum():
                    print("❌ Username chỉ được chứa chữ cái, số, dấu _ và dấu .")
                    continue
                    
                try:
                    num_videos = int(input(f"Nhập số lượng video muốn crawl từ @{username} (1-30): "))
                    if 1 <= num_videos <= 30:
                        crawl_tiktok_by_user(username, num_videos)
                    else:
                        print("❌ Số lượng video phải từ 1-30")
                except ValueError:
                    print("❌ Vui lòng nhập số hợp lệ")
            else:
                print("❌ Username không được để trống")
        
        elif choice == "4":
            print("👋 Tạm biệt!")
            break
        
        else:
            print("❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    main()