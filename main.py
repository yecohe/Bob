import streamlit as st
import pandas as pd
import random

# Define puppets, emotions, and prompts
PUPPETS = ["Taylor", "Fade", "Apexeus", "Adam", "Foil", "Sure", "Weeee", "Doña María", "Zizi", "Nahas"]
EMOTIONS = [
    "Joy", "Excitement", "Gratitude", "Pride", "Hope", "Wonder or Awe", "Relief", "Trust", "Sadness", "Disappointment", "Loneliness", "Grief", "Heartbreak", "Hopelessness or Despair", "Regret", "Fear", "Stress", "Overwhelm", "Vulnerability", "Anger", "Frustration", "Resentment", "Betrayal", "Hate", "Disgust", "Guilt", "Shame", "Embarrassment", "Humiliation", "Stupidity or Foolishness", "Admiration", "Empathy", "Belonging", "Separation", "Boundaries", "Schadenfreude", "Confusion or Lost"
]
PROMPTS = [
    "A story you tell often, but maybe haven't analyzed much.", "A story about a time you felt like a hero.", "A story you rarely tell.", "A story where you don't understand what happened.", "A story that you're still not sure how you feel about.", "A story that changed your life in a big or small way.", "A story that makes you laugh every time.", "A story about a time you messed up.", "A story about a time you surprised yourself.", "A story about a time you were surprised by someone else.", "A story that you think reveals something essential about who you are.", "A story about a time you had to make a difficult decision.", "A story about a time you learned a valuable lesson.", "A story that happened to you overseas.", "A story with someone in this room.", "A story with someone from work.", "A story with your best friend.", "A story from your family.", "A story you heard from someone else.", "A story from a book, tv show or a movie.", "A story from your childhood.", "A story about a time you tried something new.", "A story about an unexpected encounter.", "A story about a time you had to keep a secret.", "A story about a time you had to pretend to be someone you weren’t.", "A story about a time you completely misunderstood a situation.", "A story about a bad date.", "A story about a coincidence you've experienced.", "A story about a time you made a really bad (or really great) first impression.", "A story about something that happened at a party.", "A story about a time you had to wear something unusual.", "A story about an animal encounter.", "A story about a time you were in the wrong place at the wrong time.", "A story where food plays a major role.", "A story that takes place in a car, train, or airplane.", "A story about a competition or a bet.", "A story that takes place in the middle of the night.", "A story that happened during summer.", "A story that happened during the holiday season."
]

# Game session storage
if "players" not in st.session_state:
    st.session_state.players = []
if "game_data" not in st.session_state:
    st.session_state.game_data = []
if "step" not in st.session_state:
    st.session_state.step = 1
if "first_round_completed" not in st.session_state:
    st.session_state.first_round_completed = False

# Step 1: Set up players (only happens once)
st.title("Blame It on Bob")
st.subheader("Enter player names (3-8 players):")
player_names = st.text_area("Players (one per line)").split("\n")
player_names = [p.strip() for p in player_names if p.strip()]
if st.button("Start Game"):
    if 3 <= len(player_names) <= 8:
        st.session_state.players = player_names
        st.session_state.round = 1
        st.session_state.step = 2
    else:
        st.error("Please enter between 3 and 8 players.")

# Only proceed if players are set
if st.session_state.players and st.session_state.step >= 2:
    st.subheader(f"Round {st.session_state.round}")
    
    # Step 2: Draw random cards
    emotion = random.choice(EMOTIONS)
    prompt = random.choice(PROMPTS)
    st.caption(f"Emotion: {emotion}")
    st.caption(f"Prompt: {prompt}")
    
    # Step 3: Write a story
    story = st.text_area("Write your story")
    
    # Step 4: Add characters (Minimum 2, Maximum: number of players)
    character_inputs = []
    st.write("### Enter characters from your story")
    for i in range(len(st.session_state.players)):
        char_name = st.text_input(f"Enter character {i+1}", key=f"char_{i}")
        if char_name:
            character_inputs.append(char_name)
    
    if 2 <= len(character_inputs) <= len(st.session_state.players):
        if st.button("Next"):
            st.session_state.characters = character_inputs
            st.session_state.step = 3
    
    # Step 5: Assign characters to players (Select Box, only if step >= 3)
    if st.session_state.step >= 3:
        st.write("### Match characters with players")
        assigned_players = {}
        for char in st.session_state.characters:
            selected_player = st.selectbox(f"Assign {char} to a player", st.session_state.players, key=f"player_{char}")
            assigned_players[char] = selected_player
        
        # Step 6: Assign characters to puppets (Select Box)
        st.write("### Match characters with puppets")
        assigned_puppets = {}
        for char in st.session_state.characters:
            selected_puppet = st.selectbox(f"Assign {char} to a puppet", PUPPETS, key=f"puppet_{char}")
            assigned_puppets[char] = selected_puppet
        
        # Step 7: Notes
        notes = st.text_area("Additional notes")
        
        # Step 8: Save results
        if st.button("Finish Round"):
            row_data = {
                "emotion": emotion,
                "prompt": prompt,
                "story": story,
                "notes": notes,
            }
            row_data.update({puppet: f"{assigned_players[char]} - {char}" for char, puppet in assigned_puppets.items()})
            
            # Save the data
            st.session_state.game_data.append(row_data)
            
            # Empty input fields for next round
            st.session_state.characters = []
            st.session_state.step = 2
            st.session_state.round += 1
            st.session_state.first_round_completed = True
    
    # Step 9: Download CSV (only after first round)
    if st.session_state.first_round_completed:
        df = pd.DataFrame(st.session_state.game_data)
        st.download_button("Download Game Data", df.to_csv(index=False), "game_data.csv", "text/csv")
