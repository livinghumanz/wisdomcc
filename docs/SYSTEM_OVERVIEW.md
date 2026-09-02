# WisdomCC — End-to-End System Overview

**Baseline document.** Written 2026-09-02 against branch `feature/wisdomcc_UI_Update` @ `3cf2d4c`
(working tree clean). This describes the system *as it exists today*, before the upcoming
requirements change. Treat it as the "before" snapshot to diff future work against.

Companion docs: [UI_CHANGE_REQUESTS.md](UI_CHANGE_REQUESTS.md) is where new UI work gets
requested; [DEFERRED_FIXES.md](DEFERRED_FIXES.md) is the tickable list of the defects in §11.

---

## 1. What this is

A Django server-rendered website for **Wisdom Coaching Centre (WCC)**, a tuition/coaching
institute with two branches — **Redhills** and **Kanathur**, Chennai. Live at `wisdomcc.in`
(EC2, `3.146.206.48`).

It does five things:

1. **Public marketing site** — home, about, courses, gallery (links out to Google Drive folders).
2. **Online admission enquiry** — a modal form that writes an `Admision` row.
3. **Faculty upload portal** — staff upload notes / attendance sheets / mark lists as files.
4. **Admin dashboard** — Django-auth user views the admission enquiry list, exports CSV.
5. **Student dashboard** — student logs in with reg-no + password, sees profile, fee status,
   notes, marks, timetable; downloads an attendance CSV.

There is no JS framework, no REST API, no async work, no email/SMS, no payment integration
(the "Pay Online" section is stubbed and hidden with `display:none`).

---

## 2. Stack and versions

| Layer | What's actually there |
|---|---|
| Python | 3.12.3 (venv at `venv/`, `home = /usr/bin`) |
| Django | **6.0.1 installed**; code and settings comments are written for **3.2.3** |
| DB (prod) | PostgreSQL — db `wisdomcc_db`, user `wisdomcc`, localhost:5432 |
| DB (repo) | `db.sqlite3` is committed but **0 bytes** — dead file |
| Other deps | Pillow, psycopg2-binary, pytz, sqlparse (`requirements.txt`, all unpinned) |
| Frontend | Bootstrap 4.5.2 + jQuery 3.5.1 + popper, all from CDN; hand-written CSS; Font Awesome 4.0.3 via `@import` |
| Server | gunicorn (3 workers, unix socket) behind nginx |
| Host | Ubuntu EC2, app at `/home/ubuntu/app` |
| CI/CD | GitHub Actions → SSH → `git pull` + `collectstatic` + `migrate` + restart |

> The Django 3.2 → 6.0 jump is the single biggest latent risk in the repo. `manage.py check`
> passes today, but the code was never reviewed against 4.x/5.x/6.x removals.
> `USE_L10N` in [settings.py](../wisdomcc/settings.py) was removed from Django in 5.0 and is
> now simply ignored.

---

## 3. Repository layout

```
wisdomcc/
├── manage.py
├── requirements.txt
├── db.sqlite3                  # tracked, empty, unused
├── gunicorn.service            # copy of /etc/systemd/system/gunicorn.service
├── sites-available_slash_wisdomcc  # copy of the nginx server block
├── wisdomccPemKey.pem          # EC2 key, gitignored (*.pem), present on disk
├── .github/workflows/deploy.yml
├── wisdomcc/                   # project package
│   ├── settings.py
│   ├── local_settings.py       # TRACKED IN GIT — see §11
│   ├── urls.py, wsgi.py, asgi.py
│   └── static/                 # SOURCE static files (STATICFILES_DIRS)
├── home/                       # public site app
├── Dashboard/                  # admin + student dashboard app
├── templates/                  # ALL templates (project-level DIRS)
│   ├── base.html
│   ├── home/, dashboard/, admin/
└── static/                     # BUILD OUTPUT of collectstatic (STATIC_ROOT) — gitignored
```

### The two `static/` directories — important

- `wisdomcc/static/` is the **source of truth** (`STATICFILES_DIRS`) and is tracked in git.
- `static/` at repo root is `STATIC_ROOT`, the **collectstatic output**, and is gitignored
  (`/static` in `.gitignore`). It also holds the copied Django admin assets.
