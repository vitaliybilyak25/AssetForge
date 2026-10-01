"""Unit tests for Adobe Stock CSV validators (issue #26).

Covers all 10 AC items and all 16 rule IDs from the Validation Summary Table
in docs/adobe-stock-output-spec.md.
"""

import pytest

from src.channel_adaptation.validators.adobe_stock import (
    ADOBE_STOCK_VALID_CATEGORY_CODES,
    RowValidationReport,
    ValidationResult,
    validate_category_must_be_numeric,
    validate_category_required,
    validate_category_valid_code,
    validate_filename_no_path,
    validate_filename_required,
    validate_keywords_no_brand_names,
    validate_keywords_separator_format,
    validate_max_keyword_count,
    validate_min_keyword_count,
    validate_releases_exact_filename_match,
    validate_releases_separator_format,
    validate_releases_state_enforced,
    validate_row,
    validate_title_max_length,
    validate_title_no_brand_names,
    validate_title_required,
    validate_title_sentence_case,
)


# ---------------------------------------------------------------------------
# AC8 — validator output contract
# ---------------------------------------------------------------------------

class TestValidationResult:
    def test_pass_has_no_fix_suggestion(self):
        r = ValidationResult(column="Title", rule_id="title-required", passed=True)
        assert r.fix_suggestion is None

    def test_fail_carries_fix_suggestion(self):
        r = ValidationResult(
            column="Title", rule_id="title-required", passed=False, fix_suggestion="Add a title."
        )
        assert r.fix_suggestion == "Add a title."

    def test_pass_result_fields(self):
        r = ValidationResult(column="Filename", rule_id="filename-required", passed=True)
        assert r.column == "Filename"
        assert r.rule_id == "filename-required"
        assert r.passed is True


class TestRowValidationReport:
    def test_failures_filters_only_failed(self):
        results = [
            ValidationResult("Filename", "filename-required", True),
            ValidationResult("Title", "title-required", False, "Add title."),
            ValidationResult("Keywords", "min-keyword-count", False, "Add keywords."),
        ]
        report = RowValidationReport(passed=False, results=results)
        assert len(report.failures) == 2
        assert all(not r.passed for r in report.failures)

    def test_failures_empty_when_all_pass(self):
        results = [ValidationResult("Filename", "filename-required", True)]
        report = RowValidationReport(passed=True, results=results)
        assert report.failures == []


# ---------------------------------------------------------------------------
# AC3 — Filename validators
# ---------------------------------------------------------------------------

class TestFilenameRequired:
    def test_pass_non_empty(self):
        r = validate_filename_required("photo.jpg")
        assert r.passed is True
        assert r.rule_id == "filename-required"
        assert r.column == "Filename"

    def test_fail_empty_string(self):
        r = validate_filename_required("")
        assert r.passed is False
        assert r.fix_suggestion is not None

    def test_fail_whitespace_only(self):
        # empty string only — whitespace is non-empty; only pure empty fails
        r = validate_filename_required("photo.jpg")
        assert r.passed is True


class TestFilenameNoPath:
    def test_pass_bare_filename_with_extension(self):
        r = validate_filename_no_path("photo.jpg")
        assert r.passed is True
        assert r.rule_id == "filename-no-path"

    def test_fail_forward_slash(self):
        r = validate_filename_no_path("folder/photo.jpg")
        assert r.passed is False
        assert r.fix_suggestion is not None

    def test_fail_backslash(self):
        r = validate_filename_no_path("folder\\photo.jpg")
        assert r.passed is False

    def test_fail_no_extension(self):
        r = validate_filename_no_path("photo")
        assert r.passed is False

    def test_pass_hidden_file_with_extension(self):
        # .hidden.jpg has a dot after stripping leading dot
        r = validate_filename_no_path(".hidden.jpg")
        assert r.passed is True

    def test_fail_hidden_file_no_real_extension(self):
        # '.hidden' — after lstrip('.') becomes 'hidden', no dot → fail
        r = validate_filename_no_path(".hidden")
        assert r.passed is False

    def test_pass_multiple_dots(self):
        r = validate_filename_no_path("my.photo.final.jpg")
        assert r.passed is True


