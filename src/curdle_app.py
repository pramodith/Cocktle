import streamlit as st
import pandas as pd
from PIL import Image

def get_image(image_name):
    image = Image.open(f"../data/images/{image_name}.png")
    image = image.resize((300, 300))
    final_image.image(image)

st.title("Curdle : So you think you know your drinks? :beer: ")
final_message = st.empty()
final_image = st.empty()
clue_text = st.empty()
st.subheader("Ingredients")


if 'curr_index' not in st.session_state:
    st.session_state['curr_index'] = 0
    df = pd.read_csv("../data/cocktail_ingredients.csv")
    row = df.sample(1).reset_index()
    clues = row.loc[0, 'Ingredients'].split("|")
    cocktail = row.loc[0,"Cocktails"]
    st.session_state['clues'] = clues
    st.session_state['cocktail'] = cocktail
    for i in range(len(clues)):
        st.session_state[str(i)] = ""
    clue_text.write(f"Clue {st.session_state['curr_index']+1} : {clues[st.session_state['curr_index']]}")

else:
    clues = st.session_state['clues']
    cocktail = st.session_state['cocktail']

empty_containers = [st.empty() for i in range(len(clues))]
guesses = [empty_containers[i].text_input(label=f"Guess {i+1}",key=i, value=st.session_state[i], disabled= st.session_state[i]!="") for i in range(len(empty_containers))]

if st.session_state['curr_index']<len(clues) and st.session_state[st.session_state['curr_index']].lower() == cocktail.lower():
    print("here")
    final_message.markdown("Great job! Time to chug that drink :cocktail: ")
    get_image(cocktail)

else:
    if st.session_state[st.session_state['curr_index']] != "" :
        st.session_state['curr_index'] += 1
        if st.session_state['curr_index'] == len(clues):
            final_message.markdown(f"Bro do you even drink? :grin: The right answer is {cocktail} ")
            get_image(cocktail)
        else:
            if st.session_state['curr_index'] < len(clues):
                clue_text.write(f"Clue {st.session_state['curr_index'] + 1} : {clues[st.session_state['curr_index']]}")
