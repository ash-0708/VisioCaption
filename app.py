import streamlit as st
from PIL import Image
import google.generativeai as genai
import io

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="visioCaption",
    page_icon="🔍",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark background */
.stApp {
    background-color: #0f0f0f;
    color: #e8e8e8;
}

/* Header */
.main-header {
    text-align: center;
    padding: 2.5rem 0 1rem 0;
}
.main-header h1 {
    font-family: 'Space Mono', monospace;
    font-size: 3rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -1px;
    margin-bottom: 0;
}
.main-header h1 span {
    color: #a78bfa;
}
.main-header p {
    color: #888;
    font-size: 1rem;
    font-weight: 300;
    margin-top: 0.5rem;
}

/* Cards */
.caption-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
}
.caption-card h4 {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #a78bfa;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.caption-card p {
    color: #ddd;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
}

/* Tone badge */
.tone-badge {
    display: inline-block;
    background: #2a1f4a;
    color: #a78bfa;
    border: 1px solid #4a3a7a;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    margin-bottom: 0.5rem;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #2a2a2a;
    margin: 1.5rem 0;
}

/* Buttons */
.stButton > button {
    background: #a78bfa;
    color: #0f0f0f;
    border: none;
    border-radius: 8px;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 0.6rem 1.5rem;
    transition: background 0.2s;
}
.stButton > button:hover {
    background: #c4b5fd;
    color: #0f0f0f;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #141414;
    border-right: 1px solid #2a2a2a;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #1a1a1a;
    border: 1px dashed #3a3a3a;
    border-radius: 12px;
    padding: 1rem;
}

/* Image captions */
img {
    border-radius: 10px;
}

/* Info box */
.info-box {
    background: #1a1a1a;
    border-left: 3px solid #a78bfa;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: #aaa;
}

/* Success */
.stSuccess {
    background: #0f2a1a !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helper functions ──────────────────────────────────────────────────────────

def setup_gemini(api_key: str):
    """Configure the Gemini client with the given API key."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def build_prompt(tone: str) -> str:
    """Return a tone-specific prompt for caption generation."""
    prompts = {
        "Descriptive": (
            "Look at this image carefully and write a clear, detailed caption. "
            "Describe what you see: the main subject, setting, colors, and any notable details. "
            "Keep it factual and informative. 2-3 sentences max."
        ),
        "Professional": (
            "Analyze this image and write a polished, professional caption suitable for a "
            "business presentation, report, or corporate context. "
            "Be concise, precise, and formal in tone. 1-2 sentences."
        ),
        "Social Media": (
            "Write a fun, engaging caption for this image as if posting it on Instagram or Twitter. "
            "Make it catchy and relatable. You can add 2-3 relevant emojis. "
            "Keep it short and punchy — under 30 words."
        ),
    }
    return prompts.get(tone, prompts["Descriptive"])


def generate_caption(model, image: Image.Image, tone: str) -> str:
    """Send image + prompt to Gemini and return the caption text."""
    prompt = build_prompt(tone)
    response = model.generate_content([prompt, image])
    return response.text.strip()


def images_to_download_text(results: list) -> str:
    """Format all captions into a plain text string for download."""
    lines = ["visioCaption — Generated Captions", "=" * 40, ""]
    for i, (filename, tone, caption) in enumerate(results, 1):
        lines.append(f"Image {i}: {filename}")
        lines.append(f"Tone   : {tone}")
        lines.append(f"Caption: {caption}")
        lines.append("")
    return "\n".join(lines)


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")

    api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Get your free key at https://aistudio.google.com",
    )

    st.markdown("---")

    tone = st.radio(
        "Caption Tone",
        options=["Descriptive", "Professional", "Social Media"],
        index=0,
        help="Choose how the caption should sound.",
    )

    tone_descriptions = {
        "Descriptive": "📋 Detailed & factual — great for documentation.",
        "Professional": "💼 Polished & formal — great for reports.",
        "Social Media": "🎉 Fun & catchy — great for Instagram/Twitter.",
    }
    st.markdown(
        f'<div class="info-box">{tone_descriptions[tone]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        "<small style='color:#555;'>Built with Google Gemini Vision API + Streamlit</small>",
        unsafe_allow_html=True,
    )


# ── Main UI ───────────────────────────────────────────────────────────────────

st.markdown("""
<div class="main-header">
    <h1>visio<span>Caption</span></h1>
    <p>AI-powered image captions using Google Gemini Vision</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

uploaded_files = st.file_uploader(
    "Upload one or more images",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True,
    help="You can upload multiple images at once for batch captioning.",
)

if not api_key:
    st.markdown(
        '<div class="info-box">👈 Enter your Gemini API key in the sidebar to get started. '
        'Get a free key at <a href="https://aistudio.google.com" target="_blank" style="color:#a78bfa;">aistudio.google.com</a></div>',
        unsafe_allow_html=True,
    )

elif uploaded_files:
    generate_btn = st.button("✨ Generate Captions", use_container_width=True)

    if generate_btn:
        try:
            model = setup_gemini(api_key)
        except Exception as e:
            st.error(f"Could not connect to Gemini API. Check your API key.\n\nError: {e}")
            st.stop()

        st.markdown("---")
        all_results = []

        # Process each uploaded image
        for uploaded_file in uploaded_files:
            col1, col2 = st.columns([1, 2], gap="large")

            with col1:
                image = Image.open(uploaded_file)
                st.image(image, caption=uploaded_file.name, use_container_width=True)

            with col2:
                with st.spinner(f"Generating caption for **{uploaded_file.name}**..."):
                    try:
                        caption = generate_caption(model, image, tone)
                        st.markdown(
                            f"""
                            <div class="caption-card">
                                <h4>Generated Caption</h4>
                                <div class="tone-badge">{tone}</div>
                                <p>{caption}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        all_results.append((uploaded_file.name, tone, caption))

                    except Exception as e:
                        st.error(f"Failed to caption **{uploaded_file.name}**: {e}")

            st.markdown("---")

        # Download button (shown after all captions are generated)
        if all_results:
            download_text = images_to_download_text(all_results)
            st.download_button(
                label="⬇️ Download All Captions (.txt)",
                data=download_text,
                file_name="visiocaption_output.txt",
                mime="text/plain",
                use_container_width=True,
            )
            st.success(f"✅ Done! {len(all_results)} caption(s) generated.")

elif not uploaded_files and api_key:
    st.markdown(
        '<div class="info-box">⬆️ Upload one or more images above to begin.</div>',
        unsafe_allow_html=True,
    )
