# UI-001 — Wisdom Group rebrand + London Kids brand separation

**Status:** `NEW` · **Raised:** 2026-09-02 · **Source:** client (relayed by Ramesh)
**Tracking entry:** [UI_CHANGE_REQUESTS.md](../UI_CHANGE_REQUESTS.md)

> This is the first request of the larger requirements change. It is a **brief**, not a plan —
> nothing here has been built or decided yet. Edit it freely as the client sends more.

---

## 1. The ask, in one paragraph

The client is rebranding **Wisdom Coaching Centre** under an umbrella identity,
**Wisdom Group of Institutions**. Under that umbrella sits a second brand,
**London Kids International Play School**, described as a franchise / tie-up
("A Unit of Wisdom Group of Institutions"). They want the two **visually and
structurally separated**: one home page with good UI for Wisdom Coaching Centre, and a
separate one for London Kids. Logo update also requested. More requirements are expected.

---

## 2. Open questions — need answers before design starts

These are listed in the order they'll block work.

1. **⚠️ Brand name conflict — "London Kids" or "Wisdom Kids"?**
   All the written copy the client sent says **London Kids International Play School**.
   Both logo images he then sent say **WISDOM KIDS INTERNATIONAL PRESCHOOL**
   ("Educate, Enjoy, Explore"). Those are two different names *and* two different
   descriptors (Play School vs Preschool). Possibilities: the franchise is being renamed;
   these are two separate brands under the group; or the logos are drafts/explorations.
   **Do not build anything until this is answered** — the name drives the domain, the page
   titles, every SEO keyword, and the logo itself. See §8.
2. **Site structure.** Which of these is it?
   - (a) One umbrella `wisdomcc.in` landing page for Wisdom Group, linking to a WCC section
     and a London Kids section
   - (b) `wisdomcc.in` stays the WCC home, London Kids lives at `/london-kids/` or a subdomain
   - (c) Two genuinely separate sites/domains, sharing one Django project
   - (d) Two separate projects entirely

   This decides URL structure, navigation, and — importantly — how SEO effort splits between
   the brands. **Everything else waits on this and on the name above.**
3. **Domain(s).** Does London Kids get its own domain, a subdomain, or a path? Has anything
   been registered already?
4. **Shared or separate chrome?** Does London Kids get its own navbar, footer, colour palette
   and logo (likely, for a play school vs a NEET coaching centre), or a shared Wisdom Group
   shell with a brand switch?
5. **Is Kanathur still active?** The current site advertises Redhills + Kanathur branches. The
   contact list in this brief names **Gandhi Nagar** and **Kamaraj Nagar** (both Redhills) and
   does **not** mention Kanathur. Is Kanathur closed, renamed, or just omitted?
6. **London Kids address vs WCC Kamaraj Nagar** — London Kids is at Vetrivel Street, Kamarajar
   Nagar, Redhills, and there is also a "Wisdom Coaching Centre, Kamaraj Nagar". Same campus?
7. **Logos.** Need the actual asset files — Wisdom Group, Wisdom Coaching Centre, London Kids.
   What formats exist (SVG preferred, PNG with transparency acceptable)?
8. **"Looping link to connect our WhatsApp catalog"** — unclear phrasing. Does this mean a
   persistent floating WhatsApp button on every page, a link to a WhatsApp Business catalog,
   or a `wa.me` click-to-chat link? Ask the client what they picture.
9. **Photos for VAC / Playgroup** — who supplies them, and when?

---

## 3. Content supplied by the client — London Kids

Reproduced as sent. This is the source copy for the London Kids pages.

### Hero / welcome

> **Welcome to London Kids International Play School**
> *(A Unit of Wisdom Group of Institutions)*
>
> At London Kids International Play School, we believe every child deserves a joyful beginning
> to their learning journey. As a proud member of the Wisdom Group of Institutions, we provide
> a safe, caring, and stimulating environment where children learn through play, exploration,
> and meaningful experiences.
>
> Our child-centered approach helps build confidence, creativity, communication skills, and a
> lifelong love for learning.

### About Us

