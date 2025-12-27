import streamlit as st
import base64
from pathlib import Path
import sys
import streamlit.components.v1 as components

# --------------------------------------------------
# Path setup 
# --------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.retrieval.retriever import retrieve
from src.generation.llm import generate_answer

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="🪄 Harry Potter RAG",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# Asset paths
# --------------------------------------------------
ASSETS = Path(__file__).parent / "assets"
BG_IMAGE = ASSETS / "hp_library.png"
THEME_MUSIC = ASSETS / "theme.mp3"
MAGIC_SOUND = ASSETS / "magic.mp3"

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def load_base64(file_path: Path) -> str:
    try:
        if not file_path.exists():
            return ""
        return base64.b64encode(file_path.read_bytes()).decode()
    except Exception:
        return ""

bg_base64 = load_base64(BG_IMAGE)
theme_base64 = load_base64(THEME_MUSIC)
magic_base64 = load_base64(MAGIC_SOUND)

# --------------------------------------------------
# 🎵 Background Music - Auto-play on page load
# --------------------------------------------------
def play_hidden_music(mp3_file):
    with open(mp3_file, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    
    components.html(
        f"""
        <audio id="bg-audio" loop>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        <script>
            const audio = document.getElementById('bg-audio');
            audio.volume = 0.25;
            
            const startAudio = () => {{
                audio.play().catch(e => console.log("Playback blocked"));
                window.removeEventListener('click', startAudio);
            }};

            window.parent.document.addEventListener('click', startAudio);
        </script>
        """,
        height=0,
    )

play_hidden_music(THEME_MUSIC)

# --------------------------------------------------
# CSS Styling
# --------------------------------------------------
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=IM+Fell+English:ital@0;1&display=swap');

    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .stApp::before {{
        content: '';
        position: fixed;
        inset: 0;
        background: rgba(10, 10, 20, 0.88);
        z-index: 0;
    }}

    .main > div {{
        position: relative;
        z-index: 1;
    }}

    #MainMenu, footer {{ visibility: hidden; }}
    header {{ visibility: visible; }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(20,15,30,0.98), rgba(35,25,45,0.98));
        border-right: 3px solid #d4af37;
        padding-top: 1rem;
    }}

    [data-testid="stSidebar"] h2 {{
        font-family: 'Cinzel', serif;
        color: #ffd700;
        text-align: center;
        text-shadow: 0 0 12px rgba(255,215,0,0.5);
        margin-bottom: 0.8rem;
    }}

    [data-testid="stSidebar"] h3 {{
        font-family: 'Cinzel', serif;
        color: #d4af37;
        font-size: 1.15rem;
        margin-top: 1.2rem;
        margin-bottom: 0.5rem;
    }}

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] li {{
        font-family: 'IM Fell English', serif;
        color: #c9b885;
        font-size: 1rem;
        line-height: 1.6;
    }}

    [data-testid="stSidebar"] button {{
        background: rgba(75, 40, 110, 0.65) !important;
        border: 1.5px solid #d4af37 !important;
        border-radius: 10px !important;
        color: #f0e6d2 !important;
        font-family: 'IM Fell English', serif !important;
        font-size: 0.95rem !important;
        text-align: left !important;
        padding: 10px 14px !important;
        margin-bottom: 6px !important;
        transition: all 0.25s ease;
    }}

    [data-testid="stSidebar"] button:hover {{
        background: rgba(95, 60, 130, 0.85) !important;
        border-color: #ffd700 !important;
        transform: translateX(6px);
        box-shadow: 0 0 18px rgba(255,215,0,0.4);
    }}

    [data-testid="collapsedControl"] {{
        background: rgba(212, 175, 55, 0.9) !important;
        border: 2px solid #ffd700 !important;
        border-radius: 0 8px 8px 0 !important;
        color: #2c1810 !important;
    }}
    
    [data-testid="collapsedControl"]:hover {{
        background: rgba(255, 215, 0, 0.9) !important;
        transform: translateX(5px);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    }}

    .sidebar-footer {{
        background: rgba(212,175,55,0.12);
        border: 1px solid #d4af37;
        border-radius: 12px;
        padding: 14px;
        margin-top: 1rem;
    }}

    .sidebar-footer strong {{
        color: #ffd700;
        font-family: 'Cinzel', serif;
    }}

    .main-title {{
        font-family: 'Cinzel', serif;
        font-size: 3.5rem;
        text-align: center;
        color: #ffd700;
        text-shadow: 0 0 30px rgba(255,215,0,0.6);
        animation: glow 2s ease-in-out infinite alternate;
    }}

    .subtitle {{
        text-align: center;
        color: #c9b885;
        font-size: 1.3rem;
        font-family: 'IM Fell English', serif;
        font-style: italic;
        margin-bottom: 2.5rem;
    }}

    @keyframes glow {{
        from {{ text-shadow: 0 0 20px rgba(255,215,0,0.4); }}
        to {{ text-shadow: 0 0 35px rgba(255,215,0,0.8); }}
    }}

    /* 🌟 INPUT BOX — clean full golden border */
    .stTextInput > div {{
        border: 3px solid #d4af37 !important;
        border-radius: 15px !important;
        padding: 0 !important;
        background: transparent !important;
    }}

    .stTextInput > div > div {{
        border: none !important;
        background: transparent !important;
    }}

    .stTextInput > div > div > input {{
        border: none !important;
        background: linear-gradient(135deg, rgba(75, 40, 110, 0.9), rgba(95, 60, 130, 0.9)) !important;
        font-size: 1.2rem !important;
        padding: 18px 20px !important;
        color: #f0e6d2 !important;
        font-family: 'IM Fell English', serif !important;
    }}

    .stTextInput > div:focus-within {{
        border-color: #ffd700 !important;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.5) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ Hogwarts Library")
    st.markdown(
        "Ask questions across all **seven books**, including "
        "**songs, poems, and magical lore**."
    )

    st.divider()
    st.markdown("### ✨ Example Queries")

    examples = [
        "What phrase activates the Marauder’s Map?",
        "Recite the Hogwarts school song",
        "Who is the Half-Blood Prince?",
        "Which Horcrux was destroyed first?",
        "What are the Deathly Hallows?",
        "Describe the Patronus charm"
    ]

    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state["query"] = ex
            st.rerun()

    st.divider()
    st.markdown(
        """
        <div class="sidebar-footer">
        <strong>Powered by</strong><br>
        The Room of Requirement 🏰<br>
        Gemini — your wizarding AI 🧠<br>
        Memory-aware story retrieval ✨
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------
# Main content
# --------------------------------------------------
st.markdown("<h1 class='main-title'>🪄 The Marauder's Knowledge Archive</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>I solemnly swear that I am up to no good.</p>", unsafe_allow_html=True)

query = st.text_input(
    "Ask a question",
    value=st.session_state.get("query", ""),
    placeholder="Ask anything about the wizarding world…",
    label_visibility="collapsed"
)

if "answer_count" not in st.session_state:
    st.session_state.answer_count = 0

if query:
    with st.spinner("🔮 Consulting the ancient texts..."):
        try:
            chunks = retrieve(query)
            context = "\n\n".join(c["text"] for c in chunks)
            answer = generate_answer(context, query)

            st.session_state.answer_count += 1
            answer_id = st.session_state.answer_count

            import random
            unique_key = random.randint(10000, 99999)

            if magic_base64:
                components.html(
                    f"""
                    <audio id="magic-sound-{answer_id}-{unique_key}" autoplay>
                        <source src="data:audio/mpeg;base64,{magic_base64}">
                    </audio>
                    <script>
                    (function() {{
                        const magic = document.getElementById('magic-sound-{answer_id}-{unique_key}');
                        if (magic) {{
                            magic.volume = 0.6;
                            magic.play().catch(e => console.log('Magic blocked'));
                        }}
                    }})();
                    </script>
                    """,
                    height=0,
                )

            # 🌟 ANSWER BOX — fully visible + scrolls inside
            components.html(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=IM+Fell+English:ital@0;1&display=swap');

    .answer-box-animated {{
        background: linear-gradient(135deg, rgba(40,30,50,0.95), rgba(60,40,70,0.95));
        border: 3px solid #d4af37;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 0 40px rgba(212,175,55,0.4);
        position: relative;
        overflow: hidden;

        /* 👇 keep box fully visible + scroll inside */
        max-height: 60vh;
        overflow-y: auto;

        /* ✨ magical reveal animation */
        animation: magicalReveal 2s ease-out forwards;
    }}

    @keyframes magicalReveal {{
        0% {{
            opacity: 0;
            transform: scale(0.9) translateY(25px);
            filter: blur(10px);
        }}
        60% {{
            opacity: 0.8;
            transform: scale(1.02);
            filter: blur(2px);
        }}
        100% {{
            opacity: 1;
            transform: scale(1) translateY(0);
            filter: blur(0);
        }}
    }}

    /* ✨ subtle shimmer sweep */
    .answer-box-animated::after {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.25),
            transparent
        );
        animation: shimmer 2.5s ease-out;
    }}

    @keyframes shimmer {{
        0% {{ left: -100%; }}
        100% {{ left: 100%; }}
    }}
    </style>

    <div class="answer-box-animated">
        <div style="
            font-family: 'Cinzel', serif;
            font-size: 1.8rem;
            color: #ffd700;
            text-align: center;
            margin-bottom: 20px;
        ">
            📜 Answer from the Archives
        </div>

        <div style="
            font-family: 'IM Fell English', serif;
            font-size: 1.25rem;
            color: #f0e6d2;
            line-height: 1.7;
        ">
            {answer.replace(chr(10), "<br>")}
        </div>
    </div>
    """,
    height=560,
    scrolling=False
)


            with st.expander("📚 View Source Excerpts"):
                for i, chunk in enumerate(chunks[:3], 1):
                    book = chunk.get("book", "Unknown Book")
                    chapter = chunk.get("chapter", "Unknown Chapter")
                    text_snippet = (chunk.get("text", "")[:250] + "...").strip()

                    st.markdown(f"### 📖 Source {i}")
                    st.markdown(f"**Book:** {book}")
                    st.markdown(f"**Chapter:** {chapter}")
                    st.caption(text_snippet)

                    if i < len(chunks[:3]):
                        st.divider()


        except Exception as e:
            st.error(f"⚡ A spell went wrong: {e}")

else:
    st.markdown(
        """
        <div class="answer-container">
            <div class="answer-text" style="text-align:center; font-style:italic;">
                The library awaits your question.<br>
                What knowledge do you seek?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()
st.markdown(
    "<p style='text-align:center; color:#8b7355; font-family: IM Fell English;'>"
    "Mischief Managed 🗺️ • Built with black magic 🐦‍⬛"
    "</p>",
    unsafe_allow_html=True
)
