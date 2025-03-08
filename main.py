import streamlit as st
import pandas as pd
import random

# Puppet list
PUPPETS = ["Taylor", "Fade", "Apexeus", "Adam", "Foil", "Sure", "Weeee", "Doña María", "Zizi", "Nahas"]

# Emotion cards
EMOTIONS = [
    "Joy", "Excitement", "Gratitude", "Pride", "Hope", "Wonder or Awe", "Relief", "Trust", "Sadness",
    "Disappointment", "Loneliness", "Grief", "Heartbreak", "Hopelessness or Despair", "Regret", "Fear", 
    "Stress", "Overwhelm", "Vulnerability", "Anger", "Frustration", "Resentment", "Betrayal", "Hate", 
    "Disgust", "Guilt", "Shame", "Embarrassment", "Humiliation", "Stupidity or Foolishness", "Admiration", 
    "Empathy", "Belonging", "Separation", "Boundaries", "Schadenfreude", "Confusion or Lost"
]

# Prompt cards
PROMPTS = [
    "A story you tell often, but maybe haven't analyzed much.", "A story about a time you felt like a hero.",
    "A story you rarely tell.", "A story where you don't understand what happened.", 
    "A story that you're still not sure how you feel about.", "A story that changed your life in a big or small way.",
    "A story that makes you laugh every time.", "A story about a time you messed up.", 
    "A story about a time you surprised yourself.", "A story about a time you were surprised by someone else.",
    "A story that you think reveals something essential about who you are.", 
    "A story about a time you had to make a difficult decision.", 
    "A story about a time you learned a valuable lesson.", "A story that happened to you overseas.",
    "A story with someone in this room.", "A story with someone from work.", "A story with your best friend.",
    "A story from your family.", "A story you heard from someone else.", "A story from a book, tv show or a movie.",
    "A story from your childhood.", "A story about a time you tried something new.", 
    "A story about an unexpected encounter.", "A story about a time you had to keep a secret.", 
    "A story about a time you had to pretend to be someone you weren’t.", 
    "A story about a time you completely misunderstood a situation.", "A story about a bad date.", 
    "A story about a coincidence you've experienced.", "A story about a time you made a really bad (or really great) first impression.",
    "A story about something that happened at a party.", "A story about a time you had to wear something unusual.",
    "A story about an animal encounter.", "A story about a time you were in the wrong place at the wrong time.",
    "A story where food plays a major role.", "A story that takes place in a car, train, or airplane.",
    "A story about a competition or a bet.", "A story that takes place in the middle of the night.",
    "A story that happened during summer.", "A story that happened during the holiday season."
]

# Store data across rounds
if "players" not in st.session_state:
    st.session_state.players = []
if "rounds" not in st.session_state:
    st.session_state.rounds = []

# Step 1: Enter Players
st.title("Blame It on Bop")

if not st.session_state.players:
    st.subheader("Enter Player Names (3-8)")
    player_names = st.text_area("Enter names separated by commas:", "")
    
    if st.button("Start Game"):
        names = [name.strip() for name in player_names.split(",") if name.strip()]
        if 3 <= len(names) <= 8:
            st.session_state.players = names
            st.experimental_rerun()
        else:
            st.error("Please enter between 3 and 8 player names.")

# Step 2: Game Round
else:
    st.subheader("New Round")

    # Assign random emotion and prompt
    emotion = random.choice(EMOTIONS)
    prompt = random.choice(PROMPTS)

    st.caption(f"### Emotion: **{emotion}**")
    st.caption(f"### Prompt: **{prompt}**")

    # Step 3: Write Story
    story = st.text_area("Write your story:")

    # Step 4: Add Characters
    num_players = len(st.session_state.players)
    st.write(f"Add up to {num_players} characters from your story:")
    
    character_inputs = []
    for i in range(num_players):
        character = st.text_input(f"Character {i+1} (leave blank if not needed):", key=f"char_{i}")
        if character:
            character_inputs.append(character)

    # Step 5: Match Characters to Players
    if character_inputs:
        st.subheader("Match Characters to Players")
        character_to_player = {}
        
        for character in character_inputs:
            selected_player = st.selectbox(f"Who will play {character}?", st.session_state.players, key=f"player_{character}")
            character_to_player[character] = selected_player

        # Step 6: Match Characters to Puppets
        st.subheader("Match Characters to Puppets")
        character_to_puppet = {}

        for character in character_inputs:
            selected_puppet = st.selectbox(f"Which puppet will represent {character}?", PUPPETS, key=f"puppet_{character}")
            character_to_puppet[character] = selected_puppet

        # Step 7: Add Notes
        notes = st.text_area("Additional Notes:")

        # Step 8: Save Round
        if st.button("Finish Round"):
            round_data = {
                "Emotion": emotion,
                "Prompt": prompt,
                "Story": story,
                "Characters": character_inputs,
                "Player Match": character_to_player,
                "Puppet Match": character_to_puppet,
                "Notes": notes
            }
            st.session_state.rounds.append(round_data)
            st.success("Round saved! Start a new round.")

    # Download CSV
    if st.session_state.rounds:
        if st.button("Download CSV"):
            df = pd.DataFrame(st.session_state.rounds)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download Game Data", csv, "blame_it_on_bop.csv", "text/csv")

        # Option to reset game
        if st.button("Reset Game"):
            st.session_state.players = []
            st.session_state.rounds = []
            st.experimental_rerun()
