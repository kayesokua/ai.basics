import random
import uuid
import json
from database import core, linking, intro, outro, all_moves
from extensions import get_preview_songs_by_mood

class ChoreographyPlanner:
    def __init__(self):
        self.moves = all_moves

    def define_known_movements(self, user_known_movements):
        self.user_known_movements = user_known_movements

    def define_blacklisted_movements(self, user_blacklisted_movements):
        self.user_blacklisted_movements = user_blacklisted_movements

    def define_mood(self, mood):
        self.playlist = get_preview_songs_by_mood(mood)

    def define_goal(self, goal):
        self.goal = goal

        if len(self.user_known_movements) < 10:
            print(f"You need to learn new moves!")
            goal == "learn"

        if goal == "review":
            self.wishlist = self.user_known_movements
            self.blacklist = [move for move in self.moves if move not in self.user_known_movements]
            self.blacklist += self.user_blacklisted_movements

        elif goal == "feel-good":
            self.wishlist = random.sample(self.user_known_movements, round(0.9 * len(self.user_known_movements)))
            self.blacklist = self.user_blacklisted_movements

        elif goal == "improve":
            self.wishlist = random.sample(self.user_known_movements, round(0.6 * len(self.user_known_movements)))
            self.blacklist = self.user_blacklisted_movements

        elif goal == "challenge":
            self.wishlist = random.sample(self.user_known_movements, round(0.3 * len(self.user_known_movements)))
            self.blacklist = self.user_blacklisted_movements

        elif goal == "learn":
            self.wishlist = []
            self.blacklist = self.user_blacklisted_movements
            self.blacklist += self.user_known_movements

        else:
            print("Please enter a valid goal from selection.")

    def generate_dance_sequence(self, num_sequences):
        def filtered_choice(choices, used_wishlist):
            lowercase_wishlist = [item.lower() for item in self.wishlist]
            valid_choices = [choice for choice in choices if not any(blackword.lower() in choice.lower() for blackword in self.blacklist)]
            random.shuffle(valid_choices)
            return random.choice(valid_choices)
        new_choreo = []
        used_wishlist = set()

        new_choreo.append(filtered_choice(intro, used_wishlist))

        for i in range(num_sequences):
            new_choreo.append(filtered_choice(linking, used_wishlist))

            for _ in range(4):
                new_choreo.append(filtered_choice(core, used_wishlist))

        new_choreo.append(filtered_choice(linking, used_wishlist))

        new_choreo.append(filtered_choice(outro, used_wishlist))

        for wish in self.wishlist:
            if wish not in used_wishlist:
                replacement_index = random.randint(1, len(new_choreo) - 2)  # Exclude intro and outro
                new_choreo[replacement_index] = wish

        dance_session = {
            "id": str(uuid.uuid4()),
            "song": random.sample(self.playlist,1),
            "sequence": {index: movement for index, movement in enumerate(new_choreo)},
            "wishlist": self.wishlist,
            "blacklist": self.blacklist,
            "goal": self.goal,
        }

        with open(f"data/{dance_session['id']}.json", "w") as f:
            json.dump(dance_session, f, indent=4)

        return print(f"Your dance session has been saved as {dance_session['id']}.json")


user_movements = random.sample(all_moves, 9)
user_blacklist = []

while len(user_blacklist) < 5:
    movement = random.choice(all_moves)
    if movement not in user_movements and movement not in user_blacklist:
        user_blacklist.append(movement)

planner = ChoreographyPlanner()

# Set the vocabulary
planner.define_known_movements(user_movements)
planner.define_blacklisted_movements(user_blacklist)

# Set the mood
planner.define_mood("emotive")
planner.define_goal("learn")

# Generate the dance sequence
for i in range(5):
    planner.generate_dance_sequence(3)