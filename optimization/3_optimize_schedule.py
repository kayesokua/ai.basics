import json
import random
import copy
from deap import base, creator, tools, algorithms


def load_instructors_data():
    with open("data/instructors_score.json", "r") as f:
        instructors_data = json.load(f)
    return instructors_data

instructors_data = load_instructors_data()

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

# Define the genetic algorithm parameters
POPULATION_SIZE = 100
GENERATIONS = 100
CROSSOVER_PROBABILITY = 0.5
MUTATION_PROBABILITY = 0.2

# Define the fitness function to maximize the total trust score
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

def evaluate_schedule(individual):
    # Convert the individual into a program schedule
    proposed_program_schedule = {}
    program_days = [1, 2, 3, 4, 5]
    classes_to_schedule = copy.deepcopy(individual)

    for day in program_days:
        day_classes = set()
        day_classes.add(classes_to_schedule.pop())
        day_classes.add(classes_to_schedule.pop())
        proposed_program_schedule[day] = day_classes

    # Get the recommended instructors for the program schedule
    recommended_instructors, total_trust_score = recommend_instructors_based_on_schedule(proposed_program_schedule)

    return (total_trust_score,)

# Define the genetic algorithm operators
toolbox = base.Toolbox()
toolbox.register("gene", random.choice, list(program_requirements.keys()))
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.gene, n=len(program_requirements)*2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate_schedule)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Run the genetic algorithm
population = toolbox.population(n=POPULATION_SIZE)
for gen in range(GENERATIONS):
    offspring = algorithms.varAnd(population, toolbox, CROSSOVER_PROBABILITY, MUTATION_PROBABILITY)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(offspring, k=len(population))
    top_schedule = tools.selBest(population, k=1)[0]
    top_trust_score = top_schedule.fitness.values[0]
    print(f"Generation {gen+1}: Best trust score = {top_trust_score}")

# Get the final recommended schedule and instructors
proposed_program_schedule = {}
program_days = [1, 2, 3, 4, 5]
classes_to_schedule = copy.deepcopy(top_schedule)

for day in program_days:
    day_classes = set()
    day_classes.add(classes_to_schedule.pop())
    day_classes.add(classes_to_schedule.pop())
    proposed_program_schedule[day] = day_classes

recommended_instructors, total_trust_score = recommend_instructors_based_on_schedule(proposed_program_schedule)

# Convert sets to lists
proposed_program_schedule = {k: list(v) for k, v in proposed_program_schedule.items()}
for day in recommended_instructors:
    for style in recommended_instructors[day]:
        recommended_instructors[day][style] = list(recommended_instructors[day][style])

# Dump data to JSON
with open('data/final_proposed_schedule.json', 'w') as f:
    json.dump({'proposed_schedule': proposed_program_schedule,
               'recommended_instructors': recommended_instructors,
               'total_trust_score': total_trust_score}, f, indent=4)