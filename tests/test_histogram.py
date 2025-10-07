import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Histogram import Histogram

def test_histogram_counts_and_render():
    h = Histogram()
    h.add(3); h.add(3); h.add(5)
    out = h.render()
    # basic checks: keys appear and counts look right
    assert "3:" in out and "5:" in out
    assert "(2)" in out  # two occurrences of 3
    assert "(1)" in out  # one occurrence of 5
