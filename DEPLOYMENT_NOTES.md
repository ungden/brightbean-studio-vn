# Deployment Notes - Railway

## URLs

- **GitHub Repo:** https://github.com/ungden/brightbean-studio-vn
- **Railway Project:** https://railway.com/project/4bc22b1e-6a12-4f2f-8396-f3661c15effb
- **App URL:** https://brightbean-app-production-5f36.up.railway.app

## Credentials

### Superuser mặc định

```
Email:    admin@brightbean.local
Password: AdminPassword123!
```

**⚠️ ĐỔI NGAY password này sau khi login lần đầu!**

Login tại: https://brightbean-app-production-5f36.up.railway.app/accounts/login/

## Environment Variables đã set

- `DJANGO_SETTINGS_MODULE=config.settings.production`
- `SECRET_KEY` (auto-generated, 86 chars)
- `ENCRYPTION_KEY_SALT` (auto-generated, 43 chars)
- `DEBUG=False`
- `ALLOWED_HOSTS=.up.railway.app,.railway.app`
- `DATABASE_URL` (từ Postgres service via reference)
- `APP_URL=https://${{RAILWAY_PUBLIC_DOMAIN}}`
- `STORAGE_BACKEND=local`
- `EMAIL_BACKEND_TYPE=console`
- `PORT=8000`

## Cần thêm env vars cho production thật

### 1. Platform OAuth credentials (để connect social media)

Set qua Railway dashboard hoặc CLI:
```bash
railway variables --set "PLATFORM_FACEBOOK_APP_ID=..." \
  --set "PLATFORM_FACEBOOK_APP_SECRET=..." \
  --set "PLATFORM_INSTAGRAM_APP_ID=..." \
  # ... các platform khác
```

### 2. Email (để gửi invitation, password reset)

```bash
railway variables --set "EMAIL_BACKEND_TYPE=smtp" \
  --set "EMAIL_HOST=smtp.sendgrid.net" \
  --set "EMAIL_PORT=587" \
  --set "EMAIL_HOST_USER=apikey" \
  --set "EMAIL_HOST_PASSWORD=SG..." \
  --set "DEFAULT_FROM_EMAIL=noreply@yourdomain.com"
```

### 3. Cloud storage (khuyến nghị cho production)

Default là `STORAGE_BACKEND=local` → files lưu trong container (mất khi redeploy). Nên đổi sang S3/R2:

```bash
railway variables --set "STORAGE_BACKEND=s3" \
  --set "S3_ACCESS_KEY=..." \
  --set "S3_SECRET_KEY=..." \
  --set "S3_BUCKET_NAME=..." \
  --set "S3_ENDPOINT_URL=https://...r2.cloudflarestorage.com"
```

### 4. Sentry (error tracking)

```bash
railway variables --set "SENTRY_DSN=https://...@sentry.io/..."
```

### 5. Google OAuth (SSO)

```bash
railway variables --set "GOOGLE_AUTH_CLIENT_ID=..." \
  --set "GOOGLE_AUTH_CLIENT_SECRET=..."
```

## Custom domain

### Thêm domain trong Railway:
1. Vào dashboard → Service brightbean-app → Settings → Networking
2. Add custom domain
3. Cập nhật DNS (CNAME hoặc A record)

### Update env var:
```bash
railway variables --set "ALLOWED_HOSTS=yourdomain.com,.up.railway.app" \
  --set "APP_URL=https://yourdomain.com"
```

## Các lệnh quản trị

### Chạy migration sau khi có schema changes:
```bash
railway ssh --service brightbean-app "python manage.py migrate --noinput"
```

### Compile translations sau khi update .po:
```bash
railway ssh --service brightbean-app "python manage.py compilemessages"
```

### Django shell:
```bash
railway ssh --service brightbean-app "python manage.py shell"
```

### Xem logs:
```bash
railway logs                    # runtime logs
railway logs --build            # build logs
```

### Redeploy:
```bash
git push myrepo main            # triggers deploy via GitHub
# hoặc
railway up --detach             # deploy từ local
```

## Cleanup

Project hiện có 3 Postgres services thừa (Postgres, Postgres-touC, Postgres-9v3g) do timeout lúc setup. Xóa qua dashboard:

https://railway.com/project/4bc22b1e-6a12-4f2f-8396-f3661c15effb

Giữ lại: **Postgres-ozjq** (service app đang dùng)

## Backup database

```bash
# Export
railway ssh --service Postgres-ozjq "pg_dump -U postgres railway" > backup.sql

# Hoặc dùng Railway dashboard → Postgres → Data → Export
```

## Monitoring

- Railway Metrics: Dashboard → brightbean-app → Metrics
- Health check: https://brightbean-app-production-5f36.up.railway.app/health/
- Admin panel: https://brightbean-app-production-5f36.up.railway.app/admin/

## Chi phí Railway

- **Free tier:** $5 credit/tháng (đủ cho dev/test)
- **Hobby:** $5/tháng (basic usage)
- **Pro:** $20/tháng (production, nhiều resource hơn)

Kiểm tra usage: Dashboard → Usage tab

## Nâng cấp production

Khi sẵn sàng cho traffic thật:

1. ✅ Upgrade lên Railway Pro
2. ✅ Set custom domain + HTTPS
3. ✅ Config email SMTP (SendGrid/Mailgun/SES)
4. ✅ Config S3/R2 storage
5. ✅ Setup Sentry
6. ✅ Connect social platform OAuth apps
7. ✅ Enable 2FA cho admin accounts
8. ✅ Backup database định kỳ (Railway Pro có auto-backup)
