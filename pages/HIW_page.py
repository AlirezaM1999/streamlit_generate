
import streamlit as st




def hiw_page():
    with st.container():
        st.write('---')
        col1, col2 = st.columns((1.2, 1))
        with col1:
            st.header("Artificial Neural Networks")
            st.markdown(
                """
                    <p1 style="font-size:20px;">
                    Neural Networks Form the base of deep learning, A subfield of machine learning where the alogrithms are inspired by the structure of the human brain. 
                    Neural networks take in data and train themselves to recoginise the patterns and predict the output for new sets of data.
                    </p1> 
                    </br>
                    </br>
                    </br>
                    <p1 style="font-size:20px;">
                    Neural Networks are made of layers of neurons. The neurons are the core processing units of the network. The first layer of the network is the input layer which recives the input data.
                    The output layer predicts our final output. In between, There are hidden layers which perform most of the computation. The ouput for each layer is passed as input for the next layer
                    until we reach the final layer. 
                    </p1>  
                    """, unsafe_allow_html=True)

        with col2:
            st.image('images/neural_nerworks.png')

    st.text('')
    st.write('---')
    

    with st.container():
        st.header("Types Of Neural Networks")
        st.markdown(
            """
            <p1 style="font-size:20px;">
            Technology is moving very fast specially in deep learning as new techniques and tools are developed everyday. while there are many types of neural networks, There are 3 common types;
            <b>Artificial Neural Networks(ANN)</b>, <b>Convolutional Neural Networks (CNN)</b> and <b>Recurrent Neural</b>. ANN is the classic neural network that was discussed. ANNs are versitile allround and used 
            in a variety of fields in deep learning. CNNs mainly prevellent image and video processing. CNNs have filters which extract the common features from images which are then used to 
            classify images. 
            </p1>  
            </br>
            </br>

            """, unsafe_allow_html=True)

        col1, col2 = st.columns((1, 2))
        with col1:
            st.image('images/nn_structure.png', width=550,
                    caption='A Basic Neural Networks Structure')
        with col2:
            st.image('images/cnn.jpeg', width=600,
                    caption='Convolutional Neural Network')

        st.write('')
        st.write('---')

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.header('Why Reucrrent Neural Networks?')

            st.markdown(
                """
                <p1 style="font-size:20px;">
                RNNs were created due to a few limitations in Feed Forward Neural networks:
                <ol>
                    <li>Feed-forward neural networks are not efficient enough to handle large amounts of sequential data</li>
                    <li>Feed-forward neural networks considers all datapoints independent therefore only consider the current input</li>
                    <li>Feed-forward neuralnetworks do not have a memory mechnism to deal with depedent datapoints like sequential data</li>
                </ol> 
                </p1>  
                """, unsafe_allow_html=True)

            st.text('')
            st.text('')
            st.text('')
            st.subheader('How Does Recurrent Neural Netowork Work? ')
            st.markdown(

                """
                <p1 style="font-size:20px;">
                Reccurent Neural Networks are desinged to deal with sequential data. This can be things such as weather forecast, text or musical notes where each datapoint dependent on its other datapoints.
                This is unlike CNNs and ANNs where datapoints are indepdent. RNNs are specially good for sequential data as they have sequential memory. RNNs have a looping  mechanism that acts a highway to allow information to flow
                from one step to the next which is called <b>hidden state </b>. This allows them to remmeber information about privious datapoints which subsequently determines the outcome for the next datapoint.
                </p1>
                """, unsafe_allow_html=True)

        with col2:
            for _ in range(17):
                st.text('')
            st.image('images/rnn_pics.gif', width=850,
                    caption='Working of Reucurrent Neural Network')

    st.write('---')

    with st.container():
        col1, col2 = st.columns(2)

        st.header("Music Generation Using Recurrent Neural Networks")
        st.markdown(
            """
            <p1 style="font-size:20px;">
            Melody consists of a sequence of notes and rests. Because of this , we can take a melody and transform it to a time series representation. <b>Time series</b> is a sequential data structure where we have samples 
            that are taken at equally spaced position in time.After the transformation, melody generation problem is now a time series prediction problem. Reuccrrent neural networks are the most effective way  
            time series prediction problems there we will use RNN to generate the next note given a melody.
            </p1>
            </br>
            </br> 
            <p1 style="font-size:20px;">
            Once the model is trained, we start with a seed melody. The seed melody is a set of beginning notes that we feed in to our trained network in order to predict the next note in melody. You can specify the number of steps
            you want the model to predict which ultimatly defines the length of your generated melody. 
            </p1> 

            """, unsafe_allow_html=True)
        st.text('')
        st.text('')
        col1, col2 = st.columns((1.2, 1))
        with col1:
            st.image('images/melody_rnn.png', width=800,
                    caption='we pass sets of songs and melodies to train our neural network. Network gradually learns to predict the next note when given a set of notes')
        with col2:
            st.image('images/predict.png', width=800, caption='The predicted note is then appended to the seed melody and then fed back in to the network to predict the next note. this process happens with same number of steps the user has specified')

        st.text('')