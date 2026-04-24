# Tài liệu Đặc tả API Hệ thống (API Specification)

Tài liệu này mô tả chi tiết cấu trúc dữ liệu JSON, ví dụ và các yêu cầu bảo mật cho tất cả các endpoint.

---

## 1. Xác thực (Authentication)
**Tiền tố**: `/api/v1/auth`

### 1.1 Đăng nhập
- **Endpoint**: `POST /login`
- **Request Body**:
```json
{
  "username": "admin",
  "password": "Admin@123"
}
```
- **Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 691200,
  "need_change_password": false,
  "user": {
    "id": 1,
    "username": "admin"
  }
}
```

### 1.2 Đăng xuất
- **Endpoint**: `POST /logout`
- **Header**: `Authorization: Bearer <token>`
- **Response (200 OK)**:
```json
{
  "message": "Successfully logged out"
}
```

### 1.3 Đổi mật khẩu
- **Endpoint**: `POST /change-password`
- **Request Body**:
```json
{
  "old_password": "OldPassword123",
  "new_password": "NewPassword@2024"
}
```
- **Response (200 OK)**:
```json
{
  "message": "Password updated successfully"
}
```

---

## 2. Thông tin quyền hạn (Me Permissions)
**Tiền tố**: `/api/v1/me`

### 2.1 Lấy ma trận quyền hiệu lực
- **Endpoint**: `GET /permissions`
- **Response (200 OK)**:
```json
{
  "user": {
    "id": 1,
    "username": "admin"
  },
  "resources": [
    {
      "resourceCode": "job_monitor",
      "view": true,
      "fore": true,
      "effectiveFore": true
    },
    {
      "resourceCode": "user_admin",
      "view": true,
      "fore": false,
      "effectiveFore": false
    }
  ]
}
```

---

## 3. Giám sát công việc (Job Monitor)
**Tiền tố**: `/api/v1/job-monitor`

### 3.1 Xem danh sách công việc
- **Endpoint**: `GET /items`
- **Quyền**: `job_monitor:view`
- **Response (200 OK)**:
```json
{
  "items": [
    {
      "jobId": 1,
      "status": "running"
    }
  ]
}
```

---

## 4. Quản trị Người dùng (Admin Users)
**Tiền tố**: `/api/v1/admin/users`

### 4.1 Lấy danh sách người dùng
- **Endpoint**: `GET /`
- **Quyền**: `user_admin:view`
- **Response (200 OK)**:
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "name": "System Admin",
    "is_active": true,
    "roleCodes": ["super_admin"]
  }
]
```

### 4.2 Tạo người dùng mới
- **Endpoint**: `POST /`
- **Quyền**: `user_admin:fore`
- **Request Body**:
```json
{
  "username": "kỹ thuật viên",
  "name": "Nguyen Van A",
  "email": "technician@example.com",
  "password": "password123",
  "roleCodes": ["operator"]
}
```

---

## 5. Quản trị Vai trò (Admin Roles)
**Tiền tố**: `/api/v1/admin/roles`

### 5.1 Lấy danh sách vai trò
- **Endpoint**: `GET /`
- **Quyền**: `role_admin:view`

### 5.2 Tạo vai trò mới
- **Endpoint**: `POST /`
- **Quyền**: `role_admin:fore`
- **Request Body**:
```json
{
  "role_code": "manager",
  "role_name": "Manager",
  "description": "Standard management role",
  "is_active": true
}
```

### 5.3 Cập nhật quyền cho Vai trò
- **Endpoint**: `PUT /{role_code}/permissions`
- **Quyền**: `role_admin:fore`
- **Request Body**:
```json
{
  "resources": [
    {
      "resourceCode": "job_monitor",
      "view": true,
      "fore": true
    }
  ]
}
```

---

## 6. Mã lỗi ví dụ

### 403 Forbidden (Thiếu quyền)
```json
{
  "detail": {
    "code": "FORBIDDEN",
    "message": "You do not have permission to view job_monitor"
  }
}
```

### 400 Bad Request (Sai logic quyền)
```json
{
  "detail": "Invalid permission configuration for job_monitor: 'fore' requires 'view' to be true"
}
```
