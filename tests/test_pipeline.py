import pytest
import numpy as np
import json
from pipeline.classifier import ChronisClassifier
from pipeline.formatter import JSONFormatter

@pytest.fixture
def classifier():
    return ChronisClassifier(window=7, threshold=0.35, min_logs=7, min_mentions=3)

def test_sparse_logs(classifier):
    # Missing logs
    n = np.array([0.5]*7)
    b = np.array([0.5, 0.5, 0.5, 0.5, np.nan, np.nan, np.nan])
    t, c, m = classifier.classify(n, b)
    assert t == "INSUFFICIENT_EVIDENCE"
    assert m["valid_logs"] == 4

def test_sparse_entries(classifier):
    # Missing entries
    n = np.array([0.8, 0.8, np.nan, np.nan, np.nan, np.nan, np.nan])
    b = np.array([0.5]*7)
    t, c, m = classifier.classify(n, b)
    assert t == "INSUFFICIENT_EVIDENCE"
    assert m["valid_entries"] == 2

def test_over(classifier):
    # High N, Low B, rising B to avoid Aspiration Gap
    n = np.array([0.8]*7)
    b = np.array([0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.4])
    t, c, m = classifier.classify(n, b)
    assert t == "OVERSTATEMENT"

def test_under(classifier):
    # Low N, High B
    n = np.array([0.2]*7)
    b = np.array([0.8]*7)
    t, c, m = classifier.classify(n, b)
    assert t == "UNDERSTATEMENT"

def test_blind(classifier):
    # No N, High B (Bypass abstention for testing)
    classifier.mm = 0 
    n = np.array([0.1]*7)
    b = np.array([0.8]*7)
    t, c, m = classifier.classify(n, b)
    assert t == "BLIND_SPOT"

def test_aspire(classifier):
    # High N, falling B
    n = np.array([0.8]*7)
    b = np.array([0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2])
    t, c, m = classifier.classify(n, b)
    assert t == "ASPIRATION_GAP"

def test_json():
    # Valid JSON
    out = JSONFormatter.format_output("U1", "fit", "2026-06-01", "2026-06-07", 0.8, 0.2, 0.6, "OVER", 0.9)
    try:
        j = json.loads(out)
        assert j["user_id"] == "U1"
    except:
        pytest.fail("Invalid JSON")
