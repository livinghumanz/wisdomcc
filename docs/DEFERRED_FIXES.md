# Deferred fixes

Known defects found in the 2026-09-02 baseline review, parked by decision — we are doing UI
work first. Full explanation of every item is in [SYSTEM_OVERVIEW.md §11](SYSTEM_OVERVIEW.md#11-risks-and-defects--consolidated);
this file is just the tickable list so nothing gets lost.

IDs match the overview. Tick with `[x]` and add the commit when one gets fixed.

## Security

- [ ] **S1** `wisdomcc/local_settings.py` committed to git — SECRET_KEY + DB password in history
- [ ] **S2** HTTPS 301-redirects *to* HTTP on a snakeoil cert; credentials in cleartext
- [ ] **S3** Student passwords stored and compared in plaintext
- [ ] **S4** `/Dashboard/export/` has no auth — dumps all enquirer PII as CSV
- [ ] **S5** `/Dashboard/attendance` has no ownership check on `regno`
- [ ] **S6** Faculty portal authenticates on empid alone, then accepts any file
- [ ] **S7** Admin login never calls `auth.login()`, never checks `is_staff`
- [ ] **S8** `ALLOWED_HOSTS` contains `'*'`
- [ ] **S9** `wisdomccPemKey.pem` (EC2 private key) sits in the working directory
- [ ] **S10** No `SECURE_*` / secure-cookie / HSTS settings

## Functional

- [ ] **F1** Student dashboard CSS 404s — backslash in `{% static 'css\dashboard_user.css' %}`
- [ ] **F2** All media (photos, timetables, notes) unreachable in production
- [ ] **F3** Mark-list CSV export commented out; `print(marks[0][1])` IndexErrors on empty marks
- [x] **F4** Mobile nav toggle throws on missing `#footer` element — fixed in the UI-001 redesign
- [x] **F5** Gallery dropdown anchors point at sections that no longer exist — removed in the UI-001 redesign
- [ ] **F6** Student with no timetable/photo → `ValueError` on `.url`
- [ ] **F7** Admission POST with a missing field → unhandled 500
- [ ] **F8** Admission success banner is inside a commented-out block — no confirmation shown
- [ ] **F9** Dashboards are POST-response-only: no bookmark, no refresh, no logout
- [x] **F10** Course page `<title>` says "About Us" — fixed by the new base template
- [ ] **F11** Root `static/` build output stale vs `wisdomcc/static/`

## Structural

- [ ] Django 6.0.1 running code written for 3.2.3 — never audited across four majors
- [ ] `requirements.txt` unpinned, and the deploy never runs `pip install`
- [ ] Zero tests (both `tests.py` are untouched stubs)
- [ ] No `Form`/`ModelForm` — every POST hand-parsed from `request.POST`
- [ ] All FKs `on_delete=DO_NOTHING`; no `related_name`
- [ ] `TIME_ZONE = 'UTC'` for an India-only institute
- [ ] No `LOGGING` config; leftover `print()` in production paths
- [ ] No `Branch` model — "redhills"/"kanathur" is a magic string
- [ ] All content (addresses, bios, testimonials, courses) hardcoded in templates
- [ ] Large blocks of dead commented-out HTML in `Wcourses_service.html`, `WGallery.html`, `index.html`

## Notes

Some of these are cheap to fix *while* doing UI work and I'll flag them when I'm already in
the file — F1, F4, F5, F8, F10 and F11 in particular. Say the word and I'll fold them in;
otherwise I leave them alone and just tick nothing.