> London Kids International Play School is dedicated to providing quality early childhood
> education that nurtures every child's intellectual, emotional, social, and physical
> development.
>
> Our experienced educators create engaging learning experiences using interactive activities,
> storytelling, music, art, games, and hands-on exploration. We focus on developing strong
> foundations that prepare children for future academic success.

### Our Programs

| Program | Age | Focus areas |
|---|---|---|
| **Play Group** | 2–3 years | Social interaction · Sensory play · Fine and gross motor skills · Language development · Music and movement · Creative activities |
| **Nursery** | 3–4 years | Early literacy · Number concepts · Vocabulary building · Creative thinking · Social skills · Independence |
| **Junior KG (LKG)** | 4–5 years | Reading readiness · Writing practice · Basic mathematics · General awareness · Art and creativity · Communication skills |
| **Senior KG (UKG)** | 5–6 years | Reading and writing · Mathematics · Science concepts · Logical thinking · Problem-solving · Leadership and confidence |

Intro lines as sent:
- Play Group — "Our Play Group program introduces children to a fun and welcoming learning environment. Activities focus on:"
- Nursery — "The Nursery program encourages curiosity and early learning through engaging activities that develop:"
- Junior KG — "Our Junior KG curriculum prepares children with strong foundational skills through:"
- Senior KG — "Senior KG prepares children for primary school by strengthening:"

### Our Speech Curriculum

> One of the highlights of our educational program is our specially designed Speech Curriculum,
> which helps children become confident communicators from an early age.

Includes: Daily conversation practice · Vocabulary enrichment · Storytelling · Rhymes and songs ·
Public speaking activities · Show and Tell · Role play · Phonics-based pronunciation ·
Listening skills · Confidence-building exercises

> Our goal is to help every child communicate clearly, confidently, and effectively.

*(Client calls this "one of the highlights" — treat it as a featured section, not a bullet list
buried in a page.)*

### Why Choose London Kids?

Safe and child-friendly campus · Experienced and caring teachers · Play-based learning approach ·
Smart classrooms · Activity-based curriculum · Speech Development Program · Individual attention ·
Creative learning environment · Regular parent interaction · Celebration of festivals and special
days · Indoor and outdoor activities · Focus on holistic child development

### Our Learning Approach

> We believe children learn best when they are happy, engaged, and encouraged to explore.

Learning through play · Activity-based education · Hands-on experiences · Interactive storytelling ·
Music and movement · Creative arts and crafts · Practical life activities · Experiential learning

### Vision

> To inspire young minds through quality early childhood education while nurturing confident,
> compassionate, and lifelong learners.

### Mission

> To provide a joyful, safe, and stimulating environment where every child develops academically,
> socially, emotionally, and creatively through innovative teaching methods and personalized care.

### Facilities

Bright and colorful classrooms · Safe indoor play area · Outdoor play zone · Learning resource
center · CCTV surveillance · Hygienic campus · Child-friendly furniture · Activity room ·
Celebration area · Parent interaction sessions

### Admissions

> Admissions are now open for: Play Group · Nursery · Junior KG · Senior KG
>
> Give your child the perfect start with an education that builds confidence, creativity,
> communication, and character.
>
> Enroll today and become a part of the London Kids International Play School family.

### Tagline

> "Where Little Minds Grow, Explore, and Shine."

---

## 4. Branch / contact directory

Client instruction: **"Use logos for all social media accordingly."**
Shared WhatsApp number across the group: **9791148553**

### London Kids International Play School (A Wisdom Group of Institutions)

| | |
|---|---|
| Programs | Play Group \| Nursery \| Junior KG \| Senior KG |
| Phone | 9791148553 |
| Email | info.londonkidsredhills@gmail.com |
| Address | Vetrivel Street, Kamarajar Nagar, Redhills, Chennai 600052 |
| Facebook | https://www.facebook.com/share/1ELhBVdH7B/ |
| Instagram | https://www.instagram.com/londonkidsredhills?igsh=MXF1eWw0N3Byc2Nlbw== |
| WhatsApp Channel | https://whatsapp.com/channel/0029VaULsccLSmbbiZnrTR15 |
| YouTube | https://youtube.com/@wisdomcoachingcentre7947 |
| Google Maps | https://maps.app.goo.gl/Y6XWJrQBJrTf9UxF9 |

