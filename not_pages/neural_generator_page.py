
import streamlit as st
from models.pokemon_model.pokemon_model import generate_pokemon
from models.beethoven_model.beethoven_model import generate_beethoven
from models.folk_model.folk_model import generate_folk
from models.lofi_model.lofi_model import generate_lofi
import numpy as np
import pretty_midi
import io
from scipy.io import wavfile
import time




def generate_melody(Login, user, storage, db):
    
    st.title('Neural Generator')
    st.text(
        'Select your preference and get your free AI generated melody')
  

    form = st.form(key='submit-form')
    file_name = form.text_input('Select a unique name for your file', placeholder='Name',
                                help='The name must be unique to prevent the file from being overidden if you generate a file with the same name')
    genre = form.selectbox(
        'Genre', options=['Classic', 'Gaming', 'Folk', 'Lofi'])
    num_steps = form.slider('Number of steps to predict', min_value=1, value=200, step=10, max_value=400,
                            help='The number of musical steps you want the model the predict, the higher the number of steps, the longer the melody is going to be. You can think of this as the number of notes you want the model to predict from the start')
    key_sig = form.selectbox('Key Signature', options=[
                            'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'])
    predictability = form.number_input('Temperature - The lower the number, the less predictable the generated output will be', min_value=0.1, max_value=1.0, step=0.1, value=0.8,
                                    help='Temperature determines the rate at which the model picks the highest probabilistic output, i.e if the temperature is 0.8, theres an %80 chance that the model is going pick the output with the highest probability')
    generate_button = form.form_submit_button('Generate')

    if generate_button:
        if not file_name:
            st.error('Please enter a name')
        else:
            with st.spinner('Generating'):

                if genre == 'Classic':
                    generate_beethoven(
                        file_name=file_name, n_steps=num_steps, temperature=predictability, key_signature=key_sig)
                elif genre == 'Gaming':
                    generate_pokemon(
                        file_name=file_name, n_steps=num_steps, temperature=predictability, key_signature=key_sig)
                elif genre == 'Folk':
                    generate_folk(
                        file_name=file_name, n_steps=num_steps, temperature=predictability, key_signature=key_sig)
                elif genre == 'Lofi':
                    generate_lofi(
                        file_name=file_name, n_steps=num_steps, temperature=predictability, key_signature=key_sig)

                midi_data = pretty_midi.PrettyMIDI(
                    file_name+'.mid')
                audio_data = midi_data.synthesize()
                audio_data = np.int16(
                    audio_data /
                    np.max(np.abs(audio_data)) * 32767 * 0.9
                )   # -- Normalize 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py

                audio_file = io.BytesIO()
                wavfile.write(audio_file, 44100, audio_data)
                st.audio(audio_file)

                with open(file_name+'.mid', 'rb') as fp:
                    btn = st.download_button(
                        label='Download Midi File',
                        data=fp,
                        file_name=f'{file_name}.mid'

                    )

    if st.button('Save File'):

        if file_name:
            if Login:
                uid = user['localId']
                fireb_upload = storage.child(
                    uid+'_'+file_name+'.mid').put(file_name+'.mid', user['idToken'])
                stored_file = storage.child(
                    uid+'_'+file_name+'.mid').get_url(fireb_upload['downloadTokens'])
                db.child(uid).child('Audio_Files').push(stored_file)
                st.success('Done!')
                time.sleep(0.4)
                st.experimental_rerun()

            else:
                st.error('Please login to save your files')

        else:
            st.error('Please generate a file first')