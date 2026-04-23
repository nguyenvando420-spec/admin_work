# Tài liệu Hướng dẫn Sử dụng Hệ thống Auth & RBAC (FastAPI)

Hệ thống này cung cấp giải pháp xác thực (Authentication) bằng JWT và phân quyền theo vai trò (Role-Based Access Control - RBAC) cho ứng dụng FastAPI.

## 1. Tổng quan kiến trúc

Hệ thống được thiết kế theo mô hình:
- **User**: Người dùng trong hệ thống.
- **Role**: Vai trò (ví dụ: Super Admin, Admin, Viewer, Operator). Một User có thể có nhiều Role.
- **Resource**: Các tính năng/màn hình trong ứng dụng (ví dụ: `user_admin`, `job_monitor`).
- **Permission**: Quyền cụ thể trên Resource. Gồm 2 loại chính:
    - `view`: Quyền xem dữ liệu/truy cập màn hình.
    - `fore`: Quyền thao tác/thực thi hành động (Job/Action).
- **Quy tắc hiệu lực**: Quyền thao tác (`fore`) chỉ có hiệu lực khi người dùng có cả quyền xem (`view`).

---

## 2. Cài đặt và Chạy dự án

### 2.1 Yêu cầu hệ thống
- Python 3.9+
- Thư viện: FastAPI, SQLAlchemy, Alembic, Passlib, JWT.

### 2.2 Khởi tạo môi trường
Nếu bạn chạy lần đầu, hãy thực hiện các bước sau:

```bash
# Tạo môi trường ảo
python3 -m venv venv
source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt
pip install email-validator "httpx<0.28.0" "bcrypt<4.0.0" pytest
```

### 2.3 Khởi tạo dữ liệu
Hệ thống sử dụng SQLite làm database cục bộ (`admin.db`).

```bash
# Chạy migration để tạo bảng
alembic upgrade head

# Seed dữ liệu mẫu (Tạo Admin, Roles, Resources)
python seed.py
```

### 2.4 Chạy ứng dụng
```bash
uvicorn app.main:app --reload
```
Truy cập giao diện Swagger UI tại: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 3. Hướng dẫn sử dụng API

### 3.1 Xác thực (Authentication)
1. Truy cập `/api/v1/auth/login`.
2. Sử dụng tài khoản mặc định:
   - **Username**: `admin`
   - **Password**: `Admin@123`
3. Hệ thống trả về `access_token`. Sử dụng token này trong header: `Authorization: Bearer <token>` cho các API khác.

### 3.2 Quản lý User (Admin User)
- **Lấy danh sách User**: `GET /api/v1/admin/users` (Yêu cầu quyền `user_admin:view`).
- **Tạo User mới**: `POST /api/v1/admin/users` (Yêu cầu quyền `user_admin:fore`).
  - Bạn có thể gán `roleCodes` (ví dụ: `["admin", "viewer"]`) ngay khi tạo.

### 3.3 Quản lý Quyền (Admin Role)
- **Cập nhật quyền cho Role**: `PUT /api/v1/admin/roles/{role_code}/permissions` (Yêu cầu quyền `role_admin:fore`).
  - **Lưu ý**: Nếu bạn gán `fore=True` nhưng `view=False`, hệ thống sẽ trả về lỗi 400 để đảm bảo tính nhất quán.

### 3.4 Kiểm tra quyền cá nhân
- **Lấy quyền hiện tại**: `GET /api/v1/me/permissions`
  - Trả về danh sách các Resource và trạng thái `view`, `fore`, `effectiveFore`. Đây là API dùng để frontend ẩn/hiện menu hoặc nút bấm.

---

## 4. Kiểm thử (Testing)

Hệ thống đi kèm bộ test suite để đảm bảo tính an toàn:
```bash
PYTHONPATH=. pytest tests/
```
Các kịch bản đã test:
- Đăng nhập đúng/sai.
- Truy cập không có token.
- Phân quyền: Viewer không được chạy Job, Operator được chạy Job.
- Chặn quyền `fore` nếu thiếu `view`.

---

## 5. Cấu trúc thư mục quan trọng
- `app/core`: Cấu hình hệ thống và bảo mật (JWT, Hashing).
- `app/models`: Định nghĩa bảng Database (SQLAlchemy).
- `app/dependencies`: Middleware kiểm tra Token và Permission.
- `app/services`: Logic tính toán quyền hiệu lực.
- `app/api/v1/endpoints`: Định nghĩa các Router API.
- `seed.py`: Script tạo dữ liệu ban đầu.
