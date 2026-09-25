# UI-002 — Admin dashboard: students, marks, attendance, fees

**Status:** `BUILT — pending client answers` · **Raised:** 2026-09-25 · **Source:** client handwritten spec (3 pages, PDF)
**Tracking entry:** [UI_CHANGE_REQUESTS.md](../UI_CHANGE_REQUESTS.md)

---

## 1. What exists today

Checked by logging into both dashboards locally and screenshotting them.

### Admin dashboard (`/Dashboard/`, admin login)

A **single read-only table of admission enquiries** — name, school, contact, location, class,
course, email — plus a CSV export link. That is the entire admin area. None of the screens in
the client's spec exist in any form.

### Student dashboard (`/Dashboard/`, student login)

A sidebar (Profile / Notes / Attendance / Mark-list / Timetable / Log-out) over a profile
panel and a fee-status table. Its current state:

| Problem | Cause |
|---|---|
| Stylesheet 404s, layout collapses, sidebar overlaps the content | `{% static 'css\dashboard_user.css' %}` — a **backslash**. Deferred defect **F1**. Confirmed: backslash path 404, forward-slash path 200. |
| Profile photo and timetable show broken-image placeholders | `MEDIA_URL` is only wired through `static()`, which is a no-op when `DEBUG=False` — i.e. always, in production. Deferred defect **F2**. |
| Aqua background, yellow-green sidebar | Inline `style="background-color: aqua"` plus the stylesheet's own palette. Does not resemble the rest of the site. |

### Blocking problem: the admin area has no real authentication

`Dashboard/views.py` calls `auth.authenticate(...)` and then **never calls `auth.login()`**, never
checks `is_staff`, and has no `@login_required` anywhere. Deferred defects **S7** and **S4**.

Today that exposes only the enquiry list. The spec turns this area into a store of **student PII
and fee records** — Aadhaar numbers, parent mobile numbers, addresses, payment balances. Proper
authentication is therefore a **prerequisite** for this work, not an optional extra, and is being
fixed as part of it.

---

## 2. What the client asked for

Transcribed from the handwritten spec.

### Page 1 — Students Details

Add / delete students, with photo upload and these fields:

| Field | Notes |
|---|---|
| Name | |
| STD | dropdown, **KG – 12th** |
| Category | dropdown — *purpose not stated, see Q1* |
| Curriculum | dropdown — **State / CBSE / IGCSE** |
| School | |
| Address | |
| Father Name | |
| Father mobile No | plus separate **WhatsApp** number |
| Mother Mobile no | plus separate **WhatsApp** number |
| Student Aadhaar no | |
| Branch | dropdown — **WCC R / WCC G / WCC A** |
| Active Status | **Active / Discontinued / Re-Joining** |
| Fee Amount | |
| Team | **Ripplers / Planners** |

### Page 2 — Marks (Internal / External)

- Choose **number of subjects** from a dropdown, then an **Add** button.
- Per subject row: **Name of subject** (dropdown), **Faculty** (dropdown: Faculty 1/2/3),
  **Mark**, **Out of**, **Out of 100**, **P/F**.
- **Total marks** across subjects.
- *"Based on Faculty choosing, the marks of the student should reflect in the faculty Result
  Analysis"* — marks roll up per faculty member.
- *"Based on Sub mark entered, it should reflect in Growth card in bar chart format"* — a
  **Growth Card** bar chart, subjects on the X axis, marks on the Y.

### Page 3 — Attendance

List of **active students** — Sl, Name, SID, School — with three states per student:
**Present / Absent / No Class (Holiday)**. Footer totals: Total Present, Total Absent, No Class.

### Page 3 — Fee Update

List of **active students** — Sl, Name, SID, Fee Amount, Paid Amount, Balance, Admission Amount,
Balance, Jersey Amount, Material Amount, **Total**, **Status (Paid / Yet to pay)**.

---

## 3. Open questions

1. **"Category"** — the spec has a Category dropdown with no values given. What are the options?
   (Stream? Fee category? Day-scholar vs daycare?)
2. **Branch codes "WCC R / WCC G / WCC A"** — R and G presumably Redhills and Gandhi Nagar. What
   is **A**? Note UI-001 established the branches as Gandhi Nagar and Kamaraj Nagar, which does
   not obviously map to R/G/A.
3. **Faculty "Faculty 1 / 2 / 3"** — a placeholder for the real staff list, or literally three slots?
4. **Internal vs External marks** — one entry carrying both, or two separate exam records per subject?
5. **"Out of" vs "Out of 100"** — is "Out of 100" a normalised percentage computed from Mark ÷ Out of,
   or a separately entered figure?
6. **P/F** — entered by hand, or derived from a pass threshold? If derived, what threshold?
7. **Two "Balance" columns** on the fee sheet — one against fees and one against the admission
   amount, or is the second a running total?
8. **Jersey / Material amounts** — fixed per student, per year, or entered ad hoc?
9. **Student ID (SID)** — the existing primary key is `regnum`. Is SID the same thing?

None of these block starting: the data model is being built so each is a field or a choice list
that can be adjusted without restructuring.

