import os
import json
import numpy as np
import random
from database.dance.terms import all_moves
from extensions.synonyms import get_all_synonyms
from extensions.songs import recommend_song_by_mood
import os
import json


def generate_user_statistics(user_dir):
    history_memory = set()
    history_blacklist = set()
    history_mood = {}
    history_goal = {}
    successful_sequences = []
    total_entries = 0
    total_success = 0
    total_movements = 0
    for filename in os.listdir(user_dir):
        if filename.endswith(".json"):
            with open(f"database/user/{filename}") as f:
                session_data = json.load(f)

                mood = session_data["mood"]
                history_mood[mood] = history_mood.get(mood, 0) + 1
                goal = session_data["goal"]
                history_goal[goal] = history_goal.get(goal, 0) + 1

                if session_data["success"]:
                    history_memory.update(set(session_data["memory"]))
                    history_blacklist.update(set(session_data["blacklist"]))
                    successful_sequences.append(session_data["sequence"])
                    total_movements += int(len(session_data["sequence"]))
                    total_success += 1
                total_entries += 1

    user_statistics = {
        "total_dance_sessions": total_entries,
        "memory": {
            "total": len(history_memory),
            "rate": int(round(len(history_memory) / total_entries,0))
        },
        "blacklist": {
            "total": len(history_blacklist),
            "rate": int(round(len(history_blacklist) / total_entries,0))
        },
        "sequence": {
            "avg_movement": int(round(total_movements / total_entries,0)),
            "avg_set": int(round(total_movements / total_entries,0) / 8),
            "history": successful_sequences,
        },
        "mood": history_mood,
        "goal": history_goal
    }
    return user_statistics

def filter_choices(user_dir):
    blacklist = set()
    for filename in os.listdir(user_dir):
        if filename.endswith(".json"):
            with open(os.path.join(user_dir, filename), "r") as f:
                data = json.load(f)
                blacklist.update(set(data["blacklist"]))

    choices = [move for move in all_moves if move not in blacklist]
    return choices

def generate_possible_sequence_sets(user_dir):
    choices = filter_choices(user_dir)
    possible_sequences = []
    for i in range(1,6):
        for j in range(2000):
            random.shuffle(choices)
            new_set = random.sample(choices, k=8 * i)
            if new_set not in possible_sequences:
                possible_sequences.append(new_set)
    return possible_sequences


def generate_training_data(user_statistics, user_choices):
    X_train = []
    y_train = []
    limit = 1000
    mood_vocabulary = get_all_synonyms(user_statistics["mood"])

    if len(user_statistics["sequence"]["history"]) < limit:
        return []

    for i in range(limit):
        new_playlist = []
        while not new_playlist:
            new_playlist = recommend_song_by_mood(random.choice(mood_vocabulary))
        new_song = random.choice(new_playlist)
        old_sequence = np.random.choice(user_statistics["sequence"]["history"])
        new_sequence = random.sample(user_choices, k=user_statistics["sequence"]["avg_movement"])
        X_train.append(old_sequence)
        y_train.append(new_sequence)

    np.save("X_train.npy", X_train)
    np.save("y_train.npy", y_train)

    if len(X_train) != len(y_train):
        raise Exception("X_train and y_train are not the same length")

    return print(f"Training data generated, {len(X_train)} entries")


user_statistics = generate_user_statistics("database/user")
user_choices = filter_choices("database/user")
generate_training_data(user_statistics, user_choices)

