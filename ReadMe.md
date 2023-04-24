# Artificial Intelligence Basic Applications

This repository contains a variety of basic applications of artificial intelligence in different areas, for the purpose of learning. The applications have been specifically developed with the dance industry in mind.

## Reasoning: Training Recommendation

The recommendation chatbot helps users pick the right exercises based on the techniques they want to learn, their skill level, focus, and intensity level. The chatbot uses a decision tree model to learn patterns and relationships between these inputs and recommendations. The model predicts the recommendation based on the best matching label found using the Jaccard similarity.

**To run this application:**

```terminal
cd/reasoning

# Generate random chats with generated recomendations
python seed.py

# Generate recommendation based on keyword
python chat.py
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

## Generative: Sequence Generator

The Choreography Planner app generates personalized dance sequences based on user-defined settings such as known movements, blacklisted movements, mood, and learning goals. The app uses a rule-based algorithm and can generate new sequences based on past choices using an LSTM model, promoting "dancing from memory". This results in new, customized dance sequences that match the user's preferences without requiring constant manual input.

```terminal
cd /generative

# To initialize the planner and generate mock dance sessions
python planner.py

# To extract features from succesful history
python 1-extract-features.py

# To create a model using supervised learning
python 2-model.py

# To predict/generate new sequences from memory
python 3-model.py
```

## Machine Learning

The dance classifier system predicts the dance style of a new video using the YouTube API. The videos are labeled based on a keyword search, and pose features are extracted from frames that are detected using Media Pipe. The system utilizes the pre-trained MobileNetV2 network and a decision tree classifier for modeling.

```terminal
cd /machine-learning

# To download YouTube videos using a keyword search:
# Please make sure to use your own credentials in keyfile.json
python 1-downloader.py

# To extract pose features from the downloaded videos:
python 2-extract-features.py

# To train the model and predict the dance style:
python 3-classifier.py
```