# ---------------------------------------------------------------------------
# AC4 — Title validators
# ---------------------------------------------------------------------------

class TestTitleRequired:
    def test_pass_non_empty(self):
        r = validate_title_required("A beautiful sunset")
        assert r.passed is True
        assert r.rule_id == "title-required"

    def test_fail_empty(self):
        r = validate_title_required("")
        assert r.passed is False


class TestTitleMaxLength:
    def test_pass_exactly_200(self):
        r = validate_title_max_length("A" * 200)
        assert r.passed is True
        assert r.rule_id == "title-max-length"

    def test_pass_under_200(self):
        r = validate_title_max_length("Short title")
        assert r.passed is True

    def test_fail_201_chars(self):
        r = validate_title_max_length("A" * 201)
        assert r.passed is False
        assert "201" in r.fix_suggestion

    def test_fail_reports_actual_length(self):
        title = "X" * 250
        r = validate_title_max_length(title)
        assert "250" in r.fix_suggestion


class TestTitleSentenceCase:
    def test_pass_first_word_capitalised(self):
        r = validate_title_sentence_case("Beautiful sunset over the ocean")
        assert r.passed is True
        assert r.rule_id == "title-sentence-case"

    def test_fail_first_word_lowercase(self):
        r = validate_title_sentence_case("beautiful sunset")
        assert r.passed is False

    def test_fail_subsequent_capitals(self):
        r = validate_title_sentence_case("Beautiful Sunset Over The Ocean")
        assert r.passed is False
        assert r.fix_suggestion is not None

    def test_pass_empty_title_skipped(self):
        # empty title is caught by title-required; sentence-case skips
        r = validate_title_sentence_case("")
        assert r.passed is True

    def test_pass_single_word_capitalised(self):
        r = validate_title_sentence_case("Sunset")
        assert r.passed is True

    def test_fail_multiple_subsequent_caps_reported(self):
        r = validate_title_sentence_case("Beautiful Sunset Over Ocean")
        assert not r.passed
        assert "3" in r.fix_suggestion  # 3 subsequent capitals


class TestTitleNoBrandNames:
    def test_pass_empty_logo_marks(self):
        r = validate_title_no_brand_names("Nike logo on shirt", [])
        assert r.passed is True
        assert r.rule_id == "title-no-brand-names"

    def test_fail_brand_in_title(self):
        r = validate_title_no_brand_names("Nike shoes on display", ["Nike"])
        assert r.passed is False
        assert "Nike" in r.fix_suggestion

    def test_fail_case_insensitive(self):
        r = validate_title_no_brand_names("NIKE shoes", ["nike"])
        assert r.passed is False

    def test_pass_brand_absent_from_title(self):
        r = validate_title_no_brand_names("Running shoes on track", ["Nike"])
        assert r.passed is True

    def test_fail_multiple_brands(self):
        r = validate_title_no_brand_names("Nike and Adidas products", ["Nike", "Adidas"])
        assert r.passed is False
        assert "Nike" in r.fix_suggestion
        assert "Adidas" in r.fix_suggestion


# ---------------------------------------------------------------------------
# AC5 — Keywords validators
# ---------------------------------------------------------------------------

class TestMinKeywordCount:
    def test_pass_exactly_5(self):
        r = validate_min_keyword_count("a,b,c,d,e")
        assert r.passed is True
        assert r.rule_id == "min-keyword-count"

    def test_pass_more_than_5(self):
        r = validate_min_keyword_count("a,b,c,d,e,f,g")
        assert r.passed is True

    def test_fail_4_keywords(self):
        r = validate_min_keyword_count("a,b,c,d")
        assert r.passed is False
        assert "4" in r.fix_suggestion

    def test_fail_empty(self):
        r = validate_min_keyword_count("")
        assert r.passed is False

    def test_fail_one_keyword(self):
        r = validate_min_keyword_count("sunset")
        assert r.passed is False


