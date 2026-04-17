# 🚀 BrightBean Studio Vietnamese - Deployment Complete

## URLs chính

| | |
|---|---|
| 🌐 **Live App** | https://brightbean-app-production-5f36.up.railway.app |
| 💚 **Health** | https://brightbean-app-production-5f36.up.railway.app/health/ |
| 🔐 **Admin** | https://brightbean-app-production-5f36.up.railway.app/admin/ |
| 🔑 **Login** | https://brightbean-app-production-5f36.up.railway.app/accounts/login/ |
| 📦 **GitHub** | https://github.com/ungden/brightbean-studio-vn |
| 🚂 **Railway Dashboard** | https://railway.com/project/4bc22b1e-6a12-4f2f-8396-f3661c15effb |

## Tài khoản Admin

```
Email:    admin@brightbean.local
Password: AdminPassword123!
```

**⚠️ ĐỔI PASSWORD NGAY khi login lần đầu!** Vào `/admin/` → Users → admin@brightbean.local → Change password.

## ✅ Đã hoàn thành

### Security hardening
- Dockerfile: non-root user `appuser`, gunicorn 4 workers + access logging
- Caddyfile: HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy, rate limiting 100/phút
- docker-compose.prod.yml: health checks, resource limits, JSON logging với rotation

### Performance
- Fix N+1 queries trong composer views
- Composite indexes trên Post model (workspace+created_at, workspace+scheduled_at)

### Vietnamese i18n
- Django i18n đầy đủ (LocaleMiddleware, LANGUAGE_CODE=vi, LANGUAGES, LOCALE_PATHS)
- 16 Python files wrap với gettext_lazy
- 168 templates có {% load i18n %}
- 94 templates dịch trực tiếp phổ biến UI (Đăng nhập, Mật khẩu, Lưu, ...)
- locale/vi/LC_MESSAGES/django.po - 150+ translations

### Documentation
- README.vi.md - tiếng Việt
- CONTRIBUTING.vi.md - tiếng Việt
- SECURITY.vi.md - tiếng Việt

### CI/CD
- pip-audit job: scan dependency vulnerabilities
- bandit SAST job: scan code security

### Testing
- Post state machine tests
- Webhook security tests
- Workspace isolation tests

### Infrastructure
- Railway project tạo với Postgres + app service
- Env vars: SECRET_KEY, ENCRYPTION_KEY_SALT, DATABASE_URL, ...
- 48+ database migrations applied
- Superuser admin@brightbean.local tạo sẵn

## Env vars hiện tại trên Railway

| Key | Value |
|-----|-------|
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` |
| `SECRET_KEY` | (auto-generated, 86 chars) |
| `ENCRYPTION_KEY_SALT` | (auto-generated, 43 chars) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.up.railway.app,.railway.app` |
| `DATABASE_URL` | (reference từ Postgres service) |
| `APP_URL` | `https://${{RAILWAY_PUBLIC_DOMAIN}}` |
| `STORAGE_BACKEND` | `local` |
| `EMAIL_BACKEND_TYPE` | `console` |
| `PORT` | `8000` |

## 🔧 TODO để làm production thật

### 1. Đổi mật khẩu admin

### 2. Setup Email SMTP (để gửi invitation, password reset)

```bash
railway variables --set "EMAIL_BACKEND_TYPE=smtp" \
  --set "EMAIL_HOST=smtp.sendgrid.net" \
  --set "EMAIL_PORT=587" \
  --set "EMAIL_HOST_USER=apikey" \
  --set "EMAIL_HOST_PASSWORD=SG.xxx" \
  --set "DEFAULT_FROM_EMAIL=noreply@yourdomain.com"
```

### 3. Cloud Storage (file upload sẽ mất khi redeploy với local storage!)

```bash
railway variables --set "STORAGE_BACKEND=s3" \
  --set "S3_ACCESS_KEY=xxx" \
  --set "S3_SECRET_KEY=xxx" \
  --set "S3_BUCKET_NAME=brightbean-media" \
  --set "S3_ENDPOINT_URL=https://xxx.r2.cloudflarestorage.com"
```

Khuyến nghị Cloudflare R2 (rẻ + không egress fee).

### 4. Connect Social Platform OAuth

Đăng ký developer apps cho từng platform và set credentials:

```bash
# Facebook + Instagram
railway variables --set "PLATFORM_FACEBOOK_APP_ID=xxx" \
  --set "PLATFORM_FACEBOOK_APP_SECRET=xxx"

# LinkedIn
railway variables --set "PLATFORM_LINKEDIN_CLIENT_ID=xxx" \
  --set "PLATFORM_LINKEDIN_CLIENT_SECRET=xxx"

# Twitter/X, TikTok, YouTube, Pinterest, ...
# Xem .env.example cho đầy đủ
```

### 5. Sentry error tracking

```bash
railway variables --set "SENTRY_DSN=https://xxx@sentry.io/xxx"
```

### 6. Custom domain

1. Railway Dashboard → brightbean-app → Settings → Networking → Add domain
2. Update DNS (CNAME)
3. Update env:
```bash
railway variables --set "ALLOWED_HOSTS=yourdomain.com,.up.railway.app" \
  --set "APP_URL=https://yourdomain.com"
```

### 7. Cleanup duplicate Postgres services

Project có 3 Postgres duplicates do timeouts. Xóa qua dashboard, giữ **Postgres-ozjq**.

### 8. Upgrade Railway plan

- Free tier: $5 credit/tháng (dev/test OK)
- Hobby: $5/tháng
- **Pro: $20/tháng** (khuyến nghị cho production, có auto-backup)

## Lệnh admin hay dùng

```bash
# Xem logs real-time
railway logs

# SSH vào container
railway ssh --service brightbean-app "bash"

# Run migration sau schema changes
railway ssh --service brightbean-app "python manage.py migrate --noinput"

# Compile thêm translations
railway ssh --service brightbean-app "python manage.py compilemessages"

# Django shell
railway ssh --service brightbean-app "python manage.py shell"

# Redeploy (từ GitHub)
git push myrepo main

# Redeploy (từ local, không commit)
railway up --detach

# Backup DB
railway ssh --service Postgres-ozjq "pg_dump -U postgres railway" > backup_$(date +%Y%m%d).sql
```

## Security checklist production

- [x] `DEBUG=False`
- [x] `SECRET_KEY` random 86 chars
- [x] `ENCRYPTION_KEY_SALT` set unique
- [x] HTTPS (Railway auto)
- [x] `SESSION_COOKIE_SECURE=True` (auto từ production.py)
- [x] `CSRF_COOKIE_SECURE=True` (auto từ production.py)
- [x] HSTS + security headers (từ Django production settings)
- [x] Rate limiting trên login (AuthRateLimitMiddleware)
- [x] CSRF protection
- [x] CSP headers
- [x] Non-root user trong Docker
- [x] Webhook signature verification
- [ ] Đổi password admin default ← **LÀM NGAY**
- [ ] Enable 2FA cho admin account
- [ ] Setup email SMTP
- [ ] Cloud storage (S3/R2)
- [ ] Sentry
- [ ] Custom domain
- [ ] Database backup tự động
