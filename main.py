import streamlit as st
import pandas as pd
import random
import gspread
from google.oauth2 import service_account
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import streamlit_authenticator as stauth

# Google Authentication Setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/userinfo.profile"]
SPREADSHEET_ID = st.secrets["google_sheet_id"]  # Store in Streamlit secrets

def get_gspread_client():
    try:
        creds = service_account.Credentials.from_service_account_info(
            {
                "type": st.secrets["type"],
                "project_id": st.secrets["project_id"],
                "private_key_id": st.secrets["private_key_id"],
                "private_key": st.secrets["private_key"],
                "client_email": st.secrets["client_email"],
                "client_id": st.secrets["client_id"],
                "auth_uri": st.secrets["auth_uri"],
                "token_uri": st.secrets["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["client_x509_cert_url"],
            },
            scopes=SCOPES,
        )
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Authentication failed. Please check your credentials. {e}")
        return None

def save_to_google_sheets(data):
    client = get_gspread_client()
    if client:
        sheet = client.open_by_key(SPREADSHEET_ID).sheet1
        row_data = list(data.values())
        sheet.append_row(row_data)
        st.info("Added to Google sheets")

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
if "round" not in st.session_state:
    st.session_state.round = 1

# Step 1: Set up players (only happens once)
st.title("Blame It on Bob")
st.write("The data is saved [here](https://docs.google.com/spreadsheets/d/13JeDyfS6wMtmoGiKHwWMh-4Rp-PL8fwWl3d3bqTOJPs/edit?gid=0#gid=0).")
st.subheader("Enter player names (3-8 players):")
player_names = st.text_area("Players (one per line)").split("\n")
player_names = [p.strip() for p in player_names if p.strip()]
if st.button("Start Game"):
    if 3 <= len(player_names) <= 8:
        st.session_state.players = player_names
        st.session_state.step = 2
        st.session_state.round = 1
        st.session_state.first_round_completed = False
        st.session_state.game_data = []  # Reset game data for new session
        st.rerun()  # Use st.rerun() to move to the next step
    else:
        st.error("Please enter between 3 and 8 players.")

# Only proceed if players are set
if st.session_state.players and st.session_state.step >= 2:
    st.subheader(f"Round {st.session_state.round}")
    
    # Step 2: Draw random cards (Only select once per round)
    if f"emotion_{st.session_state.round}" not in st.session_state:
        st.session_state[f"emotion_{st.session_state.round}"] = random.choice(EMOTIONS)
    
    if f"prompt_{st.session_state.round}" not in st.session_state:
        st.session_state[f"prompt_{st.session_state.round}"] = random.choice(PROMPTS)
    
    emotion = st.session_state[f"emotion_{st.session_state.round}"]
    prompt = st.session_state[f"prompt_{st.session_state.round}"]
    
    st.caption(f"Emotion: {emotion}")
    st.caption(f"Prompt: {prompt}")

    
    # Step 3: Write a story - Create new input field for each round
    story_key = f"story_input_round_{st.session_state.round}"
    story = st.text_area("Write your story", key=story_key)
    
    # Step 4: Add characters - Create new input fields for each round
    character_inputs = []
    st.write("### Enter characters from your story")
    for i in range(len(st.session_state.players)):
        char_key = f"char_{i}_round_{st.session_state.round}"
        char_name = st.text_input(f"Enter character {i+1}", key=char_key)
        if char_name:
            character_inputs.append(char_name)
    
    if 2 <= len(character_inputs) <= len(st.session_state.players):
        if st.button("Next"):
            st.session_state.characters = character_inputs
            st.session_state.story_input = story
            st.session_state.step = 3
            st.rerun()  # Use st.rerun() to move to the next step
    
    # Step 5: Assign characters to players (Select Box, only if step >= 3)
    if st.session_state.step >= 3:
        st.write("### Match characters with players")
        assigned_players = {}
        remaining_players = st.session_state.players.copy()
        for char in st.session_state.characters:
            selected_player = st.selectbox(f"Assign {char} to a player", remaining_players, key=f"player_{char}_round_{st.session_state.round}")
            assigned_players[char] = selected_player
            remaining_players.remove(selected_player)  # Remove selected player from remaining options
        
        # Step 6: Assign characters to puppets (Select Box)
        st.write("### Match characters with puppets")
        assigned_puppets = {}
        remaining_puppets = PUPPETS.copy()
        for char in st.session_state.characters:
            selected_puppet = st.selectbox(f"Assign {char} to a puppet", remaining_puppets, key=f"puppet_{char}_round_{st.session_state.round}")
            assigned_puppets[char] = selected_puppet
            remaining_puppets.remove(selected_puppet)  # Remove selected puppet from remaining options
        
        # Step 7: Notes
        notes_key = f"notes_input_round_{st.session_state.round}"
        notes = st.text_area("Additional notes", key=notes_key)
        
        # Step 8: Save results
        if st.button("Finish Round"):
            row_data = {
                "Emotion": st.session_state[f"emotion_{st.session_state.round}"],
                "Prompt": st.session_state[f"prompt_{st.session_state.round}"],
                "Characters": ", ".join(character_inputs),
                "Story": story,
                "Notes": notes,
            }

            # Ensure puppets are always in the correct order
            puppet_assignments = {puppet: "" for puppet in PUPPETS}  # Initialize all puppets as empty
        
            # Fill in assigned players and characters in a consistent order
            for puppet in PUPPETS:
                for char, assigned_puppet in assigned_puppets.items():
                    if assigned_puppet == puppet:
                        puppet_assignments[puppet] = f"{assigned_players[char]} - {char}"
            
            # Ensure puppet order is consistent
            for puppet in PUPPETS:
                row_data[puppet] = puppet_assignments[puppet]

            # Add ordered puppet assignments to row data
            row_data.update(puppet_assignments)

            if not get_gspread_client():
                st.error("Could not save data to Google Sheets due to authentication failure.")
            else:
                save_to_google_sheets(row_data)
                st.session_state.round += 1
                st.session_state.step = 2
                st.rerun()


