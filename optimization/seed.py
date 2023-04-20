import random
import json

program_topics = ['Ballet', 'Contemporary', 'Choreography-Improvisation', 'Graham-Based Modern', 'Body Conditioning', 'Jazz']
instructors = {}

def generate_mock_instructors(size):
    """
    Generate a list of instructors with expertise, rate, tenure, availability, and ratings.
    This represents the data collected by the hiring team.
    """
    instructors = {}

    for i in range(size):
        name = f"instructor_{i}"
        expertise = {}
        topics = random.sample(program_topics, 2)
        for topic in topics:
            expertise[topic] = random.randint(1, 8)
        rate_per_hour = round(random.uniform(50, 100))
        tenure = round(random.uniform(1, 5))
        availability = random.sample(range(1, 6), 3)
        if 1 in availability and 2 in availability:
            availability.remove(2)
        elif 5 in availability and 4 in availability:
            availability.remove(4)
        ratings = round(random.uniform(3, 5), 1)
        instructors[name] = {"expertise": expertise,
                            "rate_per_hour": rate_per_hour,
                            "tenure": tenure,
                            "availability": availability,
                            "ratings": ratings,
                            "trust_score": {}}

    # sort instructors from lowest to highest rate
    instructors = dict(sorted(instructors.items(), key=lambda x: x[1]["rate_per_hour"]))

    with open('data/instructors.json', 'w') as f:
        json.dump(instructors, f)

    return print(f"Generated {size} mock instructors")

def trust_score(expertise, tenure, ratings, cost_index, max_cost_index):
    """
    Calculate the trust score for an instructor based on expertise, tenure, ratings, and cost.
    The scoring system represents the business's priorities.
    """
    expertise_weight = 0.5
    tenure_weight = 0.25
    ratings_weight = 0.25
    cost_weight = 0.2 * ((max_cost_index - cost_index) / max_cost_index)
    return (expertise * expertise_weight) + (tenure * tenure_weight) + (ratings * ratings_weight) + (cost_weight)

def generate_trust_score(json_data):
    """Generate trust score for each instructor and subject expertise"""
    with open(json_data, 'r') as f:
        data = json.load(f)
    # Sort the instructors based on rate_per_hour in ascending order
    sorted_instructors = sorted(data.items(), key=lambda x: x[1]["rate_per_hour"])
    max_cost_index = len(sorted_instructors) - 1  # calculate the maximum cost index
    instructors_with_trust_score = {}
    for i, (instructor, info) in enumerate(sorted_instructors):
        trust_scores = {}
        for subject, expertise in info["expertise"].items():
            tenure = info["tenure"]
            ratings = info["ratings"]
            cost_index = i  # use the index of the instructor in the sorted list as the cost index
            trust = trust_score(expertise, tenure, ratings, cost_index, max_cost_index)
            trust_scores[subject] = trust
        info["trust_score"] = trust_scores
        instructors_with_trust_score[instructor] = info

    with open('data/instructors_score.json', 'w') as f:
        json.dump(instructors_with_trust_score, f)

    print(f"Generated trust score for {len(instructors_with_trust_score)} instructors")
    return instructors_with_trust_score

generate_mock_instructors(size=100)
generate_trust_score(json_data="data/instructors.json")