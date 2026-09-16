"""Branding and theme constants for the Africa Data Intelligence dashboard."""

COLORS = {
    "beige": "#cbbeb5",
    "red": "#ff6666",
    "dark_grey": "#525266",
    "dark": "#423f3b",
    "light_beige": "#ffe5a9",
}

FONT_STACK = "'IBM Plex Sans', sans-serif"


def css() -> str:
    """Return the global CSS stylesheet for the dashboard."""
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: {FONT_STACK} !important;
        }}

        .stApp {{
            background-color: {COLORS['beige']};
        }}

        section[data-testid="stSidebar"] {{
            background-color: {COLORS['dark']} !important;
        }}
        section[data-testid="stSidebar"] * {{
            color: {COLORS['beige']} !important;
        }}

        h1, h2, h3, h4, h5, h6 {{
            color: {COLORS['dark_grey']} !important;
        }}

        .stButton > button {{
            background-color: {COLORS['red']} !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }}
    </style>
    """


def apply_theme(st) -> None:
    """Inject the CSS into a Streamlit app instance."""
    st.markdown(css(), unsafe_allow_html=True)

