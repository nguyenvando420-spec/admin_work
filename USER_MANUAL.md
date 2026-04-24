# Tài liệu Hướng dẫn Sử dụng Hệ thống Auth & RBAC (FastAPI)

Hệ thống này cung cấp giải pháp xác thực (Authentication) bằng JWT và phân quyền theo vai trò (Role-Based Access Control - RBAC) chuyên sâu cho ứng dụng FastAPI.

---

## 1. Tổng quan Kiến trúc

Hệ thống quản lý quyền dựa trên các thành phần:
- **User**: Người dùng trong hệ thống.
- **Role**: Vai trò (ví dụ: `super_admin`, `admin`, `viewer`). Một User có thể sở hữu nhiều Role.
- **Resource**: Các tài nguyên/tính năng (ví dụ: `user_admin`, `job_monitor`).
- **Permission**: Quyền cụ thể trên Resource, gồm 2 loại:
    - `view`: Quyền truy cập/xem.
    - `fore`: Quyền thực thi/thao tác (Action).
- **Quy tắc Logic**: Quyền `fore` chỉ có hiệu lực (Effective) khi người dùng có đồng thời quyền `view`.

---

## 2. Cài đặt và Khởi tạo

### 2.1 Môi trường
Yêu cầu: **Python 3.9+** và **PostgreSQL** (hoặc SQLite cho môi trường test).

```bash
# Cài đặt môi trường ảo và thư viện
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2.2 Khởi tạo Dữ liệu (Seeding)
Script `seed.py` đã được tối ưu để hỗ trợ cả khởi tạo lần đầu và cập nhật tính năng:
- **Tự động cập nhật**: Khi bạn thêm Resource mới vào `seed.py`, chỉ cần chạy lại script, Role `super_admin` sẽ tự động nhận thêm các quyền mới.
- **Gán Role mặc định**: Đảm bảo tài khoản Admin (cấu hình trong `.env`) luôn có quyền cao nhất.

```bash
# Chạy migration và seed dữ liệu
alembic upgrade head
python seed.py
```

---

## 3. Danh mục API chính

### 3.1 Xác thực (Authentication)
- `POST /api/v1/auth/login`: Đăng nhập lấy JWT Token.

### 3.2 Quản lý User (Admin User)
- `GET /api/v1/admin/users`: Lấy danh sách người dùng.
- `POST /api/v1/admin/users`: Tạo người dùng mới và gán Role.

### 3.3 Quản lý Role & Quyền (Admin Role) - *Mới*
- `GET /api/v1/admin/roles/`: Liệt kê tất cả các vai trò trong hệ thống.
- `POST /api/v1/admin/roles/`: Tạo vai trò (Role) mới.
- `PUT /api/v1/admin/roles/{role_code}/permissions`: Cấu hình ma trận quyền cho một Role.
    - *Lưu ý*: Hệ thống tự động kiểm tra logic `fore` và `view`.

### 3.4 Thông tin cá nhân (Me)
- `GET /api/v1/me/permissions`: Trả về toàn bộ quyền "hiệu lực" của người dùng đang đăng nhập. Dùng để xử lý ẩn/hiện menu ở Frontend.

---

## 4. Kiểm thử (Testing)

Hệ thống sử dụng `pytest` với độ bao phủ cao:
```bash
# Chạy toàn bộ test suite
PYTHONPATH=. venv/bin/pytest tests/
```
Các file test quan trọng:
- `tests/test_auth.py`: Kiểm tra đăng nhập và bảo mật token.
- `tests/test_rbac.py`: Kiểm tra logic phân quyền trên API thực tế.
- `tests/test_roles.py`: Kiểm tra CRUD và gán quyền cho Role.
- `tests/test_seed_logic.py`: Đảm bảo script seed hoạt động đúng khi cập nhật dữ liệu.

---

## 5. Cấu trúc dự án
- `app/api/v1/endpoints`: Chứa định nghĩa logic các API.
- `app/services/permission_service.py`: Trái tim của hệ thống phân quyền (tính toán quyền hiệu lực).
- `app/dependencies/permission.py`: Decorator `require_permission` dùng để bảo vệ các endpoint.
- `seed.py`: Nơi định nghĩa các Resource và Role mặc định ban đầu.