class TestMaxKeywordCount:
    def test_pass_exactly_49(self):
        kw = ",".join(str(i) for i in range(49))
        r = validate_max_keyword_count(kw)
        assert r.passed is True
        assert r.rule_id == "max-keyword-count"

    def test_pass_fewer_than_49(self):
        r = validate_max_keyword_count("a,b,c,d,e")
        assert r.passed is True

    def test_fail_50_keywords(self):
        kw = ",".join(str(i) for i in range(50))
        r = validate_max_keyword_count(kw)
        assert r.passed is False
        assert "50" in r.fix_suggestion


class TestKeywordsNoBrandNames:
    def test_pass_empty_logo_marks(self):
        r = validate_keywords_no_brand_names("nike,shoes,sport", [])
        assert r.passed is True
        assert r.rule_id == "keywords-no-brand-names"

    def test_fail_brand_in_keywords(self):
        r = validate_keywords_no_brand_names("nike,shoes,sport", ["nike"])
        assert r.passed is False

    def test_fail_case_insensitive(self):
        r = validate_keywords_no_brand_names("NIKE,shoes", ["nike"])
        assert r.passed is False

    def test_pass_brand_absent(self):
        r = validate_keywords_no_brand_names("shoes,sport,running", ["Nike"])
        assert r.passed is True


class TestKeywordsSeparatorFormat:
    def test_pass_no_spaces(self):
        r = validate_keywords_separator_format("cat,dog,bird")
        assert r.passed is True
        assert r.rule_id == "keywords-separator-format"

    def test_fail_space_after_comma(self):
        r = validate_keywords_separator_format("cat, dog, bird")
        assert r.passed is False

    def test_fail_space_before_comma(self):
        r = validate_keywords_separator_format("cat ,dog ,bird")
        assert r.passed is False

    def test_pass_single_keyword(self):
        r = validate_keywords_separator_format("cat")
        assert r.passed is True

    def test_pass_empty(self):
        r = validate_keywords_separator_format("")
        assert r.passed is True


# ---------------------------------------------------------------------------
# AC6 — Category validators
# ---------------------------------------------------------------------------

class TestCategoryRequired:
    def test_pass_valid_int(self):
        r = validate_category_required(5)
        assert r.passed is True
        assert r.rule_id == "category-required"

    def test_fail_none(self):
        r = validate_category_required(None)
        assert r.passed is False

    def test_fail_empty_string(self):
        r = validate_category_required("")
        assert r.passed is False

    def test_fail_whitespace(self):
        r = validate_category_required("   ")
        assert r.passed is False

    def test_pass_zero_int(self):
        # 0 is non-None and str() is "0" (non-empty), so required passes
        # (valid-code will fail separately)
        r = validate_category_required(0)
        assert r.passed is True


class TestCategoryMustBeNumeric:
    def test_pass_integer(self):
        r = validate_category_must_be_numeric(5)
        assert r.passed is True
        assert r.rule_id == "category-must-be-numeric"

    def test_fail_string_name(self):
        r = validate_category_must_be_numeric("Food/Drink")
        assert r.passed is False

    def test_fail_string_digit(self):
        r = validate_category_must_be_numeric("5")
        assert r.passed is False

    def test_fail_bool(self):
        # bool is a subclass of int in Python — explicitly rejected
        r = validate_category_must_be_numeric(True)
        assert r.passed is False

    def test_fail_float(self):
        r = validate_category_must_be_numeric(5.0)
        assert r.passed is False


class TestCategoryValidCode:
    def test_pass_code_1(self):
        r = validate_category_valid_code(1)
        assert r.passed is True
        assert r.rule_id == "category-valid-code"

    def test_pass_code_20(self):
        r = validate_category_valid_code(20)
        assert r.passed is True

    def test_fail_code_0(self):
        r = validate_category_valid_code(0)
        assert r.passed is False

    def test_fail_code_21(self):
        r = validate_category_valid_code(21)
        assert r.passed is False

    def test_fail_code_negative(self):
        r = validate_category_valid_code(-1)
        assert r.passed is False

    @pytest.mark.parametrize("code", range(1, 21))
    def test_pass_all_20_valid_codes(self, code):
        r = validate_category_valid_code(code)
        assert r.passed is True

    def test_valid_codes_constant_size(self):
        assert len(ADOBE_STOCK_VALID_CATEGORY_CODES) == 20