- The two are currently **out of sync**: root `static/` is a stale build. It is missing
  `img/courses/*` and `img/home_slider/bg_color.jpg`, and its `index_test.css` /
  `Whomepage.css` are older revisions. Only edit `wisdomcc/static/`; never edit root `static/`.

---

## 4. Configuration

`wisdomcc/settings.py` holds structure only; secrets and environment live in
`wisdomcc/local_settings.py`, imported at the bottom via a `try/except ImportError` tail.

| Setting | Value |
|---|---|
| `INSTALLED_APPS` | `home`, `Dashboard`, plus the six Django contrib defaults |
| `MIDDLEWARE` | Django defaults, unmodified |
| `TEMPLATES.DIRS` | `BASE_DIR/templates` (+ `APP_DIRS: True`, though no app has a `templates/` dir) |
| `STATIC_URL` / `STATIC_ROOT` | `/static/` → `BASE_DIR/static` |
| `STATICFILES_DIRS` | `BASE_DIR/wisdomcc/static` |
| `MEDIA_URL` / `MEDIA_ROOT` | `/media/` → `BASE_DIR/media` (**directory does not exist yet**) |
| `TIME_ZONE` | `UTC` — not `Asia/Kolkata`, despite an all-India user base |
| `DEBUG` | `False` (in local_settings) |
| `ALLOWED_HOSTS` | `['*', 'wisdomcc.in', 'www.wisdomcc.in']` — the `'*'` makes the rest moot |
| `AUTH_PASSWORD_VALIDATORS` | Django defaults — applies to admin users only, **not** to `Student` |

No `LOGGING`, no `CACHES`, no `EMAIL_*`, no `SECURE_*`/HSTS/cookie-security settings,
no `CSRF_TRUSTED_ORIGINS`.

---

## 5. URL map

Root: `wisdomcc/urls.py`

| URL | name | View | Method(s) | Auth |
|---|---|---|---|---|
| `/` | `Home` | `home.views.HomeIndex` | GET | public |
| `/About/` | `about` | `home.views.about` | GET | public |
| `/Course-Services/` | `course` | `home.views.course_service` | GET, POST | public |
| `/Gallery/` | `gallery` | `home.views.gallery` | GET | public |
| `/Faculty-portal/` | `Faculty-portal` | `home.views.Faculty_portal` | GET, POST | **none — empid only** |
| `/Dashboard/` | `Dashboard` | `Dashboard.views.dashboard` | POST (login) | see §7 |
| `/Dashboard/export/` | `export` | `Dashboard.views.export` | GET | **none** |
| `/Dashboard/<stid>` | `report` | `Dashboard.views.reportdown` | POST | **none** |
| `/admin/` | — | Django admin | — | Django auth |
| `/media/<path>` | — | `static()` helper | GET | **DEBUG-only, see §10** |

Note `/Dashboard/<str:stid>` is a greedy catch-all under `/Dashboard/`; only `attendance`
and `mark` are handled, everything else falls through to a redirect. `export/` is matched
first because it is declared earlier.

---

## 6. Data model

Two apps, seven models, no `AbstractUser` subclass — `Student` and `Staff` are plain models
completely disconnected from `django.contrib.auth`.

### `Dashboard` app

**`Student`** — the core record.
`regnum` (PK, char 20) · `image` (ImageField `images/profilepic/%y/%m/%d/`) · `name` · `dob` ·
`DateofJoin` · `aadhar` (char 20) · `address` · `ystudy` (class/year, char 10) · `school` ·
`fname` / `mname` · `foccupation` / `moccupation` · `contact` (BigInteger) · `WhatsappNo` ·
**`password` (CharField 40, plaintext)** · `timetable` (ImageField) · `FeeDue` (bool, default `True`) ·
`FeeDate` · `FeeAmount`.

**`Staff`** — `empid` (PK, char 20) · `name`. That's it. No password, no contact, no branch.

**`Course`** — `staffid` (FK → Staff, `DO_NOTHING`) · `cname` (char 20).

**`Attendance`** — `studentid` (FK → Student) · `edate` · `present` (bool) · `late` (bool).

**`Mark`** — `studentid` (FK) · `courseid` (FK → Course) · `score` (int) · `examdate`.

### `home` app