### Wisdom Coaching Centre — Gandhi Nagar

| | |
|---|---|
| Facebook | https://www.facebook.com/wisdomcoachingcentre20/ |
| Instagram | https://www.instagram.com/wisdom_coaching_centre20/ |
| YouTube | https://youtube.com/@wisdomcoachingcentre7947 |
| Google Maps | https://maps.app.goo.gl/WQfgRTnc82DhU7uG8 |

### Wisdom Coaching Centre — Kamaraj Nagar

| | |
|---|---|
| Facebook | https://www.facebook.com/profile.php?id=100091439325900 |
| Instagram | https://www.instagram.com/wisdomcoachingcentre_redhills/ |
| YouTube | https://youtube.com/@wisdomcoachingcentre7947 |
| Google Maps | https://maps.app.goo.gl/QBc5XRexhtTXc3xX6 |

### Notes on this directory

- The **YouTube channel is shared** across all three — one link, three placements.
- The site currently hardcodes **different** Facebook/Instagram links and an old Instagram
  *invite* URL in [templates/base.html](../../templates/base.html); those are superseded by
  the table above.
- Phone numbers currently in the footer (044-26323939 / 9791148553 for Redhills,
  044-27444739 / 7200744739 for Kanathur) are **not** in this brief. Confirm what stays.
- No address supplied for either WCC branch in this brief — only for London Kids. Needed.

---

## 5. Website requirements as stated by the client

Verbatim, with my read on what each actually involves. **Only the first three are UI work.**