# ---------------------------------------------------------------------------
# AC7 — Releases validators
# ---------------------------------------------------------------------------

class TestReleasesStateEnforced:
    def test_pass_state_c_not_required_empty(self):
        r = validate_releases_state_enforced("", release_required=False)
        assert r.passed is True
        assert r.rule_id == "releases-state-enforced"

    def test_pass_state_a_required_and_present(self):
        r = validate_releases_state_enforced("release-a.pdf", release_required=True)
        assert r.passed is True

    def test_fail_state_b_required_but_empty(self):
        r = validate_releases_state_enforced("", release_required=True)
        assert r.passed is False
        assert r.fix_suggestion is not None

    def test_fail_state_b_required_but_whitespace(self):
        r = validate_releases_state_enforced("   ", release_required=True)
        assert r.passed is False


class TestReleasesExactFilenameMatch:
    def test_pass_empty_releases(self):
        r = validate_releases_exact_filename_match("", confirmed_release_filenames=None)
        assert r.passed is True
        assert r.rule_id == "releases-exact-filename-match"

    def test_pass_exact_match(self):
        r = validate_releases_exact_filename_match(
            "release-a.pdf",
            confirmed_release_filenames=["release-a.pdf", "release-b.pdf"],
        )
        assert r.passed is True

    def test_pass_multiple_exact_matches(self):
        r = validate_releases_exact_filename_match(
            "release-a.pdf,release-b.pdf",
            confirmed_release_filenames=["release-a.pdf", "release-b.pdf"],
        )
        assert r.passed is True

    def test_fail_no_confirmed_list(self):
        r = validate_releases_exact_filename_match(
            "release-a.pdf", confirmed_release_filenames=None
        )
        assert r.passed is False

    def test_fail_unmatched_name(self):
        r = validate_releases_exact_filename_match(
            "Release-A.pdf",  # capitalisation differs
            confirmed_release_filenames=["release-a.pdf"],
        )
        assert r.passed is False
        assert "Release-A.pdf" in r.fix_suggestion

    def test_fail_partial_match_not_accepted(self):
        r = validate_releases_exact_filename_match(
            "release-a",
            confirmed_release_filenames=["release-a.pdf"],
        )
        assert r.passed is False


class TestReleasesSeparatorFormat:
    def test_pass_empty(self):
        r = validate_releases_separator_format("")
        assert r.passed is True
        assert r.rule_id == "releases-separator-format"

    def test_pass_single_filename(self):
        r = validate_releases_separator_format("release-a.pdf")
        assert r.passed is True

    def test_pass_multiple_no_spaces(self):
        r = validate_releases_separator_format("release-a.pdf,release-b.pdf")
        assert r.passed is True

    def test_fail_space_after_comma(self):
        r = validate_releases_separator_format("release-a.pdf, release-b.pdf")
        assert r.passed is False

    def test_fail_space_before_comma(self):
        r = validate_releases_separator_format("release-a.pdf ,release-b.pdf")
        assert r.passed is False


# ---------------------------------------------------------------------------
# AC9 — Row-level gate (validate_row)
# ---------------------------------------------------------------------------

VALID_ROW = dict(
    filename="photo.jpg",
    title="Beautiful sunset over the ocean",
    keywords="sunset,ocean,sky,water,nature",
    category=1,
    releases="",
    logo_marks_detected=[],
    release_required=False,
    confirmed_release_filenames=None,
)


