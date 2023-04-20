import random
import uuid
import json
from datetime import datetime
import curses
import os

def input_with_unique_choices(message, choices, num_choices):
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    cursor = 0
    KEY_UP = 259
    KEY_DOWN = 258
    KEY_ENTER = 10
    chosen_items = []
    for i in range(num_choices):
        stdscr.clear()
        stdscr.addstr(message + "\n")
        for j, choice in enumerate(choices):
            if j == cursor:
                stdscr.addstr("  > " + choice + "\n")
            else:
                stdscr.addstr("    " + choice + "\n")
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key == KEY_UP:
                cursor = max(cursor - 1, 0)
            elif key == KEY_DOWN:
                cursor = min(cursor + 1, len(choices) - 1)
            elif key == KEY_ENTER:
                if choices[cursor] in chosen_items:
                    stdscr.addstr("You have already chosen this item. Please choose a different one.\n")
                    stdscr.refresh()
                    continue
                chosen_items.append(choices[cursor])
                choices.remove(choices[cursor])
                break
            stdscr.clear()
            stdscr.addstr(message + "\n")
            for j, choice in enumerate(choices):
                if j == cursor:
                    stdscr.addstr("  > " + choice + "\n")
                else:
                    stdscr.addstr("    " + choice + "\n")
            stdscr.refresh()
    curses.echo()
    stdscr.keypad(False)
    curses.endwin()
    return chosen_items

def input_with_choices(message, choices):
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    cursor = 0
    KEY_UP = 259
    KEY_DOWN = 258
    KEY_ENTER = 10
    stdscr.addstr(message + "\n")
    while True:
        for i, choice in enumerate(choices):
            if i == cursor:
                stdscr.addstr("  > " + choice + "\n")
            else:
                stdscr.addstr("    " + choice + "\n")
        stdscr.refresh()
        key = stdscr.getch()
        if key == KEY_UP:
            cursor = max(cursor - 1, 0)
        elif key == KEY_DOWN:
            cursor = min(cursor + 1, len(choices) - 1)
        elif key == KEY_ENTER:
            break
        stdscr.clear()
        stdscr.addstr(message + "\n")
    curses.echo()
    stdscr.keypad(False)
    curses.endwin()
    return choices[cursor]

def load_movement_vocabulary():
    with open("vocabulary.json", "r") as f:
        movement_vocabulary = json.load(f)
    return movement_vocabulary

def load_techniques_list():
    techniques_list = []
    for k, v in movement_vocabulary.items():
        techniques_list.append(k)
    return techniques_list

def load_session_data():
    sessions = []
    for filename in os.listdir("data/"):
        if filename.endswith(".json"):
            with open("data/" + filename, "r") as f:
                session_data = json.load(f)
                session_data["id"] = filename.split(".")[0]
                sessions.append(session_data)
    return sessions

movement_vocabulary = load_movement_vocabulary()

choices = {
    "techniques": load_techniques_list(),
    "expertise": ["amateur", "intermediate", "advanced"],
    "focus": ["stability", "flexibility", "coordination", "artistry"],
    "intensity": ["low", "medium", "high"],
}

questions = {
    "techniques": ["Which technique are you interested in practicing?", "What technique would you like to practice today?", "What technique would you like to focus on today?"],
    "expertise": ["How much experience do you have with this technique?", "What is your level of expertise with this technique?", "What is your level of experience with this technique?"],
    "focus": ["What is your focus for today's practice?", "What is your goal for today's practice?", "What is your intention for today's practice?"],
    "intensity": ["What level of intensity would you like for your practice today?", "What level of intensity would you like for your practice today?", "What level of intensity would you like for your practice today?", "What level of intensity would you like for your practice today?"],
}

def create_user_session(questions, choices):
    user_responses = {}
    user_responses["id"] = str(uuid.uuid4())
    user_responses["timestamp"] = str(datetime.now())
    user_responses["techniques"] = input_with_unique_choices(random.choice(questions["techniques"]), choices["techniques"], 3)
    user_responses["expertise"] = []
    for i, technique in enumerate(user_responses["techniques"]):
        question = f"How much experience do you have with {technique}?"
        response = input_with_choices(question, choices["expertise"])
        user_responses["expertise"].append(response)
    user_responses["focus"] = input_with_unique_choices(random.choice(questions["focus"]), choices["focus"], 1)
    user_responses["intensity"] = input_with_unique_choices(random.choice(questions["intensity"]), choices["intensity"], 1)

    with open(f'data/{user_responses["id"]}.json', 'w') as f:
        json.dump(user_responses, f)

    return user_responses["id"]


def generate_recommendation(session_id):
    with open(f"data/{session_id}.json", "r") as f:
        session_data = json.load(f)

    recommendations = []
    for technique, expertise in zip(session_data["techniques"], session_data["expertise"]):
        instructions = movement_vocabulary[technique][expertise]["instructions"]
        exercises = movement_vocabulary[technique][expertise]["exercises"]
        focus_exercises = movement_vocabulary[technique]["focus"][session_data["focus"][0]]
        intensity = movement_vocabulary[technique]["intensity"][session_data["intensity"][0]]
        defintion = movement_vocabulary[technique]["definition"]

        statement = f"{technique} is {defintion}. For practicing {technique} as a/an {expertise} performance, the recommended warm-up exercises are {', '.join(exercises)} for {intensity[0]}. After warming up, you should practice the following instructions: {', '.join(instructions)} for {intensity[0]}. Since you want to particularly focus on {session_data['focus'][0]}, additional exercises could include {', '.join(focus_exercises)}."

        recommendations.append(statement)

    session_data["recommendations"] = recommendations

    with open(f"data/{session_id}.json", "w") as f:
        json.dump(session_data, f, indent=4)

    return recommendations

def generate_chat_session_data(choices):
    user_responses = {}
    user_responses["id"] = str(uuid.uuid4())
    user_responses["timestamp"] = str(datetime.now())
    user_responses["techniques"] = [random.choice(choices["techniques"]) for i in range(3)]
    user_responses["expertise"] = [random.choice(choices["expertise"]) for i in range(3)]
    user_responses["focus"] = [random.choice(choices["focus"])]
    user_responses["intensity"] = [random.choice(choices["intensity"])]

    with open(f'data/{user_responses["id"]}.json', 'w') as f:
        json.dump(user_responses, f)

    generate_recommendation(user_responses["id"])
    message = f"Your session ID is {user_responses['id']}. Please save this ID for future reference."

    return print(message)