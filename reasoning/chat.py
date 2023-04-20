from app import load_session_data, load_techniques_list
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline

def jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

chat_sessions = load_session_data()

X = []
y = []

for chat_session in chat_sessions:
    techniques = chat_session['techniques']
    focus = chat_session['focus'][0]
    intensity = chat_session['intensity'][0]
    expertise = chat_session['expertise']
    for recommendation in chat_session['recommendations']:
        X.append(recommendation)
        y.append(f"{techniques[0]} {focus} {intensity} {expertise[0]}")

pipeline = make_pipeline(
    CountVectorizer(),
    DecisionTreeClassifier()
)
pipeline.fit(X, y)

# Example usage of the model to generate a response

while True:
    chat_input = input("What would you like to do?")

    # Example: "Fish roll"
    # Example: "Roll with stability"
    # Example: "pique turn with flexibility"

    keywords = chat_input.lower().split()

    # Create a list of possible technique and focus keywords
    technique_keywords = load_techniques_list()
    focus_keywords = {
        "stability": ["stability", "balance", "center", "core", "strength", "steadiness", "balance", "poise", "equilibrium", "firmness"],
        "flexibility": ["flexibility", "stretch", "stretching", "flex", "flexing"],
        "coordination": ["coordination", "control", "controlling", "timing", "harmony", "synchronization","collaboration", "organization"],
        "artistry": ["artistry", "expression", "expressing", "express", "style", "styling"],
        "amateur": ["basic", "beginner", "beginners", "beginning", "fundamentals"],
        "intermediate": ["experienced", "intermediate", "intermediates", "intermediary", "intermediating", "intermediation"],
        "advanced": ["professional", "expert", "industry"]
    }

    technique_words_split = []
    for technique in technique_keywords:
        technique_words_split.extend(technique.lower().split())

    # Find the technique and focus keywords in the user input
    match_found = []

    for keyword in keywords:
        for focus_key, focus_values in focus_keywords.items():
            if keyword in focus_values:
                match_found.append(focus_key)

        if keyword in technique_words_split:
            match_found.append(keyword)

    # Convert matchfound into a set of lowercase words
    matchfound_set = set(match_found)

    # Find the best matching label using Jaccard similarity
    best_label_index = -1
    max_similarity = 0

    for i, label in enumerate(y):
        label_set = set(label.lower().split())
        similarity = jaccard_similarity(matchfound_set, label_set)
        if similarity > max_similarity:
            max_similarity = similarity
            best_label_index = i

    if best_label_index != -1:
        best_recommendation = X[best_label_index]
        print(f"Here's my recommendation: {best_recommendation}")
    else:
        print(f"No instructions found for {chat_input}")