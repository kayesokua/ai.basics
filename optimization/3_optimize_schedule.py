import json
import random

# Load instructor data from json file
with open('data/instructors_score.json', 'r') as f:
    instructors_data = json.load(f)

def get_top3_experts_per_day(dance_style, day, data=instructors_data):
    available_instructors = [(k, v) for k, v in data.items() if dance_style in v['expertise'] and day in v['availability']]
    if available_instructors:
        return sorted(available_instructors, key=lambda x: x[1]['trust_score'][dance_style], reverse=True)[:5]
    return []

def create_program_schedule(program_requirements):
    """A recursive function that creates a program schedule based on the program requirements."""
    proposed_program_schedule = {}
    program_days = [1, 2, 3, 4, 5]
    classes_to_schedule = []

    for dance_style, num_classes in program_requirements.items():
        for i in range(num_classes):
            classes_to_schedule.append(dance_style)

    while True:
        random.shuffle(classes_to_schedule)
        valid_schedule = True
        for day in program_days:
            day_classes = set()
            day_classes.add(classes_to_schedule.pop())
            day_classes.add(classes_to_schedule.pop())
            if len(day_classes) < 2:
                valid_schedule = False
                return create_program_schedule(program_requirements)
            proposed_program_schedule[day] = day_classes
        if valid_schedule:
            break

    return proposed_program_schedule

def recommend_instructors_based_on_schedule(schedule, data=instructors_data):
    instructors_scores = {}
    for instructor, values in data.items():
        instructors_scores[instructor] = sum(values['trust_score'].values())

    top2_experts = {}
    for day, classes in schedule.items():
        top2_experts[day] = {}
        for dance_style in classes:
            available_instructors = [(k, v) for k, v in data.items() if dance_style in v['expertise'] and day in v['availability']]
            if available_instructors:
                instructors_scores_subset = {k: v for k, v in instructors_scores.items() if k in [i[0] for i in available_instructors]}
                instructors_ranking = sorted(available_instructors, key=lambda x: instructors_scores_subset[x[0]], reverse=True)[:2]
                top2_experts[day][dance_style] = [instructor[0] for instructor in instructors_ranking]

    total_trust_score = 0
    for k, v in top2_experts.items():
        for k1, v1 in v.items():
            total_trust_score += sum([instructors_scores[i] for i in v1])

    return top2_experts, round(total_trust_score,2)

program_requirements = {'Ballet':2, 'Contemporary':3, 'Choreography-Improvisation':1, 'Graham-Based Modern': 2, 'Body Conditioning': 1, 'Jazz':1}


for i in range(3):
    recommended_schedule = create_program_schedule(program_requirements)
    print(recommended_schedule)
    recommended_instructors, score = recommend_instructors_based_on_schedule(recommended_schedule)
    print(recommended_instructors)

    with open(f'data/proposed_schedule_{score}.json', 'w') as f:
        json.dump(recommended_instructors, f)