**`Admision`** *(sic — misspelled everywhere, including the DB table)* — the admission enquiry.
`sname` · `school` · `contact` (BigInteger) · `slocation` (`redhills`/`kanathur`) ·
`ystudy` · `mailid` · `scourse` (nullable). No timestamp, no status/workflow field.

**`Fupload`** — a faculty file upload.
`empid` (FK → `Dashboard.Staff`, `DO_NOTHING`) · `mtype` (`notes`/`attendance`/`mark`) ·
`update` (DateField, `auto_now_add`) · `comment` (free text; doubles as subject name for notes) ·
`fdata` (FileField → `uploadedfiles/facultyportal/%y/%m/%d/`).

### Relationship notes

- Every FK uses `on_delete=DO_NOTHING`, which will leave dangling rows / integrity errors on delete.
- There is **no branch/location model**. "Redhills" vs "Kanathur" exists only as a free string
  on `Admision.slocation` and as hardcoded HTML.
- There is **no link between `Student` and `Course`** — enrolment is implicit via `Mark` rows.
- Uploaded attendance/mark files (`Fupload`) are never parsed into the `Attendance`/`Mark`
  tables. Those tables are populated by hand through Django admin.

### Migration state

`home` at `0007`, `Dashboard` at `0005`. All generated by Django 3.2.3, newest dated 2022-05-28.
All models are registered flat in Django admin with no `ModelAdmin` customisation
(no list_display, no search, no filters) — see `home/admin.py` and `Dashboard/admin.py`.

---

## 7. Authentication and sessions — read this carefully

**There is effectively no session-based auth in the app.** This is the most consequential
design fact in the codebase.

`Dashboard.views.authencateuser` (a class instantiated per-request, called from `dashboard()`)
branches on a `ltype` radio in the login modal:

- **`ltype == 'admin'`** → `auth.authenticate(username=lid.lower(), password=passwd)`.
  The result is checked for `None`, but **`auth.login()` is never called** — no session is
  created. There is also no `is_staff` / `is_superuser` check, so *any* Django user account
  can view the full admission enquiry list.
- **`ltype == 'student'`** → `Student.objects.filter(regnum=lid, password=passwd)` — a
  **plaintext password comparison in a DB query**. On match, `dashboard_user.html` is
  rendered directly from the POST response.

Consequences you must design around:

1. Both dashboards exist only as the **response body of a POST**. Refresh → browser re-POST
   prompt or bounce to `/`. There is no bookmarkable dashboard URL and no logout (the
   "LOG-OUT" link is just a link to `/`).
2. `base.html` renders `{% if user.is_authenticated %}Hello, {{user.username}}{% endif %}`
   and swaps Login→Dashboard — **this can never be true**, because login is never persisted.
   That whole branch is dead code.
3. `/Dashboard/export/` has **no auth check at all**. Anyone who GETs it downloads every
   admission enquiry as CSV (names, schools, phone numbers, emails).
4. `/Dashboard/attendance` takes `regno` from POST body with **no ownership check** —
   any reg-no can be posted to pull any student's attendance record.
5. `/Faculty-portal/` authenticates on **employee ID alone** — `Staff.objects.filter(empid=Fid)`
   returning exactly one row is the entire check. The `Fname` field is collected and discarded.
   Anyone who knows or guesses an empid can upload arbitrary files to the server.
6. Student passwords are stored and compared in plaintext, max 40 chars, no validators.

### The `mark` report is broken

`reportdown(request, 'mark')` builds a `marks` list, `print`s it, and then the entire CSV
response is commented out — so the function falls through to
`messages.info(...)` + `redirect('/')`. The UI has already been worked around this: the
MARK-LIST nav item calls `hello('marks')` (client-side div toggle) instead of
`sendformdata('M')`. Additionally `print(marks[0][1])` will **raise IndexError** if the
student has no marks. Only ATTENDANCE actually posts to this view.

---

## 8. Views — behaviour detail

### `home/views.py`

- `HomeIndex`, `about`, `gallery` — plain template renders.
- `course_service` — on POST, reads seven fields straight out of `request.POST` with no
  Django `Form`, no validation, no try/except; a missing key raises `MultiValueDictKeyError`
  (500). Creates the `Admision` row, re-renders with `result='1'`. **Nothing is emailed or
  notified** — the enquiry just sits in the DB until someone opens the dashboard.
  Note the success banner it renders into lives inside a commented-out block in
  `Wcourses_service.html`, so the user sees no confirmation.
