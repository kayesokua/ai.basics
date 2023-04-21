import pulp
import json

def load_intstructors_data():
    with open("data/instructors.json") as f:
        instructors_data = json.loads(f.read())
    return instructors_data

instructors = load_intstructors_data()


requirements = {
    "expertise": {
        "Contemporary": 3,
        "Ballet": 3,
        "Choreography-Improvisation": 1,
        "Graham-Based Modern": 1,
        "Body Conditioning": 1,
        "Jazz": 1
    },
    "rate_per_hour": 55,
    "ratings": 4,
    "tenure": 2,
    "availability": [1, 2, 3, 4, 5]

}

def solve_optimal_instructor_lp(instructors, requirements):
    prob = pulp.LpProblem("Optimal Instructor", pulp.LpMinimize)

    # Decision variables
    x = pulp.LpVariable.dicts("instructor", instructors.keys(), 0, 1, pulp.LpInteger)

    # Objective function
    prob += pulp.lpSum([x[i] * instructors[i]["rate_per_hour"] for i in instructors])

    # Constraints
    for req_expertise in requirements["expertise"]:
        prob += pulp.lpSum([x[i] * instructors[i]["expertise"].get(req_expertise, 0) for i in instructors]) >= requirements["expertise"][req_expertise]

    for i in instructors:
        prob += x[i] * instructors[i]["ratings"] >= requirements["ratings"] * x[i]
        prob += x[i] * instructors[i]["tenure"] >= requirements["tenure"] * x[i]
        prob += pulp.lpSum([x[i] * (day in instructors[i]["availability"]) for day in requirements["availability"]]) >= 1 * x[i]

    prob.solve()

    if pulp.LpStatus[prob.status] == "Infeasible":
        return False
    else:
        hiring_count = len([i for i in instructors if x[i].value() == 1])
        filtered_instructors = {
            "instructors":{
                i: instructors[i] for i in instructors if x[i].value() == 1
            },
            "cost": round(pulp.value(prob.objective) / hiring_count)
        }
    return filtered_instructors

filtered_instructors = solve_optimal_instructor_lp(instructors, requirements)
print(f"""
    Instructors that meets the requirements:
    Intructors: {filtered_instructors["instructors"].keys()}

    Objective Function: Lowest hiring count

    Hiring Count: {len(filtered_instructors["instructors"])}
    Rate per hour: {filtered_instructors["cost"]}
    Per Week: {filtered_instructors["cost"] * 10}
    """)