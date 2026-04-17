# Hướng dẫn đóng góp cho BrightBean Studio

Cảm ơn bạn đã quan tâm đến việc đóng góp! Tài liệu này sẽ hướng dẫn bạn cách đóng góp hiệu quả.

## Quy trình phát triển

### 1. Thiết lập môi trường

```bash
# Fork repo trên GitHub, sau đó clone về máy
git clone https://github.com/YOUR_USERNAME/brightbean-studio.git
cd brightbean-studio

# Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt

# Copy và cấu hình .env
cp .env.example .env
# Chỉnh SECRET_KEY, ENCRYPTION_KEY_SALT, DATABASE_URL

# Chạy migrations
python manage.py migrate

# Tạo superuser
python manage.py createsuperuser
```

### 2. Chạy dev server

Bạn cần 3 terminal cùng chạy:

```bash
# Terminal 1: Tailwind watcher
cd theme/static_src
npm install
npm run dev

# Terminal 2: Django dev server
python manage.py runserver

# Terminal 3: Background worker
python manage.py process_tasks
```

### 3. Workflow đóng góp

1. Tạo branch từ `main`: `git checkout -b feature/ten-tinh-nang`
2. Viết code + tests
3. Chạy tests và linters (xem bên dưới)
4. Commit với message rõ ràng
5. Push lên fork của bạn và mở Pull Request

## Chạy tests

```bash
# Chạy toàn bộ tests
pytest

# Chạy tests cho một app cụ thể
pytest apps/composer/

# Chạy với coverage
pytest --cov=apps --cov-report=term-missing

# Chạy một test file cụ thể
pytest apps/composer/tests/test_idea_media_flows.py
```

## Code style & linting

Dự án dùng **ruff** (linting + formatting) và **mypy** (type checking):

```bash
# Lint check
ruff check .

# Auto-format
ruff format .

# Type check
mypy apps/ config/ providers/ tests/ --ignore-missing-imports
```

## Quy tắc commit

Format: `<type>: <mô tả ngắn>`

Các type:
- `feat`: Tính năng mới
- `fix`: Sửa bug
- `docs`: Thay đổi tài liệu
- `style`: Format code (không đổi logic)
- `refactor`: Refactor code
- `test`: Thêm/sửa tests
- `chore`: Công việc linh tinh (deps, build, ...)

Ví dụ:
```
feat: add LinkedIn video upload support
fix: resolve N+1 query in composer view
docs: update deployment guide for Railway
```

## Quy tắc Pull Request

- PR title rõ ràng, mô tả ngắn gọn thay đổi
- Link issue liên quan (nếu có): `Fixes #123`
- Checklist cho PR:
  - [ ] Tests đã pass (`pytest`)
  - [ ] Lint đã sạch (`ruff check .`)
  - [ ] Format đúng (`ruff format --check .`)
  - [ ] Type check đã pass (`mypy ...`)
  - [ ] Đã thêm/cập nhật tests cho thay đổi
  - [ ] Đã cập nhật docs nếu cần

## Cấu trúc dự án

```
brightbean-studio/
├── apps/                    # Django apps theo tính năng
│   ├── accounts/            # User, auth, 2FA
│   ├── composer/            # Post editor, ideas
│   ├── calendar/            # Lịch và scheduling
│   ├── inbox/               # Hộp thư mạng xã hội
│   ├── media_library/       # Quản lý media
│   ├── approvals/           # Quy trình duyệt
│   ├── social_accounts/     # OAuth kết nối platforms
│   ├── members/             # RBAC, invitations
│   └── ...
├── providers/               # Module tích hợp API từng platform
│   ├── base.py              # Abstract SocialProvider
│   ├── facebook.py, instagram.py, ...
├── config/
│   ├── settings/            # base, development, production, test
│   └── urls.py
├── templates/               # Django templates
├── static/                  # Static assets
├── theme/                   # Tailwind theme
├── locale/                  # i18n translations (vi, en)
├── tests/                   # Test suite
└── requirements.txt
```

## Thêm tích hợp platform mới

1. Tạo module mới trong `providers/` (vd: `providers/threads.py`)
2. Implement class kế thừa `SocialProvider` trong `providers/base.py`
3. Các method bắt buộc:
   - `platform_name`, `auth_type`, `supported_post_types`
   - `get_auth_url`, `exchange_code`, `refresh_token`
   - `get_profile`, `publish_post`
4. Các method tùy chọn: `publish_comment`, `get_post_metrics`, `get_messages`
5. Thêm platform config vào `apps/social_accounts/config.py`
6. Thêm env vars vào `.env.example`
7. Viết tests trong `tests/providers/test_<platform>.py`
8. Cập nhật tài liệu (README + architecture.md)

## Làm việc với i18n (tiếng Việt/tiếng Anh)

Dự án hỗ trợ i18n đầy đủ với tiếng Việt là mặc định.

### Thêm string cần dịch trong Python

```python
from django.utils.translation import gettext_lazy as _

class MyModel(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Enter the name"),
    )

# Trong views
messages.success(request, _("Saved successfully."))
```

### Thêm string cần dịch trong templates

```django
{% load i18n %}
<h1>{% trans "Welcome" %}</h1>
<p>{% blocktrans %}Hello {{ user.name }}{% endblocktrans %}</p>
```

### Generate và compile .po files

```bash
# Extract strings mới từ code
python manage.py makemessages -l vi

# Dịch trong locale/vi/LC_MESSAGES/django.po

# Compile thành .mo file
python manage.py compilemessages
```

## Báo bug / Yêu cầu tính năng

- Mở GitHub Issue với template đầy đủ
- Mô tả rõ:
  - Hành vi mong đợi
  - Hành vi thực tế
  - Các bước tái hiện
  - Version, OS, browser (nếu liên quan)

## License

Bằng việc đóng góp, bạn đồng ý code của mình được cấp phép theo AGPL-3.0.

## Cảm ơn!

Mọi đóng góp dù nhỏ đều được trân trọng. 🙌