- `Faculty_portal` — see §7.5. Dispatches on the `upload` radio (`notes`/`attendance`/`mark`),
  picks the matching file input, sets a canned `comment` for attendance/mark. **No file type
  or size validation** — any file, any extension, stored under `MEDIA_ROOT` and served back.
  On success: `messages.info` + redirect back to the portal.
- `get_range` — a filter registered onto `django.template.defaulttags.register`, which is a
  hack (it mutates the built-in library) and is **not used by any template**. Dead code.

### `Dashboard/views.py`

- `dashboard` — the login dispatcher described in §7.
- `export` — streams all `Admision` rows to CSV. Header row says 7 columns and matches.
- `reportdown` — attendance CSV works; mark CSV is dead (§7).
- Student marks for the dashboard are assembled in `authuser()` by looping rows and doing a
  **per-row `Course` lookup** (N+1 query) to replace the course id with `cname`.
- `sob[0].image.url` and `sob[0].timetable.url` are dereferenced unconditionally — a student
  with no timetable uploaded gets a `ValueError` (`The 'timetable' attribute has no file`).

---

## 9. Templates and front-end

`templates/base.html` (351 lines) is the shell for every public page. It contains, inline:
the navbar, the **Apply Online modal**, the **Login modal**, the full footer (addresses,
phone numbers, payment QR images, social links), and a `{% for message in messages %}` loop
that renders each Django message as a raw `alert()`.

Blocks it exposes: `title`, `link`, `content`, `aditionaljs` *(sic)*.

| Template | Extends base | Notes |
|---|---|---|
| `home/index.html` | yes | Bootstrap carousel (4 slides, several commented out), about card with a YouTube embed, three hard-coded testimonial cards, hidden "SCAN & PAY / COMING SOON" block |
| `home/Wabout.html` | yes | Six hard-coded management profiles (the 6th, Dr. A. Rosy, is `display:none`), careers banner |
| `home/Wcourses_service.html` | yes | Six hard-coded course cards. ~50 lines of the *old* long-form course copy and the entire *old* inline admission form are commented out but still in the file |
| `home/WGallery.html` | yes | No images — just a `list-group` of **Google Drive folder links**. ~120 lines of the real photo-grid gallery are commented out inside a `{% block deletedcontent %}` |
| `home/WFaculty_portal.html` | yes | Upload form + inline JS that toggles required-ness of the three file inputs |
| `dashboard/dashboard.html` | yes | Admission list table + CSV export icon |
| `dashboard/dashboard_user.html` | **no** | Standalone full HTML doc; duplicates the CDN links; has stray no-op `{% block %}` tags after `</html>` |
| `admin/base_site.html` | admin/base | Rebrands the admin header only |

### Front-end debt worth knowing before you redesign

- Title block on `Wcourses_service.html` says **"About Us"** (copy-paste from `Wabout.html`).
- Navbar dropdowns link to `#infrastructure`, `#expo2021`, `#expo2019`, `#daycare` on the
  gallery page — **none of those anchors exist any more**, they were in the commented-out
  gallery. All four links land at the top of the gallery.
- `dashboard_user.html:15` uses a **Windows backslash** in the static path:
  `{% static 'css\dashboard_user.css' %}` → resolves to `/static/cssdashboard_user.css`,
  a 404. **The student dashboard has been rendering unstyled in production.**
- `index_test.js` `myFunction()` (mobile nav toggle) does `document.getElementById("footer")`,
  but no element has `id="footer"` — the footer uses `<footer class="page-footer">`. This
  throws on every mobile menu tap and the nav never opens.
- Enormous amounts of inline `style=` attributes, several `style` attributes duplicated on
  the same tag (later one silently wins), and deprecated `<center>` tags throughout.
- CSS filenames are legacy: `index_test.css` is the *global site* stylesheet.
- `home/index.html` links `Whomepage.css?v=2` while `Wabout.html` links it with no cache-buster.

---

## 10. Deployment

**Pipeline** — `.github/workflows/deploy.yml`, triggered on push to `main` only.
Uses `appleboy/ssh-action@v0.1.5` with secrets `SERVER_HOST`, `SERVER_USER`, `SERVER_SSH_KEY`:

