import pickle, os, music21
import numpy as np
from music21 import *
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import  LSTM, Bidirectional, Input
from tensorflow.keras.layers import Activation
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint, History





def load_network_weights(network_input, num_vocab):
    input_layer = Input(shape=(network_input.shape[1], network_input.shape[2]))
    hidden1 = LSTM(512, return_sequences=True)(input_layer)
    hidden2 = Dropout(0.3)(hidden1)
    hidden3 = LSTM(512, return_sequences=True)(hidden2)
    hidden4 = Dropout(0.3)(hidden3)
    hidden5 = LSTM(512)(hidden4)
    hidden6 = Dense(256)(hidden5)
    hidden7 = Dropout(0.3)(hidden6)
    output_layer = Dense(num_vocab, activation='softmax')(hidden7)
    
    model = Model(input_layer, output_layer)
    model.load_weights('models//pokemon_model//pokemon_weights.hdf5')
    
    return model 
    
    

# prepare sequences to be given to the network for a prediction
def create_sequences(notes, pitch_names, num_vocab):
    
    """ Prepare the sequences used by the Neural Network """
    # map between notes and integers and back
    note_to_int = dict((note, number) for number, note in enumerate(pitch_names))

    # define sequence length of 100
    sequence_length = 100
    # empty list for network input
    network_input = []
    # empty list for output
    output = []
    # from 0 to one element before len(notes - sequence_length)
    # in increments of 1
    for i in range(0, len(notes) - sequence_length, 1):
        # sequence of length 100 from i to one element before i + sequence_length
        # in notes list
        sequence_in = notes[i:i + sequence_length]
        # sequence out is a single note that is the one right after
        # sequence_in
        sequence_out = notes[i + sequence_length]
        # network_input is int represenation of notes and chords from
        # sequence_in
        network_input.append([note_to_int[char] for char in sequence_in])
        # int representation of note or chord from sequence_out
        output.append(note_to_int[sequence_out])

    # number of patterns eq length of network_input
    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    normalized_network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    # normalize input
    normalized_network_input = normalized_network_input / float(num_vocab)

    return (network_input, normalized_network_input)


def sample_with_temperature(probabilities, temperature):
    # temperature ->  infinity - complete random value
    # temperature -> 0 - the highest probabilty gets picked
    # temperature = 1 - we just use a normal sampling, nothing changes

    predictions = np.log(probabilities) / temperature
    probabilities = np.exp(predictions) / np.sum(np.exp(predictions))
    probabilities = probabilities.flatten()

    choices = range(len(probabilities)) # [0, 1, 2, 3]
    index = np.random.choice(choices, p=probabilities)

    return index

#generate notes based on the given sequence
def predict_notes(model, network_input, pitch_names, num_vocab, num_steps, temperature):
    """ Generate notes from the neural network based on a sequence of notes """
    # pick a random sequence from the input as a starting point for the prediction
    # value from 0 to length of input - 1
    start = np.random.randint(0, len(network_input)-1)

    # create dict with key int and value note
    int_to_note = dict((number, note) for number, note in enumerate(pitch_names))
    
    # pattern is the randomly chosen starting point in the input
    pattern = network_input[start]
    # empty list for prediction output
    prediction_output = []

    # generate 500 notes
    # from 0 - 499
    for note_index in range(num_steps):
        # input is the pattern chosen from some random starting point
        # reshaped for LSTM
        prediction_input = np.reshape(pattern, (1, len(pattern), 1))
        # normalize input
        prediction_input = prediction_input / float(num_vocab)

        # form prediction from model
        prediction = model.predict(prediction_input, verbose=0)
        
        index = sample_with_temperature(prediction,temperature)

        # get max value from prediction for index
       # index = np.argmax(prediction)
        # the result is the note at index
        result = int_to_note[index]

        # append result to prediction_output list       
        prediction_output.append(result)

        # pattern appends index
        pattern.append(index)
        # pattern equals pattern from 1 to length of pattern
        pattern = pattern[1:len(pattern)]
    

    return prediction_output

def remove_generated_midis():
    exclude = set(['env'])
    for root, dirs, files in os.walk(os.getcwd()):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            if file[-4:] == '.mid':
                # print(os.path.join(root, file))
                os.remove(os.path.join(root, file))


def generate_midi(prediction_output, name, key_signature):
    
    """ convert the output from the prediction to notes and create a midi file
        from the notes """
        
    remove_generated_midis()
    offset = 0
    output_notes = []

    # create note and chord objects based on the values generated by the model
    for pattern in prediction_output:
        # pattern is a chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        # pattern is a note
        else:
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        # increase offset each iteration so that notes do not stack
        offset += 0.5
    
    midi_stream = stream.Stream(output_notes)
    
    
    key  = midi_stream.analyze('key')
    interval = music21.interval.Interval(key.tonic, music21.pitch.Pitch(key_signature))
    transposed_song = midi_stream.transpose(interval)
    
    transposed_song.write('midi', fp=name)
    
    
    
def generate_pokemon(n_steps, temperature, file_name='untitled', key_signature='C'):
    
    with open('models//pokemon_model//pokemon_notes', 'rb') as fp:
        notes = pickle.load(fp)

    pitchnames = sorted(set(item for item in notes))

    n_vocab = len(set(notes))

    network_input, normalised_input = create_sequences(notes, pitchnames, n_vocab)

    model = load_network_weights(normalised_input, n_vocab)
    
    
    prediction_output = predict_notes(model, network_input, pitchnames, n_vocab, n_steps, temperature)
    
    file_name+='.mid'
    generate_midi(prediction_output, file_name, key_signature)
  
  
  
if __name__ == "__main__":
  generate_pokemon(130, 1.0,'pokemon', 'D')

  