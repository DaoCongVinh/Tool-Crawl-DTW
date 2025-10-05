# TikTok Video Crawler System

[![GitHub stars](https://img.shields.io/github/stars/DaoCongVinh/Tool-Crawl-DTW)](https://github.com/DaoCongVinh/Tool-Crawl-DTW/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/DaoCongVinh/Tool-Crawl-DTW)](https://github.com/DaoCongVinh/Tool-Crawl-DTW/network)
[![GitHub issues](https://img.shields.io/github/issues/DaoCongVinh/Tool-Crawl-DTW)](https://github.com/DaoCongVinh/Tool-Crawl-DTW/issues)

Hệ thống crawl và phân tích dữ liệu video TikTok với MySQL database.

## 🚀 Tính năng chính

- 🎯 **Crawl video trending** từ TikTok
- 👤 **Crawl theo user cụ thể** (nhập username)
- 🏷️ **Crawl theo hashtag** 
- 📊 **Thống kê và phân tích** dữ liệu
- 🔍 **Tìm kiếm video** theo từ khóa
- 💾 **Lưu trữ MySQL** với schema tối ưu

## 📦 Cài đặt

### Yêu cầu hệ thống
- Python 3.7+
- MySQL Server
- Git

### Bước 1: Clone repository
```bash
git clone https://github.com/DaoCongVinh/Tool-Crawl-DTW.git
cd Tool-Crawl-DTW
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình MySQL
- Khởi động MySQL server
- Tạo database `video_crawler`
- Cập nhật thông tin kết nối trong `config.py`

## 🎮 Sử dụng

### 1. Khởi tạo Database
```bash
python models_mysql.py
```

### 2. Crawl video trending
```bash
python tiktok_scraper.py
# Chọn option 1, nhập số lượng video
```

### 3. Crawl từ user cụ thể
```bash
python crawl_user.py
# Nhập username: kplus.sports_official
# Chọn số lượng video: 20
```

### 4. Xem dữ liệu
```bash
python view_data.py
```

## 📁 Cấu trúc Project

```
Tool-Crawl-DTW/
├── 📄 models_mysql.py     # Database models
├── 📄 tiktok_scraper.py   # Main scraper
├── 📄 crawl_user.py       # User-specific crawler
├── 📄 view_data.py        # Data viewer
├── 📄 config.py           # Configuration
├── 📄 requirements.txt    # Dependencies
└── 📄 README.md           # Documentation
```

## 🗄️ Database Schema

### Authors Table
- `authorID` (VARCHAR(255), Primary Key)
- `name` (VARCHAR(255))
- `avatar` (TEXT)

### Videos Table  
- `videoID` (BIGINT, Primary Key)
- `authorID` (VARCHAR(255), Foreign Key)
- `textContent` (TEXT)
- `duration` (INT)
- `createTime` (DATETIME)
- `webVideoUrl` (TEXT)

### VideoInteractions Table
- `interactionID` (INT, Auto Increment)
- `videoID` (BIGINT, Foreign Key)
- `diggCount`, `playCount`, `shareCount`, etc.

## 📊 Ví dụ Output

```
🚀 Bắt đầu crawl 10 video từ @kplus.sports_official...
✅ Video 1/10: Dance cover trending 💃 #dance #viral - Saved!
✅ Video 2/10: Review sản phẩm hot 📱 #review #unboxing - Saved!

📊 Kết quả: 10/10 video đã lưu thành công!
```

## ⚠️ Lưu ý quan trọng

- 🔒 **Tuân thủ Terms of Service** của TikTok
- 📝 **Phiên bản hiện tại** sử dụng dữ liệu mẫu
- 🔑 **API thực tế** cần TikTok Developer Account
- ⏱️ **Rate limiting** để tránh bị block

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📞 Hỗ trợ

- 📧 Email: [your-email@example.com]
- 🐛 Issues: [GitHub Issues](https://github.com/DaoCongVinh/Tool-Crawl-DTW/issues)
- 📖 Wiki: [GitHub Wiki](https://github.com/DaoCongVinh/Tool-Crawl-DTW/wiki)

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---
⭐ **Star** repository nếu bạn thấy hữu ích!