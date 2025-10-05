import mysql.connector
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="video_crawler"
    )

def show_database_stats():
    """Hiển thị thống kê dữ liệu trong database"""
    conn = get_connection()
    c = conn.cursor()
    
    print("📊 THỐNG KÊ DATABASE VIDEO_CRAWLER")
    print("=" * 50)
    
    # Đếm Authors
    c.execute("SELECT COUNT(*) FROM Authors")
    author_count = c.fetchone()[0]
    print(f"👥 Tổng số Authors: {author_count}")
    
    # Đếm Videos
    c.execute("SELECT COUNT(*) FROM Videos")
    video_count = c.fetchone()[0]
    print(f"📹 Tổng số Videos: {video_count}")
    
    # Đếm VideoInteractions
    c.execute("SELECT COUNT(*) FROM VideoInteractions")
    interaction_count = c.fetchone()[0]
    print(f"💬 Tổng số VideoInteractions: {interaction_count}")
    
    print("\n" + "=" * 50)
    
    # Top 5 authors có nhiều video nhất
    print("🏆 TOP 5 AUTHORS CÓ NHIỀU VIDEO NHẤT:")
    c.execute("""
        SELECT a.name, a.authorID, COUNT(v.videoID) as video_count
        FROM Authors a
        LEFT JOIN Videos v ON a.authorID = v.authorID
        GROUP BY a.authorID, a.name
        ORDER BY video_count DESC
        LIMIT 5
    """)
    
    top_authors = c.fetchall()
    for i, (name, author_id, count) in enumerate(top_authors, 1):
        print(f"   {i}. {name} ({author_id}): {count} videos")
    
    print("\n" + "=" * 50)
    
    # Video có tương tác cao nhất
    print("🔥 TOP 5 VIDEO CÓ TƯƠNG TÁC CAO NHẤT:")
    c.execute("""
        SELECT v.videoID, a.name, v.textContent, 
               vi.diggCount, vi.playCount, vi.commentCount
        FROM Videos v
        JOIN Authors a ON v.authorID = a.authorID
        JOIN VideoInteractions vi ON v.videoID = vi.videoID
        ORDER BY (vi.diggCount + vi.commentCount + vi.shareCount) DESC
        LIMIT 5
    """)
    
    top_videos = c.fetchall()
    for i, (video_id, author_name, text, digg, play, comment) in enumerate(top_videos, 1):
        print(f"   {i}. {author_name}")
        print(f"      Video: {text[:60]}...")
        print(f"      👍 {digg:,} | 👀 {play:,} | 💬 {comment:,}")
        print()
    
    conn.close()

def show_recent_videos(limit=10):
    """Hiển thị video mới nhất"""
    conn = get_connection()
    c = conn.cursor()
    
    print(f"🆕 {limit} VIDEO MỚI NHẤT:")
    print("=" * 50)
    
    c.execute("""
        SELECT v.videoID, a.name, v.textContent, v.createTime, 
               vi.diggCount, vi.playCount
        FROM Videos v
        JOIN Authors a ON v.authorID = a.authorID
        JOIN VideoInteractions vi ON v.videoID = vi.videoID
        ORDER BY v.createTime DESC
        LIMIT %s
    """, (limit,))
    
    videos = c.fetchall()
    for i, (video_id, author_name, text, create_time, digg, play) in enumerate(videos, 1):
        print(f"{i:2d}. {author_name}")
        print(f"    📝 {text[:70]}...")
        print(f"    🕒 {create_time} | 👍 {digg:,} | 👀 {play:,}")
        print()
    
    conn.close()

def search_videos_by_keyword(keyword):
    """Tìm kiếm video theo từ khóa"""
    conn = get_connection()
    c = conn.cursor()
    
    print(f"🔍 TÌM KIẾM VIDEO VỚI TỪ KHÓA: '{keyword}'")
    print("=" * 50)
    
    c.execute("""
        SELECT v.videoID, a.name, v.textContent, 
               vi.diggCount, vi.playCount, vi.commentCount
        FROM Videos v
        JOIN Authors a ON v.authorID = a.authorID
        JOIN VideoInteractions vi ON v.videoID = vi.videoID
        WHERE v.textContent LIKE %s
        ORDER BY vi.playCount DESC
        LIMIT 10
    """, (f"%{keyword}%",))
    
    results = c.fetchall()
    
    if not results:
        print(f"❌ Không tìm thấy video nào với từ khóa '{keyword}'")
    else:
        print(f"✅ Tìm thấy {len(results)} video:")
        for i, (video_id, author_name, text, digg, play, comment) in enumerate(results, 1):
            print(f"{i:2d}. {author_name}")
            print(f"    📝 {text}")
            print(f"    👍 {digg:,} | 👀 {play:,} | 💬 {comment:,}")
            print()
    
    conn.close()

def main():
    print("🎵 TIKTOK DATABASE VIEWER 🎵")
    print("=" * 40)
    
    while True:
        print("\nChọn chức năng:")
        print("1. Xem thống kê tổng quan")
        print("2. Xem video mới nhất")
        print("3. Tìm kiếm video theo từ khóa")
        print("4. Thoát")
        
        choice = input("\nNhập lựa chọn (1-4): ").strip()
        
        if choice == "1":
            show_database_stats()
        
        elif choice == "2":
            try:
                limit = int(input("Nhập số video muốn xem (1-50): "))
                if 1 <= limit <= 50:
                    show_recent_videos(limit)
                else:
                    print("❌ Số lượng phải từ 1-50")
            except ValueError:
                print("❌ Vui lòng nhập số hợp lệ")
        
        elif choice == "3":
            keyword = input("Nhập từ khóa tìm kiếm: ").strip()
            if keyword:
                search_videos_by_keyword(keyword)
            else:
                print("❌ Từ khóa không được để trống")
        
        elif choice == "4":
            print("👋 Tạm biệt!")
            break
        
        else:
            print("❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Đã thoát!")
    except Exception as e:
        print(f"❌ Lỗi: {e}")