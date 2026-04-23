-- RBAC schema for FastAPI admin/auth system

CREATE TABLE users (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    last_login_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE roles (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    role_code VARCHAR(100) NOT NULL UNIQUE,
    role_name VARCHAR(255) NOT NULL,
    description VARCHAR(500),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE resources (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    resource_code VARCHAR(100) NOT NULL UNIQUE,
    resource_name VARCHAR(255) NOT NULL,
    menu_key VARCHAR(100),
    menu_label VARCHAR(255),
    route_path VARCHAR(255),
    parent_menu_key VARCHAR(100),
    display_order INT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE permissions (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    resource_id BIGINT NOT NULL REFERENCES resources(id),
    action_code VARCHAR(20) NOT NULL,
    description VARCHAR(500),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_permissions_resource_action UNIQUE (resource_id, action_code),
    CONSTRAINT ck_permissions_action_code CHECK (action_code IN ('view', 'fore'))
);

CREATE TABLE user_roles (
    user_id BIGINT NOT NULL REFERENCES users(id),
    role_id BIGINT NOT NULL REFERENCES roles(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE role_permissions (
    role_id BIGINT NOT NULL REFERENCES roles(id),
    permission_id BIGINT NOT NULL REFERENCES permissions(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (role_id, permission_id)
);

CREATE INDEX idx_permissions_resource_id ON permissions(resource_id);
CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);
CREATE INDEX idx_role_permissions_permission_id ON role_permissions(permission_id);

CREATE TABLE authorization_audit_logs (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT,
    username VARCHAR(100),
    action_type VARCHAR(100) NOT NULL,
    resource_code VARCHAR(100),
    action_code VARCHAR(20),
    detail VARCHAR(2000),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Optional if you want refresh token persistence
CREATE TABLE refresh_tokens (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    token_id VARCHAR(255) NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    revoked_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO resources (
    resource_code,
    resource_name,
    menu_key,
    menu_label,
    route_path,
    parent_menu_key,
    display_order
) VALUES
('user_admin', 'User Administration', 'user_admin', 'Users', '/admin/users', 'admin', 10),
('role_admin', 'Role Administration', 'role_admin', 'Roles', '/admin/roles', 'admin', 20),
('job_monitor', 'Job Monitor', 'job_monitor', 'Job Monitor', '/jobs/monitor', 'jobs', 30);

INSERT INTO permissions (resource_id, action_code, description)
SELECT id, 'view', resource_name || ' - view'
FROM resources;

INSERT INTO permissions (resource_id, action_code, description)
SELECT id, 'fore', resource_name || ' - run job/action'
FROM resources;

INSERT INTO roles (role_code, role_name, description) VALUES
('super_admin', 'Super Admin', 'Full access to all features'),
('admin', 'Admin', 'Manage users, roles, and assigned modules'),
('viewer', 'Viewer', 'Read-only access to assigned screens'),
('operator', 'Operator', 'Can run jobs on assigned screens');

-- Replace with a real bcrypt hash before running in a real environment
INSERT INTO users (
    username,
    full_name,
    email,
    password_hash,
    is_superuser,
    status
) VALUES (
    'admin',
    'System Admin',
    'admin@example.com',
    '$2b$12$replace_with_real_bcrypt_hash',
    TRUE,
    'ACTIVE'
);
