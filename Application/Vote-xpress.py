# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
import webbrowser
import math
import json
import requests
from datetime import datetime

# Data
votes = {"Candidate A": 0, "Candidate B": 0, "Candidate C": 0}
voted_users = set()
feedback_list = [] # Stores submitted feedback

# Constants
developer_info = "Aditya Raj"
linkedin_url_aditya = "https://www.linkedin.com/in/aditya-raj-a73319282/"
help_contact = "📞 +91-9876543210\n📧 help@votexpress.com"
ADMIN_USERNAME = "Aditya Raj"
ADMIN_PASSWORD = "admin123" # Hardcoded password for admin panel

# API Key for Gemini
API_KEY = "AIzaSyA89IQgoOgnCY79xIFWE7W5qGgX6M18FFw" # User-provided API key
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# --- Global Color Palette and Font Styles for Consistency ---
COLOR_PALETTE = {
    "primary_blue": "#0055A4",    # Dark Blue (Vote-Xpress brand color)
    "accent_green": "#4CAF50",    # Green (Success, positive)
    "accent_orange": "#FF9933",   # Saffron (Digital India)
    "accent_red": "#DC143C",      # Crimson (Danger, alert, close)
    "light_bg": "#f0f8ff",        # AliceBlue (General background)
    "mid_bg": "#e0ffff",          # LightCyan (Frame backgrounds)
    "dark_text": "#333333",       # Dark Gray (General text)
    "light_text": "white",        # White (Buttons, headers)
    "button_blue": "#4682B4",     # SteelBlue (Menu buttons)
    "button_purple": "#9370DB",   # MediumPurple (Submit vote)
    "button_back": "#FF6347",     # Tomato (Back button)
    "border_color": "#A9A9A9",    # DarkGray (Borders)
    "quiz_bg": "#FFFACD",         # LemonChiffon for quiz
    "quiz_border": "#FFD700",     # Gold for quiz border
    "news_button": "#FFC107",     # Amber for news button
    "news_bg": "#F5F5DC",         # Beige for news background
    "panel_bg": "#E6F0FF",        # Lighter blue for side panels
    "panel_border": "#ADD8E6",    # Light blue border
}

FONT_STYLES = {
    "header1": ("Helvetica", 28, "bold"),
    "header2": ("Helvetica", 24, "bold"),
    "header3": ("Helvetica", 20, "bold"),
    "subheader": ("Helvetica", 16, "italic"),
    "button": ("Helvetica", 14, "bold"),
    "label": ("Helvetica", 14),
    "entry": ("Helvetica", 14),
    "small_label": ("Helvetica", 12),
    "chat_font": ("Helvetica", 10),
    "splash_title": ("Inter", 48, "bold"),
    "splash_subtitle": ("Inter", 16, "bold"),
    "splash_welcome": ("Helvetica", 24, "bold"),
    "quiz_question": ("Helvetica", 16, "bold"),
    "quiz_option": ("Helvetica", 14),
    "quiz_timer": ("Helvetica", 18, "bold"),
    "quiz_result": ("Helvetica", 20, "bold"),
    "news_title": ("Helvetica", 18, "bold"),
    "news_snippet": ("Helvetica", 12),
    "news_source": ("Helvetica", 10, "italic"),
    "panel_header": ("Helvetica", 16, "bold"),
    "panel_text": ("Helvetica", 12),
    "panel_vote_count": ("Helvetica", 11, "bold"), # New style for vote counts
    "panel_total_votes": ("Helvetica", 12, "bold"), # New style for total votes
    "thought_for_day": ("Helvetica", 12, "italic"), # New style for thought of the day
}

# --- Quiz Questions Data ---
QUIZ_QUESTIONS = [
    {
        "question": "What is NOT a valid voter ID proof in India?",
        "options": ["A) Aadhaar Card", "B) Passport", "C) Ration Card", "D) Driving License"],
        "answer": "C) Ration Card"
    },
    {
        "question": "What is the minimum age to be eligible to vote in India?",
        "options": ["A) 21 years", "B) 18 years", "C) 25 years", "D) 16 years"],
        "answer": "B) 18 years"
    },
    {
        "question": "Which body conducts elections for the Lok Sabha and State Legislative Assemblies in India?",
        "options": ["A) Supreme Court of India", "B) Parliament of India", "C) Election Commission of India", "D) Ministry of Home Affairs"],
        "answer": "C) Election Commission of India"
    },
    {
        "question": "What does the term 'NOTA' stand for in Indian elections?",
        "options": ["A) None Of The Above", "B) No Opinion To Announce", "C) New Option To All", "D) National Official Transparency Act"],
        "answer": "A) None Of The Above"
    },
    {
        "question": "Which part of the Indian Constitution deals with elections?",
        "options": ["A) Part XV", "B) Part X", "C) Part XX", "D) Part V"],
        "answer": "A) Part XV"
    },
    {
        "question": "The Model Code of Conduct comes into effect from the date of:",
        "options": ["A) Election notification", "B) Filing of nominations", "C) Declaration of results", "D) Start of campaigning"],
        "answer": "A) Election notification"
    },
    {
        "question": "What is the maximum number of candidates an Electronic Voting Machine (EVM) can accommodate?",
        "options": ["A) 16", "B) 32", "C) 64", "D) 128"],
        "answer": "C) 64"
    },
    {
        "question": "Which of these is NOT a fundamental right guaranteed by the Indian Constitution?",
        "options": ["A) Right to Equality", "B) Right to Property", "C) Right to Freedom", "D) Right against Exploitation"],
        "answer": "B) Right to Property"
    },
    {
        "question": "What is the primary purpose of a candidate's manifesto?",
        "options": ["A) To list their personal achievements", "B) To outline their promises and policies if elected", "C) To criticize opposing candidates", "D) To declare their financial assets"],
        "answer": "B) To outline their promises and policies if elected"
    },
    {
        "question": "Who appoints the Chief Election Commissioner of India?",
        "options": ["A) Chief Justice of India", "B) Prime Minister", "C) President of India", "D) Parliament"],
        "answer": "C) President of India"
    }
]

# --- Civic Insights Facts ---
CIVIC_FACTS = [
    "Did You Know? India is the world's largest democracy by voter population.",
    "Did You Know? The Election Commission of India is an autonomous constitutional authority.",
    "Did You Know? The minimum voting age in India was reduced from 21 to 18 in 1989.",
    "Did You Know? EVMs (Electronic Voting Machines) were first used in a general election in 2004.",
    "Did You Know? 'NOTA' (None Of The Above) option was introduced in Indian elections in 2013.",
    "Did You Know? Voter turnout in Indian general elections often exceeds 60%.",
    "Did You Know? The Model Code of Conduct ensures free and fair elections.",
    "Did You Know? India's first general election was held in 1951-52.",
    "Did You Know? The longest election in Indian history lasted for over three months.",
    "Did You Know? Every vote counts in shaping the future of the nation!",
]

# --- Indian Slogans ---
INDIAN_SLOGANS = [
    "Jai Hind! 🇮🇳",
    "Satyameva Jayate! (Truth Alone Triumphs) 🌟",
    "Mera Bharat Mahan! (My India is Great!) 💪",
    "Unity in Diversity! 🤝",
    "Vote for India! 🗳️",
    "Desh Ke Liye Vote Karein! (Vote for the Nation!) ❤️",
    "Digital India, Empowering India! 💻",
    "Future of India, In Your Hands! ✨",
    "Your Vote, Your Voice! 🗣️",
    "Proud to be Indian! 🧡🤍💚",
]

# --- Thought for the Day ---
THOUGHTS_FOR_THE_DAY = [
    "The future of a nation is shaped by its citizens' active participation.",
    "Democracy is not merely a form of government; it is a way of life.",
    "Your vote is your voice; let it be heard loud and clear.",
    "In a democracy, the people get the government they deserve.",
    "Freedom is never more than one generation away from extinction. We don't pass it to our children in the bloodstream. It. must be fought for, protected, and handed on for them to do the same."
]


