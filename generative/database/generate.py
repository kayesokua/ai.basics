X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
np.random.seed(42)
tf.random.set_seed(42)

model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2])),
    tf.keras.layers.Dense(len(all_moves), activation='softmax')
])
model.compile(loss='categorical_crossentropy', optimizer='adam')
model.fit(X_train, y_train, epochs=10, validation_data=(X_val, y_val))

# Generate new dance sequences
seed_sequence = [...]  # Seed sequence to start the generation
desired_length = ...  # Desired length of the generated sequence

generated_sequence = seed_sequence.copy()
while len(generated_sequence) < desired_length:
    last_move = generated_sequence[-1]
    input_seq = np.array([one_hot_dict[last_move]])
    output_prob = model.predict(input_seq)[0]
    next_move_idx = np.argmax(output_prob)
    next_move = all_moves[next_move_idx]
    if next_move not in sequence["blacklist"]:
        generated_sequence.append(next_move)