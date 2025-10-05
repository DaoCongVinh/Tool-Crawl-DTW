# Cấu hình cho TikTok Scraper

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root", 
    "password": "",  # Thay đổi password nếu cần
    "database": "video_crawler"
}

# Scraping Configuration
SCRAPING_CONFIG = {
    "delay_min": 1,      # Delay tối thiểu giữa các request (giây)
    "delay_max": 3,      # Delay tối đa giữa các request (giây)
    "max_retries": 3,    # Số lần thử lại khi request thất bại
    "timeout": 30,       # Timeout cho request (giây)
}

# TikTok URLs và endpoints (mẫu)
TIKTOK_CONFIG = {
    "base_url": "https://www.tiktok.com",
    "trending_endpoint": "/trending",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Giới hạn crawling
LIMITS = {
    "max_videos_trending": 100,
    "max_videos_hashtag": 50,
    "max_videos_user": 30
}