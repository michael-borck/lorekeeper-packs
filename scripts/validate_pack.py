#!/usr/bin/env python3
"""Validate pack submissions without the signing key."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBMISSIONS = ROOT / "submissions"
MAX_BYTES = 4_500_000
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]*$")
KINDS = {
    "reading",
    "checkpoint",
    "exercise",
    "order",
    "fill",
    "hotspot",
    "review",
    "scenario",
    "calibration",
    "viva",
    "api",
    "sql",
    "terminal",
    "story",
}
META = {"packId", "title", "author", "contact", "licence", "version", "description", "changes"}


def fail(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT)}: {message}")


def validate_pack(path: Path, errors: list[str]) -> str | None:
    if path.stat().st_size > MAX_BYTES:
        fail(errors, path, "pack is larger than 4.5 MB")
    try:
        pack = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, path, f"not valid JSON: {exc}")
        return None

    if pack.get("format") != "lorekeeper.pack" or int(pack.get("version", 0)) != 1:
        fail(errors, path, "wrong format or version")
        return None
    pack_id = str(pack.get("id", ""))
    if not SLUG.match(pack_id):
        fail(errors, path, f"invalid pack id {pack_id!r}")
    if not pack.get("title"):
        fail(errors, path, "missing title")
    if not isinstance(pack.get("courses"), list) or not pack["courses"]:
        fail(errors, path, "missing courses")
        return pack_id

    for entry in pack["courses"]:
        slug = str(entry.get("slug", ""))
        if not SLUG.match(slug):
            fail(errors, path, f"invalid course slug {slug!r}")
        course = entry.get("course")
        if not isinstance(course, dict):
            fail(errors, path, f"course {slug}: missing course object")
            continue
        unit = course.get("unit") or {}
        if unit.get("slug") != slug:
            fail(errors, path, f"course {slug}: unit slug mismatch")
        modules = course.get("modules")
        if not isinstance(modules, list):
            fail(errors, path, f"course {slug}: missing modules")
            continue
        stories = entry.get("stories")
        if not isinstance(stories, dict):
            fail(errors, path, f"course {slug}: missing story map")
            stories = {}
        for story_src, story in stories.items():
            if not isinstance(story, dict) or "inkVersion" not in story or "root" not in story:
                fail(errors, path, f"course {slug}: story {story_src} is not compiled Ink")
        for module in modules:
            for lesson in module.get("lessons") or []:
                lesson_id = lesson.get("id", "?")
                kind = lesson.get("kind")
                if kind not in KINDS:
                    fail(errors, path, f"{slug}/{lesson_id}: unknown lesson kind {kind!r}")
                for block in lesson.get("blocks") or []:
                    btype = block.get("type")
                    if btype == "story" and block.get("src") not in stories:
                        fail(errors, path, f"{slug}/{lesson_id}: missing story {block.get('src')!r}")
                    if btype == "exercise":
                        tests = block.get("tests")
                        if not isinstance(tests, list) or not tests:
                            fail(errors, path, f"{slug}/{lesson_id}: exercise has no tests")
                        else:
                            for test in tests:
                                if not isinstance(test, dict) or not test.get("script"):
                                    fail(errors, path, f"{slug}/{lesson_id}: invalid test")
    return pack_id


def validate_meta(path: Path, pack_id: str | None, errors: list[str]) -> None:
    meta_path = path.parent / "submission.json"
    if not meta_path.is_file():
        fail(errors, meta_path, "missing submission.json")
        return
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, meta_path, f"not valid JSON: {exc}")
        return
    for key in META:
        if not str(meta.get(key, "")).strip():
            fail(errors, meta_path, f"missing {key}")
    if pack_id and meta.get("packId") != pack_id:
        fail(errors, meta_path, f"packId {meta.get('packId')!r} does not match {pack_id!r}")


def main() -> int:
    errors: list[str] = []
    slugs: set[str] = set()
    packs = sorted(SUBMISSIONS.glob("*/pack.json"))
    if not packs:
        print("No submissions found.", file=sys.stderr)
        return 1
    for path in packs:
        pack_id = validate_pack(path, errors)
        validate_meta(path, pack_id, errors)
        try:
            pack = json.loads(path.read_text(encoding="utf-8"))
            for entry in pack.get("courses", []):
                slug = str(entry.get("slug", ""))
                if slug in slugs:
                    fail(errors, path, f"duplicate course slug {slug!r}")
                slugs.add(slug)
        except (OSError, json.JSONDecodeError):
            pass
    if errors:
        for error in errors:
            print(f"x {error}", file=sys.stderr)
        return 1
    print(f"OK {len(packs)} submission(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
