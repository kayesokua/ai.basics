import json

def load_intstructors_data():
    with open("data/instructors.json") as f:
        instructors_data = json.loads(f.read())
    return instructors_data

instructors = load_intstructors_data()

requirements = {
    # First Constraint: Minimum Requirements
    "schedule": {
        1: {"Ballet": [], "Contemporary": []},
        2: {"Graham-Based Modern": [], "Jazz": []},
        3: {"Contemporary": [], "Jazz": []},
        4: {"Ballet": [], "Contemporary": []},
        5: {"Body Conditioning": [], "Choreography-Improvisation": []},
    },
    # Second Constraint: Someone who can teach a certain quality
    "expertise": {
        "Contemporary": 3,
        "Ballet": 3,
        "Choreography-Improvisation": 3,
        "Graham-Based Modern": 1,
        "Body Conditioning": 1,
        "Jazz":1
    },
    # Third Constraint: Someone well-liked
    "ratings": 4,

    # Fourth Constraint: Someone we know
    "tenure": 2,

}

def filter_available_instructors(requirements):
    available_instructors = {day: {subject: [] for subject in subjects} for day, subjects in requirements["schedule"].items()}
    for day, subjects in requirements["schedule"].items():
        for subject in subjects:
            if subjects[subject] != '':
                for instructor in instructors:
                    if day in instructors[instructor]["availability"] and subject in instructors[instructor]["expertise"]:
                        available_instructors[day][subject].append(instructor)
    return available_instructors

def filter_instructors_by_subject_expertise(requirements):
    filtered_instructors = {subject: [] for subject in requirements["expertise"]}
    for instructor in instructors:
        expertise = instructors[instructor]["expertise"]
        for subject in filtered_instructors:
            if expertise.get(subject, 0) >= requirements["expertise"][subject]:
                filtered_instructors[subject].append(instructor)
    return filtered_instructors

available_instructors = filter_available_instructors(requirements)
expertise_instructors = filter_instructors_by_subject_expertise(requirements)

print(f"""
    Number of instructors that are available:
    Day 1: {len(available_instructors[1]['Ballet']), len(available_instructors[1]['Contemporary'])}
    Day 2: {len(available_instructors[2]['Graham-Based Modern']), len(available_instructors[2]['Jazz'])}
    Day 3: {len(available_instructors[3]['Contemporary']), len(available_instructors[3]['Jazz'])}
    Day 4: {len(available_instructors[4]['Ballet']), len(available_instructors[4]['Contemporary'])}
    Day 5: {len(available_instructors[5]['Body Conditioning']), len(available_instructors[5]['Choreography-Improvisation'])}
    """)

print(f"""
    Number of instructors that meets the skill requirements:
    Contemporary: {len(expertise_instructors['Contemporary'])}
    Ballet: {len(expertise_instructors['Ballet'])}
    Choreography-Improvisation: {len(expertise_instructors['Choreography-Improvisation'])}
    Graham-Based Modern: {len(expertise_instructors['Graham-Based Modern'])}
    Body Conditioning: {len(expertise_instructors['Body Conditioning'])}
    Jazz: {len(expertise_instructors['Jazz'])}
""")

def filter_available_experts(available_instructors, expertise_instructors):
    filtered_list = {}
    for day, subjects in available_instructors.items():
        filtered_list[day] = {}
        for subject, instructors in subjects.items():
            if subject in expertise_instructors.keys():
                filtered_instructors = list(set(instructors).intersection(set(expertise_instructors[subject])))
                filtered_list[day][subject] = filtered_instructors
            else:
                filtered_list[day][subject] = []
    return filtered_list

available_experts = filter_available_experts(available_instructors, expertise_instructors)

def filter_available_experts_by_tenure_ratings_and_cost(requirements, available_experts):
    hourly_rates = {instructor: instructors[instructor]["rate_per_hour"] for instructor in instructors}
    filtered_experts = {}
    day_costs = {day: 0 for day in available_experts}
    for day, expertises in available_experts.items():
        filtered_experts[day] = {}
        for expertise, instructors_list in expertises.items():
            filtered_instructors = []
            for instructor in instructors_list:
                tenure = instructors[instructor]["tenure"]
                rating = instructors[instructor]["ratings"]
                if tenure >= requirements["tenure"] and rating >= requirements["ratings"]:
                    filtered_instructors.append(instructor)
            if filtered_instructors:
                selected_instructor = min(filtered_instructors, key=lambda x: hourly_rates[x])
                filtered_experts[day][expertise] = [selected_instructor]
                day_costs[day] += hourly_rates[selected_instructor]
    total_cost = sum(day_costs.values())

    return filtered_experts, day_costs, total_cost

filtered_experts, day_costs, total_cost = filter_available_experts_by_tenure_ratings_and_cost(requirements, available_experts)

unique_hires = set()
for day, expertises in filtered_experts.items():
    for instructors_list in expertises.values():
        unique_hires.update(instructors_list)

print(f"""
    Proposed Hires:

    {filtered_experts}

    Unique Hires: {len(unique_hires)}

    Rate per day: {day_costs}
    *note* day 4 is taught by the same instructor

    Per Week: {total_cost + 59}
    """)