import streamlit as st
import random
from main import validate_input  # Import your validation function
# Page configuration with enhanced settings
st.set_page_config(
   page_title="Number Guessing Game",
   page_icon="🎯",
   layout="centered",
   initial_sidebar_state="expanded"
)
# Custom CSS for styling
st.markdown("""
<style>
   .main {
       padding: 2rem;
   }
   .stButton>button {
       width: 100%;
       border-radius: 10px;
       padding: 10px;
       font-weight: bold;
       transition: all 0.3s ease;
       background: linear-gradient(145deg, #6a11cb 0%, #2575fc 100%);
       color: white;
   }
   .stButton>button:hover {
       transform: scale(1.05);
       box-shadow: 0 5px 15px rgba(0,0,0,0.2);
   }
   .result-box {
       border-radius: 15px;
       padding: 25px;
       margin: 20px 0;
       box-shadow: 0 4px 8px rgba(0,0,0,0.1);
   }
   .win-box {
       background: linear-gradient(145deg, #d4f4dd, #a8e6cf);
       border: 2px solid #28a745;
   }
   .lose-box {
       background: linear-gradient(145deg, #f8d7da, #ffaaa5);
       border: 2px solid #dc3545;
   }
   .stats-box {
       background: linear-gradient(145deg, #e9ecef, #f8f9fa);
       border-radius: 15px;
       padding: 20px;
       margin: 20px 0;
       box-shadow: 0 4px 8px rgba(0,0,0,0.1);
   }
   .header {
       text-align: center;
       color: #2c3e50;
       margin-bottom: 30px;
   }
   .attempt-counter {
       font-size: 1.2rem;
       font-weight: bold;
       color: #6a11cb;
       text-align: center;
       margin: 15px 0;
   }
   .progress-bar {
       height: 20px;
       border-radius: 10px;
       margin: 15px 0;
       background-color: #e9ecef;
   }
   .progress-fill {
       height: 100%;
       border-radius: 10px;
       background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
       transition: width 0.5s ease;
   }
   .guess-dot {
       width: 40px;
       height: 40px;
       border-radius: 50%;
       display: flex;
       align-items: center;
       justify-content: center;
       color: white;
       font-weight: bold;
       margin: 5px;
       box-shadow: 0 2px 4px rgba(0,0,0,0.2);
   }
   .guess-container {
       display: flex;
       flex-wrap: wrap;
       gap: 10px;
       margin: 15px 0;
       justify-content: center;
   }
   .quit-box {
       background: linear-gradient(145deg, #ffeaa7, #fdcb6e);
       border: 2px solid #e17055;
       border-radius: 15px;
       padding: 25px;
       margin: 20px 0;
       box-shadow: 0 4px 8px rgba(0,0,0,0.1);
   }
   .input-section {
       background-color: #f8f9fa;
       border-radius: 10px;
       padding: 20px;
       margin: 15px 0;
   }
</style>
""", unsafe_allow_html=True)
# Initialize session state
if "rand_num" not in st.session_state:
   st.session_state.rand_num = random.randint(1, 100)
if "attempts" not in st.session_state:
   st.session_state.attempts = 0
if "message" not in st.session_state:
   st.session_state.message = ""
if "game_over" not in st.session_state:
   st.session_state.game_over = False
if "game_stats" not in st.session_state:
   st.session_state.game_stats = {
       "games_played": 0,
       "games_won": 0,
       "best_score": float('inf'),
       "total_attempts": 0
   }
if "guess_history" not in st.session_state:
   st.session_state.guess_history = []  # Store guess value and status
if "show_celebration" not in st.session_state:
   st.session_state.show_celebration = False
if "user_quit" not in st.session_state:
   st.session_state.user_quit = False
if "quit_selected" not in st.session_state:
   st.session_state.quit_selected = "Continue playing"
