import numpy as np
import tensorflow as tf
from database.dance.terms import all_moves
import random
from features import one_hot_encode_dance_move
from model import max_sequence_length, X_train

def generate_dance_sequence(model, seed_sequence, sequence_length, all_moves):
    generated_sequence = []

    # Convert seed_sequence to one_hot_encoded format
    input_sequence = np.array([one_hot_encode_dance_move(move) for move in seed_sequence])
    input_sequence = input_sequence.reshape((1, input_sequence.shape[0], input_sequence.shape[1]))

    for i in range(sequence_length):
        predicted_probs = model.predict(input_sequence)[0][-1]

        # Sample a dance move based on the predicted probabilities
        predicted_index = np.random.choice(len(all_moves), p=predicted_probs)
        predicted_move = all_moves[predicted_index]

        # Add the predicted dance move to the generated sequence
        generated_sequence.append(predicted_move)

        # Update the input sequence to include the new predicted dance move
        new_move_encoded = one_hot_encode_dance_move(predicted_move)
        input_sequence = np.append(input_sequence, new_move_encoded.reshape((1, 1, -1)), axis=1)
        input_sequence = input_sequence[:, -max_sequence_length:, :]  # Keep only the last max_sequence_length moves

    return generated_sequence

# Load the saved model
model = tf.keras.models.load_model("user1_dance_preferences.h5")

seed_sequence = random.choice(X_train)
seed_moves = [all_moves[np.argmax(move)] for move in seed_sequence]

generated_sequence_length = 10  # Set the desired length of the generated sequence
generated_sequence = generate_dance_sequence(model, seed_moves, generated_sequence_length, all_moves)

print("\nGenerated dance sequence:")
print(generated_sequence)