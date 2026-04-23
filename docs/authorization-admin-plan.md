# Ke hoach trien khai auth, admin va phan quyen cho FastAPI

## 1. Ket luan sau khi review

Ke hoach truoc dung o phan RBAC, nhung chua day du cho backend vi thieu lop `authentication`.

Thu tu dung cho he thong phai la:

1. Xac thuc request
2. Xac dinh `current_user`
3. Nap role va permission cua user
4. Check quyen `view` hoac `fore`
5. Moi vao business logic

Neu chua co buoc 1 va 2, thi phan `API check quyen` chua the van hanh dung.

## 2. Muc tieu backend

Backend FastAPI can ho tro:

1. Dang nhap de lay token
2. Tao user
3. Gan role cho user
4. Gan permission cho role
5. Check quyen cho business API

Quy tac nghiep vu:

- `view`: duoc truy cap API doc du lieu va mo man hinh
- `fore`: duoc goi API job/action
- `fore` khong co hieu luc neu khong co `view`

Quy tac HTTP:

- `401 Unauthorized`: chua dang nhap, token sai, token het han, user bi khoa
- `403 Forbidden`: da xac thuc nhung thieu quyen

## 3. Kien truc de xuat

Nen tach ro 2 lop:

### 3.1 Authentication

De xuat cho FastAPI:

- `OAuth2PasswordBearer`
- JWT Bearer token
- Hash password bang `passlib` + `bcrypt`

Dependency can co:

- `get_current_user`
- `get_current_active_user`

### 3.2 Authorization

De xuat:

- RBAC theo `user -> role -> permission`
- Check quyen bang FastAPI dependency:
  - `Depends(require_permission("job_monitor", "view"))`
  - `Depends(require_permission("job_monitor", "fore"))`

## 4. Mo hinh quyen

Moi chuc nang duoc dinh danh bang `resource_code`.

Vi du:

- `user_admin`
- `role_admin`
- `job_monitor`
- `invoice_sync`

Moi resource co 2 action:

- `view`
- `fore`

Permission key:

- `job_monitor:view`
- `job_monitor:fore`

Quyen hieu luc:

- `effective_fore = assigned_view AND assigned_fore`

## 5. Thiet ke du lieu

Bang can co:

- `users`
- `roles`
- `resources`
- `permissions`
- `user_roles`
- `role_permissions`

Bang tuy chon:

- `refresh_tokens`
- `authorization_audit_logs`

Ghi chu:

- `permissions` chi luu action `view` va `fore`
- metadata render menu/route co the dat trong `resources`

## 6. API backend can co

### 6.1 Authentication

- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/auth/refresh` neu dung refresh token

### 6.2 Admin user

- `POST /api/admin/users`
- `GET /api/admin/users`
- `GET /api/admin/users/{id}`
- `PATCH /api/admin/users/{id}`
- `POST /api/admin/users/{id}/roles`

### 6.3 Admin role

- `POST /api/admin/roles`
- `GET /api/admin/roles`
- `GET /api/admin/roles/{id}`
- `PUT /api/admin/roles/{id}/permissions`

### 6.4 Runtime permission

- `GET /api/me/permissions`
- `GET /api/me/menus`

### 6.5 Business API

- API doc du lieu check `resource:view`
- API run job check `resource:fore`

## 7. Cach trien khai trong FastAPI

### 7.1 Cau truc module de xuat

- `app/core/security.py`
- `app/dependencies/auth.py`
- `app/dependencies/permission.py`
- `app/models/`
- `app/schemas/`
- `app/repositories/`
- `app/services/auth_service.py`
- `app/services/permission_service.py`
- `app/api/v1/endpoints/`

### 7.2 Flow xac thuc va phan quyen

1. Client goi `POST /api/auth/login`
2. Backend verify password
3. Backend tra JWT access token
4. Client goi business API kem `Authorization: Bearer <token>`
5. `get_current_user` giai ma token va tim user
6. `require_permission` nap quyen hieu luc va check `view`/`fore`

### 7.3 Dependency de xuat

Pseudo flow:

```python
current_user = Depends(get_current_active_user)
permission_guard = Depends(require_permission("job_monitor", "fore"))
```

Xu ly:

- khong co token => `401`
- token sai/het han => `401`
- user bi khoa => `401`
- thieu quyen => `403`

## 8. Ke hoach Alembic

Nen chia nho:

### Migration 1

- Tao bang `users`
- Tao bang `roles`
- Tao bang `resources`
- Tao bang `permissions`
- Tao bang `user_roles`
- Tao bang `role_permissions`

### Migration 2

- Seed `roles`
- Seed `resources`
- Seed `permissions`

### Migration 3

- Seed tai khoan admin dau tien

Khuyen nghi:

- Schema migration tach rieng voi data seed
- Seed admin ban dau qua script secure neu production nhay cam

## 9. Ke hoach trien khai chuan lai

### Phase 1. Authentication

- Tao `security.py`
- Hash password bang bcrypt
- Tao JWT access token
- Tao `POST /api/auth/login`
- Tao `get_current_user`
- Tao `get_current_active_user`

### Phase 2. Authorization foundation

- Tao schema RBAC bang Alembic
- Seed `roles/resources/permissions`
- Tao `permission_service`
- Tinh `effective_fore = view AND fore`

### Phase 3. Permission dependency

- Tao `require_permission(resource, action)`
- Gan vao admin API va business API
- Chuan hoa loi `401/403`

### Phase 4. Admin API

- Tao user
- Liet ke user
- Gan role cho user
- Tao role
- Gan permission cho role

### Phase 5. Hardening

- Audit log
- Cache permission neu can
- Test unit + integration

## 10. Cac diem nghiep vu can chot

### 10.1 Nen gan quyen qua role, khong gan truc tiep user

Phase dau chi nen dung role-based de de audit va don gian hoa.

### 10.2 Khong nen nhoi permission vao JWT

Khuyen nghi JWT chi chua:

- `sub`
- `exp`
- thong tin toi thieu

Moi request se nap permission tu DB hoac cache. Cach nay tranh tinh huong admin vua doi role xong ma token cu van con quyen.

### 10.3 Rule xu ly `fore`

`fore` khong duoc phep nang quyen `view`.

Neu cau hinh role gui len:

- `view = false`
- `fore = true`

thi co 2 cach xu ly dung:

- cach 1 khuyen nghi: backend tra `400` vi request khong hop le
- cach 2: backend chuan hoa va luu `fore = false`

Khong nen tu dong bat `view = true`, vi nhu vay backend dang thay doi y nghia quyen ma admin da chon.

### 10.4 Bao ve admin API

Khong chi business API, tat ca admin API cung phai co quyen rieng:

- `user_admin:view`
- `user_admin:fore`
- `role_admin:view`
- `role_admin:fore`

Neu muon ro hon, co the doi `fore` thanh `manage`, nhung neu ban muon giu dung 2 quyen thi van co the xem `fore` la quyen thao tac.

## 11. Test case backend bat buoc

- Dang nhap dung => 200
- Sai mat khau => 401
- Khong gui token => 401
- Token het han => 401
- User `ACTIVE` co `view` => goi API doc du lieu thanh cong
- User co `fore` nhung khong co `view` => API job phai bi chan `403`
- User co `view + fore` => API job thanh cong
- User da dang nhap nhung khong co quyen => `403`

## 12. Tieu chi hoan thanh

- Co login API va current user dependency
- Co migration Alembic cho RBAC
- Co API tao user va gan role
- Co API gan permission cho role
- Co permission dependency cho FastAPI
- API doc du lieu check `view`
- API run job check `fore`
- Rule `fore` phu thuoc `view` duoc xu ly dung
- `401` va `403` duoc tach dung
