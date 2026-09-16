"""Unit tests for the dashboard theme module."""

from dashboard import theme


def test_css_contains_all_brand_colours():
    css = theme.css()
    for value in theme.COLORS.values():
        assert value in css


def test_css_contains_ibm_plex_import():
    assert "IBM+Plex+Sans" in theme.css()


def test_font_stack_mentions_ibm_plex():
    assert "IBM Plex Sans" in theme.FONT_STACK


def test_css_includes_button_styling():
    css = theme.css()
    assert "stButton" in css
    assert "border-radius" in css


def test_css_includes_sidebar_styling():
    assert "stSidebar" in theme.css()


def test_apply_theme_calls_markdown():
    calls = []

    class FakeStreamlit:
        @staticmethod
        def markdown(body, unsafe_allow_html=False):
            calls.append((body, unsafe_allow_html))

    theme.apply_theme(FakeStreamlit)
    assert len(calls) == 1
    assert calls[0][1] is True

