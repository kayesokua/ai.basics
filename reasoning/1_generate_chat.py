from helpers import input_with_choices, input_with_unique_choices
import random
import uuid
import json
from datetime import datetime
import time

def load_movement_vocabulary():
    with open("vocabulary.json", "r") as f:
        movement_vocabulary = json.load(f)
    return movement_vocabulary

def load_techniques_list():
    techniques_list = []
    for k, v in movement_vocabulary.items():
        techniques_list.append(k)
    return techniques_list

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

        statement = f"For practicing {technique} as a {expertise} performer, the recommended warm-up exercises are {', '.join(exercises)} for {intensity[0]}. After warming up, you should practice the following instructions: {', '.join(instructions)} for {intensity[0]}. Since you want to particularly focus on {session_data['focus'][0]}, additional exercises could include {', '.join(focus_exercises)}."

        recommendations.append(statement)

    session_data["recommendations"] = recommendations

    with open(f"data/{session_id}.json", "w") as f:
        json.dump(session_data, f, indent=4)

    return recommendations

# Just for demonstration purposes
# session_id = create_user_session(questions, choices)
# print(f"Your session ID is {session_id}.")
# recommendations = generate_recommendation(session_id)
# time.sleep(5)
# print("Generating recommendations...")
# time.sleep(5)
# print(f"The recommendations for {session_id}:")
# print(recommendations)