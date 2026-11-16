import contextlib
import io
import sys
from pathlib import Path

import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from storage import PET_COUNT, load_game, save_game
from tamagotchi import Tamagotchi


st.set_page_config(page_title="Tamagotchi Garden", page_icon="🐣", layout="wide")

st.markdown(
    """
    <style>
    :root {
        color-scheme: light;
    }
    .stApp {
        --background-color: #f3f7f2;
        --secondary-background-color: #ffffff;
        --text-color: #17382d;
        --primary-color: #28734f;
        color: #17382d;
        background:
            radial-gradient(ellipse at 10% 0%, #dcecdf 0, transparent 38%),
            #f3f7f2;
    }
    [data-testid="stAppViewContainer"] {
        color: #17382d;
    }
    [data-testid="stAppViewContainer"] :is(h1, h2, h3, h4, p, label, li),
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] *,
    [data-testid="stCaptionContainer"] *,
    [data-testid="stWidgetLabel"] * {
        color: #17382d !important;
    }
    [data-testid="stCaptionContainer"] * {
        color: #4a6254 !important;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    .hero {
        padding: 1.5rem 0 0.6rem;
    }
    .hero h1 {
        color: #234b3b;
        font-size: clamp(2.2rem, 5vw, 3.5rem);
        letter-spacing: -0.04em;
        margin-bottom: 0.25rem;
    }
    .hero p {
        color: #4a6254 !important;
        font-size: 1.05rem;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border-color: #cbd9ce;
        border-radius: 18px;
    }
    div.stButton > button {
        background-color: #e5efe7;
        border: 1px solid #799783;
        color: #17382d !important;
        border-radius: 10px;
        min-height: 2.7rem;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background-color: #d5e7d9;
        border-color: #28734f;
        color: #123b29 !important;
    }
    div.stButton > button[kind="primary"] {
        background-color: #28734f !important;
        border-color: #28734f !important;
        color: #ffffff !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #1f5e40 !important;
        border-color: #1f5e40 !important;
    }
    [data-testid="stTextInput"] input {
        background-color: #ffffff !important;
        border-color: #82988a !important;
        color: #17382d !important;
    }
    [data-testid="stTextInput"] input::placeholder {
        color: #52695b !important;
        opacity: 1;
    }
    [data-testid="stAlert"] {
        background-color: #ffffff;
        border: 1px solid #cbd9ce;
        color: #17382d;
    }
    [data-testid="stAlert"] * {
        color: #17382d !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "pets" not in st.session_state:
    st.session_state.pets = None
if "notice" not in st.session_state:
    st.session_state.notice = None


def set_notice(message: str, kind: str = "success") -> None:
    st.session_state.notice = (kind, message)


def show_notice() -> None:
    notice = st.session_state.notice
    if notice is None:
        return
    kind, message = notice
    getattr(st, kind)(message)
    st.session_state.notice = None


def create_game(names: list[str]) -> None:
    st.session_state.pets = [Tamagotchi(name) for name in names]
    set_notice("Your new garden is ready. Take good care of your pets!")


def load_saved_game() -> None:
    try:
        pets = load_game()
    except (OSError, ValueError) as error:
        set_notice(f"Could not load the saved game: {error}", "error")
        return

    if pets is None:
        set_notice("No saved game was found yet.", "warning")
        return

    st.session_state.pets = pets
    set_notice("Saved game loaded. Welcome back!")


def save_current_game() -> None:
    try:
        save_game(st.session_state.pets)
    except (OSError, ValueError) as error:
        set_notice(f"Could not save the game: {error}", "error")
    else:
        set_notice("Game saved successfully.")


def perform_action(pet: Tamagotchi, action: str) -> None:
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        getattr(pet, action)()
        pet.random_event()

    messages = [line for line in output.getvalue().splitlines() if line.strip()]
    action_feedback = {
        "feed": "had a meal",
        "play": "had some playtime",
        "sleep": "got some rest",
        "heal": "received care",
    }
    result = messages[-1] if messages else f"{pet.name} {action_feedback[action]}."
    set_notice(result)


def render_pet(pet: Tamagotchi, index: int) -> None:
    with st.container(border=True):
        st.subheader(f"🐾 {pet.name}")
        if pet.is_alive():
            st.caption("🌱 Happy and growing")
        else:
            st.caption("🕊️ This pet has passed away")

        stat_columns = st.columns(2)
        stat_columns[0].metric("❤️ Health", pet.health)
        stat_columns[1].metric("🍎 Hunger", pet.hunger)
        stat_columns[0].metric("🎾 Boredom", pet.boredom)
        stat_columns[1].metric("🌙 Exhaustion", pet.exhaustion)

        st.caption("Lower hunger, boredom, and exhaustion are better.")
        actions = st.columns(4)
        action_labels = (
            ("feed", "🍎 Feed"),
            ("play", "🎾 Play"),
            ("sleep", "🌙 Sleep"),
            ("heal", "💚 Heal"),
        )
        for column, (action, label) in zip(actions, action_labels):
            if column.button(
                label,
                key=f"{action}-{index}",
                disabled=not pet.is_alive(),
                use_container_width=True,
            ):
                perform_action(pet, action)
                st.rerun()


show_notice()
st.markdown(
    """
    <div class="hero">
        <h1>🐣 Tamagotchi Garden</h1>
        <p>A little care goes a long way. Check in on your pets and help them thrive.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

pets = st.session_state.pets
if pets is None:
    new_game_column, load_game_column = st.columns(2, gap="large")

    with new_game_column:
        with st.container(border=True):
            st.subheader("🌼 Start a new garden")
            st.write(f"Choose names for your {PET_COUNT} new pets.")
            with st.form("new-game-form"):
                names = [
                    st.text_input(f"Pet {index + 1}", value=default_name)
                    for index, default_name in enumerate(("Mochi", "Pippin", "Biscuit"))
                ]
                submitted = st.form_submit_button(
                    "Create my garden",
                    type="primary",
                    use_container_width=True,
                )
            if submitted:
                cleaned_names = [name.strip() for name in names]
                if any(not name for name in cleaned_names):
                    st.error("Please enter a name for each pet.")
                else:
                    create_game(cleaned_names)
                    st.rerun()

    with load_game_column:
        with st.container(border=True):
            st.subheader("🏡 Continue your garden")
            st.write("Pick up where you left off using your saved game.")
            if st.button("Load saved game", use_container_width=True):
                load_saved_game()
                st.rerun()
else:
    alive_count = sum(pet.is_alive() for pet in pets)
    average_health = sum(pet.health for pet in pets) / len(pets)
    summary_columns = st.columns(3)
    summary_columns[0].metric("🐾 Your pets", len(pets))
    summary_columns[1].metric("🌿 Doing well", f"{alive_count} / {len(pets)}")
    summary_columns[2].metric("❤️ Average health", f"{average_health:.1f}")

    top_left, top_right = st.columns([4, 1])
    with top_left:
        st.subheader("Your garden")
    with top_right:
        if st.button("💾 Save game", type="primary", use_container_width=True):
            save_current_game()
            st.rerun()

    pet_columns = st.columns(len(pets), gap="medium")
    for index, (column, pet) in enumerate(zip(pet_columns, pets)):
        with column:
            render_pet(pet, index)
