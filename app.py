from fileinput import filename
import streamlit as st 
from models.pokemon_model.pokemon_model import generate_pokemon
from models.beethoven_model.beethoven_model import generate_beethoven


st.title('Neural Generator')
st.text('AI that generates music melodies with a variety og genres')
st.markdown("""
            Find more information here""")



form = st.form(key='submit-form')
genre = form.selectbox('genre', options=['Classic', 'Gaming'])
file_name = form.text_input('What would you like your file to be named?', placeholder='Name')
num_steps = form.number_input('number of steps in 16th notes (Song length)',min_value=1, value=200, step=10)
predictability = form.number_input('predictibilty - the lower the number, the less preditable the generated output will be', min_value=0.1, max_value=1.0, step=0.1)
generate_button = form.form_submit_button('Generate')


    

if generate_button:
    if not file_name:
        st.error('Please enter a name')
    else:
        with st.spinner("Generating..."):
            
            match genre:
                case "Classic":
                    generate_beethoven(file_name=file_name,n_steps=num_steps, temperature=predictability)
                    with open(file_name+'.mid', 'rb') as fp:
                        btn = st.download_button(
                            label='Download Midi File', 
                            data = fp, 
                            file_name=f'{file_name}.mid'
                            
                        )
                case "Gaming":
                     generate_pokemon(file_name=file_name,n_steps=num_steps, temperature=predictability)
                     with open(file_name+'.mid', 'rb') as fp:
                        btn = st.download_button(
                            label='Download Midi File', 
                            data = fp, 
                            file_name=f'{file_name}.mid'
                            
                        )
                    