| # | Client's words | What it actually needs |
|---|---|---|
| R1 | "Need to maintain the website with updates of programs in different branches. (Twice a month)" | Content must be **editable without a code deploy** — i.e. programs/branches become database models edited via admin. This forces the CMS decision in [SYSTEM_OVERVIEW §12.4](../SYSTEM_OVERVIEW.md#12-what-to-settle-before-the-requirements-change). Today every word is hardcoded in templates. |
| R2 | "Need to display content related to VAC, Playgroup and a few photos of it." | New/expanded content sections + a real image gallery. Note the current gallery is only Google Drive links, and **uploaded media does not serve in production** (deferred F2) — that has to be fixed before any photo feature works. |
| R3 | "Need to update details like branch and location of it" | A proper **`Branch` model** with address, phone, maps link and social handles. Today "redhills"/"kanathur" is a magic string ([SYSTEM_OVERVIEW §12.3](../SYSTEM_OVERVIEW.md#12-what-to-settle-before-the-requirements-change)). |
| R4 | "Need to display our website top when user search with certain keywords (Covering all courses)" | **SEO.** Not a UI task. Needs: per-page `<title>`/meta descriptions (site has none), `sitemap.xml`, `robots.txt`, structured data, Google Business Profile per branch, and **working HTTPS** — the server currently 301-redirects HTTPS *down* to HTTP on a self-signed cert (deferred **S2**), which alone will suppress ranking. No ranking can be promised, only the groundwork. |
| R5 | "Need a report of no of users visited before and after our service started and a monthly visiting users report." | **Analytics.** Needs Google Analytics 4 + Search Console installed. ⚠️ "Before our service started" data **cannot be recovered retroactively** — no analytics has ever been installed on this site. The baseline starts the day we install it. Tell the client this early. |
| R6 | "Need to create looping link to connect our whatsapp catalog" | Unclear — see open question 8. Likely a floating WhatsApp button + `wa.me` / catalog link. |
| R7 | "Newsletter" | Email capture form + a sending mechanism. The project has **no email configuration at all** (no `EMAIL_*` settings). Needs either an ESP (Mailchimp/Brevo/etc.) or SMTP + a subscriber model. Also a consent/unsubscribe path. |

---

## 6. SEO keywords supplied

Client wants these covered across courses/programs:

Tuition · One to One Session · Preschool · Daycare · Playschool · Abacus · Spoken English ·
Hindi Prachar Sabha · Spoken Hindi · Music · Drawing · Yoga

**Gap:** the current site's course page covers only NEET, mock tests, regular coaching (8–12),
VAC, Hindi and Abacus. These keywords are **not represented anywhere on the site today**:
One to One Session · Preschool · Daycare · Playschool · Spoken Hindi · Music · Drawing · Yoga.

Keywords only rank if there is real page content behind them — each of these needs a genuine
section or page, not a meta tag. Confirm with the client that all twelve are services they
actually offer, and at which branches.

---

## 7. Still outstanding from the client

- Logo files (Wisdom Group, WCC, London Kids) — "logo update" requested, assets not yet sent
- "and some more" — client has further requirements not yet relayed
- Photos for VAC and Playgroup
- Addresses/phones for the two WCC branches

---

## 8. Logo assets shared by the client (2026-09-02)

Two logo images were sent in chat. **The image files are not yet in the repo** — Ramesh needs
to save them to `docs/requests/assets/UI-001/` (any filename), and the production-ready
versions eventually to `wisdomcc/static/img/brand/`.

Both read: **WISDOM KIDS · INTERNATIONAL PRESCHOOL · "Educate, Enjoy, Explore"** —
see the ⚠️ name conflict in open question 1.

**Variant A — circular badge.** A rainbow-ringed circle on white. Cartoon panda mascot in a
colourful outfit waving, sitting behind a white banner, rainbow arc + clouds + stars behind it.
"WISDOM" in multicolour rounded caps, "KIDS" below in blue/pink/green/orange (the dot on the
"i" is a heart), "INTERNATIONAL PRESCHOOL" in navy, tagline in red/green/blue with star accents.
Roughly square (~1250×1250).

**Variant B — horizontal lockup.** Same panda, wider composition — panda with a backpack behind
a stack of books, plus a pencil cup, paint brushes, a paper plane, rainbow and clouds. "WISDOM"
in large glossy multicolour caps, "KIDS" reversed out of a blue ribbon, "INTERNATIONAL
PRESCHOOL" in a yellow pill, tagline below. Shown on black (~1280×853).

### Observations for when we use these

- Both look **AI-generated**: the rendering is raster, not vector. Ask for **SVG or layered
  source** if it exists — at logo sizes in a navbar these will look soft, and neither can be
  cleanly recoloured or resized.
- **Variant B's background needs checking** — if that black is baked in rather than transparent,
  it can't sit on a light navbar. Needs a transparent PNG or SVG.
- **Variant A is the practical one** for a navbar/favicon (square, works small). Variant B suits
  a hero or letterhead. Likely we want both, plus a favicon crop of the panda alone.
- The palette is *very* saturated rainbow — fine for a preschool brand, but it will clash hard
  with the existing WCC site colours (teal `#0ec7a7`, orange footer `#fb6e1a`, pink/red course
  band). This is concrete evidence for giving the two brands **separate chrome** (open question 4).
- No Wisdom Group or Wisdom Coaching Centre logo has been supplied yet — only this one.

---

## 9. What has been built (2026-09-02) — and the assumptions behind it

First increment is done and running locally. **Three assumptions were taken so work could
start; all three are cheap to reverse, but confirm them with the client.**

### Assumptions taken

1. **Brand name is a database field, not copy.** Seeded as "London Kids International Play
   School" because that is what the written copy says. If it turns out to be *Wisdom Kids
   International Preschool*, it is one edit at `/admin/institutions/brand/` — no code change,
   no deploy. The "Why Choose London Kids?" section title is likewise a field.
2. **URL structure:** Wisdom Coaching Centre keeps `/`; the preschool lives at `/preschool/`.
   Chosen because the existing domain holds whatever search history and inbound links exist,
   and a path moves cleanly to a subdomain later if the client wants one.
3. **Separate chrome, not shared.** The preschool has its own navbar, footer, palette and
   stylesheet. The logo's rainbow palette cannot sit inside the coaching centre's teal/orange
   shell without both looking broken. The two link to each other in the nav and footer.

### Files added

| File | What it is |
|---|---|
| `institutions/models.py` | `Brand`, `Program`, `BrandSection`, `Branch` — all admin-editable |
| `institutions/admin.py` | Proper admin: inlines, filters, search, inline reordering |
| `institutions/views.py`, `urls.py` | `/preschool/` |
| `institutions/tests.py` | 4 tests covering render, unpublished sections, inactive brand, bullet parsing |
| `institutions/migrations/0001_initial.py` | Schema |
| `institutions/migrations/0002_seed_wisdom_group_content.py` | Seeds every word the client supplied |
| `templates/institutions/preschool_base.html` | Preschool chrome — nav, footer, floating WhatsApp |
| `templates/institutions/preschool_home.html` | The home page |
| `wisdomcc/static/css/preschool.css` | Brand stylesheet, palette taken from the logo |

Modified: `wisdomcc/settings.py` (app registered), `wisdomcc/urls.py` (route added).
Nothing in `home/` or `Dashboard/` was touched — the existing site is unchanged.

### What the page has

Sticky nav · hero with logo slot and tagline · About · the four programs as colour-coded cards
with age badges and focus lists · Speech Curriculum as a featured panel · Learning Approach ·
Why Choose · Facilities · Vision & Mission · Admissions call-to-action with call/email buttons ·
contact cards per branch with maps and social icons · footer · floating WhatsApp button.

Responsive down to mobile, keyboard-accessible nav, honours `prefers-reduced-motion`, and
carries a real `<title>` and meta description (first SEO groundwork — see R4).

### Requirements progress

| Req | State |
|---|---|
| R1 — programs editable per branch, twice a month | **Foundation done.** Programs/sections/branches are admin-editable. Programs are per-*brand* today; per-*branch* variation needs one more FK if the client actually runs different programs at different branches — ask. |
| R2 — VAC & Playgroup content + photos | Playgroup content done. **VAC not started** (it belongs on the coaching centre side). Photos blocked on deferred **F2** — uploaded media does not serve in production. |
| R3 — branch and location details | **Done** for the preschool page. The old coaching-centre templates still hardcode addresses; migrating them to `Branch` is the next pass. |
| R4 — search ranking | Started: title + meta description. Still needs sitemap, robots.txt, structured data, per-branch Google Business Profiles, and **working HTTPS (deferred S2)**. |
| R5 — visitor reports | Not started. Needs GA4 + Search Console. Reminder: pre-installation history cannot be recovered. |
| R6 — WhatsApp catalog link | Floating `wa.me` button shipped. Catalog link still needs the client to clarify what he means. |
| R7 — Newsletter | Not started. Project has no email configuration at all. |

### Next up

1. Get the three assumptions above confirmed (especially the name).
2. Get the logo files into `wisdomcc/static/img/brand/` and set them on the Brand record —
   the hero and navbar currently show a panda emoji placeholder where the logo goes.
3. Redesign the Wisdom Coaching Centre home page under the Wisdom Group umbrella.
4. Migrate the old hardcoded branch/course content onto these models.
5. Fix F2 before any photo galleries are promised.

---

## 10. Second increment (2026-09-02) — Wisdom Coaching Centre redesign

The first increment left `/` on the old design. That was a misread of scope: the client asked
for good UI on **both** home pages. The coaching-centre side is now redesigned too.

### What changed

- **`templates/base.html` rewritten.** New chrome for the whole WCC site: an umbrella
  "{Wisdom Group of Institutions}" bar that switches between the two brands, a sticky nav with
  dropdowns, a redesigned footer driven by the `Branch` model, and a floating WhatsApp button.
  Bootstrap 4 and jQuery are still loaded — About, Courses, Gallery and the dashboards depend
  on the grid and on jQuery for the modals. Old backup at `scratchpad/base.html.bak`.
- **`wisdomcc/static/css/wcc.css`** — new site stylesheet, replacing `index_test.css`. Brand
  anchor is the existing teal `#0ec7a7`, paired with deep navy and amber. Classes that would
  collide with Bootstrap are prefixed (`.wbtn`, `.wcard`, `.wdrop`).
- **`templates/home/index.html` rebuilt** — hero with the carousel and trust stats, About with
  the video, six course cards, a cross-promo panel for the preschool brand, testimonials,
  branch cards, and a closing call to action.
- **`institutions/context_processors.py`** — makes group name, both brands and the WCC branches
  available to every template including `base.html`.
- **`wisdomcc/static/js/index_test.js` rewritten** — fixes deferred **F4** (the mobile nav
  threw on a missing `#footer` element and never opened).
- **Migration `0003`** — fills in the Gandhi Nagar address and phones, carried across from the
  old hardcoded footer.

### Deferred items fixed along the way

- **F4** — mobile nav toggle no longer throws.
- **F5** — dead gallery anchors (`#expo2021`, `#daycare`, …) removed from the nav.
- **F10** — the Courses page title said "About Us"; the new base gives every page a real title.

### New assumptions to confirm

4. **The old footer's "Wisdom @ Redhills" address is the Gandhi Nagar branch.** The old address
   reads "Gandhi Nagar west, Redhills", so it was mapped there. **Kamaraj Nagar has no address
   on record** — the client needs to supply one; its card currently shows phone and map only.
5. **Kanathur is still offered in the admission form's location radio**, because nothing has
   confirmed it is closed (open question 5). It has no `Branch` record, so it no longer appears
   in the footer or branch cards. Settle this before it confuses an enquirer.
6. **Home page stats ("Since 2018", "7 days", "Class 8–12")** are drawn from existing site copy.
   Verify the numbers before this goes live.

### Still not done

Wabout / Wcourses_service / WGallery keep their own inner markup — they inherit the new chrome
and a compatibility shim in `wcc.css`, but their bodies have not been rebuilt. That is the next
pass, along with the items in §9.

---

## 11. Management profiles trimmed (2026-09-02)

Client instruction: list **only Ebinezer and Dency**. The four other profiles hardcoded in the
old About page — Aaron Thanasingh, Jansi D Aaron, G. J. Bain and Dr. A. Rosy — are no longer
shown. (Rosy's card was already hidden with `display:none` in the old template.)

Rather than deleting markup, profiles are now a `TeamMember` model, because who is listed is
exactly the kind of thing that changes again. Adding or removing someone is now an admin edit
at `/admin/institutions/teammember/`, not a code change.

`templates/home/Wabout.html` was rebuilt in the new design at the same time — hero, a
two-profile management grid, careers banner. The bios were carried across verbatim.

**Note on photos:** `TeamMember` has both `photo` (admin upload) and `photo_static` (a path to
a file already in `static/`). The seeded profiles use `photo_static`, because uploaded media
still does not serve in production — deferred defect **F2**. Once F2 is fixed, `photo_static`
can be dropped and photos managed entirely through the admin.

The old profile images for the four removed people are still on disk in
`wisdomcc/static/img/About_us/` — nothing was deleted, in case they come back.

---

## 12. Visual QA pass (2026-09-02)

Set up headless-Chromium screenshotting and reviewed every page at 1440px and 390px.
Snap-packaged Firefox could not write screenshots (confinement blocks non-home paths), so
Playwright's Chromium was installed to `~/.cache/ms-playwright`. Capture script:
`~/.cache/wisdomcc-shots/shoot.sh` — restarts the server, then shoots all six pages at both
widths and reports console errors and horizontal overflow.

### The root cause of the "out of sync, not organised" look

`.card__media`, `.card__body` and `.card__tag` were **never renamed** when the Bootstrap-collision
prefixing was applied. The `sed` used `\.card\b`, and `_` is a word character, so `.card__media`
did not match while `.card` did. Templates emitted `wcard__*`; the stylesheet still defined
`card__*`. Every card's interior — image aspect ratio, padding, the tag pill — was unstyled.

### Also fixed

| Problem | Fix |
|---|---|
| Brandmark text overlapped the nav links | The logo is a **wordmark** that already reads "Wisdom Coaching Centre" — the text label beside it was duplicating it and was 164px wide. Removed; logo now sized by height with a max-width. |
| Nav bar crowded, items colliding | Dropped Testimonials and Branches from the top nav (same-page anchors, still in the footer); collapse to the hamburger raised from 980px to 1100px. |
| Six course cards fell 4 + 2 | `.wcard-grid--3` / `--2` modifiers for explicit column counts above 992px. |
| Preschool nav wrapped onto three lines | Added `BrandSection.nav_label` — a short menu label separate from the section title, admin-editable. Blank keeps a section out of the menu. Seeded: Speech, Why Us, Approach, Facilities. |
| Cross-link "Wisdom Coaching Centre" wrapped | Shortened to "Coaching Centre". |
| Cards uneven height in a row | `align-items: stretch` + `height: 100%` on cards, quotes, mini-cards and branch cards. |
| Footer social icons read as blank white discs on navy | Footer-specific translucent-white treatment. |
| Menu button pushed off-screen at 390px (both sites) | The brandmark had `flex: 0 0 auto` and would not shrink. Now shrinks and truncates below the collapse breakpoint. |

### Verified clean

All six pages at 1440px and 390px: no console errors, no page errors, no horizontal overflow,
no clipped text. `manage.py check` clean, 4 tests passing.

**One thing that is not a bug:** the About section's YouTube embed renders as an empty white
box in the screenshots because the headless browser has no outbound network access. It should
be checked once in a real browser.

---

## 13. Brand chooser, slider fix and polish (2026-09-02)

### Brand separation on the home page — as requested

The home page now leads with the two institutions side by side, before anything else:

- **Two boxes**, one per brand, each a full-card link.
- **Children pop out from behind the card on hover** — four circular bubbles rise in a
  staggered arc from under the top edge, with a spring easing. Wisdom Coaching Centre uses the
  three real student photos already in `static/`; London Kids uses coloured bubbles, because
  **no London Kids photos exist yet** — swap those for real children's photos when the client
  supplies them.
- **Click targets:** Wisdom Coaching Centre → `/Course-Services/`; London Kids → `/preschool/`.
- Names, tagline and links come from the `Brand` records, so a rename does not touch markup.
- On touch screens the pop-outs are hidden and the hover-lift disabled — there is no hover
  there, and a stuck `:hover` state after a tap looks broken.

### Slider fixed

The slider was in the hero's right-hand column (hence "half image") and used
`object-fit: cover`, which cropped every slide. The source images range from **2.34** aspect
(`wisdomccBanner.jpg`, 1920×822) to **1.33** (the 4128×3096 photos) — no single crop can suit
both. It is now a **full-width band** below the hero using `object-fit: contain` on a navy
backdrop, so each image is shown whole. Slide image width now scales 1074px → 350px across
1440px → 390px viewports.

### Navbar compacted

Height down to **51px** on desktop (62px with the umbrella bar on tablet and mobile), from a
noticeably taller bar: smaller logo, tighter padding, smaller group bar, and the group-bar
label hidden under 480px.

### Visual lift

Hero given a soft two-tone radial wash instead of flat white; gradient treatments on the
primary and amber buttons; the two brand cards carry their own accent tint that fades in on
hover; navy slider band adds contrast between the hero and the content sections.

### Verified

0 horizontal overflow at 1440 / 1280 / 1024 / 768 / 390px. All six pages clean at desktop and
mobile — no console errors, no clipped text. `manage.py check` clean, 4 tests passing.

**Resolved:** the About-section YouTube embed renders correctly; the earlier blank box was the
sandbox having no outbound network, not a page defect.

### Outstanding for this section

- Real London Kids children's photos to replace the emoji bubbles.
- `wisdomccBanner.jpg` has a large black region baked into the right of the image. It now
  displays whole rather than cropped, so that dead area is visible — worth asking the client
  for a cleaner banner.

---

## 14. Carousel fix (2026-09-02)

**Symptom:** the slider did not work.

**Cause:** `.slider-shell .carousel-item { display: flex }` — added to centre each image inside
the band — outranks Bootstrap's `.carousel-item { display: none }` (two classes vs one, and
`wcc.css` loads after Bootstrap). Nothing was ever hidden: all four slides rendered stacked at
the same position, the last one painting over the rest, so sliding had no visible effect.

**Fix:** size the item on `.carousel-item`, but apply the flex centring only to the slides
Bootstrap actually shows — `.active`, `.carousel-item-next`, `.carousel-item-prev` — leaving
`display: none` intact on the others.

**Verified in a real browser:** exactly one slide visible at a time; next, prev and all four
indicators change the active slide; autoplay advances every 5s; pause-on-hover behaves as
Bootstrap intends.

**Worth remembering:** any custom `display` rule on `.carousel-item` breaks Bootstrap's
carousel. The same trap applies to `.modal`, `.dropdown-menu` and `.collapse` — all of which
this project uses.