class TestValidateRow:
    def test_pass_all_valid(self):
        report = validate_row(**VALID_ROW)
        assert report.passed is True
        assert report.failures == []

    def test_fail_collects_all_failures(self):
        # Multiple columns fail at once
        report = validate_row(
            filename="",              # filename-required
            title="",                 # title-required
            keywords="a,b",           # min-keyword-count
            category="Food/Drink",    # category-must-be-numeric + category-valid-code
            releases="",
        )
        assert report.passed is False
        failed_ids = {r.rule_id for r in report.failures}
        assert "filename-required" in failed_ids
        assert "title-required" in failed_ids
        assert "min-keyword-count" in failed_ids
        assert "category-must-be-numeric" in failed_ids

    def test_fail_one_column_blocks_row(self):
        row = {**VALID_ROW, "title": ""}
        report = validate_row(**row)
        assert report.passed is False

    def test_report_has_16_results(self):
        report = validate_row(**VALID_ROW)
        assert len(report.results) == 16

    def test_all_16_rule_ids_present(self):
        expected_ids = {
            "filename-required",
            "filename-no-path",
            "title-required",
            "title-max-length",
            "title-sentence-case",
            "title-no-brand-names",
            "min-keyword-count",
            "max-keyword-count",
            "keywords-no-brand-names",
            "keywords-separator-format",
            "category-required",
            "category-must-be-numeric",
            "category-valid-code",
            "releases-state-enforced",
            "releases-exact-filename-match",
            "releases-separator-format",
        }
        report = validate_row(**VALID_ROW)
        actual_ids = {r.rule_id for r in report.results}
        assert actual_ids == expected_ids

    def test_state_b_row_blocked(self):
        row = {**VALID_ROW, "release_required": True, "releases": ""}
        report = validate_row(**row)
        assert report.passed is False
        failed_ids = {r.rule_id for r in report.failures}
        assert "releases-state-enforced" in failed_ids

    def test_state_a_row_passes_with_confirmed_names(self):
        row = {
            **VALID_ROW,
            "release_required": True,
            "releases": "model-release.pdf",
            "confirmed_release_filenames": ["model-release.pdf"],
        }
        report = validate_row(**row)
        assert report.passed is True

    def test_logo_marks_propagated_to_title_and_keywords(self):
        row = {
            **VALID_ROW,
            "title": "Nike shoes on display",
            "keywords": "nike,shoes,sport,running,outdoor",
            "logo_marks_detected": ["Nike"],
        }
        report = validate_row(**row)
        assert report.passed is False
        failed_ids = {r.rule_id for r in report.failures}
        assert "title-no-brand-names" in failed_ids
        assert "keywords-no-brand-names" in failed_ids

    def test_default_logo_marks_is_empty(self):
        # logo_marks_detected defaults to [] — no brand-name failures
        report = validate_row(
            filename="photo.jpg",
            title="Beautiful sunset",
            keywords="sunset,ocean,sky,water,nature",
            category=1,
            releases="",
        )
        # brand-name validators should pass when no logo marks provided
        brand_results = [
            r for r in report.results
            if r.rule_id in ("title-no-brand-names", "keywords-no-brand-names")
        ]
        assert all(r.passed for r in brand_results)


# ---------------------------------------------------------------------------
# AC2 — Rule IDs match the spec (completeness check)
# ---------------------------------------------------------------------------

EXPECTED_RULE_IDS = [
    "filename-required",
    "filename-no-path",
    "title-required",
    "title-max-length",
    "title-sentence-case",
    "title-no-brand-names",
    "min-keyword-count",
    "max-keyword-count",
    "keywords-no-brand-names",
    "keywords-separator-format",
    "category-required",
    "category-must-be-numeric",
    "category-valid-code",
    "releases-state-enforced",
    "releases-exact-filename-match",
    "releases-separator-format",
]


def test_all_16_rule_ids_defined():
    """AC2 + AC10: All 16 rule IDs are present with no additions."""
    report = validate_row(**VALID_ROW)
    actual = [r.rule_id for r in report.results]
    assert actual == EXPECTED_RULE_IDS


def test_exactly_16_rules():
    """AC10: No rule is silently absent."""
    assert len(EXPECTED_RULE_IDS) == 16
