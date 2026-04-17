# Chính sách bảo mật

## Các phiên bản được hỗ trợ

Chỉ phiên bản release mới nhất trên branch `main` nhận được cập nhật bảo mật.

| Phiên bản | Hỗ trợ |
| ------- | ------ |
| main (latest) | ✅ |
| Các phiên bản cũ hơn | ❌ |

## Báo cáo lỗ hổng bảo mật

**Không** mở GitHub Issue public cho lỗ hổng bảo mật.

Thay vào đó, gửi email riêng cho maintainers:

- Email: security@brightbean.xyz
- Đính kèm: mô tả chi tiết, các bước tái hiện, tác động, PoC (nếu có)

Chúng tôi sẽ:
1. Xác nhận trong vòng 48 giờ
2. Đánh giá và phân loại mức độ
3. Sửa lỗ hổng và phát hành bản vá
4. Công khai khi đã vá (với credit cho người báo cáo, nếu đồng ý)

## Trong phạm vi (In Scope)

- Lỗi xác thực/phân quyền (authentication / authorization bypass)
- Rò rỉ dữ liệu (data leaks)
- SQL injection, XSS, CSRF
- Remote code execution (RCE)
- Rò rỉ credential OAuth, token
- Lỗi trong encryption tại rest
- Session hijacking / fixation
- Lỗi trong quy trình magic link của client portal

## Ngoài phạm vi (Out of Scope)

- Các báo cáo tự động từ scanner không có PoC
- Các lỗ hổng phụ thuộc vào cấu hình sai từ phía user (vd: SECRET_KEY yếu)
- Missing security headers (đã có Caddyfile cho production)
- Self-XSS yêu cầu user tự dán payload
- Các nền tảng cũ/outdated mà chúng tôi không còn hỗ trợ

## Best practices bảo mật khi self-host

### 1. Bắt buộc khi deploy production

- [ ] `DEBUG=False` trong `.env`
- [ ] `SECRET_KEY` đủ dài, ngẫu nhiên (ít nhất 50 ký tự)
- [ ] `ENCRYPTION_KEY_SALT` ngẫu nhiên và duy nhất
- [ ] `ALLOWED_HOSTS` chỉ chứa domain thực của bạn
- [ ] Dùng HTTPS (Caddy auto-HTTPS hoặc reverse proxy khác)
- [ ] `SESSION_COOKIE_SECURE=True` (tự động trong production settings)
- [ ] `CSRF_COOKIE_SECURE=True` (tự động trong production settings)

### 2. Mã hóa & lưu trữ

- OAuth tokens được mã hóa AES-256-GCM trước khi lưu DB
- Password hash bằng bcrypt (cost factor 12)
- Không bao giờ log `SECRET_KEY`, tokens, hoặc password
- 2FA (TOTP) nên được khuyến khích bật cho tất cả admin

### 3. Network security

- Firewall chỉ mở port 443 (HTTPS) public
- PostgreSQL không expose public (bind 127.0.0.1 hoặc chỉ trong private network)
- Rate limiting đã có sẵn trong Caddyfile (100 req/phút)
- Thiết lập fail2ban hoặc equivalent trên VPS

### 4. Backups

- Backup database hàng ngày
- Lưu backup ở nơi tách biệt (S3, Backblaze B2)
- Test restore backup định kỳ
- Mã hóa backup khi lưu trữ

### 5. Updates

- Theo dõi security advisory cho:
  - Django (djangoproject.com/weblog/)
  - Python
  - PostgreSQL
  - Các dependency khác (dùng `pip-audit`)
- CI đã chạy `pip-audit` và `bandit` tự động trên mỗi PR

### 6. Monitoring

- Cấu hình Sentry để track errors production
- Theo dõi failed login attempts (rate limit đã có)
- Alert cho các event bất thường (nhiều 403/500 liên tiếp)

### 7. Quản lý OAuth credentials

- Dùng app credentials riêng cho môi trường dev/staging/production
- Định kỳ rotate app secrets (3-6 tháng)
- Giới hạn redirect URIs chỉ tới domain thực
- Review và revoke các app không dùng

## Đặc trưng bảo mật của BrightBean Studio

- ✅ **AES-256-GCM** mã hóa OAuth tokens và credentials
- ✅ **bcrypt** password hashing
- ✅ **2FA (TOTP)** tùy chọn cho user
- ✅ **CSRF protection** trên mọi forms
- ✅ **Content Security Policy (CSP)** chặt chẽ
- ✅ **Rate limiting** cho login và API
- ✅ **Webhook signature verification** (HMAC-SHA256 cho Facebook, HMAC-SHA1 cho YouTube)
- ✅ **Workspace-scoped queries** tự động (ngăn data leak giữa workspaces)
- ✅ **Custom permission decorators** cho RBAC
- ✅ **Magic link** với token crypto-secure cho client portal

## Credits

Cảm ơn các security researcher đã có responsible disclosure. Các đóng góp sẽ được ghi nhận tại CHANGELOG.md.