```
cd /home/ubuntu/app && git pull
source venv/bin/activate
python manage.py collectstatic --noinput
python manage.py migrate --noinput
sudo systemctl restart gunicorn && sudo systemctl restart nginx
```

Note: the step is misleadingly named "Checkout repository", there is no
`pip install -r requirements.txt` step (new dependencies will **not** be installed by a deploy),
and there is no build/test gate — a push to `main` deploys straight to production.

**gunicorn** — `gunicorn.service`: 3 workers, `unix:/run/gunicorn.sock`, `Requires=gunicorn.socket`
(the matching `gunicorn.socket` unit is **not in this repo**).

**nginx** — `sites-available_slash_wisdomcc`:
- `:80` serves `wisdomcc.in` / `3.146.206.48`; `/static/` aliased to `/home/ubuntu/app/static`;
  everything else proxied to the gunicorn socket.
- `:443` is configured with the **snakeoil self-signed cert** and does
  `return 301 http://$host$request_uri` — i.e. **HTTPS is deliberately redirected down to HTTP**.
  There is no real TLS. Every login (student password, admin password) crosses the wire in cleartext.

### The media-files gap

`urls.py` appends `static(settings.MEDIA_URL, document_root=MEDIA_ROOT)` unconditionally, but
Django's `static()` helper **returns an empty list when `DEBUG=False`**. nginx has no
`location /media/` block. Therefore, in production:

- student profile photos → broken
- student timetable images → broken
- faculty notes downloads → broken

Uploads still *write* to `/home/ubuntu/app/media/` (the dir is created on first upload); they
are simply never served. `MEDIA_ROOT` is also outside any backup or the git repo.

---

## 11. Risks and defects — consolidated

Ordered roughly by severity. File references are clickable.

### Security