# Header section with enhanced visuals
st.markdown("<h1 class='header'>🎯 Number Guessing Game</h1>", unsafe_allow_html=True)
st.markdown("### Guess a number between 1 and 100!")
# Display game progress
max_attempts = 55
progress_percentage = min(st.session_state.attempts / max_attempts * 100, 100)
st.markdown(f"<div class='attempt-counter'>Attempts: {st.session_state.attempts} / {max_attempts}</div>", unsafe_allow_html=True)
st.markdown("<div class='progress-bar'><div class='progress-fill' style='width: {}%;'></div></div>".format(progress_percentage), unsafe_allow_html=True)
# Display guess history as colored dots
if st.session_state.guess_history:
   st.markdown("### 📋 Your Guesses")
   st.markdown("<div class='guess-container'>", unsafe_allow_html=True)
   
   for guess_data in st.session_state.guess_history:
       guess = guess_data["value"]
       status = guess_data["status"]
       
       if status == "correct":
           color = "#28a745"  # Green for correct guess
       elif status == "high":
           color = "#dc3545"  # Red for too high
       else:  # low
           color = "#007bff"  # Blue for too low
           
       st.markdown(f"""
           <div class="guess-dot" style="background-color: {color};">
               {guess}
           </div>
       """, unsafe_allow_html=True)
   
   st.markdown("</div>", unsafe_allow_html=True)
   
   # Add legend
   col1, col2, col3 = st.columns(3)
   with col1:
       st.markdown("🔴 Too high")
   with col2:
       st.markdown("🔵 Too low")
   with col3:
       st.markdown("🎯 Correct!")
# Input section with separate boxes
st.markdown("<div class='input-section'>", unsafe_allow_html=True)
st.subheader("🎮 Game Controls")
# Two columns for input and quit selection
col1, col2 = st.columns(2)
with col1:
   # Number input box
   user_guess = st.number_input(
       "Enter your guess (1-100):",
       min_value=1,
       max_value=100,
       step=1,
       key="guess_input",
       help="Enter a number between 1 and 100"
   )
with col2:
   # Quit select box
   quit_option = st.selectbox(
       "Game options:",
       ["Continue playing", "Quit game (q)"],
       key="quit_selector",
       help="Select 'Quit game' if you want to exit"
   )