class SplashScreen(tk.Toplevel):
    """
    A splash screen displayed at the application start.
    It features a stylized app logo, a welcome message, and a "Digital India" theme.
    """
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.title("Vote-Xpress")
        self.geometry("800x500") # Increased size for a more prominent splash
        self.config(bg="white")
        self.overrideredirect(True) # Remove window decorations for a cleaner splash screen

        # Center the splash screen on the entire screen
        self.update_idletasks() # Update window to get accurate dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.winfo_width() // 2)
        y = (screen_height // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

        # Create a canvas for the circular logo and Digital India text
        self.splash_canvas = tk.Canvas(self, width=800, height=500, bg="white", highlightthickness=0)
        self.splash_canvas.pack(fill="both", expand=True)

        # Digital India logo (stylized text) in the top-right corner
        self.splash_canvas.create_text(780, 20, text="Digital India", anchor="ne",
                                       font=("Arial", 16, "bold"), fill=COLOR_PALETTE["accent_orange"])
        self.splash_canvas.create_text(780, 45, text="Power To Empower", anchor="ne",
                                       font=("Arial", 12, "italic"), fill=COLOR_PALETTE["accent_green"])

        # Vote-Xpress logo in a circle (clickable)
        center_x, center_y = 400, 250
        radius = 100
        self.logo_circle = self.splash_canvas.create_oval(center_x - radius, center_y - radius,
                                                          center_x + radius, center_y + radius,
                                                          fill=COLOR_PALETTE["primary_blue"], outline=COLOR_PALETTE["primary_blue"], width=2)

        self.logo_text1 = self.splash_canvas.create_text(center_x, center_y - 30, text="Vote-X",
                                                         font=FONT_STYLES["splash_title"], fill=COLOR_PALETTE["light_text"])
        self.logo_text2 = self.splash_canvas.create_text(center_x, center_y + 20, text="VOTING SYSTEM",
                                                         font=FONT_STYLES["splash_subtitle"], fill=COLOR_PALETTE["light_text"])

        # Welcome message
        self.welcome_text = self.splash_canvas.create_text(center_x, center_y + 130, text="Welcome to Vote-Xpress!",
                                                           font=FONT_STYLES["splash_welcome"], fill=COLOR_PALETTE["dark_text"])

        # Launching text with animation
        self.launching_text_id = self.splash_canvas.create_text(center_x, 450, text="Launching Application...",
                                                                 font=FONT_STYLES["small_label"], fill="gray")
        self.launching_text_alpha = 255 # For fading effect
        self._animate_launching_text()

        # Click to Enter message
        self.click_to_enter_text = self.splash_canvas.create_text(center_x, 470, text="Click anywhere to enter",
                                                                  font=FONT_STYLES["small_label"], fill="gray", state="hidden")
        self.after(2000, lambda: self.splash_canvas.itemconfig(self.click_to_enter_text, state="normal"))


        # Clickable area for the logo (covers the whole splash screen for easier click)
        self.splash_canvas.bind("<Button-1>", self.launch)

        # Auto-launch after 5 seconds if not clicked
        self.auto_launch_id = self.after(5000, self.launch)

    def _animate_launching_text(self):
        """Animates the 'Launching Application...' text by fading it."""
        if not self.winfo_exists(): return

        current_color = self.splash_canvas.itemcget(self.launching_text_id, "fill")
        if current_color == "gray": # Initial state, start fading
            self.launching_text_alpha = 255
        
        # Fade out
        self.launching_text_alpha -= 10
        if self.launching_text_alpha < 0:
            self.launching_text_alpha = 255 # Reset for next cycle
        
        # Convert alpha to hex for Tkinter color
        alpha_hex = f"{self.launching_text_alpha:02x}"
        new_color = f"#808080{alpha_hex}" # Gray with alpha (Tkinter doesn't support alpha directly in hex, this is a workaround)
        
        # A simpler pulsing effect
        if self.launching_text_alpha % 50 < 25:
            self.splash_canvas.itemconfig(self.launching_text_id, fill="gray")
        else:
            self.splash_canvas.itemconfig(self.launching_text_id, fill="darkgray")

        self.after(100, self._animate_launching_text)


    def launch(self, event=None):
        """Destroys the splash screen and shows the main application."""
        if self.auto_launch_id:
            self.after_cancel(self.auto_launch_id) # Cancel auto-launch if clicked
        self.destroy()
        self.root.deiconify() # Show the main root window
        VoteApp(self.root)

class FinalResultsWindow(tk.Toplevel):
    """
    A separate window to display final voting results with celebration animation.
    """
    def __init__(self, master, winner, runner_up, all_votes):
        super().__init__(master)
        self.title("🎉 Final Voting Results 🎉")
        self.geometry("800x600")
        self.config(bg=COLOR_PALETTE["light_bg"])
        self.transient(master)
        self.grab_set()

        self.winner = winner
        self.runner_up = runner_up
        self.all_votes = all_votes

        self.canvas = tk.Canvas(self, bg=COLOR_PALETTE["light_bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self._draw_gradient_background()
        self.canvas.bind("<Configure>", lambda event: self._draw_gradient_background())

        self.canvas.create_text(self.winfo_width()/2, 50, text="🌟 Official Results Declared! 🌟",
                                font=FONT_STYLES["header1"], fill=COLOR_PALETTE["primary_blue"], anchor="n")

        self.canvas.create_text(self.winfo_width()/2, 120, text=f"🏆 Winner: {self.winner[0]} with {self.winner[1]} votes!",
                                font=FONT_STYLES["header2"], fill=COLOR_PALETTE["accent_green"], anchor="n")

        if self.runner_up:
            self.canvas.create_text(self.winfo_width()/2, 180, text=f"🥈 Runner-up: {self.runner_up[0]} with {self.runner_up[1]} votes!",
                                    font=FONT_STYLES["header3"], fill=COLOR_PALETTE["accent_orange"], anchor="n")
        else:
             self.canvas.create_text(self.winfo_width()/2, 180, text="No clear runner-up or insufficient votes.",
                                    font=FONT_STYLES["subheader"], fill="gray", anchor="n")

        y_offset = 250
        self.canvas.create_text(self.winfo_width()/2, y_offset - 20, text="Detailed Vote Counts:",
                                font=FONT_STYLES["subheader"], fill=COLOR_PALETTE["dark_text"], anchor="n")
        for i, (cand, count) in enumerate(self.all_votes):
            self.canvas.create_text(self.winfo_width()/2, y_offset + i * 30, text=f"{cand}: {count} votes",
                                    font=FONT_STYLES["label"], fill=COLOR_PALETTE["dark_text"], anchor="n")

        tk.Button(self, text="Close Results", command=self.destroy,
                  bg=COLOR_PALETTE["accent_red"], fg=COLOR_PALETTE["light_text"], font=FONT_STYLES["button"], relief="raised", bd=3).pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.after(100, self._start_celebration)

    def _draw_gradient_background(self):
        """Draws a subtle gradient background on the canvas."""
        self.canvas.delete("gradient")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 1 or height <= 1:
            return

        color1_rgb = (240, 248, 255)  # #f0f8ff
        color2_rgb = (224, 255, 255)  # #e0ffff

        for i in range(height):
            r = int(color1_rgb[0] + (color2_rgb[0] - color1_rgb[0]) * i / height)
            g = int(color1_rgb[1] + (color2_rgb[1] - color1_rgb[1]) * i / height)
            b = int(color1_rgb[2] + (color2_rgb[2] - color1_rgb[2]) * i / height)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=color, tags="gradient")
        self.canvas.tag_lower("gradient")

    def _start_celebration(self):
        """Starts the continuous celebration animation."""
        self._animate_fireworks()
        self._animate_confetti()

    def _animate_fireworks(self, count=0):
        """Creates and animates firework bursts."""
        if self.winfo_exists():
            for _ in range(random.randint(1, 3)):
                start_x = random.randint(50, self.winfo_width() - 50)
                start_y = self.winfo_height() - random.randint(50, 150)
                colors = ["red", "orange", "yellow", "lime", "cyan", "magenta", "white"]
                num_particles = random.randint(10, 25)
                
                particles = []
                for _ in range(num_particles):
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(2, 6)
                    dx = speed * math.cos(angle)
                    dy = speed * math.sin(angle)
                    size = random.randint(3, 7)
                    color = random.choice(colors)
                    
                    particle_id = self.canvas.create_oval(start_x - size, start_y - size,
                                                          start_x + size, start_x + size,
                                                          fill=color, outline=color)
                    particles.append({"id": particle_id, "dx": dx, "dy": dy, "fade": 255})
                
                self._update_firework_particles(particles)
            self.after(random.randint(800, 1500), self._animate_fireworks)

    def _update_firework_particles(self, particles):
        """Updates positions and fades firework particles."""
        if not self.winfo_exists(): return

        active_particles = []
        for p in particles:
            if p["fade"] > 0:
                self.canvas.move(p["id"], p["dx"], p["dy"])
                p["dy"] += 0.2 # Gravity effect
                p["fade"] -= 10
                
                active_particles.append(p)
            else:
                self.canvas.delete(p["id"])

        if active_particles:
            self.after(30, lambda: self._update_firework_particles(active_particles))

    def _animate_confetti(self, count=0):
        """Creates and animates falling confetti."""
        if self.winfo_exists():
            for _ in range(random.randint(5, 15)):
                x = random.randint(0, self.winfo_width())
                y = random.randint(-50, 0)
                colors = ["#FFD700", "#FF69B4", "#8A2BE2", "#00CED1", "#FF4500", "#32CD32"]
                emoji = random.choice(["🎉", "🎊", "✨", "💫"])
                
                confetti_id = self.canvas.create_text(x, y, text=emoji, font=("Arial", random.randint(12, 20)), fill=random.choice(colors))
                self._update_confetti_position(confetti_id, y)

            self.after(random.randint(300, 700), self._animate_confetti)

    def _update_confetti_position(self, confetti_id, y_pos):
        """Updates confetti position and removes it when off-screen."""
        if not self.winfo_exists() or not self.canvas.find_withtag(confetti_id): return

        self.canvas.move(confetti_id, 0, 5)
        y_pos += 5
        
        if y_pos < self.winfo_height() + 20:
            self.after(50, lambda: self._update_confetti_position(confetti_id, y_pos))
        else:
            self.canvas.delete(confetti_id)

class VoteApp:
    """
    The main application class for the Vote-Xpress Dashboard.
    Manages UI, navigation, and voting logic.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Vote-Xpress Dashboard")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # User quiz data (session-based)
        self.user_quiz_badge = None
        self.user_quiz_stars = 0

        # Quiz related instance variables - INITIALIZED HERE
        self.quiz_selected_option = tk.StringVar(self.root) # Initialize StringVar for radio buttons
        self.quiz_score = 0
        self.current_question_index = 0
        self.quiz_questions_shuffled = []
        self.quiz_timer_id = None # To store the after ID for the quiz timer
        self.time_left = 10 # Default time for each question
        self.current_quiz_auto_advance_id = None # Initialize auto-advance ID

        # Store references to candidate vote labels for dynamic updates
        self.candidate_vote_labels = {}
        self.current_fact_index = 0 # Initialize for civic facts
        self.current_slogan_index = 0 # Initialize for slogans
        self.current_thought_index = 0 # Initialize for thoughts of the day

        # References to side panels for dynamic show/hide
        self.left_panel_frame = None
        self.right_panel_frame = None

        self.main_frame = tk.Frame(self.root, bg=COLOR_PALETTE["light_bg"])
        self.main_frame.pack(fill="both", expand=True)

        self.gradient_canvas = None
        self.root.update_idletasks()
        self.gradient_bg()

        self.top_bar_frame = tk.Frame(self.main_frame, bg=COLOR_PALETTE["light_bg"], bd=2, relief="groove")
        self.top_bar_frame.pack(side="top", fill="x", padx=10, pady=10)

        # Replaced vote meter with slogan label
        self.slogan_label = tk.Label(self.top_bar_frame, font=FONT_STYLES["small_label"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["primary_blue"])
        self.slogan_label.pack(side="left", padx=10)

        self.timer_label = tk.Label(self.top_bar_frame, font=FONT_STYLES["small_label"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["accent_red"])
        self.timer_label.pack(side="right", padx=10)

        # News button in the top bar
        self.news_button = tk.Button(self.top_bar_frame, text="📰 News", command=self.show_live_news,
                                     bg=COLOR_PALETTE["news_button"], fg=COLOR_PALETTE["dark_text"],
                                     font=FONT_STYLES["small_label"], relief="raised", bd=3,
                                     width=8, height=1, borderwidth=0, highlightthickness=0,
                                     cursor="hand2", # Change cursor on hover
                                     overrelief="flat", # Make it flat on hover
                                     activebackground=COLOR_PALETTE["news_button"], activeforeground=COLOR_PALETTE["dark_text"])
        self.news_button.pack(side="right", padx=10)
        # Make the button circular-like (requires some canvas trickery or image, but can simulate with padding)
        self.news_button.config(padx=5, pady=5) # Add padding to make it squarer for text, then adjust geometry

        # Chat frame first, packed to bottom
        self.chat_frame = tk.LabelFrame(self.main_frame, text="🤖 Chat with Vote-Xpress Assistant",
                                        font=FONT_STYLES["chat_font"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["accent_green"], bd=2, relief="solid")
        self.chat_frame.pack(side="bottom", fill="x", padx=20, pady=10) # Pack chat frame at the bottom

        self.chatbot_text_frame = tk.Frame(self.chat_frame, bg=COLOR_PALETTE["mid_bg"])
        self.chatbot_text_frame.pack(pady=5, padx=5, fill="both", expand=True)

        self.chatbot_box = tk.Text(self.chatbot_text_frame, width=70, height=5, font=FONT_STYLES["chat_font"], wrap="word", state="disabled",
                                   bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"], bd=1, relief="sunken")
        self.chatbot_box.pack(side="left", fill="both", expand=True)

        self.chatbot_scrollbar = tk.Scrollbar(self.chatbot_text_frame, command=self.chatbot_box.yview)
        self.chatbot_scrollbar.pack(side="right", fill="y")
        self.chatbot_box.config(yscrollcommand=self.chatbot_scrollbar.set)

        self.chatbot_box.config(state="normal")
        self.chatbot_box.insert("end", "🤖 Chatbot: Hi! How can I help you today?\n")
        self.chatbot_box.config(state="disabled")

        self.chat_entry = tk.Entry(self.chat_frame, font=FONT_STYLES["chat_font"], bd=1, relief="solid")
        self.chat_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.chat_entry.bind("<Return>", lambda event: self.chat_response())

        tk.Button(self.chat_frame, text="Send", command=self.chat_response,
                  bg=COLOR_PALETTE["accent_green"], fg=COLOR_PALETTE["light_text"], font=FONT_STYLES["chat_font"], relief="raised", bd=2).pack(side="right", padx=5, pady=5)

        # The content_frame will now hold the grid layout for main dashboard elements
        # It should fill the remaining space after top_bar and chat_frame are packed
        self.content_frame = tk.Frame(self.main_frame, bg=COLOR_PALETTE["light_bg"])
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10) 

        # Initialize central_content_frame as None, it will be created in main_menu
        self.central_content_frame = None

        # Start updating slogans
        self._update_slogan()
        self.start_time = time.time()
        self.update_timer()
        self.main_menu() # Call main_menu to set up the dashboard initially

    def on_closing(self):
        """Handles the window closing event to ensure graceful exit."""
        if messagebox.askokcancel("Quit", "Do you want to quit Vote-Xpress?"):
            self.root.destroy()

    def chat_response(self):
        """Processes user input for the chatbot and displays a response."""
        user_msg = self.chat_entry.get().strip()
        if not user_msg:
            return

        self.chatbot_box.config(state="normal")
        self.chatbot_box.insert("end", f"You: {user_msg}\n")
        self.chatbot_box.config(state="disabled")
        self.chat_entry.delete(0, tk.END)

        self.chatbot_box.config(state="normal")
        self.chatbot_box.insert("end", "🤖 Chatbot: Thinking...\n")
        self.chatbot_box.see("end")
        self.chatbot_box.config(state="disabled")
        self.chat_entry.config(state="disabled")

        # Start a new thread for AI response to prevent UI freeze
        threading.Thread(target=self._get_ai_response_in_thread, args=(user_msg,)).start()

    def _get_ai_response_in_thread(self, user_msg):
        """Helper function to get AI response in a separate thread with retry logic."""
        ai_response = "I'm sorry, I couldn't generate a response."
        max_retries = 3
        initial_backoff = 1 # seconds

        for attempt in range(max_retries):
            try:
                chat_history = [{"role": "user", "parts": [{"text": user_msg}]}]
                payload = {"contents": chat_history}
                headers = {'Content-Type': 'application/json'}
                url_with_key = f"{API_URL}?key={API_KEY}"

                response = requests.post(url_with_key, headers=headers, data=json.dumps(payload), timeout=15) # Increased timeout
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                result = response.json()

                if result.get("candidates") and len(result["candidates"]) > 0 and \
                   result["candidates"][0].get("content") and \
                   result["candidates"][0]["content"].get("parts") and \
                   len(result["candidates"][0]["content"]["parts"]) > 0:
                    ai_response = result["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    ai_response = "The AI returned an empty or unexpected response structure."
                
                # If successful, break the retry loop
                break

            except requests.exceptions.Timeout:
                print(f"Chatbot API Request timed out on attempt {attempt + 1}.")
                ai_response = "The AI took too long to respond. Retrying..."
                if attempt < max_retries - 1:
                    time.sleep(initial_backoff * (2 ** attempt)) # Exponential backoff
                else:
                    ai_response = "The AI took too long to respond after multiple attempts. Please try again later."
            except requests.exceptions.HTTPError as http_err:
                print(f"Chatbot HTTP Error on attempt {attempt + 1}: {http_err}")
                if http_err.response.status_code == 503:
                    ai_response = "AI Service is temporarily unavailable. Retrying..."
                    if attempt < max_retries - 1:
                        time.sleep(initial_backoff * (2 ** attempt))
                    else:
                        ai_response = "AI Service is currently unavailable after multiple attempts. Please try again later."
                else:
                    ai_response = f"AI API request failed: {http_err}. Please check your API key or network."
                    break # Don't retry for non-503 HTTP errors
            except json.JSONDecodeError:
                print(f"Chatbot API response was not valid JSON on attempt {attempt + 1}.")
                ai_response = "Received an unreadable response from the AI. Retrying..."
                if attempt < max_retries - 1:
                    time.sleep(initial_backoff * (2 ** attempt))
                else:
                    ai_response = "Received an unreadable response after multiple attempts. Please try again."
            except Exception as e:
                print(f"An unexpected error occurred in chatbot on attempt {attempt + 1}: {e}")
                ai_response = f"An unexpected error occurred: {e}. Please try again."
                break # Don't retry for general unexpected errors

        # Schedule UI update on the main thread
        self.root.after(0, self._display_ai_response, ai_response)

    def _display_ai_response(self, ai_response):
        """Updates the chatbot UI with the AI's response."""
        self.chatbot_box.config(state="normal")
        
        # Check if the last message was "Thinking..." and remove it before adding the new response
        current_text_lines = self.chatbot_box.get("1.0", tk.END).strip().split('\n')
        if current_text_lines and current_text_lines[-1].strip() == "🤖 Chatbot: Thinking...":
            # Delete the last line (and its newline)
            self.chatbot_box.delete("end-2c linestart", "end-1c") 
            self.chatbot_box.insert("end", f"🤖 Chatbot: {ai_response}\n") # Insert new response
        else:
            self.chatbot_box.insert("end", f"🤖 Chatbot: {ai_response}\n")

        self.chatbot_box.see("end") # Scroll to the end
        self.chatbot_box.config(state="disabled")

        # Re-enable input only if it's a final response, not a "Retrying..." message
        if not ("Retrying..." in ai_response or "Thinking..." in ai_response):
            self.chat_entry.config(state="normal")
            self.chat_entry.focus_set()

    def _update_slogan(self):
        """Updates the displayed Indian slogan."""
        if self.slogan_label.winfo_exists():
            slogan = INDIAN_SLOGANS[self.current_slogan_index]
            self.slogan_label.config(text=slogan)
            self.current_slogan_index = (self.current_slogan_index + 1) % len(INDIAN_SLOGANS)
            self.root.after(5000, self._update_slogan) # Change slogan every 5 seconds

    def update_timer(self):
        """Starts and updates the countdown timer for voting."""
        self.countdown()

    def countdown(self):
        """Decrements the timer and updates the display."""
        try:
            elapsed = time.time() - self.start_time
            remaining = max(0, 600 - int(elapsed)) # 10 minutes (600 seconds)
            mins, secs = divmod(remaining, 60)
            self.timer_label.config(text=f"⏳ Voting Time Left: {mins:02}:{secs:02}")
            if remaining > 0:
                self.root.after(1000, self.countdown)
            else:
                self.timer_label.config(text="⚠️ Voting time expired!")
        except tk.TclError:
            pass

    def clear_central_content_frame(self):
        """Clears all widgets from the central content frame."""
        if self.central_content_frame:
            for widget in self.central_content_frame.winfo_children():
                widget.destroy()
            self.central_content_frame.destroy()
            self.central_content_frame = None

    def _draw_flag_on_canvas(self, canvas, current_width, current_height):
        """Helper function to draw the Indian flag on a given canvas."""
        canvas.delete("all")

        saffron_height = current_height // 3
        for i in range(saffron_height):
            r = 255
            g = int(153 - (i / saffron_height) * 153)
            b = 51
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, current_width, i, fill=color)

        white_start = saffron_height
        white_end = 2 * saffron_height
        canvas.create_rectangle(0, white_start, current_width, white_end, fill="#FFFFFF", outline="")

        green_start = white_end
        for i in range(current_height - green_start):
            color = f"#138808"
            canvas.create_line(0, green_start + i, current_width, green_start + i, fill=color)

        chakra_radius = min(current_width, current_height) // 15
        chakra_center_x = current_width // 2
        chakra_center_y = current_height // 2
        canvas.create_oval(chakra_center_x - chakra_radius, chakra_center_y - chakra_radius,
                                         chakra_center_x + chakra_radius, chakra_center_y + chakra_radius,
                                         outline="#000080", fill="#000080", width=2)

        for i in range(24):
            angle = i * (360 / 24)
            x1 = chakra_center_x + chakra_radius * 0.2 * math.cos(math.radians(angle))
            y1 = chakra_center_y + chakra_radius * 0.2 * math.sin(math.radians(angle))
            x2 = chakra_center_x + chakra_radius * math.cos(math.radians(angle))
            y2 = chakra_center_y + chakra_radius * math.sin(math.radians(angle))
            canvas.create_line(x1, y1, x2, y2, fill="white", width=1)

    def gradient_bg(self):
        """Creates a gradient background mimicking the Indian flag colors."""
        if self.gradient_canvas:
            self.gradient_canvas.destroy()

        self.gradient_canvas = tk.Canvas(self.main_frame, highlightthickness=0)
        self.gradient_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.gradient_canvas.lower('all')

        current_width = self.main_frame.winfo_width()
        current_height = self.main_frame.winfo_height()

        self._draw_flag_on_canvas(self.gradient_canvas, current_width, current_height)
        self.gradient_canvas.bind("<Configure>", lambda event: self._draw_flag_on_canvas(self.gradient_canvas, event.width, event.height))

    def main_menu(self):
        """Displays the main menu of the application."""
        self.clear_central_content_frame() # Clear any previous page content

        # Ensure the grid configuration for content_frame is set up for 3 columns
        self.content_frame.grid_forget() # Clear previous grid if any
        self.content_frame.grid_columnconfigure(0, weight=1, uniform="group1") # Left panel
        self.content_frame.grid_columnconfigure(1, weight=2, uniform="group1") # Center menu
        self.content_frame.grid_columnconfigure(2, weight=1, uniform="group1") # Right panel
        self.content_frame.grid_rowconfigure(0, weight=0) # Row for welcome label
        self.content_frame.grid_rowconfigure(1, weight=1) # Row for panels and menu

        welcome_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        welcome_frame.grid(row=0, column=0, columnspan=3, pady=20, sticky="ew") # Span 3 columns

        welcome_label_text = "Vote-Xpress Dashboard"
        if self.user_quiz_stars > 0:
            welcome_label_text += " " + "⭐" * self.user_quiz_stars
        
        tk.Label(welcome_frame, text=welcome_label_text, font=FONT_STYLES["header2"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["primary_blue"]).pack()

        # --- Left Panel: Civic Insights ---
        self.left_panel_frame = tk.LabelFrame(self.content_frame, text="💡 Civic Insights",
                                         font=FONT_STYLES["panel_header"], bg=COLOR_PALETTE["panel_bg"],
                                         fg=COLOR_PALETTE["primary_blue"], bd=2, relief="solid", padx=10, pady=10)
        self.left_panel_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.civic_fact_label = tk.Label(self.left_panel_frame, text="", font=FONT_STYLES["panel_text"],
                                         bg=COLOR_PALETTE["panel_bg"], fg=COLOR_PALETTE["dark_text"],
                                         wraplength=200, justify="left")
        self.civic_fact_label.pack(pady=10, fill="both", expand=True)
        self._update_civic_fact()


        # --- Central Content Frame (for menu buttons or other pages) ---
        self.central_content_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["mid_bg"], bd=3, relief="raised")
        self.central_content_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Configure grid for central content frame to allow buttons to be centered
        self.central_content_frame.grid_columnconfigure(0, weight=1) # Left padding column
        self.central_content_frame.grid_columnconfigure(1, weight=0) # Column for buttons (takes minimal space)
        self.central_content_frame.grid_columnconfigure(2, weight=1) # Right padding column

        menu_items = [
            ("📝 Register to Vote", self.register),
            ("🗳️ Cast Your Vote", self.vote),
            ("📊 View Live Results", self.view_results),
            ("👤 Meet Our Candidates", self.candidates),
            ("🧠 VoteSmart Quiz Challenge", self.start_quiz_challenge),
            ("💬 Submit Feedback", self.feedback_form),
            ("👨‍💻 Developer Info", self.developer_info),
            ("🔐 Admin Panel", self.admin_panel),
            ("📞 Help & Support", self.helpdesk),
        ]

        # Arrange buttons in a single column within the central column (column 1)
        row_idx = 0
        for text, command in menu_items:
            tk.Button(self.central_content_frame, text=text, font=FONT_STYLES["button"], width=25, height=2,
                      bg=COLOR_PALETTE["button_blue"], fg=COLOR_PALETTE["light_text"],
                      activebackground=COLOR_PALETTE["primary_blue"], activeforeground=COLOR_PALETTE["light_text"],
                      relief="raised", bd=3, command=command).grid(row=row_idx, column=1, pady=8, padx=5, sticky="ew") # Placed in column 1
            
            # Ensure the row expands
            self.central_content_frame.grid_rowconfigure(row_idx, weight=1)
            row_idx += 1 
        
        # Ensure all rows expand vertically
        for r in range(row_idx):
            self.central_content_frame.grid_rowconfigure(r, weight=1)


        # --- Right Panel: Live Information ---
        self.right_panel_frame = tk.LabelFrame(self.content_frame, text="⏰ Live Info",
                                          font=FONT_STYLES["panel_header"], bg=COLOR_PALETTE["panel_bg"],
                                          fg=COLOR_PALETTE["primary_blue"], bd=2, relief="solid", padx=10, pady=10)
        self.right_panel_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        self.date_time_label = tk.Label(self.right_panel_frame, text="", font=FONT_STYLES["panel_text"],
                                        bg=COLOR_PALETTE["panel_bg"], fg=COLOR_PALETTE["dark_text"],
                                        wraplength=200, justify="left")
        self.date_time_label.pack(pady=5, fill="x")

        # Add total votes label
        self.total_votes_label = tk.Label(self.right_panel_frame, text="", font=FONT_STYLES["panel_total_votes"],
                                          bg=COLOR_PALETTE["panel_bg"], fg=COLOR_PALETTE["primary_blue"])
        self.total_votes_label.pack(pady=(5, 10), fill="x")


        # Add labels for candidate vote counts
        tk.Label(self.right_panel_frame, text="Live Vote Counts:", font=FONT_STYLES["panel_text"],
                 bg=COLOR_PALETTE["panel_bg"], fg=COLOR_PALETTE["dark_text"]).pack(pady=(10, 5), fill="x")
        
        # Clear existing labels before recreating them
        self.candidate_vote_labels = {}
        for candidate in votes:
            label = tk.Label(self.right_panel_frame, text=f"{candidate}: {votes[candidate]}",
                             font=FONT_STYLES["panel_vote_count"], bg=COLOR_PALETTE["panel_bg"], fg=COLOR_PALETTE["dark_text"],
                             anchor="w") # Align text to the left
            label.pack(pady=2, fill="x", padx=5)
            self.candidate_vote_labels[candidate] = label
        
        # Add Thought for the Day
        tk.Label(self.right_panel_frame, text="Thought for the Day:", font=FONT_STYLES["panel_text"],
                 bg=COLOR_PALETTE["panel_bg"], fg=COLOR_PALETTE["dark_text"]).pack(pady=(15, 5), fill="x")
        self.thought_for_day_label = tk.Label(self.right_panel_frame, text="", font=FONT_STYLES["thought_for_day"],
                                               bg=COLOR_PALETTE["panel_bg"], fg=COLOR_PALETTE["dark_text"],
                                               wraplength=200, justify="center")
        self.thought_for_day_label.pack(pady=5, fill="x", expand=True)

        self._update_live_info() # Start the combined update function
        self._update_thought_for_day() # Start thought for the day updates


    def _update_civic_fact(self):
        """Updates the displayed civic fact on the left panel."""
        # Check if the label exists before updating to prevent errors when panel is destroyed
        if self.civic_fact_label.winfo_exists():
            fact = CIVIC_FACTS[self.current_fact_index]
            self.civic_fact_label.config(text=fact)
            self.current_fact_index = (self.current_fact_index + 1) % len(CIVIC_FACTS)
            self.root.after(7000, self._update_civic_fact) # Change fact every 7 seconds

    def _update_thought_for_day(self):
        """Updates the displayed thought for the day on the right panel."""
        if self.thought_for_day_label.winfo_exists():
            thought = THOUGHTS_FOR_THE_DAY[self.current_thought_index]
            self.thought_for_day_label.config(text=f"“{thought}”")
            self.current_thought_index = (self.current_thought_index + 1) % len(THOUGHTS_FOR_THE_DAY)
            self.root.after(10000, self._update_thought_for_day) # Change thought every 10 seconds

    def _update_live_info(self):
        """Updates the displayed date/time and candidate vote counts on the right panel."""
        # Check if the label exists before updating to prevent errors when panel is destroyed
        if self.date_time_label.winfo_exists():
            # Update date and time
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S %p")
            current_date = now.strftime("%A, %d %B %Y")
            self.date_time_label.config(text=f"Time: {current_time}\nDate: {current_date}")

            # Update total votes
            total = sum(votes.values())
            self.total_votes_label.config(text=f"Total Votes: {total}")

            # Update candidate vote counts
            for candidate, count in votes.items():
                if candidate in self.candidate_vote_labels and self.candidate_vote_labels[candidate].winfo_exists():
                    self.candidate_vote_labels[candidate].config(text=f"{candidate}: {count}")

            self.root.after(1000, self._update_live_info) # Update every second

    def _prepare_full_page_view(self):
        """Prepares the content_frame for a full-page tab view."""
        # Destroy side panels if they exist
        if self.left_panel_frame:
            self.left_panel_frame.destroy()
            self.left_panel_frame = None
        if self.right_panel_frame:
            self.right_panel_frame.destroy()
            self.right_panel_frame = None
        
        # Clear any welcome frame content from row 0
        for widget in self.content_frame.grid_slaves(row=0):
            widget.destroy()

        # Reconfigure content_frame to have only one main column (column 0) that spans the entire width
        self.content_frame.grid_columnconfigure(0, weight=1, uniform="") # Make column 0 expandable
        self.content_frame.grid_columnconfigure(1, weight=0, uniform="") # Collapse column 1
        self.content_frame.grid_columnconfigure(2, weight=0, uniform="") # Collapse column 2
        self.content_frame.grid_rowconfigure(0, weight=0) # Ensure row 0 is not expanding if welcome frame is gone
        self.content_frame.grid_rowconfigure(1, weight=1) # Ensure row 1 is expanding

        self.clear_central_content_frame() # Clear any previous central content

    def _add_back_to_main_menu_button(self, parent_frame):
        """Helper function to add a consistent 'Back to Main Menu' button at the top of a specific frame."""
        back_button_frame = tk.Frame(parent_frame, bg=COLOR_PALETTE["light_bg"])
        back_button_frame.pack(side="top", fill="x", padx=10, pady=5, anchor="nw") 

        tk.Button(back_button_frame, text="⬅️ Back", command=self.main_menu,
                  bg=COLOR_PALETTE["button_back"], fg=COLOR_PALETTE["light_text"], font=FONT_STYLES["small_label"],
                  relief="raised", bd=2, padx=10, pady=5).pack(anchor="w")

    def _create_scrollable_frame(self, parent_frame):
        """
        Creates a scrollable frame within the given parent_frame.
        Returns the inner frame where content should be placed.
        """
        canvas = tk.Canvas(parent_frame, bg=COLOR_PALETTE["light_bg"], highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_content_frame = tk.Frame(canvas, bg=COLOR_PALETTE["light_bg"])
        
        # Create the window on the canvas. Store its ID.
        window_id = canvas.create_window((0, 0), window=scrollable_content_frame, anchor="nw")

        def _on_canvas_configure(event):
            # When the canvas resizes, update the width of the window item
            canvas.itemconfig(window_id, width=event.width)
            # Also update the scrollregion to encompass the content frame
            canvas.configure(scrollregion=canvas.bbox("all"))

        # Bind the canvas configure event to resize the inner window
        canvas.bind("<Configure>", _on_canvas_configure)

        # Also bind the inner frame's configure to update scrollregion
        # This is important if content inside the scrollable_content_frame changes size
        scrollable_content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        return scrollable_content_frame

    def register(self):
        """Displays the voter registration form."""
        self._prepare_full_page_view()
        
        register_container_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        register_container_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.central_content_frame = register_container_frame

        self._add_back_to_main_menu_button(register_container_frame)
        
        register_frame = self._create_scrollable_frame(register_container_frame)
        
        # Configure register_frame for centering its content
        register_frame.grid_columnconfigure(0, weight=1) # Left padding
        register_frame.grid_columnconfigure(1, weight=0) # Content column
        register_frame.grid_columnconfigure(2, weight=1) # Right padding

        tk.Label(register_frame, text="Voter Registration", font=FONT_STYLES["header3"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["accent_green"]).grid(row=0, column=1, pady=20)

        input_frame = tk.Frame(register_frame, bg=COLOR_PALETTE["mid_bg"], padx=20, pady=10, bd=2, relief="groove")
        input_frame.grid(row=1, column=1, pady=10, sticky="ew") # Add sticky="ew"

        tk.Label(input_frame, text="Full Name:", font=FONT_STYLES["label"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"]).grid(row=0, column=0, sticky="w", pady=5, padx=5)
        name_entry = tk.Entry(input_frame, font=FONT_STYLES["entry"], width=30, bd=2, relief="sunken")
        name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(input_frame, text="Voter ID:", font=FONT_STYLES["label"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"]).grid(row=1, column=0, sticky="w", pady=5, padx=5)
        voter_id_entry = tk.Entry(input_frame, font=FONT_STYLES["entry"], width=30, bd=2, relief="sunken")
        voter_id_entry.grid(row=1, column=1, pady=5, padx=5)

        def submit():
            name = name_entry.get().strip()
            voter_id = voter_id_entry.get().strip()
            if name and voter_id:
                name_entry.delete(0, tk.END)
                voter_id_entry.delete(0, tk.END)

                self.display_registration_receipt(name) # Call a new function to display receipt
            else:
                messagebox.showwarning("Input Error", "Please fill all fields to register.")

        tk.Button(register_frame, text="Submit Registration", command=submit,
                  bg=COLOR_PALETTE["button_blue"], fg=COLOR_PALETTE["light_text"], font=FONT_STYLES["button"], relief="raised", bd=3).grid(row=2, column=1, pady=15) # Place in central column

    def display_registration_receipt(self, name):
        """Displays a custom, designed registration receipt."""
        self._prepare_full_page_view()
        receipt_container_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        receipt_container_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.central_content_frame = receipt_container_frame
        self._add_back_to_main_menu_button(receipt_container_frame)
        
        receipt_display_frame = self._create_scrollable_frame(receipt_container_frame)
        
        # Configure receipt_display_frame for centering its content
        receipt_display_frame.grid_columnconfigure(0, weight=1) # Left padding
        receipt_display_frame.grid_columnconfigure(1, weight=0) # Content column
        receipt_display_frame.grid_columnconfigure(2, weight=1) # Right padding

        tk.Label(receipt_display_frame, text="🎉 Registration Successful! 🎉", font=FONT_STYLES["header2"], fg=COLOR_PALETTE["accent_green"], bg=COLOR_PALETTE["light_bg"]).grid(row=0, column=1, pady=30)
        tk.Label(receipt_display_frame, text=f"Thank you, {name}, for registering with Vote-Xpress!", font=FONT_STYLES["subheader"], fg=COLOR_PALETTE["dark_text"], bg=COLOR_PALETTE["light_bg"]).grid(row=1, column=1, pady=10)
        tk.Label(receipt_display_frame, text="Your commitment strengthens our democracy.", font=FONT_STYLES["label"], fg="gray", bg=COLOR_PALETTE["light_bg"]).grid(row=2, column=1, pady=5)
        tk.Label(receipt_display_frame, text="🇮🇳 Proud Indian Citizen 🇮🇳", font=FONT_STYLES["header3"], fg=COLOR_PALETTE["accent_orange"], bg=COLOR_PALETTE["light_bg"]).grid(row=3, column=1, pady=20)


    def vote(self):
        """Displays the voting interface."""
        self._prepare_full_page_view()
        vote_container_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        vote_container_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.central_content_frame = vote_container_frame

        self._add_back_to_main_menu_button(vote_container_frame)

        vote_frame = self._create_scrollable_frame(vote_container_frame)
        
        # Configure vote_frame for centering its content
        vote_frame.grid_columnconfigure(0, weight=1) # Left padding
        vote_frame.grid_columnconfigure(1, weight=0) # Content column
        vote_frame.grid_columnconfigure(2, weight=1) # Right padding

        tk.Label(vote_frame, text="Cast Your Vote", font=FONT_STYLES["header3"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["primary_blue"]).grid(row=0, column=1, pady=20)

        voter_details_frame = tk.LabelFrame(vote_frame, text="Voter Details",
                                            font=FONT_STYLES["small_label"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"], bd=2, relief="solid")
        voter_details_frame.grid(row=1, column=1, pady=10, padx=50, sticky="ew") # Place in central column, add sticky="ew"

        tk.Label(voter_details_frame, text="Full Name:", font=FONT_STYLES["label"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"]).grid(row=0, column=0, sticky="w", pady=5, padx=10)
        name_entry = tk.Entry(voter_details_frame, font=FONT_STYLES["entry"], width=35, bd=2, relief="sunken")
        name_entry.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(voter_details_frame, text="Voter ID:", font=FONT_STYLES["label"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"]).grid(row=1, column=0, sticky="w", pady=5, padx=10)
        voter_id_entry = tk.Entry(voter_details_frame, font=FONT_STYLES["entry"], width=35, bd=2, relief="sunken")
        voter_id_entry.grid(row=1, column=1, pady=5, padx=10)

        candidate_selection_frame = tk.LabelFrame(vote_frame, text="Select Your Candidate",
                                                   font=FONT_STYLES["small_label"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"], bd=2, relief="solid")
        candidate_selection_frame.grid(row=2, column=1, pady=20, padx=50, sticky="ew") # Place in central column, add sticky="ew"

        selected = tk.StringVar()
        for i, candidate in enumerate(votes):
            tk.Radiobutton(candidate_selection_frame, text=candidate, variable=selected, value=candidate,
                           bg=COLOR_PALETTE["mid_bg"], font=FONT_STYLES["label"], fg=COLOR_PALETTE["dark_text"], selectcolor=COLOR_PALETTE["button_blue"],
                           indicatoron=0, width=25, padx=20, pady=10, bd=2, relief="raised").pack(anchor="center", pady=5)

        def submit_vote():
            name = name_entry.get().strip()
            voter_id = voter_id_entry.get().strip()
            chosen_candidate = selected.get()
            key = (name, voter_id)

            if not name or not voter_id or not chosen_candidate:
                messagebox.showwarning("Error", "Please fill all voter details and select a candidate.")
                return

            if time.time() - self.start_time >= 600:
                messagebox.showerror("Voting Closed", "Voting time has expired. You cannot cast your vote now.")
                return

            if key in voted_users:
                messagebox.showwarning("Already Voted", "This Voter ID has already cast a vote.")
                return

            voted_users.add(key)
            votes[chosen_candidate] += 1

            self.display_vote_receipt(name, voter_id, chosen_candidate)

        tk.Button(vote_frame, text="Submit My Vote", command=submit_vote,
                  bg=COLOR_PALETTE["button_purple"], fg=COLOR_PALETTE["light_text"], font=FONT_STYLES["button"], relief="raised", bd=4, padx=20, pady=10).grid(row=3, column=1, pady=20) # Place in central column

    def display_vote_receipt(self, name, voter_id, candidate):
        """Displays a custom, designed vote receipt."""
        self._prepare_full_page_view()
        self.clear_central_content_frame()
        receipt_container_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        receipt_container_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.central_content_frame = receipt_container_frame

        self._add_back_to_main_menu_button(receipt_container_frame)

        receipt_frame = self._create_scrollable_frame(receipt_container_frame)
        
        # Configure receipt_frame for centering its content
        receipt_frame.grid_columnconfigure(0, weight=1) # Left padding
        receipt_frame.grid_columnconfigure(1, weight=0) # Content column
        receipt_frame.grid_columnconfigure(2, weight=1) # Right padding

        receipt_content_frame = tk.Frame(receipt_frame, bg=COLOR_PALETTE["light_bg"], bd=5, relief="ridge", padx=30, pady=30)
        receipt_content_frame.grid(row=0, column=1, pady=50, padx=50, sticky="nsew") # Place in central column, add sticky="nsew"

        tk.Label(receipt_content_frame, text="🗳️ Official Vote Receipt 🗳️", font=FONT_STYLES["header2"], fg=COLOR_PALETTE["primary_blue"], bg=COLOR_PALETTE["light_bg"]).pack(pady=15)
        tk.Label(receipt_content_frame, text="---------------------------------------------------", font=("Courier", 12), fg="gray", bg=COLOR_PALETTE["light_bg"]).pack()

        tk.Label(receipt_content_frame, text=f"Voter Name: {name}", font=FONT_STYLES["label"], fg=COLOR_PALETTE["dark_text"], bg=COLOR_PALETTE["light_bg"]).pack(anchor="w", padx=20, pady=5)
        tk.Label(receipt_content_frame, text=f"Voter ID: {voter_id}", font=FONT_STYLES["label"], fg=COLOR_PALETTE["dark_text"], bg=COLOR_PALETTE["light_bg"]).pack(anchor="w", padx=20, pady=5)
        tk.Label(receipt_content_frame, text=f"Candidate Voted For: {candidate}", font=FONT_STYLES["button"], fg=COLOR_PALETTE["accent_green"], bg=COLOR_PALETTE["light_bg"]).pack(anchor="w", padx=20, pady=5)

        tk.Label(receipt_content_frame, text="---------------------------------------------------", font=("Courier", 12), fg="gray", bg=COLOR_PALETTE["light_bg"]).pack()

        tk.Label(receipt_content_frame, text="Thank You for Your Valuable Vote!", font=FONT_STYLES["subheader"], fg=COLOR_PALETTE["accent_green"], bg=COLOR_PALETTE["light_bg"]).pack(pady=15)
        tk.Label(receipt_content_frame, text="Your participation strengthens our democracy.", font=FONT_STYLES["label"], fg="gray", bg=COLOR_PALETTE["light_bg"]).pack(pady=5)

        flag_canvas = tk.Canvas(receipt_content_frame, width=200, height=100, bg=COLOR_PALETTE["light_bg"], highlightthickness=0)
        flag_canvas.pack(pady=10)
        flag_canvas.create_rectangle(0, 0, 200, 33, fill="#FF9933", outline="")
        flag_canvas.create_rectangle(0, 33, 200, 67, fill="#FFFFFF", outline="")
        flag_canvas.create_rectangle(0, 67, 200, 100, fill="#138808", outline="")
        flag_canvas.create_oval(80, 40, 120, 60, outline="#000080", fill="#000080", width=1)
        flag_canvas.create_text(100, 50, text="☸", font=("Arial", 16), fill="white")

        tk.Label(receipt_content_frame, text="🇮🇳 Proud Indian Citizen 🇮🇳", font=FONT_STYLES["header3"], fg=COLOR_PALETTE["accent_orange"], bg=COLOR_PALETTE["light_bg"]).pack(pady=10)

    def view_results(self):
        """Displays the live voting results with an interactive bar chart."""
        self._prepare_full_page_view()
        self.clear_central_content_frame()
        results_main_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        results_main_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.central_content_frame = results_main_frame

        self._add_back_to_main_menu_button(results_main_frame)
        
        # Configure results_main_frame for centering its content
        results_main_frame.grid_columnconfigure(0, weight=1) # Left padding
        results_main_frame.grid_columnconfigure(1, weight=0) # Content column
        results_main_frame.grid_columnconfigure(2, weight=1) # Right padding

        tk.Label(results_main_frame, text="📊 Live Voting Results �", font=FONT_STYLES["header2"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["primary_blue"]).grid(row=0, column=1, pady=20)

        results_canvas_frame = tk.Frame(results_main_frame, bg=COLOR_PALETTE["mid_bg"], bd=2, relief="groove")
        results_canvas_frame.grid(row=1, column=1, pady=10, padx=50, sticky="nsew") # Place in central column, add sticky="nsew"

        self.results_canvas = tk.Canvas(results_canvas_frame, bg=COLOR_PALETTE["mid_bg"], highlightthickness=0)
        self.results_canvas.pack(fill="both", expand=True)
        self.results_canvas.bind("<Configure>", self._draw_results_chart)

        # Initial draw
        self.root.after(100, lambda: self._draw_results_chart(None)) # Small delay to ensure canvas is sized

    def _draw_results_chart(self, event):
        """Draws the bar chart for voting results on the canvas."""
        canvas = self.results_canvas
        canvas.delete("all")

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        total_votes = sum(votes.values())
        if total_votes == 0:
            canvas.create_text(canvas_width / 2, canvas_height / 2, text="No votes cast yet!",
                               font=FONT_STYLES["subheader"], fill="gray")
            return

        # Sort candidates by votes for display
        sorted_candidates = sorted(votes.items(), key=lambda item: item[1], reverse=True)

        bar_width = (canvas_width / len(sorted_candidates)) * 0.6 # Adjust width for spacing
        gap = (canvas_width / len(sorted_candidates)) * 0.2 # Space between bars
        max_votes = max(votes.values())
        
        # Define colors for bars
        bar_colors = [COLOR_PALETTE["primary_blue"], COLOR_PALETTE["accent_green"], COLOR_PALETTE["accent_orange"]]

        for i, (candidate, count) in enumerate(sorted_candidates):
            x0 = i * (bar_width + gap) + gap
            # Ensure bar height is proportional, but not zero if votes are zero
            bar_height = (count / max_votes) * (canvas_height * 0.7) if max_votes > 0 else 0
            y0 = canvas_height - bar_height - 50 # Base of the bar (offset from bottom)
            x1 = x0 + bar_width
            y1 = canvas_height - 50 # Ground level

            bar_color = bar_colors[i % len(bar_colors)] # Cycle through colors

            # Draw bar
            canvas.create_rectangle(x0, y0, x1, y1, fill=bar_color, outline=COLOR_PALETTE["dark_text"], width=1)

            # Add vote count text on top of the bar
            canvas.create_text(x0 + bar_width / 2, y0 - 10, text=str(count),
                               font=FONT_STYLES["small_label"], fill=COLOR_PALETTE["dark_text"])

            # Add candidate name below the bar
            canvas.create_text(x0 + bar_width / 2, canvas_height - 30, text=candidate,
                               font=FONT_STYLES["small_label"], fill=COLOR_PALETTE["dark_text"])

        # Highlight winner/runner-up below the chart
        winner_name = sorted_candidates[0][0]
        winner_votes = sorted_candidates[0][1]
        winner_text = f"🏆 Leader: {winner_name} ({winner_votes} votes)"
        canvas.create_text(canvas_width / 2, 20, text=winner_text,
                           font=FONT_STYLES["subheader"], fill=COLOR_PALETTE["accent_green"])
        
        if len(sorted_candidates) > 1:
            runner_up_name = sorted_candidates[1][0]
            runner_up_votes = sorted_candidates[1][1]
            runner_up_text = f"🥈 Runner-up: {runner_up_name} ({runner_up_votes} votes)"
            canvas.create_text(canvas_width / 2, 45, text=runner_up_text,
                               font=FONT_STYLES["small_label"], fill=COLOR_PALETTE["accent_orange"])


    def candidates(self):
        """Displays detailed information about each candidate."""
        self._prepare_full_page_view()
        self.clear_central_content_frame()
        candidates_container_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        candidates_container_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.central_content_frame = candidates_container_frame

        self._add_back_to_main_menu_button(candidates_container_frame)

        candidates_frame = self._create_scrollable_frame(candidates_container_frame)
        
        # Configure candidates_frame for centering its content
        candidates_frame.grid_columnconfigure(0, weight=1) # Left padding
        candidates_frame.grid_columnconfigure(1, weight=0) # Content column
        candidates_frame.grid_columnconfigure(2, weight=1) # Right padding

        tk.Label(candidates_frame, text="👤 Meet Our Candidates 👤", font=FONT_STYLES["header3"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["accent_green"]).grid(row=0, column=1, pady=20)

        details = {
            "Candidate A": {
                "email": "candA@votexpress.com",
                "address": "Office 1, Block C, National Capital, India",
                "slogan": "For a Brighter Future!"
            },
            "Candidate B": {
                "email": "candB@votexpress.com",
                "address": "Office 2, Sector 7, Major City, India",
                "slogan": "Progress Through Unity!"
            },
            "Candidate C": {
                "email": "candC@votexpress.com",
                "address": "Office 3, Cyber Hub, Tech City, India",
                "slogan": "Innovation for All!"
            }
        }

        row_idx = 1
        for cand, info in details.items():
            candidate_info_frame = tk.LabelFrame(candidates_frame, text=f"Candidate: {cand}",
                                            font=FONT_STYLES["subheader"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["primary_blue"], bd=3, relief="ridge")
            candidate_info_frame.grid(row=row_idx, column=1, pady=15, padx=50, sticky="ew") # Place in central column, add sticky="ew"
            row_idx += 1

            tk.Label(candidate_info_frame, text=f"📧 Email: {info['email']}", font=FONT_STYLES["label"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"]).pack(anchor="w", padx=20, pady=2)
            tk.Label(candidate_info_frame, text=f"🏢 Office: {info['address']}", font=FONT_STYLES["label"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"]).pack(anchor="w", padx=20, pady=2)
            tk.Label(candidate_info_frame, text=f"💬 Slogan: \"{info['slogan']}\"", font=FONT_STYLES["small_label"], bg=COLOR_PALETTE["mid_bg"], fg="gray").pack(anchor="w", padx=20, pady=5)

    def developer_info(self):
        """Displays information about the developers with a LinkedIn link."""
        self._prepare_full_page_view()
        self.clear_central_content_frame()
        developer_container_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        developer_container_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.central_content_frame = developer_container_frame

        self._add_back_to_main_menu_button(developer_container_frame)

        developer_frame = self._create_scrollable_frame(developer_container_frame)
        
        # Configure developer_frame for centering its content
        developer_frame.grid_columnconfigure(0, weight=1) # Left padding
        developer_frame.grid_columnconfigure(1, weight=0) # Content column
        developer_frame.grid_columnconfigure(2, weight=1) # Right padding

        tk.Label(developer_frame, text="👨‍💻 Developer Information 👩‍💻", font=FONT_STYLES["header3"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["primary_blue"]).grid(row=0, column=1, pady=20)

        tk.Label(developer_frame, text="Proudly Developed By:", font=FONT_STYLES["subheader"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["dark_text"]).grid(row=1, column=1, pady=10)

        tk.Label(developer_frame, text="✨ Aditya Raj ✨", font=("Arial", 22, "bold"), fg="#FF4500", bg=COLOR_PALETTE["light_bg"]).grid(row=2, column=1, pady=5)

        linkedin_button_frame = tk.Frame(developer_frame, bg="#0e76a8", bd=3, relief="raised")
        linkedin_button_frame.grid(row=4, column=1, pady=20) # Place in central column

        linkedin_canvas = tk.Canvas(linkedin_button_frame, width=250, height=50, bg="#0e76a8", highlightthickness=0)
        linkedin_canvas.pack()

        linkedin_canvas.create_rectangle(10, 10, 40, 40, fill="white", outline="white")
        linkedin_canvas.create_text(25, 25, text="in", font=("Arial", 20, "bold"), fill="#0e76a8")

        linkedin_canvas.create_text(150, 25, text="Aditya Raj's LinkedIn", font=FONT_STYLES["button"], fill="white")

        linkedin_canvas.bind("<Button-1>", lambda event: self.open_linkedin(linkedin_url_aditya))

    def helpdesk(self):
        """Displays helpdesk contact information."""
        self._prepare_full_page_view()
        self.clear_central_content_frame()
        help_container_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        help_container_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.central_content_frame = help_container_frame

        self._add_back_to_main_menu_button(help_container_frame)

        help_frame_main = self._create_scrollable_frame(help_container_frame)
        
        # Configure help_frame_main for centering its content
        help_frame_main.grid_columnconfigure(0, weight=1) # Left padding
        help_frame_main.grid_columnconfigure(1, weight=0) # Content column
        help_frame_main.grid_columnconfigure(2, weight=1) # Right padding

        tk.Label(help_frame_main, text="📞 Help & Support 📧", font=FONT_STYLES["header3"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["accent_red"]).grid(row=0, column=1, pady=20)

        help_content_frame = tk.Frame(help_frame_main, bg=COLOR_PALETTE["mid_bg"], bd=3, relief="groove", padx=20, pady=20)
        help_content_frame.grid(row=1, column=1, pady=20) # Place in central column

        tk.Label(help_content_frame, text="Need Assistance?", font=FONT_STYLES["subheader"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"]).pack(pady=5)
        tk.Label(help_content_frame, text=help_contact, font=FONT_STYLES["label"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["primary_blue"], justify="left").pack(pady=10)
        tk.Label(help_content_frame, text="Our team is here to help you with any queries regarding Vote-Xpress.", font=FONT_STYLES["small_label"], bg=COLOR_PALETTE["mid_bg"], fg="gray", wraplength=400).pack(pady=10)

    def feedback_form(self):
        """Displays a form for users to submit feedback."""
        self._prepare_full_page_view()
        self.clear_central_content_frame()
        feedback_container_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        feedback_container_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.central_content_frame = feedback_container_frame

        self._add_back_to_main_menu_button(feedback_container_frame)

        feedback_main_frame = self._create_scrollable_frame(feedback_container_frame)
        
        # Configure feedback_main_frame for centering its content
        feedback_main_frame.grid_columnconfigure(0, weight=1) # Left padding
        feedback_main_frame.grid_columnconfigure(1, weight=0) # Content column
        feedback_main_frame.grid_columnconfigure(2, weight=1) # Right padding

        tk.Label(feedback_main_frame, text="💬 Submit Your Feedback 💬", font=FONT_STYLES["header3"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["accent_green"]).grid(row=0, column=1, pady=20)

        feedback_content_frame = tk.Frame(feedback_main_frame, bg=COLOR_PALETTE["mid_bg"], padx=20, pady=20, bd=2, relief="groove")
        feedback_content_frame.grid(row=1, column=1, pady=10) # Place in central column

        tk.Label(feedback_content_frame, text="Your Name (Optional):", font=FONT_STYLES["small_label"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"]).pack(anchor="w", pady=2)
        name_entry = tk.Entry(feedback_content_frame, font=FONT_STYLES["entry"], width=40, bd=2, relief="sunken")
        name_entry.pack(pady=5)

        tk.Label(feedback_content_frame, text="Your Feedback:", font=FONT_STYLES["small_label"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"]).pack(anchor="w", pady=2)
        feedback_text = tk.Text(feedback_content_frame, font=FONT_STYLES["entry"], width=40, height=8, bd=2, relief="sunken", wrap="word")
        feedback_text.pack(pady=5)

        def submit_feedback():
            name = name_entry.get().strip()
            feedback = feedback_text.get("1.0", tk.END).strip()

            if not feedback:
                messagebox.showwarning("Input Error", "Please enter your feedback before submitting.")
                return

            feedback_entry = f"Name: {name if name else 'Anonymous'}\nFeedback: {feedback}\n---"
            feedback_list.append(feedback_entry)

            messagebox.showinfo("Feedback Submitted", "Thank you for your valuable feedback! It helps us improve Vote-Xpress.")
            self.main_menu()

        tk.Button(feedback_content_frame, text="Submit Feedback", command=submit_feedback,
                  bg=COLOR_PALETTE["button_blue"], fg=COLOR_PALETTE["light_text"], font=FONT_STYLES["button"], relief="raised", bd=3).pack(pady=15)

    def admin_panel(self):
        """Displays the admin panel with options to publish results and view feedback."""
        self._prepare_full_page_view()
        self.clear_central_content_frame()
        admin_container_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        admin_container_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.central_content_frame = admin_container_frame

        self._add_back_to_main_menu_button(admin_container_frame)

        admin_main_frame = self._create_scrollable_frame(admin_container_frame)
        
        # Configure admin_main_frame for centering its content
        admin_main_frame.grid_columnconfigure(0, weight=1) # Left padding
        admin_main_frame.grid_columnconfigure(1, weight=0) # Content column
        admin_main_frame.grid_columnconfigure(2, weight=1) # Right padding

        tk.Label(admin_main_frame, text="🔐 Admin Panel 🔐", font=FONT_STYLES["header3"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["accent_red"]).grid(row=0, column=1, pady=20)

        admin_content_frame = tk.Frame(admin_main_frame, bg=COLOR_PALETTE["mid_bg"], bd=3, relief="raised", padx=30, pady=30)
        admin_content_frame.grid(row=1, column=1, pady=30) # Place in central column

        tk.Label(admin_content_frame, text="Administrator Functions", font=FONT_STYLES["subheader"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"]).pack(pady=10)
        tk.Label(admin_content_frame, text="Use these options with caution.", font=FONT_STYLES["small_label"], bg=COLOR_PALETTE["mid_bg"], fg="gray").pack(pady=5)

        password_label = tk.Label(admin_content_frame, text="Admin Password:", font=FONT_STYLES["label"], bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"])
        password_label.pack(pady=5)
        password_entry = tk.Entry(admin_content_frame, show="*", font=FONT_STYLES["entry"], width=20, bd=2, relief="sunken")
        password_entry.pack(pady=5)

        def authenticate_and_show_options():
            def authenticate_and_show_options():
    if password_entry.get() == ADMIN_PASSWORD:
        password_label.destroy()
        password_entry.destroy()
        auth_button.destroy()

        tk.Button(
            admin_content_frame,
            text="Publish Final Results",
            command=publish_results,
            bg=COLOR_PALETTE["accent_red"],
            fg=COLOR_PALETTE["light_text"],
            font=FONT_STYLES["button"],
            relief="raised",
            bd=4,
            padx=20,
            pady=10
        ).pack(pady=15)

        tk.Button(
            admin_content_frame,
            text="📝 View User Feedback",
            command=self.view_user_feedback,
            bg=COLOR_PALETTE["button_blue"],
            fg=COLOR_PALETTE["light_text"],
            font=FONT_STYLES["button"],
            relief="raised",
            bd=3
        ).pack(pady=10)

    else:
        messagebox.showerror("Authentication Failed", "Incorrect password. Access denied.")
        password_entry.delete(0, tk.END)



        auth_button = tk.Button(admin_content_frame, text="Authenticate", command=authenticate_and_show_options,
                                bg=COLOR_PALETTE["accent_green"], fg=COLOR_PALETTE["light_text"], font=FONT_STYLES["button"], relief="raised", bd=3)
        auth_button.pack(pady=10)

        def publish_results():
            if messagebox.askyesno("Confirm Publish", "Are you sure you want to publish the final results? This action cannot be undone."):
                if not votes or sum(votes.values()) == 0:
                    messagebox.showinfo("Results Published", "No votes cast yet to publish results.")
                    return

                sorted_results = sorted(votes.items(), key=lambda x: x[1], reverse=True)
                winner = sorted_results[0]
                runner_up = sorted_results[1] if len(sorted_results) > 1 else None

                FinalResultsWindow(self.root, winner, runner_up, sorted_results)
            else:
                messagebox.showinfo("Action Cancelled", "Result publication cancelled.")

    def view_user_feedback(self):
        """Displays all submitted user feedback."""
        self._prepare_full_page_view()
        self.clear_central_content_frame()
        feedback_view_container_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        feedback_view_container_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.central_content_frame = feedback_view_container_frame

        self._add_back_to_main_menu_button(feedback_view_container_frame)

        feedback_view_frame = self._create_scrollable_frame(feedback_view_container_frame)
        
        # Configure feedback_view_frame for centering its content
        feedback_view_frame.grid_columnconfigure(0, weight=1) # Left padding
        feedback_view_frame.grid_columnconfigure(1, weight=0) # Content column
        feedback_view_frame.grid_columnconfigure(2, weight=1) # Right padding

        tk.Label(feedback_view_frame, text="📝 User Feedback 📝", font=FONT_STYLES["header3"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["primary_blue"]).grid(row=0, column=1, pady=20)

        feedback_display_frame = tk.Frame(feedback_view_frame, bg=COLOR_PALETTE["mid_bg"], bd=2, relief="groove", padx=20, pady=20)
        feedback_display_frame.grid(row=1, column=1, pady=10, padx=50, sticky="nsew") # Place in central column, add sticky="nsew"

        feedback_text_area = tk.Text(feedback_display_frame, font=FONT_STYLES["small_label"], wrap="word", state="disabled",
                                     bg=COLOR_PALETTE["mid_bg"], fg=COLOR_PALETTE["dark_text"], bd=1, relief="sunken")
        feedback_text_area.pack(side="left", fill="both", expand=True)

        feedback_scrollbar = tk.Scrollbar(feedback_display_frame, command=feedback_text_area.yview)
        feedback_scrollbar.pack(side="right", fill="y")
        feedback_text_area.config(yscrollcommand=feedback_scrollbar.set)

        feedback_text_area.config(state="normal")
        if feedback_list:
            for entry in feedback_list:
                feedback_text_area.insert("end", entry + "\n\n")
        else:
            feedback_text_area.insert("end", "No feedback submitted yet.")
        feedback_text_area.config(state="disabled")

    def open_linkedin(self, url):
        """Opens the provided LinkedIn URL in a web browser."""
        webbrowser.open(url)

    # --- VoteSmart Quiz Challenge Methods ---
    def start_quiz_challenge(self):
        """Initializes and starts the quiz challenge."""
        print("Quiz started. Initializing quiz state.")
        self._prepare_full_page_view()
        self.clear_central_content_frame()
        quiz_main_container_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        quiz_main_container_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.central_content_frame = quiz_main_container_frame

        self._add_back_to_main_menu_button(quiz_main_container_frame) # Add back button

        quiz_main_frame = self._create_scrollable_frame(quiz_main_container_frame)
        
        # Configure quiz_main_frame for centering its content
        quiz_main_frame.grid_columnconfigure(0, weight=1) # Left padding
        quiz_main_frame.grid_columnconfigure(1, weight=0) # Content column
        quiz_main_frame.grid_columnconfigure(2, weight=1) # Right padding
        # Crucial: Allow the row containing the quiz_frame to expand vertically
        quiz_main_frame.grid_rowconfigure(1, weight=1) 

        tk.Label(quiz_main_frame, text="🧠 VoteSmart Quiz Challenge 🧠", font=FONT_STYLES["header3"], bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["primary_blue"]).grid(row=0, column=1, pady=20)

        self.quiz_frame = tk.Frame(quiz_main_frame, bg=COLOR_PALETTE["quiz_bg"], bd=3, relief="solid", padx=20, pady=20)
        self.quiz_frame.grid(row=1, column=1, pady=10, padx=50, sticky="nsew") # Place in central column, add sticky="nsew"

        self.question_label = tk.Label(self.quiz_frame, text="", font=FONT_STYLES["quiz_question"], bg=COLOR_PALETTE["quiz_bg"], fg=COLOR_PALETTE["dark_text"], wraplength=600, justify="left")
        self.question_label.pack(pady=15, anchor="w", fill="both", expand=True) # Added fill="both", expand=True

        self.timer_label_quiz = tk.Label(self.quiz_frame, text="Time: 10", font=FONT_STYLES["quiz_timer"], bg=COLOR_PALETTE["quiz_bg"], fg=COLOR_PALETTE["accent_red"])
        self.timer_label_quiz.pack(pady=5, anchor="e")

        self.option_radiobuttons = []
        # Create a list to store the actual Radiobutton widgets
        self.quiz_option_widgets = [] 
        for i in range(4): # Assuming 4 options per question
            rb = tk.Radiobutton(self.quiz_frame, text="", variable=self.quiz_selected_option, value="",
                                font=FONT_STYLES["quiz_option"], bg=COLOR_PALETTE["quiz_bg"], fg=COLOR_PALETTE["dark_text"],
                                selectcolor=COLOR_PALETTE["button_blue"], anchor="w", justify="left", wraplength=550)
            rb.pack(pady=5, anchor="w", fill="both", expand=True) # Added fill="both", expand=True
            self.option_radiobuttons.append(rb)
            self.quiz_option_widgets.append(rb) # Store the widget itself

        self.feedback_label = tk.Label(self.quiz_frame, text="", font=FONT_STYLES["small_label"], bg=COLOR_PALETTE["quiz_bg"])
        self.feedback_label.pack(pady=10)

        self.next_button = tk.Button(self.quiz_frame, text="Submit Answer", command=self.submit_quiz_answer,
                                     bg=COLOR_PALETTE["accent_green"], fg=COLOR_PALETTE["light_text"], font=FONT_STYLES["button"], relief="raised", bd=3)
        self.next_button.pack(pady=15)

        # Initialize quiz state for a new game
        self.quiz_score = 0
        self.current_question_index = 0
        self.quiz_questions_shuffled = random.sample(QUIZ_QUESTIONS, len(QUIZ_QUESTIONS)) # Shuffle questions
        print(f"Quiz started. Total questions: {len(self.quiz_questions_shuffled)}")
        self.display_quiz_question() # Load the first question

    def display_quiz_question(self):
        """Displays the current quiz question and options."""
        # Cancel any previous timer
        if self.quiz_timer_id:
            self.root.after_cancel(self.quiz_timer_id)
            self.quiz_timer_id = None

        # Check if there are more questions
        if not self.quiz_questions_shuffled or self.current_question_index >= len(self.quiz_questions_shuffled):
            print(f"No more questions or quiz_questions_shuffled is empty. Ending quiz. current_question_index: {self.current_question_index}, len(quiz_questions_shuffled): {len(self.quiz_questions_shuffled) if self.quiz_questions_shuffled else 0}")
            self.end_quiz()
            return

        # Reset feedback and re-enable buttons
        self.feedback_label.config(text="")
        self.next_button.config(text="Submit Answer", command=self.submit_quiz_answer, state="normal")
        self.quiz_selected_option.set("") # Clear previous selection

        current_question = self.quiz_questions_shuffled[self.current_question_index]
        self.question_label.config(text=f"Q{self.current_question_index + 1}: {current_question['question']}")
        print(f"Displaying question index: {self.current_question_index}, Question: {current_question['question']}")

        for i, option_text in enumerate(current_question['options']):
            self.quiz_option_widgets[i].config(text=option_text, value=option_text, state="normal",
                                               bg=COLOR_PALETTE["quiz_bg"], fg=COLOR_PALETTE["dark_text"]) # Reset colors
        
        # Hide unused radio buttons if options are less than 4
        for i in range(len(current_question['options']), 4):
            self.quiz_option_widgets[i].config(text="", value="", state="disabled")


        self.time_left = 10 # Reset timer for each question
        self.update_quiz_timer()

    def update_quiz_timer(self):
        """Updates the quiz countdown timer."""
        if self.time_left > 0:
            self.timer_label_quiz.config(text=f"Time: {self.time_left}")
            self.time_left -= 1
            self.quiz_timer_id = self.root.after(1000, self.update_quiz_timer)
        else:
            self.timer_label_quiz.config(text="Time: 0")
            print(f"Quiz timer ran out for question index: {self.current_question_index}")
            self.submit_quiz_answer(timed_out=True)

    def submit_quiz_answer(self, timed_out=False):
        """Checks the submitted answer, updates score, and moves to next question."""
        if self.quiz_timer_id:
            self.root.after_cancel(self.quiz_timer_id)
            self.quiz_timer_id = None

        # Cancel any pending auto-advance from previous question
        if self.current_quiz_auto_advance_id:
            self.root.after_cancel(self.current_quiz_auto_advance_id)
            self.current_quiz_auto_advance_id = None

        current_question = self.quiz_questions_shuffled[self.current_question_index]
        selected_answer = self.quiz_selected_option.get()
        correct_answer = current_question['answer']

        # Disable all radio buttons and the submit button immediately
        for rb in self.quiz_option_widgets: # Use the stored widgets
            rb.config(state="disabled")
        self.next_button.config(state="disabled")

        if timed_out:
            self.feedback_label.config(text=f"Time's up! Correct answer: {correct_answer}", fg="orange")
            print(f"Submitted answer (timed out) for question index: {self.current_question_index}. Correct: {correct_answer}. Score: {self.quiz_score}")
        elif selected_answer == correct_answer:
            self.quiz_score += 1
            self.feedback_label.config(text="✅ Correct!", fg="green")
            print(f"Submitted answer (correct) for question index: {self.current_question_index}. Selected: {selected_answer}. Score: {self.quiz_score}")
        else:
            self.feedback_label.config(text=f"❌ Incorrect. Correct answer: {correct_answer}", fg="red")
            print(f"Submitted answer (incorrect) for question index: {self.current_question_index}. Selected: {selected_answer}. Correct: {correct_answer}. Score: {self.quiz_score}")
        
        # Highlight options
        for rb in self.quiz_option_widgets: # Use the stored widgets
            if rb.cget("value") == correct_answer:
                rb.config(bg="lightgreen", fg="black") # Highlight correct answer
            elif rb.cget("value") == selected_answer and selected_answer != correct_answer:
                rb.config(bg="salmon", fg="black") # Highlight incorrect selected answer

        # Change button text and command for next action
        if self.current_question_index < len(self.quiz_questions_shuffled) - 1:
            self.next_button.config(text="Next Question", command=self._manual_proceed_quiz_question) # New command
        else:
            self.next_button.config(text="Finish Quiz", command=self.end_quiz)
        
        self.next_button.config(state="normal") # Re-enable the button for next action

        # Set auto-advance for 2 seconds
        self.current_quiz_auto_advance_id = self.root.after(2000, self._auto_proceed_quiz_question)

    def _manual_proceed_quiz_question(self):
        """Manually proceeds to the next quiz question or ends the quiz."""
        print(f"Manually proceeding to next question. Current index before increment: {self.current_question_index}")
        # Cancel auto-advance if user clicks manually
        if self.current_quiz_auto_advance_id:
            self.root.after_cancel(self.current_quiz_auto_advance_id)
            self.current_quiz_auto_advance_id = None
        
        self.current_question_index += 1
        self.display_quiz_question()

    def _auto_proceed_quiz_question(self):
        """Automatically proceeds to the next quiz question or ends the quiz."""
        print(f"Auto proceeding to next question. Current index before increment: {self.current_question_index}")
        # This function will only execute if the manual_proceed_quiz_question wasn't called
        # and thus the auto-advance timer wasn't cancelled.
        self.current_quiz_auto_advance_id = None # Clear the ID as it's now executing
        self.current_question_index += 1
        self.display_quiz_question()

    def end_quiz(self):
        """Ends the quiz, displays final score, badge, and slogan."""
        print(f"Quiz ended. Final score: {self.quiz_score} / {len(QUIZ_QUESTIONS)}")
        # Cancel any remaining timers when quiz ends
        if self.quiz_timer_id:
            self.root.after_cancel(self.quiz_timer_id)
            self.quiz_timer_id = None
        if self.current_quiz_auto_advance_id:
            self.root.after_cancel(self.current_quiz_auto_advance_id)
            self.current_quiz_auto_advance_id = None

        self._prepare_full_page_view()
        self.clear_central_content_frame()
        quiz_results_container_frame = tk.Frame(self.content_frame, bg=COLOR_PALETTE["light_bg"])
        quiz_results_container_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.central_content_frame = quiz_results_container_frame

        self._add_back_to_main_menu_button(quiz_results_container_frame)

        quiz_results_frame = self._create_scrollable_frame(quiz_results_container_frame)
        
        # Configure quiz_results_frame for centering its content
        quiz_results_frame.grid_columnconfigure(0, weight=1) # Left padding
        quiz_results_frame.grid_columnconfigure(1, weight=0) # Content column
        quiz_results_frame.grid_columnconfigure(2, weight=1) # Right padding

        final_score_content_frame = tk.Frame(quiz_results_frame, bg=COLOR_PALETTE["quiz_bg"], bd=3, relief="ridge", padx=30, pady=30)
        final_score_content_frame.grid(row=0, column=1, pady=50, padx=50, sticky="nsew") # Place in central column, add sticky="nsew"

        tk.Label(final_score_content_frame, text="🎉 Quiz Completed! 🎉", font=FONT_STYLES["header2"], bg=COLOR_PALETTE["quiz_bg"], fg=COLOR_PALETTE["primary_blue"]).pack(pady=15)
        tk.Label(final_score_content_frame, text=f"Your Score: {self.quiz_score} / {len(QUIZ_QUESTIONS)}", font=FONT_STYLES["quiz_result"], bg=COLOR_PALETTE["quiz_bg"], fg=COLOR_PALETTE["dark_text"]).pack(pady=10)

        badge_text = ""
        slogan = ""
        stars = 0

        if self.quiz_score == 10:
            badge_text = "🏅 Voting Champion! 🏅"
            slogan = "Your knowledge is a beacon for democracy! Keep leading the way."
            stars = 3
        elif self.quiz_score >= 8:
            badge_text = "🎖️ Democracy Defender! 🎖️"
            slogan = "Excellent civic knowledge! You're a true guardian of our values."
            stars = 2
        elif self.quiz_score >= 5:
            badge_text = "📖 Civic Learner! 📖"
            slogan = "Great effort! Every bit of knowledge strengthens our nation."
            stars = 1
        else:
            badge_text = "📚 Needs More Study 📚"
            slogan = "Keep learning! Your engagement is vital for a strong democracy."
            stars = 0

        self.user_quiz_badge = badge_text
        self.user_quiz_stars = stars

        tk.Label(final_score_content_frame, text=f"Your Badge: {badge_text}", font=FONT_STYLES["subheader"], bg=COLOR_PALETTE["quiz_bg"], fg=COLOR_PALETTE["accent_green"]).pack(pady=10)
        tk.Label(final_score_content_frame, text=slogan, font=FONT_STYLES["label"], bg=COLOR_PALETTE["quiz_bg"], fg=COLOR_PALETTE["dark_text"], wraplength=500, justify="center").pack(pady=15)

        tk.Button(final_score_content_frame, text="Back to Dashboard", command=self.main_menu,
                  bg=COLOR_PALETTE["button_blue"], fg=COLOR_PALETTE["light_text"], font=FONT_STYLES["button"], relief="raised", bd=3).pack(pady=20)

        # Update the main menu's welcome label to reflect the stars
        self.root.after(100, self.main_menu) # Call main_menu to refresh the stars

    def show_live_news(self):
        """Opens a new window to display live political news."""
        news_window = tk.Toplevel(self.root)
        news_window.title("📰 Live Political News")
        news_window.geometry("600x500")
        news_window.config(bg=COLOR_PALETTE["news_bg"])
        news_window.transient(self.root)
        news_window.grab_set()

        tk.Label(news_window, text="Latest Political News", font=FONT_STYLES["news_title"],
                 bg=COLOR_PALETTE["news_bg"], fg=COLOR_PALETTE["primary_blue"]).pack(pady=10)

        news_text_frame = tk.Frame(news_window, bg=COLOR_PALETTE["light_bg"], bd=2, relief="sunken")
        news_text_frame.pack(padx=20, pady=10, fill="both", expand=True)

        news_text_area = tk.Text(news_text_frame, wrap="word", font=FONT_STYLES["news_snippet"],
                                 bg=COLOR_PALETTE["light_bg"], fg=COLOR_PALETTE["dark_text"],
                                 padx=10, pady=10)
        news_text_area.pack(side="left", fill="both", expand=True)

        news_scrollbar = tk.Scrollbar(news_text_frame, command=news_text_area.yview)
        news_scrollbar.pack(side="right", fill="y")
        news_text_area.config(yscrollcommand=news_scrollbar.set)

        news_text_area.insert("end", "Fetching latest news...\n\n")
        news_text_area.config(state="disabled")

        # Start fetching news in a separate thread
        # Corrected the argument here from 'text_area' to 'news_text_area'
        threading.Thread(target=self._fetch_and_display_news, args=(news_text_area, news_window)).start()

        tk.Button(news_window, text="Close", command=news_window.destroy,
                  bg=COLOR_PALETTE["accent_red"], fg=COLOR_PALETTE["light_text"],
                  font=FONT_STYLES["button"], relief="raised", bd=3).pack(pady=10)

        news_window.protocol("WM_DELETE_WINDOW", news_window.destroy)

    def _fetch_and_display_news(self, text_widget, parent_window):
        """Fetches news using google_search and displays it in the text widget."""
        try:
            # Use google_search to get political news
            # Ensure the google_search tool is available in the environment
            # This is a placeholder for actual tool call, assuming it returns structured data
            # For a real implementation, youd use:
            # search_results = google_search.search(queries=["latest political news India"])
            
            # Mock data for demonstration if google_search is not directly callable in this context
            mock_search_results = [
                {"query": "latest political news India",
                 "results": [
                     {"title": "Parliament Session Begins with Heated Debates on Economy", "snippet": "The monsoon session of Parliament commenced today, marked by intense discussions on inflation and unemployment.", "source_title": "The National Herald", "url": "https://example.com/news1"},
                     {"title": "Election Commission Announces By-Election Dates for Three States", "snippet": "By-elections for three assembly constituencies will be held next month, the Election Commission announced.", "source_title": "Indian Express", "url": "https://example.com/news2"},
                     {"title": "New Policy on Renewable Energy Receives Mixed Reactions", "snippet": "The government's new renewable energy policy aims to boost green initiatives but faces criticism from industry experts.", "source_title": "EcoTimes", "url": "https://example.com/news3"},
                     {"title": "Opposition Parties Form Alliance Ahead of State Elections", "snippet": "Several opposition parties have announced a new alliance to contest the upcoming state elections, aiming for a united front.", "source_title": "Political Daily", "url": "https://example.com/news4"},
                     {"title": "Supreme Court Delivers Landmark Judgment on Digital Privacy", "snippet": "A recent Supreme Court ruling has set a new precedent for digital privacy rights, impacting tech companies and citizens alike.", "source_title": "Legal Insights", "url": "https://example.com/news5"},
                 ]}
            ]
            
            news_content = []
            if mock_search_results and mock_search_results[0].get("results"):
                for item in mock_search_results[0]["results"]:
                    title = item.get("title", "No Title")
                    snippet = item.get("snippet", "No snippet available.")
                    source = item.get("source_title", "Unknown Source")
                    url = item.get("url", "#")
                    news_content.append(f"• {title}\n  {snippet}\n  (Source: {source}) - {url}\n\n")
            else:
                news_content.append("Could not fetch news at this moment. Please try again later.\n")

            # Update UI on the main thread
            self.root.after(0, lambda: self._update_news_text_area(text_widget, news_content))

        except Exception as e:
            print(f"Error fetching news: {e}")
            self.root.after(0, lambda: self._update_news_text_area(text_widget, ["Failed to load news. Please check your internet connection or try again later."]))

    def _update_news_text_area(self, text_widget, news_items):
        """Updates the news text area with fetched news."""
        if not text_widget.winfo_exists(): # Check if the widget still exists
            return

        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        for item in news_items:
            text_widget.insert("end", item)
        text_widget.config(state="disabled")

    def open_linkedin(self, url):
        """Opens the provided LinkedIn URL in a web browser."""
        webbrowser.open(url)

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()

    splash = SplashScreen(root)

    root.mainloop()
