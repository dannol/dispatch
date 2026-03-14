#!/usr/bin/env python3
"""
generate-tasks.py
Parses tasks/*.md files and writes tasks.js for the Dispatch UI.
Run whenever you add or update a task file:
    python3 generate-tasks.py
"""

import os
import re
import json
from datetime import datetime, timezone

TASKS_DIR = os.path.join(os.path.dirname(__file__), "tasks")
OUTPUT    = os.path.join(os.path.dirname(__file__), "tasks.js")

# ── Status mapping ────────────────────────────────
STATUS_MAP = {
    "backlog":    "pending",
    "in-progress":"running",
    "blocked":    "blocked",
    "completed":  "done",
    "failed":     "failed",
    "reviewing":  "reviewing",
}

# ── Helpers ───────────────────────────────────────
def parse_frontmatter(text):
    """Extract YAML-ish frontmatter between --- delimiters."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}, text
    fm_text = m.group(1)
    body    = text[m.end():]
    meta    = {}
    for line in fm_text.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        # parse lists like [a, b, c]
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            meta[key] = [v.strip().strip('"').strip("'") for v in inner.split(",") if v.strip()] if inner else []
        elif val.lower() == "null" or val == "":
            meta[key] = None
        elif val.startswith('"') or val.startswith("'"):
            meta[key] = val.strip('"\'')
        else:
            meta[key] = val
    return meta, body

def extract_section(body, heading):
    """Return text under a ## Heading, up to the next ## heading."""
    pattern = rf"##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s|\Z)"
    m = re.search(pattern, body, re.DOTALL)
    return m.group(1).strip() if m else ""

def extract_title(body):
    """Extract the # TASK-XXX: Title line."""
    m = re.search(r"^#\s+\S+:\s+(.+)$", body, re.MULTILINE)
    return m.group(1).strip() if m else ""

def extract_checkboxes(body, heading):
    """Return (done_count, total_count) from a ## Heading's checkbox list."""
    section = extract_section(body, heading)
    total = len(re.findall(r"- \[.?\]", section))
    done  = len(re.findall(r"- \[x\]", section, re.IGNORECASE))
    return done, total

def extract_acceptance_criteria(body):
    """Return list of {text, done} dicts from ## Acceptance Criteria."""
    section = extract_section(body, "Acceptance Criteria")
    items = []
    for line in section.splitlines():
        m = re.match(r"\s*-\s*\[([ xX])\]\s*(.+)", line)
        if m:
            items.append({
                "done": m.group(1).lower() == "x",
                "text": m.group(2).strip()
            })
    return items

def latest_note(body):
    """Return the most recent timestamped note from ## Notes."""
    section = extract_section(body, "Notes")
    # find lines like: 2026-02-20 17:13 - Some text
    entries = re.findall(r"(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}.*?)(?=\n---|\Z)", section, re.DOTALL)
    if not entries:
        return None
    return entries[-1].strip()

def relative_time(iso_str):
    """Turn an ISO timestamp into a rough relative string."""
    if not iso_str:
        return None
    try:
        iso_str = iso_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(iso_str)
        now = datetime.now(timezone.utc)
        diff = now - dt
        days = diff.days
        if days == 0:
            h = diff.seconds // 3600
            if h == 0:
                return f"{diff.seconds // 60}m ago"
            return f"{h}h ago"
        elif days == 1:
            return "Yesterday"
        elif days < 7:
            return f"{days}d ago"
        elif days < 30:
            return f"{days // 7}w ago"
        else:
            return f"{days // 30}mo ago"
    except Exception:
        return iso_str

# ── Parse all task files ──────────────────────────
tasks = []

for fname in sorted(os.listdir(TASKS_DIR)):
    if not fname.endswith(".md") or fname == "README.md":
        continue
    fpath = os.path.join(TASKS_DIR, fname)
    with open(fpath, encoding="utf-8") as f:
        raw = f.read()

    meta, body = parse_frontmatter(raw)
    if not meta:
        continue

    status_raw = meta.get("status", "backlog")
    status_ui  = STATUS_MAP.get(status_raw, "pending")

    done_checks, total_checks = extract_checkboxes(body, "Acceptance Criteria")
    progress_pct = round((done_checks / total_checks) * 100) if total_checks > 0 else 0

    note = latest_note(body)

    task = {
        "id":          meta.get("id", fname.replace(".md", "")),
        "title":       extract_title(body) or meta.get("id"),
        "objective":   extract_section(body, "Objective"),
        "status":      status_ui,
        "statusRaw":   status_raw,
        "priority":    (meta.get("priority") or "medium").capitalize(),
        "agent":       meta.get("assignedTo") or "Unassigned",
        "tags":        meta.get("tags") or [],
        "skills":      meta.get("skills") or [],
        "dependencies":meta.get("dependencies") or [],
        "blockedBy":   meta.get("blockedBy") or [],
        "effort":      meta.get("estimatedEffort") or "medium",
        "created":     meta.get("created"),
        "updated":     meta.get("updated"),
        "updatedRel":  relative_time(meta.get("updated")),
        "progress":    progress_pct,
        "progressStr": f"{progress_pct}%" if total_checks > 0 else "—",
        "latestNote":  note,
        "context":             extract_section(body, "Context"),
        "description":         extract_section(body, "Objective"),
        "acceptanceCriteria":  extract_acceptance_criteria(body),
    }
    tasks.append(task)

# ── Write tasks.js ────────────────────────────────
js = f"// Auto-generated by generate-tasks.py — do not edit manually\n"
js += f"// Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n"
js += f"const DISPATCH_TASKS = {json.dumps(tasks, indent=2)};\n"

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(js)

print(f"✓ Wrote {len(tasks)} tasks to tasks.js")
for t in tasks:
    print(f"  {t['id']:12s}  {t['statusRaw']:12s}  {t['title'][:55]}")