---

## 4. What was built (2026-09-25)

Security first, because these screens hold student PII. Then the four screens, built in
parallel by four agents against a fixed shell, URL and model contract, and each reviewed and
re-verified here afterwards.

### Security — prerequisites, now closed

| Defect | Fix |
|---|---|
| **S7** admin login never called `auth.login()` and never checked `is_staff` | Real session login, `is_staff` enforced, `staff_required` on every admin view. Verified: wrong password rejected, non-staff bounced. |
| **S4** `/Dashboard/export/` had no auth at all | Gated. Anonymous request now redirects. |
| **S5** report download trusted a `regno` from the POST body | The regnum now comes from the session, so no one can pull another student's records. |
| **F9** dashboards were POST-response-only | Both are now GET-able and bookmarkable, with a real logout. |
| **F1** student stylesheet 404'd on a backslash path | Corrected to a forward slash. |
| **F2** uploaded media never served in production | nginx now has a `location /media/` block, and the deploy actually installs the config — see below. |

### Screens

- **Students** — filterable list with tiles, photo thumbnails and status pills; a grouped
  add/edit form built as a real `ModelForm` (the project's first); POST-only delete.
- **Marks** — pick student, exam type, date and number of subjects; per-row subject, faculty,
  mark and out-of. "Out of 100" and P/F are **derived, never typed** — proven by posting a
  forged `percent`/`result` and confirming the stored row ignored them.
- **Growth Card** — inline-SVG bar chart, subjects on X and percentage on Y, pass line at 35%,
  bars coloured by result, repeated subjects averaged and flagged.
- **Attendance** — daily three-state register (Present / Absent / No Class) over active
  students, with live totals, mark-all buttons and `update_or_create` upserts.
- **Fees** — spreadsheet-style editable sheet per academic year with derived balances, total
  due and status. Arithmetic is `Decimal` end to end; verified exact to the paisa.
- **Faculty Analysis** — `MarkEntry` rolled up per faculty with a pass-rate comparison chart.

### Bugs found and fixed during review

1. **Attendance history was being silently falsified.** The migration adding
   `Attendance.status` used `default='present'` with no backfill, so every pre-existing row
   claimed the student was present regardless of the legacy `present` flag. Fixed by migration
   `0007_backfill_attendance_status`. Historical rows can only map to present or absent — the
   old schema could not express "no class", so real holidays need re-marking.
2. **`update_or_create` and `update_fields`.** Since Django 4.2 the update branch passes
   `update_fields` to `save()`, so a field that `save()` computes but that is not in `defaults`
   is silently not written. On Django 6.0.1 this left the legacy `present` boolean stale.
3. **`instance.pk` is `''`, not `None`, for a new `Student`** — `regnum` is a `CharField`
   primary key, so the usual `pk is not None` test reported every create as an edit.
4. Uppercase labels with letter-spacing were closing their word gaps ("Total Present").
5. The growth card's pass-line label collided with tall bars; it now carries a white halo.

### Deployment note

The nginx config lives in this repo but **was never installed on the server**, so previous
edits to it had no effect. The deploy now installs it — but only after `nginx -t` validates it,
with a timestamped backup and automatic rollback on failure. `pip install -r requirements.txt`
was also added; the deploy had never installed dependencies.

### Decisions — CONFIRMED by Ramesh, 2026-09-25

All four decisions below were reviewed and accepted. They are settled; do not reopen them
without a new instruction.

1. **Unmarked students are not recorded** in the attendance register rather than defaulted to
   Present. A "Not marked" tile keeps the gaps visible. **Accepted.**
2. **The "Admission Paid" column stays** on the fee sheet even though it is not in the client's
   column list — without it the second Balance column could only ever equal the admission
   amount. **Accepted.**
3. **`dob` remains mandatory** on the student form. **Accepted** — no migration needed.
4. **The student login password renders as visible text** in the admin form. **Accepted and
   explicitly requested:** staff need to read the password back to a student.

   This means **S3 (passwords stored and compared in plain text) is a deliberately accepted
   risk, not an oversight.** Hashing them would make the password unreadable and defeat the
   workflow the client wants, so it must not be "fixed" in passing. The consequence to be aware
   of: anyone with database or backup access can read every student password, and students who
   reuse passwords elsewhere are exposed. If that trade-off ever needs revisiting, the middle
   ground is reversible encryption at rest plus a staff-only reveal action — not hashing.

### Original wording of the above (for reference)

- **Unmarked students are not recorded** in the attendance register rather than defaulted to
  Present. A "Not marked" tile makes gaps visible.
- **An "Admission Paid" column was added** to the fee sheet. It is not in the spec, but without
  it the second Balance column could only ever equal the admission amount.
- **`dob` remains mandatory** on the student form — the column is NOT NULL and a date has no
  empty equivalent. Allowing partial records without a DOB needs a migration.
- **The student login password renders as visible text** in the admin form, because the model
  stores it in plain text (**S3**) and staff need to read it back. Worth fixing properly by
  hashing passwords.
- The nine open questions in section 3 are all still open and still only affect field values,
  not structure.
