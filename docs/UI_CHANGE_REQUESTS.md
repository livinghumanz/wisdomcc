# UI Change Requests — intake log

**This is the file you write in.** Drop whatever you want changed at the top of the
Inbox below, in whatever shape is convenient. I read this file at the start of each
session, pick up anything marked `NEW`, and move it down to Done when it ships.

Rules of thumb:
- **Don't polish it.** Half a sentence and a screenshot path is enough. I'll ask if I need more.
- Put new items at the **top** of Inbox, newest first.
- Leave the status marker alone — I update it.
- Related background lives in [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md); known defects we're
  deliberately deferring are in [DEFERRED_FIXES.md](DEFERRED_FIXES.md).

Status markers: `NEW` (waiting on me) · `WIP` · `NEEDS INFO` (I asked a question, see the
note under the item) · `DONE` · `DROPPED`

---

## Inbox

<!-- ============ ADD NEW REQUESTS HERE, NEWEST AT THE TOP ============ -->

<!-- Copy this block:

### [NEW] <short title>
- **Date:**
- **Page / screen:** (e.g. home, about, courses, gallery, faculty portal, student dashboard, admin dashboard, navbar, footer, login modal, apply-online modal)
- **What's wrong / what you want:**
- **Reference:** (screenshot path, URL, "like X site", or nothing)
- **Notes:**

-->

### [WIP] UI-001 — Wisdom Group rebrand + London Kids / Wisdom Kids brand separation
- **Date:** 2026-09-02
- **Page / screen:** whole site — new brand structure, new home page(s)
- **What's wrong / what you want:** WCC is being rebranded under an umbrella "Wisdom Group of
  Institutions". A franchise/tie-up preschool sits under it. Client wants the two separated —
  a good-UI home page for Wisdom Coaching Centre and a separate one for the preschool. Logo
  update also requested. Full copy, contact directory, website requirements and SEO keywords
  captured in the brief.
- **Reference:** [requests/UI-001-wisdom-group-london-kids.md](requests/UI-001-wisdom-group-london-kids.md)
- **Notes:** ⚠️ **Blocked on 3 answers** before any build starts:
  (1) the brand name — all the copy says *London Kids International Play School*, both logos say
  *Wisdom Kids International Preschool*; (2) site structure — umbrella landing vs path vs
  subdomain vs separate domain; (3) logo source files (only raster images sent, none in repo yet).
  Also worth telling the client early: the "visitors before we started" report in their
  requirements **cannot be produced** — no analytics has ever been installed, so the baseline
  can only start the day we add it.
- **Progress (2026-09-02):** First increment built — `institutions` app (Brand / Program /
  BrandSection / Branch models, admin-editable), preschool site live at `/preschool/` with its
  own chrome, all client copy seeded via data migration, 4 tests passing. Assumptions taken so
  work could start are listed in §9 of the brief — **review them**. Not committed yet.
- **Progress (2026-09-02, second pass):** WCC side redesigned too — new `base.html` chrome across
  the whole site, new `wcc.css`, rebuilt home page, branch data now model-driven. Fixed deferred
  F4, F5 and F10 along the way. Details and three further assumptions in §10 of the brief.
- **Progress (2026-09-02, visual QA):** Screenshot tooling set up (`~/.cache/wisdomcc-shots/shoot.sh`);
  reviewed every page at desktop and mobile. Root cause of the broken-looking layout was a
  stylesheet/template class mismatch that left all card interiors unstyled — fixed, along with
  nav overlap, grid balance, uneven card heights and mobile overflow. §12 of the brief.
- **Progress (2026-09-02, brand chooser):** Home page now leads with the two-brand chooser —
  hover pops children out of each box; WCC → courses, London Kids → /preschool/. Slider moved
  to a full-width band with `contain` so nothing is cropped. Navbar compacted to 51px. Hero and
  buttons given gradient treatment. §13 of the brief. **Needs real London Kids child photos.**

---

## Done

_Nothing yet._

---

## Standing UI preferences

Anything you tell me once that should apply to *all* future UI work goes here, so I don't
have to be reminded. I'll add to this as we go — feel free to add your own.

- _(empty)_

---

## Quick reference — where things live

So you can point at a file if that's faster than describing it.

| What you see | File |
|---|---|
| Navbar, footer, login modal, apply-online modal | [templates/base.html](../templates/base.html) |
| Home page (carousel, about blurb, testimonials) | [templates/home/index.html](../templates/home/index.html) |
| About / management profiles | [templates/home/Wabout.html](../templates/home/Wabout.html) |
| Course cards | [templates/home/Wcourses_service.html](../templates/home/Wcourses_service.html) |
| Gallery (Drive links) | [templates/home/WGallery.html](../templates/home/WGallery.html) |
| Faculty upload form | [templates/home/WFaculty_portal.html](../templates/home/WFaculty_portal.html) |
| Admin enquiry table | [templates/dashboard/dashboard.html](../templates/dashboard/dashboard.html) |
| Student dashboard | [templates/dashboard/dashboard_user.html](../templates/dashboard/dashboard_user.html) |
| Site-wide CSS (navbar, footer, modals) | [wisdomcc/static/css/index_test.css](../wisdomcc/static/css/index_test.css) |
| Home/about/courses CSS | [wisdomcc/static/css/Whomepage.css](../wisdomcc/static/css/Whomepage.css) |
| Gallery CSS | [wisdomcc/static/css/WGallery.css](../wisdomcc/static/css/WGallery.css) |
| Student dashboard CSS | [wisdomcc/static/css/dashboard_user.css](../wisdomcc/static/css/dashboard_user.css) |
| Nav toggle + modal JS | [wisdomcc/static/js/index_test.js](../wisdomcc/static/js/index_test.js) |
| Images | [wisdomcc/static/img/](../wisdomcc/static/img/) |

Edit `wisdomcc/static/` only — the root `static/` folder is generated by `collectstatic`.
