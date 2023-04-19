import random
import json
import numpy as np

program_topics = ['Ballet', 'Contemporary', 'Choreography-Improvisation', 'Graham-Based Modern', 'Body Conditioning', 'Jazz']
instructors = {}

def generate_mock_instructors(size):
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

generate_mock_instructors(size=100)
