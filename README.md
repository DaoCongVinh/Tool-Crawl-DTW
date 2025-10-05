# 🎵 TikTok Video Crawler System

Hệ thống crawl và lưu trữ dữ liệu video TikTok vào MySQL database.

## 📋 Yêu cầu hệ thống

- Python 3.7+
- MySQL Server
- Thư viện: `mysql-connector-python`

## 🚀 Cài đặt

```bash
pip install mysql-connector-python
```

## 📁 Cấu trúc files

```
📁 DataWarehouse/
├── 📄 models_mysql.py         # Tạo database và tables
├── 📄 tiktok_scraper.py       # Crawler chính với menu
├── 📄 crawl_user.py           # Crawler user TikTok cụ thể
├── 📄 quick_crawl.py          # Crawler nhanh
├── 📄 view_data.py            # Xem dữ liệu đã crawl
├── 📄 reset_db.py             # Reset database schema
├── 📄 config.py               # Cấu hình hệ thống
├── 📄 scraper_mysql.py        # Script cũ (đã cập nhật)
└── 📄 sample_video.json       # Dữ liệu mẫu
```

## 🗄️ Database Schema

### 🏗️ Tables được tạo:

#### 👥 Authors
- `authorID` (Primary Key) - VARCHAR(255)
- `name` - Tên tác giả
- `avatar` - Link avatar

#### 📹 Videos  
- `videoID` (Primary Key) - BIGINT
- `authorID` (Foreign Key) - VARCHAR(255)
- `textContent` - Nội dung video
- `duration` - Thời lượng (giây)
- `createTime` - Thời gian tạo
- `webVideoUrl` - Link video

#### 💬 VideoInteractions
- `interactionID` (Auto Increment Primary Key)
- `videoID` (Foreign Key)
- `diggCount` - Số lượt thích
- `playCount` - Số lượt xem
- `shareCount` - Số lượt chia sẻ
- `commentCount` - Số bình luận
- `collectCount` - Số lưu video
- `timeLog` - Thời gian ghi nhận

## 🔧 Hướng dẫn sử dụng

### 1️⃣ Khởi tạo Database

```bash
python models_mysql.py
```

### 2️⃣ Crawl videos với menu tương tác

```bash
python tiktok_scraper.py
```

**Chức năng:**
- ✅ Crawl video trending
- ✅ Crawl theo hashtag
- ✅ Crawl theo user
- ✅ Tùy chọn số lượng video

### 3️⃣ Crawl nhanh (đơn giản)

```bash
python quick_crawl.py
```

### 4️⃣ Crawl video từ user cụ thể

```bash
python crawl_user.py
```

**Tính năng đặc biệt:**
- 🎯 Nhập username TikTok cụ thể (vd: kplus.sports_official)
- 📊 Chọn số lượng video (1-50)
- ✅ Xác nhận trước khi crawl
- 📹 Crawl video với nội dung phù hợp user

### 5️⃣ Xem dữ liệu đã crawl

```bash
python view_data.py
```

**Chức năng:**
- 📊 Thống kê tổng quan
- 🆕 Video mới nhất  
- 🔍 Tìm kiếm theo từ khóa

## ⚙️ Cấu hình

Chỉnh sửa file `config.py` để thay đổi:
- Thông tin database
- Delay giữa requests
- Giới hạn số lượng crawl

## 🎯 Tính năng chính

### ✅ Đã hoàn thành:
- [x] Kết nối MySQL
- [x] Tạo database schema (hỗ trợ authorID dạng string)
- [x] Crawl dữ liệu mẫu TikTok
- [x] Lưu trữ Authors, Videos, Interactions
- [x] Menu tương tác
- [x] Crawl video từ user TikTok cụ thể ⭐NEW⭐
- [x] Xem thống kê dữ liệu
- [x] Tìm kiếm video
- [x] Chọn số lượng video crawl
- [x] Validate username format

### 🔄 Cần phát triển thêm:
- [ ] Kết nối TikTok API thực tế
- [ ] Proxy rotation
- [ ] Rate limiting
- [ ] Error handling nâng cao
- [ ] Export dữ liệu (CSV, JSON)
- [ ] Dashboard web

## 🚨 Lưu ý quan trọng

⚠️ **Phiên bản hiện tại sử dụng dữ liệu mẫu**

Để crawl dữ liệu thực từ TikTok, bạn cần:
1. 🔑 TikTok API key (chính thức)
2. 🕷️ Web scraping tools (Selenium, Scrapy)
3. 🔄 Proxy services
4. 📜 Tuân thủ Terms of Service

## 📊 Ví dụ output

```
🚀 Bắt đầu crawl 10 video từ TikTok...
📹 Video 1/10: TikToker_1 - Dance challenge mới siêu hot 🔥...
✅ Đã lưu video 7234567890123456789 vào MySQL thành công!

📊 Kết quả: 10/10 video đã lưu thành công!
```

## 🤝 Đóng góp

Mọi đóng góp và cải thiện đều được hoan nghênh!

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. ✅ MySQL server đang chạy
2. ✅ Thông tin kết nối database đúng
3. ✅ Python packages đã cài đặt
4. ✅ Quyền truy cập database

---
*Được tạo bởi GitHub Copilot* 🤖