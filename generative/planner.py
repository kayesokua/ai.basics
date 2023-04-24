import random
import uuid
import datetime
import json
from database.dance.terms import all_moves
from extensions.songs import recommend_song_by_mood

class ChoreographyPlanner:
    def __init__(self):
        self.moves = all_moves

    def define_memory(self, user_known_movements):
        self.memory = user_known_movements

    def define_blacklist(self, user_blacklisted_movements):
        self.blacklist = user_blacklisted_movements

    def define_wishlist(self, wishlist):
        if not wishlist:
            self.wishlist = []
        else:
            self.wishlist = wishlist

    def define_mood(self, mood):
        self.mood = mood
        self.playlist = recommend_song_by_mood(mood)

    def define_goal(self, goal):
        self.goal = goal
        self.choices = []

        if len(self.memory) < 10:
            print(f"You need to learn new moves!")
            self.goal = "learn"

        if goal == "review":
            self.choices = [move for move in self.memory]
            self.choices = set(self.choices)
            self.choices -= set(self.blacklist)
            self.choices |= set(self.wishlist)
            self.choices = list(self.choices)

        elif goal == "feel-good":
            self.choices = random.sample(self.memory, round(0.9 * len(self.memory)))
            self.choices = set(self.choices)
            self.choices -= set(self.blacklist)
            self.choices |= set(self.wishlist)
            self.choices = list(self.choices)

        elif goal == "improve":
            self.choices = random.sample(self.memory, round(0.6 * len(self.memory)))
            self.choices = set(self.choices)
            self.choices -= set(self.blacklist)
            self.choices |= set(self.wishlist)
            self.choices = list(self.choices)

        elif goal == "challenge":
            self.choices = random.sample(self.memory, round(0.3 * len(self.memory)))
            self.choices = set(self.choices)
            self.choices -= set(self.blacklist)
            self.choices |= set(self.wishlist)
            self.choices = list(self.choices)

        elif goal == "learn":
            self.choices = [move for move in all_moves if move not in self.blacklist]

        else:
            print("Please enter a valid goal from selection.")

    def generate_dance_sequence(self, num_sequences):
        random.shuffle(self.choices)
        total_movement_count = 8 * num_sequences
        new_choreo = {}
        for i in range(total_movement_count):
            new_choreo[i] = random.choice(self.choices)

        dance_session = {
            "id": str(uuid.uuid4()),
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mood": self.mood,
            "song": random.sample(self.playlist,1),
            "sequence": new_choreo,
            "memory": self.memory,
            "wishlist": self.wishlist,
            "blacklist": self.blacklist,
            "goal": self.goal,
            "success": False
        }

        with open(f"database/user/{dance_session['id']}.json", "w") as f:
            json.dump(dance_session, f, indent=4)

        print(f"Your dance session has been saved as {dance_session['id']}.json")

        return dance_session['id']

# Generate mock data
user_memory = random.sample(all_moves, 10)
user_wishlist = random.sample(all_moves, 2)
user_blacklist = []

while len(user_blacklist) < 5:
    movement = random.choice(all_moves)
    if movement not in user_memory and movement not in user_blacklist:
        user_blacklist.append(movement)

user_mood = ["emotive", "happy", "gloomy", "sunny", "regret", "nostalgic", "romantic"]
user_goal = ["review", "feel-good", "improve", "challenge", "learn"]

# Initialize planner
planner = ChoreographyPlanner()
planner.define_memory(user_memory)
planner.define_blacklist(user_blacklist)
planner.define_wishlist(user_wishlist)

# Generate dance sessions for the next 25 days
def generate_mock_dance_sessions(limit):
    for i in range(1, limit):
        date_of_the_day = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
        mood_of_the_day = random.choice(user_mood)
        goal_of_the_day = random.choice(user_goal)
        fitness_of_the_day = random.randint(1, 5)

        planner.define_mood(mood_of_the_day)
        planner.define_goal(goal_of_the_day)
        session_id = planner.generate_dance_sequence(fitness_of_the_day)

        with open(f"database/user/{session_id}.json") as f:
            session = json.load(f)
            session["date"] = date_of_the_day
            session["success"] = random.choice([True, False])

            if session["success"]:
                for sequence_movement in session["sequence"].values():
                    if sequence_movement not in user_memory:
                        user_memory.append(sequence_movement)
                        planner.define_memory(user_memory)
                        print(f"New movement {sequence_movement} added to user movements")

        with open(f"database/user/{session_id}.json", "w") as f:
            json.dump(session, f, indent=4)

# generate_mock_dance_sessions(25)