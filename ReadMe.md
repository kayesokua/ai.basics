# Artificial Intelligence Basic Applications

This repository contains a variety of basic applications of artificial intelligence in different areas, for the purpose of learning. The applications have been specifically developed with the dance industry in mind.

## Reasoning: Training Recommendation

The recommendation chatbot helps users pick the right exercises based on the techniques they want to learn, their skill level, focus, and intensity level. The chatbot uses a decision tree model to learn patterns and relationships between these inputs and recommendations. Once trained, the model can make predictions for new inputs, recommending the appropriate exercises based on what it has learned from previous user sessions.

**To run this application:**

```terminal
cd/reasoning

# Create chat session
python 1_generate_chat.py

# Train the model based on the session data available
python 2_decision_tree.py
```

## Optimization: Schedule Optimization

The schedule optimizer generates multiple proposed schedules that meets program requirements and recommends the top 2 most trusted instructor available. The trust scoring system is based on expertise, tenure, ratings, and cost with different weight which represents priorities of the business. This AI application utilizes a genetic algorithm to optimize a program schedule based on program requirements and instructor expertise and availability, with the goal of maximizing the total trust score.

**To run this application:**

```terminal
cd/optimization

# To generate mock data
python 1_mock_data.py

# To generate score based on formulated trust score
python 2_trust_score.py

# To generate the best schedule based on available instructors
python 3_optimize_schedule.py
```

## Planning: Sequence Generator

*Writing soon*

## Machine Learning

*Writing soon*
