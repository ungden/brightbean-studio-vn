<p align="center">
  <a href="https://github.com/brightbeanxyz/brightbean-studio">
    <img src=".github/assets/brightbean-studio-logo.webp" alt="BrightBean Studio" width="280">
  </a>
</p>

<p align="center">
  <strong>Nền tảng quản lý mạng xã hội mã nguồn mở cho creator, agency và SMB.</strong>
</p>

<p align="center">
  <a href="README.md">English</a> · <strong>Tiếng Việt</strong>
</p>

---

## Giới thiệu BrightBean Studio

BrightBean Studio là một nền tảng quản lý mạng xã hội mã nguồn mở, có thể tự host, được xây dựng cho creator, agency và SMB. Nó làm những gì Sendible, SocialPilot hay ContentStudio làm, nhưng miễn phí và không giới hạn theo seat, theo kênh hay theo workspace. Lập kế hoạch, soạn, lên lịch, duyệt, đăng và theo dõi nội dung trên Facebook, Instagram, LinkedIn, TikTok, YouTube, Pinterest, Threads, Bluesky, Google Business Profile và Mastodon từ một dashboard đa workspace.

Phù hợp với người quản lý nhiều tài khoản client dưới một mái nhà - những ai muốn sở hữu social stack của mình thay vì trả $100–300/tháng cho một vendor SaaS. Mọi tính năng đều có sẵn cho mọi user. Không tier trả phí, không feature gate, không upsell.

Bạn có thể triển khai bằng nút one-click trên Heroku, Render hoặc Railway, chạy trên VPS riêng qua Docker, hoặc chạy local. Tất cả tích hợp nền tảng đều giao tiếp trực tiếp với API chính thức của bên thứ nhất qua credentials của bạn, nên không có aggregator trung gian, không vendor lock-in, và không có bên thứ ba ngồi giữa bạn và dữ liệu.

## Tính năng

| | |
|---|---|
| **Đa workspace & đội nhóm** | Không giới hạn org → workspace → thành viên. RBAC chi tiết với custom roles, lời mời, và vai trò Client riêng cho cộng tác viên bên ngoài. |
| **Trình soạn nội dung** | Editor đầy đủ với override caption/media theo nền tảng, lịch sử phiên bản, template tái sử dụng, danh mục & thẻ, bảng Kanban ý tưởng. |
| **Lịch & lên lịch** | Lịch trực quan với posting slots lặp hàng tuần theo từng account và queue có tên tự động gán bài vào slot khả dụng tiếp theo. |
| **Động cơ đăng bài** | Tích hợp API chính thức bên thứ nhất (không aggregator), tự động retry, theo dõi rate-limit theo account, và audit log đăng 90 ngày. |
| **Quy trình duyệt** | Các stage có thể cấu hình (không / tùy chọn / nội bộ / nội bộ + client), comment nội bộ & ngoài có thread, reminders, và audit trail đầy đủ. |
| **Hộp thư mạng xã hội thống nhất** | Comments, mentions, DMs, và reviews từ mọi nền tảng đã kết nối ở một nơi, với phân tích sentiment, assignments, trả lời có thread, và backfill lịch sử. |
| **Thư viện phương tiện** | Thư viện theo scope org- và workspace với folder lồng nhau, biến thể tối ưu theo nền tảng tự động, và alt text. |
| **Cổng khách hàng** | Truy cập passwordless qua magic-link 30 ngày để client duyệt/từ chối bài mà không cần tạo tài khoản. |
| **Thông báo** | Giao qua in-app, email, và webhook với tùy chọn theo user cho mọi loại sự kiện. |
| **Bảo mật & vận hành** | Lưu trữ token & credential được mã hóa, 2FA tùy chọn (TOTP), Google/GitHub SSO, Sentry support, và 7 ngày grace period có thể hoàn tác khi xóa org. |
| **Thân thiện white-label** | Branding theo workspace (logo, màu) và default workspace cho hashtag, bình luận đầu tiên, và posting template. |

## Nền tảng được hỗ trợ

| Nền tảng | Đăng bài | Comments | DMs | Insights |
|---|:---:|:---:|:---:|:---:|
| Facebook | ✓ | ✓ | ✓ | ✓ |
| Instagram | ✓ | ✓ | ✓ | ✓ |
| Instagram (Cá nhân) | ✓ | ✓ | ✓ | ✓ |
| LinkedIn (Cá nhân) | ✓ | ✓ | — | ✓ |
| LinkedIn (Công ty) | ✓ | ✓ | — | ✓ |
| TikTok | ✓ | ✓ | — | ✓ |
| YouTube | ✓ | ✓ | — | ✓ |
| Pinterest | ✓ | — | — | ✓ |
| Threads | ✓ | ✓ | — | ✓ |
| Bluesky | ✓ | ✓ | — | — |
| Google Business Profile | ✓ | — | — | ✓ |
| Mastodon | ✓ | ✓ | — | — |

