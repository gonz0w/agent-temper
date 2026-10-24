"""Check the repository's deliberately small Markdown authoring convention."""

from pathlib import Path
import os
import re
from urllib.parse import unquote, urlsplit

PLACEHOLDER = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
LINK_START = re.compile(r"!?\[[^\]\n]*\]\(")
REFERENCE = re.compile(r"^ {0,3}\[[^\]]+\]:|!?\[[^\]]*\]\[[^\]]*\]")
SKIP_DIRECTORIES = {".git", "__pycache__", ".venv"}


def without_inline_code(line):
    """Hide single-line code spans without changing source offsets."""
    return re.sub(r"(`+)(.+?)\1(?!`)", lambda match: " " * len(match[0]), line)


def destinations(line):
    """Yield inline destinations; labels and destinations stay on one line."""
    for match in LINK_START.finditer(line):
        start = match.end()
        depth = 1
        escaped = False
        for end in range(start, len(line)):
            character = line[end]
            if escaped:
                escaped = False
                continue
            if character == "\\":
                escaped = True
            elif character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    content = line[start:end].strip()
                    if content.startswith("<") and ">" in content:
                        yield content[1:content.index(">")]
                    else:
                        yield content.split(maxsplit=1)[0] if content else ""
                    break


def heading_slug(heading, used):
    """Generate common GitHub-style ATX heading anchors, including duplicates."""
    heading = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", heading)
    heading = re.sub(r"<[^>]+>", "", heading)
    pieces = re.split(r"(`+[^`]+`+)", heading)
    heading = "".join(
        piece if piece.startswith("`") else re.sub(r"(?<!\w)(_+)(.+?)\1(?!\w)", r"\2", piece)
        for piece in pieces
    )
    slug = re.sub(r"[^\w\- ]", "", heading.lower(), flags=re.UNICODE)
    slug = slug.replace(" ", "-")
    unique = slug
    number = 0
    while unique in used:
        number += 1
        unique = f"{slug}-{number}"
    return unique


def local_path_problem(root, parent, decoded):
    """Require exact on-disk spelling, even on case-insensitive filesystems."""
    current = parent
    for part in Path(decoded).parts:
        current = current.resolve()
        if not current.is_relative_to(root):
            return "link traverses outside repository"
        if part == "..":
            current = current.parent
            continue
        if not current.is_dir():
            return "missing link target"
        names = {entry.name for entry in current.iterdir()}
        if part not in names:
            if any(name.casefold() == part.casefold() for name in names):
                return "link path case mismatch"
            return "missing link target"
        current /= part
    return None


def check_repository(root):
    """Return deterministic diagnostics; never follow a path outside root."""
    root = Path(root).resolve()
    diagnostics = []
    documents = {}
    links = []

    def report(path, line, message):
        diagnostics.append(f"{path.relative_to(root).as_posix()}:{line}: {message}")

    paths = []
    for directory, directories, files in os.walk(root, followlinks=False):
        directories[:] = sorted(name for name in directories if name not in SKIP_DIRECTORIES)
        paths.extend(Path(directory) / name for name in files if Path(name).suffix.lower() == ".md")

    for path in sorted(paths):
        relative = path.relative_to(root)
        if not path.resolve().is_relative_to(root):
            report(path, 1, "Markdown path resolves outside repository")
            continue
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            report(path, 1, f"cannot read UTF-8 Markdown: {error.__class__.__name__}")
            continue

        headings = set()
        h1_count = 0
        fence = None
        template = relative.parts[0] == "templates"
        for number, line in enumerate(text.splitlines(), 1):
            if line.rstrip() != line:
                report(path, number, "trailing whitespace")
            if not template and PLACEHOLDER.search(line):
                report(path, number, "unresolved placeholder outside templates/")
            fence_match = FENCE.match(line)
            if fence:
                if (fence_match and fence_match[1][0] == fence[0][0]
                        and len(fence_match[1]) >= len(fence[0])
                        and not fence_match[2].strip()):
                    fence = None
                continue
            if fence_match:
                fence = (fence_match[1], number)
                continue
            heading = HEADING.match(line)
            if heading:
                h1_count += len(heading[1]) == 1
                headings.add(heading_slug(heading[2], headings))
            prose = without_inline_code(line)
            if REFERENCE.search(prose):
                report(path, number, "reference links are unsupported; use inline links")
            for destination in destinations(prose):
                if template and PLACEHOLDER.search(destination):
                    continue
                links.append((path, number, destination))
        if fence:
            report(path, fence[1], "unclosed code fence")
        if h1_count != 1:
            report(path, 1, f"expected exactly one H1 heading; found {h1_count}")
        documents[path.resolve()] = headings

    for source, number, destination in links:
        try:
            url = urlsplit(destination)
        except ValueError:
            report(source, number, f"invalid link destination: {destination}")
            continue
        if url.scheme.lower() in {"https", "http", "mailto"}:
            continue
        decoded = unquote(url.path)
        if url.scheme or url.netloc or decoded.startswith("/") or "\\" in decoded:
            report(source, number, f"absolute or unsupported local link: {destination}")
            continue
        target = (source.parent / decoded).resolve() if decoded else source.resolve()
        if not target.is_relative_to(root):
            report(source, number, f"link resolves outside repository: {destination}")
            continue
        path_problem = local_path_problem(root, source.parent, decoded)
        if path_problem:
            report(source, number, f"{path_problem}: {destination}")
            continue
        if not target.exists():
            report(source, number, f"missing link target: {destination}")
            continue
        if url.fragment:
            fragment = unquote(url.fragment)
            if target not in documents or fragment not in documents[target]:
                report(source, number, f"missing Markdown heading: {destination}")

    return diagnostics
