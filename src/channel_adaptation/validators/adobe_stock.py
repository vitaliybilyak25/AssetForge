"""Adobe Stock CSV field validators for the Channel Adaptation Layer (Layer 3).

Implements all 16 rule IDs from the Validation Summary Table in
docs/adobe-stock-output-spec.md (story #26).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


ADOBE_STOCK_VALID_CATEGORY_CODES: frozenset[int] = frozenset(range(1, 21))

_PATH_SEPARATOR_RE = re.compile(r"[/\\]")
_SUBSEQUENT_CAPITAL_RE = re.compile(r"(?<=\s)[A-Z]")
_SPACE_AROUND_COMMA_RE = re.compile(r"\s+,|,\s+")


@dataclass
class ValidationResult:
    """Result of one validation rule applied to one column."""

    column: str
    rule_id: str
    passed: bool
    fix_suggestion: Optional[str] = None


@dataclass
class RowValidationReport:
    """Aggregated validation result for one CSV row.

    A row may only be written to the Output Package when passed is True.
    """

    passed: bool
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def failures(self) -> list[ValidationResult]:
        """Return only the failed validation results."""
        return [r for r in self.results if not r.passed]


def _pass(column: str, rule_id: str) -> ValidationResult:
    return ValidationResult(column=column, rule_id=rule_id, passed=True)


def _fail(column: str, rule_id: str, fix: str) -> ValidationResult:
    return ValidationResult(column=column, rule_id=rule_id, passed=False, fix_suggestion=fix)


# ---------------------------------------------------------------------------
# Filename validators
# ---------------------------------------------------------------------------

def validate_filename_required(filename: str) -> ValidationResult:
    """Rule filename-required: Filename must be non-empty."""
    if filename:
        return _pass("Filename", "filename-required")
    return _fail("Filename", "filename-required", "Provide a non-empty file name.")


def validate_filename_no_path(filename: str) -> ValidationResult:
    """Rule filename-no-path: No path separators; must include a file extension."""
    if _PATH_SEPARATOR_RE.search(filename):
        return _fail(
            "Filename", "filename-no-path",
            "Remove directory components and path separators; use the bare file name only "
            "(e.g. 'photo.jpg').",
        )
    # Strip leading dots (e.g. '.hidden') then require at least one dot for extension
    if "." not in filename.lstrip("."):
        return _fail(
            "Filename", "filename-no-path",
            "File name must include a file extension (e.g. 'photo.jpg').",
        )
    return _pass("Filename", "filename-no-path")


# ---------------------------------------------------------------------------
# Title validators
# ---------------------------------------------------------------------------

def validate_title_required(title: str) -> ValidationResult:
    """Rule title-required: Title must be non-empty."""
    if title:
        return _pass("Title", "title-required")
    return _fail("Title", "title-required", "Provide a non-empty title.")


def validate_title_max_length(title: str) -> ValidationResult:
    """Rule title-max-length: Title must be 200 characters or fewer."""
    if len(title) <= 200:
        return _pass("Title", "title-max-length")
    return _fail(
        "Title", "title-max-length",
        f"Shorten the title to 200 characters or fewer (currently {len(title)} characters).",
    )


def validate_title_sentence_case(title: str) -> ValidationResult:
    """Rule title-sentence-case: First word capitalised; subsequent words lowercase (proper nouns excepted)."""
    if not title:
        return _pass("Title", "title-sentence-case")
    if not title[0].isupper():
        return _fail(
            "Title", "title-sentence-case",
            "Capitalise the first word of the title.",
        )
    subsequent_caps = _SUBSEQUENT_CAPITAL_RE.findall(title)
    if subsequent_caps:
        return _fail(
            "Title", "title-sentence-case",
            f"Subsequent words should be lowercase unless they are proper nouns "
            f"(found {len(subsequent_caps)} capitalised word(s) after the first).",
        )
    return _pass("Title", "title-sentence-case")


def validate_title_no_brand_names(
    title: str, logo_marks_detected: list[str]
) -> ValidationResult:
    """Rule title-no-brand-names: No term from logo_marks_detected may appear in the title."""
    if not logo_marks_detected:
        return _pass("Title", "title-no-brand-names")
    title_lower = title.lower()
    found = [term for term in logo_marks_detected if term.lower() in title_lower]
    if found:
        return _fail(
            "Title", "title-no-brand-names",
            f"Remove brand name(s) from the title: {', '.join(found)}.",
        )
    return _pass("Title", "title-no-brand-names")


# ---------------------------------------------------------------------------
# Keywords validators
# ---------------------------------------------------------------------------

def _split_keywords(keywords: str) -> list[str]:
    return [k for k in keywords.split(",") if k]


def validate_min_keyword_count(keywords: str) -> ValidationResult:
    """Rule min-keyword-count: Keyword list must contain at least 5 terms."""
    count = len(_split_keywords(keywords))
    if count >= 5:
        return _pass("Keywords", "min-keyword-count")
    return _fail(
        "Keywords", "min-keyword-count",
        f"Add more keywords; minimum is 5 (currently {count}).",
    )


def validate_max_keyword_count(keywords: str) -> ValidationResult:
    """Rule max-keyword-count: Keyword list must contain at most 49 terms."""
    count = len(_split_keywords(keywords))
    if count <= 49:
        return _pass("Keywords", "max-keyword-count")
    return _fail(
        "Keywords", "max-keyword-count",
        f"Remove keywords until there are 49 or fewer (currently {count}).",
    )


def validate_keywords_no_brand_names(
    keywords: str, logo_marks_detected: list[str]
) -> ValidationResult:
    """Rule keywords-no-brand-names: No term from logo_marks_detected may appear in the keyword list."""
    if not logo_marks_detected:
        return _pass("Keywords", "keywords-no-brand-names")
    kw_lower = keywords.lower()
    found = [term for term in logo_marks_detected if term.lower() in kw_lower]
    if found:
        return _fail(
            "Keywords", "keywords-no-brand-names",
            f"Remove brand name(s) from keywords: {', '.join(found)}.",
        )
    return _pass("Keywords", "keywords-no-brand-names")


def validate_keywords_separator_format(keywords: str) -> ValidationResult:
    """Rule keywords-separator-format: Comma-separated with no surrounding whitespace."""
    if _SPACE_AROUND_COMMA_RE.search(keywords):
        return _fail(
            "Keywords", "keywords-separator-format",
            "Use comma separation with no spaces around commas "
            "(e.g. 'cat,dog,outdoor' not 'cat, dog, outdoor').",
        )
    return _pass("Keywords", "keywords-separator-format")


# ---------------------------------------------------------------------------
# Category validators
# ---------------------------------------------------------------------------

def validate_category_required(category: object) -> ValidationResult:
    """Rule category-required: Category must be non-empty."""
    if category is not None and str(category).strip():
        return _pass("Category", "category-required")
    return _fail("Category", "category-required", "Provide a numeric category code.")


def validate_category_must_be_numeric(category: object) -> ValidationResult:
    """Rule category-must-be-numeric: Category must be an integer, not a string name."""
    if isinstance(category, int) and not isinstance(category, bool):
        return _pass("Category", "category-must-be-numeric")
    return _fail(
        "Category", "category-must-be-numeric",
        "Category must be an integer code (e.g. 5), not a string name (e.g. 'Food/Drink').",
    )


def validate_category_valid_code(category: object) -> ValidationResult:
    """Rule category-valid-code: Category must be one of the 20 valid Adobe Stock codes (1–20)."""
    if isinstance(category, int) and category in ADOBE_STOCK_VALID_CATEGORY_CODES:
        return _pass("Category", "category-valid-code")
    return _fail(
        "Category", "category-valid-code",
        f"Category {category!r} is not a valid Adobe Stock code. Valid codes are integers 1–20.",
    )


# ---------------------------------------------------------------------------
# Releases validators
# ---------------------------------------------------------------------------

def validate_releases_state_enforced(
    releases: str,
    release_required: bool,
) -> ValidationResult:
    """Rule releases-state-enforced: State B rows (release required, releases empty) must not be exported."""
    if release_required and not releases.strip():
        return _fail(
            "Releases", "releases-state-enforced",
            "This row is State B (release required but absent/unconfirmed). "
            "Do not export until a human reviewer has confirmed and recorded the release file name.",
        )
    return _pass("Releases", "releases-state-enforced")


def validate_releases_exact_filename_match(
    releases: str,
    confirmed_release_filenames: Optional[list[str]],
) -> ValidationResult:
    """Rule releases-exact-filename-match: When non-empty, each release file name must exactly match a confirmed name."""
    if not releases.strip():
        return _pass("Releases", "releases-exact-filename-match")
    if not confirmed_release_filenames:
        return _fail(
            "Releases", "releases-exact-filename-match",
            "Releases column is non-empty but no confirmed release file names were provided for matching.",
        )
    provided = [n.strip() for n in releases.split(",") if n.strip()]
    unmatched = [n for n in provided if n not in confirmed_release_filenames]
    if unmatched:
        return _fail(
            "Releases", "releases-exact-filename-match",
            f"Release file name(s) do not exactly match confirmed names: {', '.join(unmatched)}.",
        )
    return _pass("Releases", "releases-exact-filename-match")


def validate_releases_separator_format(releases: str) -> ValidationResult:
    """Rule releases-separator-format: Multiple file names must be comma-separated with no surrounding whitespace."""
    if not releases.strip():
        return _pass("Releases", "releases-separator-format")
    if _SPACE_AROUND_COMMA_RE.search(releases):
        return _fail(
            "Releases", "releases-separator-format",
            "Use comma separation with no spaces around commas "
            "(e.g. 'release-a.pdf,release-b.pdf').",
        )
    return _pass("Releases", "releases-separator-format")


# ---------------------------------------------------------------------------
# Row-level gate (AC9)
# ---------------------------------------------------------------------------

def validate_row(
    filename: str,
    title: str,
    keywords: str,
    category: object,
    releases: str,
    logo_marks_detected: Optional[list[str]] = None,
    release_required: bool = False,
    confirmed_release_filenames: Optional[list[str]] = None,
) -> RowValidationReport:
    """Apply all 16 Adobe Stock validators to one CSV row.

    The row may only be written to the Output Package when report.passed is True.
    All 16 rule IDs from docs/adobe-stock-output-spec.md Validation Summary Table
    are evaluated; all failures are collected before returning (no short-circuit).
    """
    if logo_marks_detected is None:
        logo_marks_detected = []

    results: list[ValidationResult] = [
        # Filename (AC3)
        validate_filename_required(filename),
        validate_filename_no_path(filename),
        # Title (AC4)
        validate_title_required(title),
        validate_title_max_length(title),
        validate_title_sentence_case(title),
        validate_title_no_brand_names(title, logo_marks_detected),
        # Keywords (AC5)
        validate_min_keyword_count(keywords),
        validate_max_keyword_count(keywords),
        validate_keywords_no_brand_names(keywords, logo_marks_detected),
        validate_keywords_separator_format(keywords),
        # Category (AC6)
        validate_category_required(category),
        validate_category_must_be_numeric(category),
        validate_category_valid_code(category),
        # Releases (AC7)
        validate_releases_state_enforced(releases, release_required),
        validate_releases_exact_filename_match(releases, confirmed_release_filenames),
        validate_releases_separator_format(releases),
    ]

    return RowValidationReport(
        passed=all(r.passed for r in results),
        results=results,
    )