| # | Issue | Where |
|---|---|---|
| S1 | `local_settings.py` is **committed to git** — `SECRET_KEY`, DB password `coldfeet1` are in public history. `.gitignore` has the entry but commented out. | [wisdomcc/local_settings.py](../wisdomcc/local_settings.py) |
| S2 | HTTPS 301-redirects **to** HTTP; snakeoil cert. All credentials sent in cleartext. | [sites-available_slash_wisdomcc](../sites-available_slash_wisdomcc) |
| S3 | Student passwords stored and compared as **plaintext**. | [Dashboard/models.py](../Dashboard/models.py), [Dashboard/views.py:37](../Dashboard/views.py#L37) |
| S4 | `/Dashboard/export/` — **no auth**; dumps all enquirer PII to CSV. | [Dashboard/views.py:76](../Dashboard/views.py#L76) |
| S5 | `/Dashboard/attendance` — **no auth, no ownership check**; any `regno` in POST body. | [Dashboard/views.py:93](../Dashboard/views.py#L93) |
| S6 | Faculty portal authenticates on **empid alone**; unrestricted file upload follows. | [home/views.py:38-45](../home/views.py#L38-L45) |
| S7 | Admin login does not call `auth.login()` and never checks `is_staff`. | [Dashboard/views.py:30](../Dashboard/views.py#L30) |
| S8 | `ALLOWED_HOSTS` contains `'*'`. | [wisdomcc/local_settings.py](../wisdomcc/local_settings.py) |
| S9 | `wisdomccPemKey.pem` (EC2 private key) sits in the working dir. Gitignored, but one `git add -f` from disaster. | repo root |
| S10 | No `SECURE_*`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, or HSTS settings. | [wisdomcc/settings.py](../wisdomcc/settings.py) |

### Functional bugs

| # | Issue | Where |
|---|---|---|
| F1 | Student dashboard CSS 404s — backslash in `{% static %}` path. | [templates/dashboard/dashboard_user.html:15](../templates/dashboard/dashboard_user.html#L15) |
| F2 | All media (photos, timetables, notes) unreachable in production. | §10 |
| F3 | Mark-list CSV export is commented out; `print(marks[0][1])` IndexErrors on empty marks. | [Dashboard/views.py:115-138](../Dashboard/views.py#L115-L138) |
| F4 | Mobile nav toggle throws on missing `#footer`. | [wisdomcc/static/js/index_test.js](../wisdomcc/static/js/index_test.js) |
| F5 | Gallery dropdown anchors point at sections that no longer exist. | [templates/base.html:59-62](../templates/base.html#L59-L62) |
| F6 | Student with no timetable/photo → `ValueError` on `.url`. | [Dashboard/views.py:60](../Dashboard/views.py#L60) |
| F7 | Admission POST with a missing field → unhandled `MultiValueDictKeyError` 500. | [home/views.py:18-25](../home/views.py#L18-L25) |
| F8 | Admission success banner is inside a commented-out block — user gets no confirmation. | [templates/home/Wcourses_service.html](../templates/home/Wcourses_service.html) |
| F9 | Dashboards are POST-response-only: no bookmark, no refresh, no logout. | §7 |
| F10 | Course page `<title>` says "About Us". | [templates/home/Wcourses_service.html:5](../templates/home/Wcourses_service.html#L5) |
| F11 | Root `static/` build output is stale vs `wisdomcc/static/`. | §3 |

### Structural / maintainability

- Django 6.0.1 running code written for 3.2.3; never audited across four major versions.
- Unpinned `requirements.txt`, and the deploy never reinstalls dependencies anyway.
- Zero tests (`tests.py` in both apps are the untouched stubs).
- No `Form`/`ModelForm` anywhere — every POST is hand-parsed from `request.POST`.
- Business logic (`authencateuser`) is a class instantiated inside a function view; no service
  layer, no separation of concerns.
- All FKs `DO_NOTHING`; no `related_name` anywhere.
- `TIME_ZONE = 'UTC'` for an India-only institute.
- No `LOGGING` config; leftover `print()` calls in production paths.
- All addresses, phone numbers, staff bios, testimonials, courses and gallery links are
  **hardcoded in templates** — there is no CMS-able content model at all.
- Large blocks of dead commented-out HTML in `Wcourses_service.html`, `WGallery.html`, `index.html`.
- Misspellings baked into the schema (`Admision`) and template blocks (`aditionaljs`).

---

## 12. What to settle before the requirements change

These are the decisions that will shape any large change; they are listed as questions, not
recommendations, because they're yours to make.

1. **Auth rewrite.** Do `Student` and `Staff` become `django.contrib.auth` users (custom user
   model or profile FK), with real sessions, hashed passwords, `@login_required`, and a logout?
   Almost every other change depends on this answer, and a custom user model is far cheaper to
   introduce with a fresh migration set than later.
2. **Django upgrade.** Audit-and-upgrade to a current LTS *before* or *as part of* the change,
   with pinned versions and a `pip install` step in the deploy.
3. **Branch/location as a model.** Redhills/Kanathur is currently a magic string. If the
   requirements involve multi-branch anything, this needs a real `Branch` model with FKs from
   `Student`, `Staff`, `Admision`, and content.
4. **Content management.** Should courses, testimonials, staff profiles, gallery and contact
   details move out of templates into models editable via admin?
5. **Media strategy.** Fix locally (nginx `/media/` block) or move to S3/object storage? This
   also decides whether uploads survive an instance replacement.
6. **Do the faculty uploads need to become data?** Today attendance and marks arrive as opaque
   files and are re-keyed by hand. If the requirement is real attendance/marks workflow, that's
   parsing or direct data entry, not file upload.
7. **Enquiry workflow.** `Admision` has no timestamp or status. Any follow-up/CRM requirement
   needs both, plus notifications (email/SMS/WhatsApp — none exist today).
8. **TLS.** Real certificate (Let's Encrypt) before any auth work ships.
9. **Front-end direction.** Stay server-rendered Django templates + Bootstrap, or introduce a
   build step / component framework? The current templates are not worth incrementally
   refactoring if a redesign is in scope.
10. **Rebuild vs. evolve.** Given §11, if the requirements change is genuinely "massive", a
    fresh app package reusing the data model and copy — rather than in-place surgery on
    `base.html` and `authencateuser` — may be the shorter path. Worth an explicit call.

---

## 13. Local setup (verified)

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
# edit wisdomcc/local_settings.py for your DB (or point it at sqlite)
./venv/bin/python manage.py migrate
./venv/bin/python manage.py createsuperuser
./venv/bin/python manage.py collectstatic
./venv/bin/python manage.py runserver
```

`./venv/bin/python manage.py check` currently reports **0 issues**.

The README's steps 10–14 (autossh into EC2, tmux, gunicorn/nginx placement) describe
production server setup, not local development.
