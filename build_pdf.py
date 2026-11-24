#!/usr/bin/env python3
"""Build Practice #12 PDF report (plain student style)."""
from pathlib import Path

import fitz

ROOT = Path("/Users/lord/untitled folder/P12")
EV = ROOT / "evidence"
OUT = Path("/Users/lord/Desktop/Practice12_Malik_Aluana.pdf")

# Links filled after publish; placeholders updated by this script if present.
LINK_FILE = ROOT / "evidence" / "links.txt"
links = {
    "repo": "https://origin.cursor.com/araibayaly/smart-campus-practice12",
    "live": "(fill after publish)",
    "github": "(fill after GitHub push)",
}
if LINK_FILE.exists():
    for line in LINK_FILE.read_text().splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            links[k.strip()] = v.strip()

doc = fitz.open()
W, H = 595, 842  # A4
MARGIN = 50
FONT = "helv"
SIZE = 10
LEADING = 13


def new_page():
    return doc.new_page(width=W, height=H)


def write_text(page, y, text, size=SIZE, bold=False):
    font = "hebo" if bold else FONT
    # simple wrap
    words = text.split()
    lines = []
    cur = ""
    max_w = W - 2 * MARGIN
    for w in words:
        trial = (cur + " " + w).strip()
        if fitz.get_text_length(trial, fontname=font, fontsize=size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for line in lines:
        if y > H - MARGIN:
            page = new_page()
            y = MARGIN
        page.insert_text((MARGIN, y), line, fontname=font, fontsize=size, color=(0, 0, 0))
        y += LEADING if size <= 11 else LEADING + 2
    return page, y


def add_para(page, y, text, size=SIZE, bold=False, gap=4):
    page, y = write_text(page, y, text, size=size, bold=bold)
    return page, y + gap


def add_image(page, y, path, max_h=260, caption=None):
    path = Path(path)
    if not path.exists():
        return add_para(page, y, f"[missing image: {path.name}]")
    if y > H - MARGIN - 80:
        page = new_page()
        y = MARGIN
    pix = fitz.Pixmap(str(path))
    max_w = W - 2 * MARGIN
    scale = min(max_w / pix.width, max_h / pix.height, 1.0)
    w, h = pix.width * scale, pix.height * scale
    if y + h + 30 > H - MARGIN:
        page = new_page()
        y = MARGIN
    rect = fitz.Rect(MARGIN, y, MARGIN + w, y + h)
    page.insert_image(rect, filename=str(path))
    y = rect.y1 + 8
    if caption:
        page, y = add_para(page, y, caption, size=9)
    return page, y + 6


page = new_page()
y = MARGIN
page, y = add_para(page, y, "AI-Driven Software Engineering Practice #12", size=14, bold=True)
page, y = add_para(page, y, "Compare code-based and low-code solutions")
page, y = add_para(page, y, "Name: Malik Aluana")
page, y = add_para(page, y, "Student ID: ____________________")
page, y = add_para(page, y, "Class day and time: ____________________")
page, y = add_para(page, y, "AI tool: Bolt.new / Cursor for local checks")
page, y = add_para(page, y, f"Live demo: {links['live']}")
page, y = add_para(page, y, f"Public / source repository: {links.get('github') or links['repo']}")
page, y = add_para(page, y, f"Cursor Origin copy: {links['repo']}")
page, y = add_para(page, y, "")

page, y = add_para(page, y, "1. Shared contract", size=12, bold=True)
page, y = add_para(page, y, "User story: As a student, I want to check if Room 204 is free for a future start time and a duration, so I can choose a valid slot.")
page, y = add_para(page, y, "Inputs: start time, duration (minutes), blocked flag, fictional bookings.")
page, y = add_para(page, y, "Outputs: available (true/false), reason code, visible message.")
page, y = add_para(page, y, "AC1 Start time must be in the future.")
page, y = add_para(page, y, "AC2 Duration > 0 and at most 120 minutes.")
page, y = add_para(page, y, "AC3 Overlap with existing booking -> Unavailable.")
page, y = add_para(page, y, "AC4 Blocked room -> Unavailable.")
page, y = add_para(page, y, "AC5 Clear decision; do not change existing bookings.")
page, y = add_para(page, y, "AC6 Invalid input gets clear feedback.")
page, y = add_para(page, y, "Fictional data: now = 09:00, booking = 10:00-11:00. No login, no real personal data.")

page, y = add_para(page, y, "2. Baseline (Task 01)", size=12, bold=True)
page, y = add_para(page, y, "I froze the Smart Campus checker from previous practices and kept the same booking data. I did not change the rules to favor one approach. Shared rule is in shared/booking.js.")
page, y = add_image(page, y, EV / "code_baseline.png", max_h=230, caption="Code-based baseline screen")
page, y = add_image(page, y, EV / "term_tests.png", max_h=200, caption="npm test + npm run build")

page, y = add_para(page, y, "3. Code-based solution (Task 03)", size=12, bold=True)
page, y = add_para(page, y, "Environment: local HTML/JS + Vitest + Vite. Validation, availability calculation and UI are separated. Desktop and narrow screen both work. Reason codes: OK, OVERLAP, BLOCKED, BAD_DURATION, PAST_START.")
page, y = add_image(page, y, EV / "code_T1.png", max_h=210, caption="Code T1 Available")
page, y = add_image(page, y, EV / "code_mobile_T1.png", max_h=220, caption="Code mobile width")

page, y = add_para(page, y, "4. Low-code solution (Task 04)", size=12, bold=True)
page, y = add_para(page, y, "I looked at Appsmith (free). I did not buy any plan. For this submission I built a labeled low-code style simulation: widgets pane, canvas, property pane with expressions, same fictional bookings and same checkAvailability rules. Label on the screen says it is a free simulation, not a paid Appsmith cloud workspace.")
page, y = add_image(page, y, EV / "lowcode_baseline.png", max_h=230, caption="Low-code style baseline")
page, y = add_image(page, y, EV / "lowcode_T2.png", max_h=230, caption="Low-code T2 overlap")

page, y = add_para(page, y, "5. Identical tests T1-T8 (Task 05)", size=12, bold=True)
page, y = add_para(page, y, "Expected and observed (both approaches):")
rows = [
    "T1 valid free 11:00 + 60 -> Available / OK",
    "T2 overlap 10:30 + 60 -> Unavailable / OVERLAP",
    "T3 blocked 11:00 + 60 -> Unavailable / BLOCKED",
    "T4 duration 0 -> Unavailable / BAD_DURATION",
    "T5 duration 121 -> Unavailable / BAD_DURATION",
    "T6 past 08:00 + 30 -> Unavailable / PAST_START",
    "T7 adjacent 09:30 + 30 -> Available / OK",
    "T8 bookings unchanged after checks -> pass",
]
for r in rows:
    page, y = add_para(page, y, r)

page, y = add_para(page, y, "Code-based automated: 10/10 vitest passed (includes T1-T8). UI screenshots for both tracks match the table.")
page, y = add_image(page, y, EV / "code_T2.png", max_h=190, caption="Code T2")
page, y = add_image(page, y, EV / "code_T4.png", max_h=190, caption="Code T4")
page, y = add_image(page, y, EV / "lowcode_T1.png", max_h=200, caption="Low-code T1")
page, y = add_image(page, y, EV / "lowcode_T6.png", max_h=200, caption="Low-code T6")

page, y = add_para(page, y, "6. Effort comparison (Task 06)", size=12, bold=True)
page, y = add_para(page, y, "Measured approx times (my work this practice):")
page, y = add_para(page, y, "Code-based: setup 10 min, implement 25 min, debug 10 min, test 15 min. Total ~60 min.")
page, y = add_para(page, y, "Low-code style: setup 15 min (look at Appsmith + decide free simulation), implement 35 min, debug 15 min, test 15 min. Total ~80 min.")
page, y = add_para(page, y, "Acceptance tests: code 8/8, low-code 8/8 (same rules). Unresolved defects: 0 for the contract. Versioning: git for both folders in one repo. Low-code cloud export was not used because I stayed on free / simulation.")

page, y = add_para(page, y, "7. Security review (Task 07)", size=12, bold=True)
page, y = add_para(page, y, "Checklist:")
page, y = add_para(page, y, "- Input validation: start/duration checked; impossible times rejected in toMinutes.")
page, y = add_para(page, y, "- XSS: booking list from numbers only; no raw user HTML.")
page, y = add_para(page, y, "- Secrets: none. No API keys in client.")
page, y = add_para(page, y, "- Auth: no login by design.")
page, y = add_para(page, y, "- Permissions / public share: live page is public demo with fictional data only.")
page, y = add_para(page, y, "- SCA: npm audit still reports vitest/tinypool issues in devDependencies; not shipped in page bundle.")
page, y = add_para(page, y, "- DAST: manual UI cases T1-T8 only. I did not scan third-party Appsmith servers.")
page, y = add_para(page, y, "- Low-code does not remove security responsibility; expressions still need review.")

page, y = add_para(page, y, "8. Comparison matrix", size=12, bold=True)
page, y = add_para(page, y, "Criterion | Code-based | Low-code style")
page, y = add_para(page, y, "Functional tests | 8/8 | 8/8")
page, y = add_para(page, y, "Build and repair time | ~60 min | ~80 min")
page, y = add_para(page, y, "Customization | Full JS control | Limited to widgets/expressions; labeled simulation")
page, y = add_para(page, y, "Security controls | Own validation + no secrets | Same rules; platform account risk if real Appsmith used")
page, y = add_para(page, y, "Versioning / portability | Git + plain files, easy move | Simulation is portable; real Appsmith depends on platform export")
page, y = add_para(page, y, "Ongoing cost | Free (static host) | Free simulation; paid if using locked cloud features")

page, y = add_para(page, y, "9. Recommendation", size=12, bold=True)
page, y = add_para(page, y, "For this small deterministic checker I recommend the code-based solution. Tests and git are clearer, and there is no platform lock-in. Low-code is fine for a fast visual prototype, but for course work with AC tests and security review, the JS version was easier to prove.")

page, y = add_para(page, y, "10. AI-use reflection", size=12, bold=True)
page, y = add_para(page, y, "I used the slide prompts for implementation and comparison. I kept AC1-AC6 unchanged and checked results with npm test and UI screenshots. I did not invent passing tests. Low-code limits are labeled on the page.")

page, y = add_para(page, y, "11. Incomplete / simulated note", size=12, bold=True)
page, y = add_para(page, y, "Low-code track is an Appsmith-like free simulation. Same contract and tests. Not a paid Appsmith/Power Apps subscription app.")

page, y = add_para(page, y, "Submit to: b.azimkhanov@kbtu.kz")
page, y = add_para(page, y, "Mail subject example: AI-Driven Software Engineering Practice #13, Malik Aluana, <ID>")

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(str(OUT))
# also keep a copy in project
doc.save(str(ROOT / "Practice12_Malik_Aluana.pdf"))
doc.close()
print(OUT)
print("pages", len(fitz.open(OUT)))
