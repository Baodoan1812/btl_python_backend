# Sử dụng Python làm base image
FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Mở các cổng cần thiết
EXPOSE 8000 8001

# Chạy lệnh khởi động server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "chat_realtime.asgi:application"]