## Deploy nhanh

### One-Click Deploy

Triển khai trực tiếp lên Heroku, Render hoặc Railway. Xem README.md tiếng Anh để có button deploy.

### Docker Compose (Khuyến nghị)

```bash
# Clone repo
git clone https://github.com/brightbeanxyz/brightbean-studio.git
cd brightbean-studio

# Copy file env và chỉnh sửa
cp .env.example .env
# Chỉnh SECRET_KEY, DATABASE_URL, các platform credentials...

# Build và chạy
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Tạo superuser
docker compose exec app python manage.py createsuperuser
```

### Chạy local (phát triển)

```bash
# Yêu cầu: Python 3.12+, PostgreSQL 16+ (hoặc SQLite cho dev)
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Cấu hình .env
cp .env.example .env

# Migrate database
python manage.py migrate

# Chạy dev server (3 terminal)
# Terminal 1: Tailwind watcher
cd theme/static_src && npm install && npm run dev

# Terminal 2: Django dev server
python manage.py runserver

# Terminal 3: Background worker
python manage.py process_tasks
```

## Stack công nghệ

- **Backend:** Django 5.x, Python 3.12+
- **Frontend:** Django templates + HTMX + Alpine.js (không SPA, không JS build)
- **CSS:** Tailwind CSS 4
- **Database:** PostgreSQL 16+ (SQLite cho dev)
- **Background jobs:** django-background-tasks (không cần Redis)
- **Web server:** Gunicorn + Caddy (reverse proxy + auto-HTTPS)
- **Xác thực:** django-allauth (email, Google OAuth, GitHub OAuth)
- **Mã hóa:** AES-256-GCM cho tokens và credentials
- **Storage:** Local filesystem hoặc S3-compatible (Cloudflare R2, AWS S3, MinIO, Backblaze B2)

## Cấu hình

Sao chép `.env.example` sang `.env` và điền các biến:

### Cốt lõi
- `SECRET_KEY` - Django secret key (sinh ngẫu nhiên, ít nhất 50 ký tự)
- `ENCRYPTION_KEY_SALT` - Salt cho mã hóa token/credential (ngẫu nhiên, duy nhất cho mỗi deployment)
- `DEBUG` - `False` cho production
- `ALLOWED_HOSTS` - Danh sách domain cho phép (phân tách bằng dấu phẩy)
- `APP_URL` - URL public của app (vd: `https://studio.example.com`)
- `DATABASE_URL` - Connection string PostgreSQL

### Storage
- `STORAGE_BACKEND` - `local` hoặc `s3`
- Các biến `S3_*` nếu dùng S3

### Email (SMTP)
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`

### OAuth & Platform credentials
- Xem `.env.example` để biết đầy đủ credentials cho từng nền tảng

## Bảo mật (đã audit & cải thiện)

Phiên bản Vietnamese/production-ready này đã được audit và cải thiện:

- ✅ Dockerfile chạy với non-root user
- ✅ Caddyfile có đầy đủ security headers (HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy)
- ✅ Rate limiting ở reverse proxy
- ✅ Health checks, resource limits, và JSON logging trong docker-compose.prod.yml
- ✅ N+1 query fixes trong composer views
- ✅ Database composite indexes cho truy vấn thường xuyên
- ✅ Django i18n đầy đủ với tiếng Việt làm ngôn ngữ mặc định
- ✅ AES-256-GCM mã hóa credentials
- ✅ 2FA (TOTP) cho user accounts
- ✅ Content Security Policy (CSP) chặt chẽ
- ✅ CSRF protection cho mọi forms, webhook signature verification

## Sao lưu Database (Production)

```bash
# Backup
docker compose exec postgres pg_dump -U postgres brightbean > backup_$(date +%Y%m%d).sql

# Restore
cat backup_20260418.sql | docker compose exec -T postgres psql -U postgres brightbean
```

Khuyến nghị: thiết lập cron backup định kỳ và lưu offsite (S3, Backblaze B2).

## Migration Rollback

Trong trường hợp migration bị lỗi trong production:

```bash
# Xem migrations hiện tại
docker compose exec app python manage.py showmigrations

# Rollback về migration trước
docker compose exec app python manage.py migrate <app_name> <previous_migration>

# Ví dụ:
docker compose exec app python manage.py migrate composer 0023
```

**Lưu ý quan trọng:** Luôn backup database trước khi migrate lên production.

## Giấy phép

AGPL-3.0 - Xem [LICENSE](LICENSE) để biết chi tiết.

## Đóng góp

Xem [CONTRIBUTING.md](CONTRIBUTING.md) để biết hướng dẫn đóng góp.

## Tài liệu tham khảo

- [Kiến trúc chi tiết](development_specs/architecture.md)
- [Đặc tả tính năng](development_specs/feature-spec-v2.md)
- [Bảo mật](SECURITY.md)
