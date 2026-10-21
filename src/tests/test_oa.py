"""Unit tests for quiver.oa parameter and proximity utilities."""

from pathlib import Path

import pytest

from quiver.oa.params import (
    compare_param_sets,
    load_param_file,
    validate_oa_params,
)
from quiver.oa.proximity import analyze_proximity_log, detect_dropouts, parse_prx_lines

REPO_ROOT = Path(__file__).resolve().parents[2]
GERMANY_PARAMS = REPO_ROOT / "docs/Operations/firmware/parameters/params-object-avoidance.param"
TEXAS_PARAMS = (
    REPO_ROOT / "docs/Operations/firmware/parameters/params-object-avoidance-texas-v1.param"
)

SAMPLE_PRX_LOG = """\
FMT, 135, 45, PRX, TimeUS,Layer,D0,D45,D90,D135,D180,D225,D270,D315,DUp,CMin,CMax
PRX, 1000000, 0, 500, 600, 700, 800, 900, 1000, 1100, 1200, 0, 1200
PRX, 1100000, 0, 480, 590, 690, 790, 890, 990, 1090, 1190, 0, 1190
PRX, 2000000, 0, 450, 560, 660, 760, 860, 960, 1060, 1160, 0, 1160
"""


def test_load_param_file_ignores_comments_and_blanks(tmp_path):
    param_file = tmp_path / "test.param"
    param_file.write_text(
        "# comment\n"
        "OA_TYPE,1\n"
        "\n"
        "OA_MARGIN_MAX,4\n",
        encoding="utf-8",
    )
    params = load_param_file(param_file)
    assert params == {"OA_TYPE": 1, "OA_MARGIN_MAX": 4}


def test_validate_oa_params_accepts_germany_baseline():
    issues = validate_oa_params(load_param_file(GERMANY_PARAMS))
    assert issues == []


def test_validate_oa_params_accepts_texas_candidate():
    issues = validate_oa_params(load_param_file(TEXAS_PARAMS))
    assert issues == []


def test_validate_oa_params_flags_margin_mismatch():
    issues = validate_oa_params(
        {
            "OA_TYPE": 1,
            "OA_BR_TYPE": 1,
            "AVOID_MARGIN": 8,
            "OA_MARGIN_MAX": 4,
            "AVOID_DIST_MAX": 6,
            "OA_BR_LOOKAHEAD": 12,
            "OA_DB_DIST_MAX": 10,
        }
    )
    assert any("AVOID_MARGIN exceeds OA_MARGIN_MAX" in issue for issue in issues)


def test_compare_param_sets_reports_texas_differences():
    diffs = compare_param_sets(load_param_file(GERMANY_PARAMS), load_param_file(TEXAS_PARAMS))
    assert diffs["OA_MARGIN_MAX"] == (4, 5)
    assert diffs["OA_BR_LOOKAHEAD"] == (12, 14)
    assert diffs["OA_DB_DIST_MAX"] == (10, 12)


def test_parse_prx_lines_extracts_minimum_distance():
    samples = parse_prx_lines(SAMPLE_PRX_LOG.splitlines())
    assert len(samples) == 3
    assert samples[0].min_distance_cm == 500
    assert samples[0].time_us == 1_000_000


def test_detect_dropouts_finds_gap():
    samples = parse_prx_lines(SAMPLE_PRX_LOG.splitlines())
    dropouts = detect_dropouts(samples, gap_threshold_s=0.5)
    assert len(dropouts) == 1
    assert dropouts[0].duration_s == pytest.approx(0.9, abs=0.01)


def test_analyze_proximity_log_round_trip(tmp_path):
    log_path = tmp_path / "sample.log"
    log_path.write_text(SAMPLE_PRX_LOG, encoding="utf-8")
    summary = analyze_proximity_log(log_path, gap_threshold_s=0.5)
    assert summary["sample_count"] == 3
    assert summary["dropout_count"] == 1
    assert summary["min_distance_m"] == 4.5
