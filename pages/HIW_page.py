
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
                    Neural networks Form the basis of deep learning, A subfield of machine learning where the algorithms are inspired by the structure of the human brain. 
                    Neural networks take in data and train themselves to recognize the patterns and predict the output for new sets of data.
                    </p1> 
                    </br>
                    </br>
                    </br>
                    <p1 style="font-size:20px;">
                    Neural networks are made of layers of neurons. The neurons are the core processing units of the network. The first layer of the network is the input layer which receives the input data.
                    The output layer predicts our final output. In between, There are hidden layers which perform majority of the computation. The output for each layer is passed as input for the next layer
                    until we reach the final layer. 
                    </p1>  
                    """, unsafe_allow_html=True)

        with col2:
            st.image('images/neural_networks.png',width=520, caption= "https://levity.ai/blog/difference-machine-learning-deep-learning - (Wolfewicz, 2021)")

    st.text('')
    st.write('---')
    

    with st.container():
        st.header("Types Of Neural Networks")
        st.markdown(
            """
            <p1 style="font-size:20px;">
            Technology is moving very fast especially in deep learning as new techniques and tools are developed everyday. While there are many types of neural networks, there are 3 common types:
            <b>Artificial Neural Networks(ANN)</b>, <b>Convolutional Neural Networks (CNN)</b> and <b>Recurrent Neural Networks</b>. ANN is the classic neural network that was discussed. ANNs are versatile allround and used 
            in a variety of fields in deep learning. CNNs mainly prevalent image and video processing. CNNs have filters which extract the common features from the image data which are then used to 
            classify images. 
            </p1>  
            </br>
            </br>

            """, unsafe_allow_html=True)

        col1, col2 = st.columns((1,0.7))
        with col1:
            st.image('images/nn_structure.png', width=470,
                    caption='A Basic Neural Network Structure - https://towardsdatascience.com/designing-your-neural-networks-a5e4617027ed - (Shukla, 2019)')
        with col2:
            st.image('images/cnn.jpeg', width=530,
                    caption='Convolutional Neural Network -  https://towardsdatascience.com/a-comprehensive-guide-to-convolutional-neural-networks-the-eli5-way-3bd2b1164a53 - (Saha, 2018)')

        st.write('')
        st.write('---')

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.header('Why Recurrent Neural Networks?')

            st.markdown(
                """
                <p1 style="font-size:20px;">
                RNNs were created due to a few limitations in Feed Forward Neural networks:
                <ol>
                    <li>Feed-forward neural networks are not efficient enough to handle large amounts of sequential data</li>
                    <li>Feed-forward neural networks considers all datapoints independent therefore, they only consider the current input</li>
                    <li>Feed-forward neural networks do not have a memory mechanism to deal with long term dependencies found in sequential data</li>
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
                Recurrent Neural Networks are designed to deal with sequential data. This can be data such as weather forecast, text or musical notes where each datapoint is dependent on its other datapoints.
                This is unlike CNNs and ANNs where datapoints are indepdent. RNNs are especially good for sequential data as they have sequential memory. RNNs have a looping  mechanism that acts a highway to allow information to flow
                from one step to the next which is called the <b>hidden state </b>. This allows them to remember information about previous datapoints which subsequently determines the outcome for the next datapoint.
                </p1>
                """, unsafe_allow_html=True)

        with col2:
            for _ in range(18):
                st.text('')
            st.image('images/rnn_pics.gif', width=750,
                    caption='Workings of Recurrent Neural Networks - https://www.simplilearn.com/tutorials/deep-learning-tutorial/rnn - (Biswal, 2022)')

    st.write('---')

    with st.container():
        col1, col2 = st.columns(2)

        st.header("Music Generation Using Recurrent Neural Networks")
        st.markdown(
            """
            <p1 style="font-size:20px;">
            Melody consists of a sequence of notes and rests. This means we can take a melody and transform it to a time series representation. <b>Time series</b> is a form of sequential data where the samples 
            are taken at equally spaced position in time. After the transformation, melody generation problem is now a time series prediction problem. Recurrent neural networks are shown to be the most effective way for  
            time series prediction problems.
            </p1>
            </br>
            </br> 
            <p1 style="font-size:20px;">
            Once the model is trained, we start with a seed melody. The seed melody is a set of beginning notes that we feed in to our trained network in order to predict the next note in melody. You can specify the number of steps
            you want the model to predict which ultimately defines the length of your generated melody. 
            </p1> 

            """, unsafe_allow_html=True)
        st.text('')
        st.text('')
        col1, col2 = st.columns((1.2, 1))
        with col1:
            st.image('images/melody_rnn.png', width=700,
                    caption='We pass datasets of MIDI files to train our neural network. The network gradually learns to predict the next note when given a set of notes')
        with col2:
            st.image('images/predict.png', width=700, caption='The predicted note is then appended to the seed melody and then fed back in to the network to predict the next note. this process happens the same number of steps the user has specified')

        st.text('')