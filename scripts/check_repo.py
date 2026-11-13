#!/usr/bin/env python3
"""Check repository invariants that no build step covers."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
CLAUDE_AGENTS = ROOT / "claude_code" / "agents"
COPILOT_AGENTS = ROOT / "copilot" / "agents"
CLAUDE_SKILLS = ROOT / "claude_code" / "skills"
COPILOT_SKILLS = ROOT / "copilot" / "skills"
UPSTREAM_SKILLS = ROOT / "pstack" / "skills"

# Files that intentionally differ from the upstream skill copy.
CLAUDE_SKILL_DIFFS = {
    "setup-pstack/SKILL.md",
    "poteto-help/SKILL.md",
}

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
PLACEHOLDER_TARGETS = {"url"}

errors: list[str] = []


def error(message: str) -> None:
    errors.append(message)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip()
    return None


def parse_list(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [item.strip().strip("'\"") for item in value.split(",") if item.strip()]


def load_agents(directory: Path, suffix: str, required: set[str]) -> dict[str, dict[str, str]]:
    agents: dict[str, dict[str, str]] = {}
    for path in sorted(directory.glob(f"*{suffix}")):
        if path.name == "README.md":
            continue
        relative = path.relative_to(ROOT)
        frontmatter = parse_frontmatter(path.read_text(encoding="utf-8"))
        if frontmatter is None:
            error(f"{relative}: missing or unterminated frontmatter")
            continue
        for key in sorted(required):
            if not frontmatter.get(key):
                error(f"{relative}: missing frontmatter key {key!r}")
        name = frontmatter.get("name", "")
        expected_name = path.name[: -len(suffix)]
        if name != expected_name:
            error(f"{relative}: name {name!r} does not match file name {expected_name!r}")
        if not parse_list(frontmatter.get("tools", "")):
            error(f"{relative}: tools is empty")
        if name:
            agents[name] = frontmatter
    return agents


def check_agents() -> None:
    claude = load_agents(CLAUDE_AGENTS, ".md", {"name", "description", "tools"})
    copilot = load_agents(COPILOT_AGENTS, ".agent.md", {"name", "description", "tools", "user-invocable"})

    if set(claude) != set(copilot):
        only_claude = sorted(set(claude) - set(copilot))
        only_copilot = sorted(set(copilot) - set(claude))
        if only_claude:
            error(f"agents only in claude_code: {', '.join(only_claude)}")
        if only_copilot:
            error(f"agents only in copilot: {', '.join(only_copilot)}")

    # The Copilot roster covers the digital employees; its two lstack-specific
    # agents are described in prose instead of the table.
    for readme, names, suffix in (
        (CLAUDE_AGENTS / "README.md", claude, ".md"),
        (COPILOT_AGENTS / "README.md", set(copilot) - {"poteto-agent", "comment-sicko"}, ".agent.md"),
    ):
        text = readme.read_text(encoding="utf-8")
        for name in sorted(names):
            if f"`{name}{suffix}`" not in text:
                error(f"{readme.relative_to(ROOT)}: missing roster entry for {name}{suffix}")

    specialists = set(copilot) - {"tech-lead", "poteto-agent", "comment-sicko"}
    listed = set(parse_list(copilot.get("tech-lead", {}).get("agents", "")))
    if listed != specialists:
        error(
            "copilot tech-lead agents list differs: "
            f"missing={sorted(specialists - listed)}, extra={sorted(listed - specialists)}"
        )

    downstream = ""
    for line in (CLAUDE_AGENTS / "tech-lead.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("- Downstream:"):
            downstream = line.split(":", 1)[1].rstrip(".")
            break
    downstream_names = {item.strip() for item in downstream.split(",") if item.strip()}
    if downstream_names != specialists:
        error(
            "claude_code tech-lead downstream list differs: "
            f"missing={sorted(specialists - downstream_names)}, extra={sorted(downstream_names - specialists)}"
        )


def skill_dirs(root: Path) -> set[str]:
    return {path.name for path in root.iterdir() if path.is_dir()}


def file_map(root: Path) -> dict[str, Path]:
    return {str(path.relative_to(root)): path for path in root.rglob("*") if path.is_file()}


def check_skills() -> None:
    upstream = skill_dirs(UPSTREAM_SKILLS)
    claude = skill_dirs(CLAUDE_SKILLS)
    copilot = skill_dirs(COPILOT_SKILLS)

    if upstream != claude:
        error(
            "claude_code skill directories differ from pstack: "
            f"missing={sorted(upstream - claude)}, extra={sorted(claude - upstream)}"
        )

    expected_copilot = (upstream - {"setup-pstack"}) | {"setup-lstack", "lstack"}
    if copilot != expected_copilot:
        error(
            "copilot skill directories differ from expected: "
            f"missing={sorted(expected_copilot - copilot)}, extra={sorted(copilot - expected_copilot)}"
        )

    for root, names in ((CLAUDE_SKILLS, claude), (COPILOT_SKILLS, copilot)):
        for name in sorted(names):
            if not (root / name / "SKILL.md").is_file():
                error(f"{root.relative_to(ROOT)}/{name}: missing SKILL.md")

    seen_diffs: set[str] = set()
    for name in sorted(upstream & claude):
        upstream_files = file_map(UPSTREAM_SKILLS / name)
        claude_files = file_map(CLAUDE_SKILLS / name)
        for relative in sorted(set(upstream_files) | set(claude_files)):
            key = f"{name}/{relative}"
            if key in CLAUDE_SKILL_DIFFS:
                seen_diffs.add(key)
                continue
            if relative not in upstream_files or relative not in claude_files:
                error(f"{key}: present in only one of pstack/skills and claude_code/skills")
            elif upstream_files[relative].read_bytes() != claude_files[relative].read_bytes():
                error(f"{key}: differs from upstream copy without an allowlist entry")

    for key in sorted(CLAUDE_SKILL_DIFFS - seen_diffs):
        error(f"{key}: allowlisted as an intentional difference but does not differ")


def check_links() -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        text = FENCE_RE.sub("", text)
        text = INLINE_CODE_RE.sub("", text)
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            if target in PLACEHOLDER_TARGETS:
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            target = unquote(target)
            base = ROOT if target.startswith("/") else path.parent
            resolved = (base / target.lstrip("/")).resolve()
            if not resolved.exists():
                error(f"{path.relative_to(ROOT)}: broken link {match.group(1)}")


def main() -> int:
    check_agents()
    check_skills()
    check_links()
    if errors:
        for message in errors:
            print(f"FAIL {message}")
        print(f"RESULT: FAIL ({len(errors)} problem(s))")
        return 1
    print("OK   agent frontmatter, rosters, and tech-lead dispatch lists")
    print("OK   skill directory sets and upstream copy drift")
    print("OK   relative Markdown links")
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
