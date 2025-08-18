from flask import Flask, render_template, request, redirect
import pymysql
import os

app = Flask(__name__)

# 👉 Hàm tạo kết nối DB (chỉ dùng khi có biến môi trường DB_* đã set trên Render)
def get_db_connection():
    try:
        conn = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print("⚠️ Lỗi kết nối MySQL:", e)
        return None

# Dữ liệu mẫu để test giao diện trước khi kết nối DB thật
books = [
    {
        'title': 'Đắc Nhân Tâm',
        'author': 'Dale Carnegie',
        'image': 'https://bookfun.vn/wp-content/uploads/2024/07/dac-nhan-tam-sach.jpg.webp'
    },
    {
        'title': 'Tuổi Trẻ Đáng Giá Bao Nhiêu',
        'author': 'Rosie Nguyễn',
        'image': 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1495635816i/32521178.jpg'
    },
    {
        'title': 'Harry Potter và Hòn Đá Phù Thủy',
        'author': 'J.K. Rowling',
        'image': 'https://images-na.ssl-images-amazon.com/images/I/81YOuOGFCJL.jpg'
    }
]

@app.route('/')
def index():
    # 👉 sau này có thể query từ DB thay vì dùng list mẫu
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    image = request.form.get('image')

    if title and author:
        books.append({'title': title, 'author': author, 'image': image})

        # 👉 nếu muốn lưu DB thật thì mở đoạn này
        # conn = get_db_connection()
        # if conn:
        #     with conn.cursor() as cursor:
        #         cursor.execute(
        #             "INSERT INTO books (title, author, image) VALUES (%s, %s, %s)",
        #             (title, author, image)
        #         )
        #     conn.commit()
        #     conn.close()

    return redirect('/')

@app.route('/delete/<int:index>')
def delete_book(index):
    if 0 <= index < len(books):
        books.pop(index)
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
