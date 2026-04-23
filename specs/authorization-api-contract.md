# API contract de xuat cho FastAPI auth va phan quyen

## 1. `POST /api/auth/login`

Request:

```json
{
  "username": "admin",
  "password": "Admin@123"
}
```

Response:

```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "admin"
  }
}
```

Loi:

- `401` neu sai username/password

## 2. `GET /api/auth/me`

Header:

```text
Authorization: Bearer <jwt-token>
```

Response:

```json
{
  "id": 1,
  "username": "admin",
  "fullName": "System Admin",
  "status": "ACTIVE",
  "roleCodes": ["super_admin"]
}
```

## 3. `POST /api/admin/users`

Request:

```json
{
  "username": "john.doe",
  "fullName": "John Doe",
  "email": "john.doe@example.com",
  "password": "Temp@123",
  "roleCodes": ["operator"]
}
```

Response:

```json
{
  "id": 101,
  "username": "john.doe",
  "status": "ACTIVE",
  "roleCodes": ["operator"]
}
```

Bao ve:

- can xac thuc
- can quyen `user_admin:fore`

## 4. `PUT /api/admin/roles/{roleCode}/permissions`

Request:

```json
{
  "resources": [
    {
      "resourceCode": "job_monitor",
      "view": true,
      "fore": true
    },
    {
      "resourceCode": "report_daily",
      "view": true,
      "fore": false
    }
  ]
}
```

Rule xu ly:

- neu `fore = true` va `view = false`, backend phai chuan hoa quyen hieu luc thanh `effectiveFore = false`
- khuyen nghi khi luu cau hinh role:
  - cach 1: backend tu dong luu `fore = false`
  - cach 2: backend tra `400` de bao request khong hop le

Khuyen nghi chon cach 2 cho API admin de tranh luu cau hinh mo ho.

Bao ve:

- can xac thuc
- can quyen `role_admin:fore`

## 5. `GET /api/me/permissions`

Response:

```json
{
  "user": {
    "id": 101,
    "username": "john.doe"
  },
  "resources": [
    {
      "resourceCode": "job_monitor",
      "view": true,
      "fore": true,
      "effectiveFore": true
    },
    {
      "resourceCode": "invoice_sync",
      "view": false,
      "fore": false,
      "effectiveFore": false
    }
  ]
}
```

## 6. `GET /api/job-monitor/items`

Bao ve:

- can xac thuc
- can `job_monitor:view`

Response 401:

```json
{
  "code": "UNAUTHORIZED",
  "message": "Not authenticated"
}
```

Response 403:

```json
{
  "code": "FORBIDDEN",
  "message": "You do not have permission to view job_monitor"
}
```

## 7. `POST /api/job-monitor/run`

Bao ve:

- can xac thuc
- can `job_monitor:fore`
- backend phai check theo rule hieu luc: `view AND fore`

Response 401:

```json
{
  "code": "UNAUTHORIZED",
  "message": "Not authenticated"
}
```

Response 403:

```json
{
  "code": "FORBIDDEN",
  "message": "You do not have permission to run job on job_monitor"
}
```

## 8. Pseudo code backend

```text
function getCurrentUser(token) {
  if (!token) raise 401
  payload = verifyJwt(token)
  user = loadUser(payload.sub)
  if (!user || user.status != "ACTIVE") raise 401
  return user
}

function hasPermission(userPermissions, resourceCode, action) {
  permission = userPermissions[resourceCode]
  if (!permission) return false

  if (action == "view") {
    return permission.view == true
  }

  if (action == "fore") {
    return permission.view == true && permission.fore == true
  }

  return false
}
```

Neu payload cap quyen dau vao co `view = false` va `fore = true`, backend khong nen coi day la quyen hop le.

## 9. Pseudo code FastAPI dependency

```text
async function requirePermission(resourceCode, action, currentUser = Depends(getCurrentUser)) {
  permissions = loadEffectivePermissions(currentUser.id)
  if (!hasPermission(permissions, resourceCode, action)) {
    raise 403
  }
}
```
