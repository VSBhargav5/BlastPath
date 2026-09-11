from blastpath.bands import risk_band


def test_bands():
    assert risk_band(10) == "low"
    assert risk_band(30) == "medium"
    assert risk_band(50) == "high"
    assert risk_band(80) == "critical"
