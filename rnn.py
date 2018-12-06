

from __future__ import print_function

import matplotlib.pyplot as plt
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Bidirectional,Concatenate
import numpy as np
import Util
import itertools


batch_size = 64  # Batch size for training.
epochs = 10  # Number of epochs to train for.
latent_dim = 256  # Latent dimensionality of the encoding space.
# Path to the data txt file on disk.
data_path = 'fra-eng/fra.txt'

# Vectorize the data.
input_texts = Util.get_name_input()
target_texts = Util.get_wordbet_output()

name = open('name.txt').read().lower()
word_bet = open('no_c.txt').read().lower()

english_chars = sorted(list(set(name)))
wordbet_chars = sorted(list(set(word_bet)))


wordbet_chars.append('\t')

input_characters = english_chars
target_characters = wordbet_chars


temp_input_char = sorted(list(input_characters))
temp_output_char = sorted(list(target_characters))

input_characters = []
target_characters = target_characters

for r in list(itertools.product(temp_input_char, temp_input_char)):
    input_characters.append(''.join(r))



num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)
max_encoder_seq_length = max([len(txt) for txt in input_texts])-1
max_decoder_seq_length = max([len(txt) for txt in target_texts])


input_token_index = dict(
    [(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict(
    [(char, i) for i, char in enumerate(target_characters)])


encoder_input_data = np.zeros(
    (len(input_texts), max_encoder_seq_length, num_encoder_tokens),
    dtype='float32')
decoder_input_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens),
    dtype='float32')
decoder_target_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens),
    dtype='float32')

for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):

    for t in range(0, len(input_text)):
        if t == len(input_text)-1: break
        char = input_text[t]
        nextChar = input_text[t+1]
        encoder_input_data[i, t, input_token_index[char + nextChar]] = 1.
    for t, char in enumerate(target_text):
        # decoder_target_data is ahead of decoder_input_data by one timestep
        decoder_input_data[i, t, target_token_index[char]] = 1.
        if t > 0:
            # decoder_target_data will be ahead by one timestep
            # and will not include the start character.
            decoder_target_data[i, t - 1, target_token_index[char]] = 1.

# Define an input sequence and process it.
encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder = Bidirectional(LSTM(latent_dim, return_state=True))
encoder_outputs, forward_h, forward_c, backward_h, backward_c = encoder(encoder_inputs)
# We discard `encoder_outputs` and only keep the states.
state_h = Concatenate()([forward_h, backward_h])
state_c = Concatenate()([forward_c, backward_c])
encoder_states = [state_h, state_c]

# Set up the decoder, using `encoder_states` as initial state.
decoder_inputs = Input(shape=(None, num_decoder_tokens))
# We set up our decoder to return full output sequences,
# and to return internal states as well. We don't use the
# return states in the training model, but we will use them in inference.
decoder_lstm = LSTM(latent_dim*2, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs,
                                     initial_state=encoder_states)
decoder_dense = Dense(num_decoder_tokens, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Define the model that will turn
# `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Run training
model.compile(optimizer='rmsprop', loss='categorical_crossentropy')
history = model.fit([encoder_input_data, decoder_input_data], decoder_target_data,
          batch_size=batch_size,
          epochs=epochs,
          validation_split=0.1)

# Save model
model.save('s2s.h5')

# Next: inference mode (sampling).
# Here's the drill:
# 1) encode input and retrieve initial decoder state
# 2) run one step of decoder with this initial state
# and a "start of sequence" token as target.
# Output will be the next target token
# 3) Repeat with the current target token and current states

# Define sampling models
encoder_model = Model(encoder_inputs, encoder_states)

decoder_state_input_h = Input(shape=(latent_dim*2,))
decoder_state_input_c = Input(shape=(latent_dim*2,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_lstm(
    decoder_inputs, initial_state=decoder_states_inputs)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = Model(
    [decoder_inputs] + decoder_states_inputs,
    [decoder_outputs] + decoder_states)

# Reverse-lookup token index to decode sequences back to
# something readable.
reverse_input_char_index = dict(
    (i, char) for char, i in input_token_index.items())
reverse_target_char_index = dict(
    (i, char) for char, i in target_token_index.items())

loss_values = []

def decode_sequence(input_seq):
    # Encode the input as state vectors.
    states_value = encoder_model.predict(input_seq)

    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    # Populate the first character of target sequence with the start character.
    target_seq[0, 0, target_token_index['\t']] = 1.

    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict(
            [target_seq] + states_value)

        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence += sampled_char

        # Exit condition: either hit max length
        # or find stop character.
        if (sampled_char == '\n' or
           len(decoded_sentence) > max_decoder_seq_length):
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.

        # Update states
        states_value = [h, c]

    return decoded_sentence


for seq_index in range(100):
    # Take one sequence (part of the training set)
    # for trying out decoding.
    input_seq = encoder_input_data[seq_index: seq_index + 1]
    decoded_sentence = decode_sequence(input_seq)
    print('-')
    print('Input sentence:', input_texts[seq_index].strip())
    print('Decoded sentence:', decoded_sentence)





while True: 
    while True:
        user = input('Enter Your Name: ')
        if not user is None: 
            break
    if user == 'exit': 
        break
    print('-')
    user = user.strip().lower() + '\n'
    print('Input Name:', user)
    appendList = []
    appendList.append(user)
    print (appendList)
    cur_input_data = np.zeros((1, max_encoder_seq_length, num_encoder_tokens),dtype='float32')

    for t in range(0, len(user)):
        if t == len(user)-1: break
        char = user[t]
        nextChar = user[t+1]
        cur_input_data[0, t, input_token_index[char + nextChar]] = 1.
    
    print('Output Name: ', decode_sequence(cur_input_data))

loss_history = history.history['loss']
val_loss_history = history.history['val_loss']
fig, ax = plt.subplots()

plt.plot(val_loss_history, color='green', label='validation loss', linewidth=2, markersize=12)
plt.plot(loss_history, color='red', label='training loss', linewidth=2,  markersize=12)
ax.grid()

plt.title('Model Training & Validation Loss', fontsize=20)
plt.ylabel('0.0 < Loss < 1.4', fontsize=16)
plt.xlabel('0 < Epoch < 60', fontsize=16)
plt.legend(loc='lower left')

plt.show()

numpy_loss_history = np.array(val_loss_history)
# np.savetxt("Graphs/loss_history"+ epochs +".txt", numpy_loss_history, delimiter=",")



plt.savefig("graph.png")