# Submit button
submit_button = st.button("🎯 Submit Guess", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
# Handle form submission
if submit_button and not st.session_state.game_over and not st.session_state.user_quit:
   # Check if user wants to quit
   if quit_option == "Quit game (q)":
       st.session_state.message = "👋 You quit the game. The number was {}.".format(st.session_state.rand_num)
       st.session_state.game_over = True
       st.session_state.user_quit = True
       
       # Update game statistics for quit game
       st.session_state.game_stats["games_played"] += 1
       st.session_state.game_stats["total_attempts"] += st.session_state.attempts
       
   else:
       # Process the guess
       if user_guess:
           st.session_state.attempts += 1
           
           if user_guess == st.session_state.rand_num:
               st.session_state.message = f"Congratulations, You won! You guessed correctly in {st.session_state.attempts} attempts!"
               st.session_state.game_over = True
               st.session_state.show_celebration = True
               
               # Add to guess history
               st.session_state.guess_history.append({
                   "value": user_guess,
                   "status": "correct"
               })
               
               # Update game statistics
               st.session_state.game_stats["games_played"] += 1
               st.session_state.game_stats["games_won"] += 1
               st.session_state.game_stats["total_attempts"] += st.session_state.attempts
               if st.session_state.attempts < st.session_state.game_stats["best_score"]:
                   st.session_state.game_stats["best_score"] = st.session_state.attempts
                   
           elif user_guess > st.session_state.rand_num:
               # Check if number is even or odd
               even_odd = "even" if st.session_state.rand_num % 2 == 0 else "odd"
               st.session_state.message = f"⬇️ Too high! Try again. The number is {even_odd}."
               
               # Add to guess history
               st.session_state.guess_history.append({
                   "value": user_guess,
                   "status": "high"
               })
                   
           else:
               # Check if number is even or odd
               even_odd = "even" if st.session_state.rand_num % 2 == 0 else "odd"
               st.session_state.message = f"⬆️ Too low! Try again. The number is {even_odd}."
               
               # Add to guess history
               st.session_state.guess_history.append({
                   "value": user_guess,
                   "status": "low"
               })
                   
           # Check if maximum attempts reached
           if st.session_state.attempts >= max_attempts and not st.session_state.game_over:
               st.session_state.message = f"😢 Game over! The number was {st.session_state.rand_num}."
               st.session_state.game_over = True
               st.session_state.game_stats["games_played"] += 1
               st.session_state.game_stats["total_attempts"] += st.session_state.attempts
# Display celebration if user won
if st.session_state.show_celebration:
   st.balloons()
   st.session_state.show_celebration = False
# Display message with appropriate styling
if st.session_state.message:
   if st.session_state.game_over:
       if "Congratulations" in st.session_state.message:
           st.markdown(f"<div class='result-box win-box'>{st.session_state.message}</div>", unsafe_allow_html=True)
       elif st.session_state.user_quit:
           st.markdown(f"<div class='quit-box'>{st.session_state.message}</div>", unsafe_allow_html=True)
       else:
           st.markdown(f"<div class='result-box lose-box'>{st.session_state.message}</div>", unsafe_allow_html=True)
   else:
       st.info(st.session_state.message)
# Display game statistics
if st.session_state.game_stats["games_played"] > 0:
   st.markdown("<div class='stats-box'>", unsafe_allow_html=True)
   st.markdown("### 📊 Game Statistics")
   
   col1, col2, col3 = st.columns(3)
   with col1:
       st.metric("Games Played", st.session_state.game_stats["games_played"])
       st.metric("Win Rate", f"{(st.session_state.game_stats['games_won'] / st.session_state.game_stats['games_played'] * 100):.1f}%")
   with col2:
       st.metric("Games Won", st.session_state.game_stats["games_won"])
       if st.session_state.game_stats["games_played"] > 0:
           avg_attempts = st.session_state.game_stats["total_attempts"] / st.session_state.game_stats["games_played"]
           st.metric("Avg. Attempts", f"{avg_attempts:.1f}")
   with col3:
       if st.session_state.game_stats["best_score"] != float('inf'):
           st.metric("Best Score", st.session_state.game_stats["best_score"])
   
   st.markdown("</div>", unsafe_allow_html=True)
# Game controls
col1, col2 = st.columns(2)
with col1:
   if st.button("🔁 New Game"):
       st.session_state.rand_num = random.randint(1, 100)
       st.session_state.attempts = 0
       st.session_state.message = "New game started! Guess a number between 1 and 100."
       st.session_state.game_over = False
       st.session_state.user_quit = False
       st.session_state.guess_history = []
       st.session_state.quit_selected = "Continue playing"
       st.rerun()
with col2:
   if st.button("❓ How to Play"):
       st.info("""
       **How to Play:**
       1. Enter a number between 1-100 in the input box
       2. Click 'Submit Guess' to make your guess
       3. Select 'Quit game (q)' from dropdown if you want to exit
       4. Try to guess the number in as few attempts as possible
       
       **Pro Tip:** Use the binary search approach for the best results!
       """)
# Add a fun fact section
with st.expander("🤔 Did You Know?"):
   facts = [
       "The optimal strategy for this game is binary search, which takes at most 7 guesses!",
       "The number guessing game is often used to teach computer science concepts like algorithms.",
       "The highest number of attempts needed to guess any number between 1-100 is just 7 with binary search!",
       "This game is sometimes called 'Hi-Lo' or 'Guess the Number' in different cultures."
   ]
   st.info(random.choice(facts))
# Footer
st.markdown("---")
st.markdown("*Built by Sara ❤️*")

 