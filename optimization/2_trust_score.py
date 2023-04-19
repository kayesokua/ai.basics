import json

def trust_score(expertise, tenure, ratings, cost_index, max_cost_index):
    """
    Calculate the trust score for an instructor based on expertise, tenure, ratings, and cost.
    The weight reflects the importance of each factor, which is dependent on the business.
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

generate_trust_score(json_data="data/instructors.json")