import streamlit as st 




def show_account_page(Login, storage, user, db):
    
    if Login:
        if not user:  #if user ticks the checkbox before log in in account page 
            st.warning('Please login to see account information')
        else:
            st.write('---')
            st.subheader('Upload A File')
            uploaded_file = st.file_uploader('Choose a file')
            upload = st.button('Upload')

            if upload:
                try:

                    uid = user['localId']
                    fireb_upload = storage.child(uid+'_'+uploaded_file.name).put(
                        uploaded_file, user['idToken'])
                    stored_file = storage.child(uid+'_'+uploaded_file.name).get_url(
                        fireb_upload['downloadTokens'])
                    db.child(uid).child(
                        'Audio_Files').push(stored_file)
                    st.success('File successfully uploaded')

                except:
                    st.error('Please select a file to upload!')

            Audio = db.child(user['localId']).child('Audio_Files').get()
            file_choices = []

            st.write('---')
            st.subheader('A list of all your uploaded files')

            try:
                for i in Audio.each():
                    i_choice = i.val()
                    file_choices.append(i_choice)
                    st.write(i_choice)

                st.write('---')
                st.subheader('Delete A File')

                file_to_be_downloaded = st.selectbox(
                    'Select the file you would like to Delete', file_choices)
                # if st.button('Download'):
                #     webbrowser.open(file_to_be_downloaded)
                if st.button('Delete'):
                    for i in Audio.each():
                        if i.val() == file_to_be_downloaded:
                            db.child(user['localId']).child(
                                'Audio_Files').child(i.key()).remove()
                            st.experimental_rerun()

            except TypeError:
                st.info('No Files')

    else:
        st.warning('Please login to see account information')

