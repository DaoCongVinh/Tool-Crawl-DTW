import mysql.connector

def reset_database():
    """Xóa và tạo lại database với schema mới"""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="video_crawler"
    )
    c = conn.cursor()
    
    print("🗑️ Đang xóa bảng cũ...")
    
    # Xóa bảng theo thứ tự (bảng con trước, bảng cha sau)
    try:
        c.execute("DROP TABLE IF EXISTS VideoInteractions")
        print("✅ Đã xóa bảng VideoInteractions")
        
        c.execute("DROP TABLE IF EXISTS Videos") 
        print("✅ Đã xóa bảng Videos")
        
        c.execute("DROP TABLE IF EXISTS Authors")
        print("✅ Đã xóa bảng Authors")
        
    except Exception as e:
        print(f"⚠️ Lỗi khi xóa bảng: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n🏗️ Tạo lại bảng với schema mới...")
    
    # Import và chạy lại init_db
    from models_mysql import init_db
    init_db()
    
    print("\n✅ Hoàn thành reset database!")

if __name__ == "__main__":
    reset_database()