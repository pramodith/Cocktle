import time
import streamlit as st
import pandas as pd
from utils import *

st.title("Curdle : So you think you know your drinks? :beer: ")
final_message = st.empty()
st.subheader("Ingredients")
clue_text = st.empty()
ingredients_table = st.empty()
final_image = st.empty()

def get_animated_image(image):
    for i in range(1, 30):
        new_image = image.resize((10 * i, 10 * i), Image.LANCZOS)
        time.sleep(0.05)
        final_image.image(new_image)

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
    print(cocktail)

else:
    clues = st.session_state['clues']
    cocktail = st.session_state['cocktail']

empty_containers = [st.empty() for i in range(len(clues))]
guesses = [empty_containers[i].text_input(label=f"Guess {i+1}",key=i, value=st.session_state[i], disabled=st.session_state[i]!="") for i in range(len(empty_containers))]
if st.session_state['curr_index']<len(clues) and st.session_state[st.session_state['curr_index']].lower() == cocktail.lower():
    ingredients_table.table(pd.DataFrame(clues, columns=["Ingredient"]))
    final_message.markdown(f"Great job! Time to chug that drink :cocktail: ")
    image = get_image(cocktail)
    get_animated_image(image)

elif st.session_state[st.session_state['curr_index']] in guesses[:st.session_state['curr_index']]:
    clue_text.write(f"Bro are you drunk? You can't guess the same drink twice! \n "
                    f"Clue {st.session_state['curr_index'] + 1} : {clues[st.session_state['curr_index']]}")
    empty_containers[st.session_state['curr_index']].text_input(label=f"Guess {st.session_state['curr_index']+1}"
                                                                ,key = st.session_state['curr_index'], disabled=False,value="")

else:
    if st.session_state[st.session_state['curr_index']] != "":
        st.session_state['curr_index'] += 1
        if st.session_state['curr_index'] == len(clues):
            ingredients_table.table(pd.DataFrame(clues, columns=["Ingredient"]))
            final_message.markdown(f"Bro do you even drink? :grin: "
                                   f"The right answer is __{cocktail}__ ")
            image = get_image(cocktail)
            get_animated_image(image)
        else:
            if st.session_state['curr_index'] < len(clues):
                if levenshtein_distance(cocktail.lower(),st.session_state[st.session_state['curr_index']-1].lower())<3:
                    clue_text.write(f"You are very close to the right answer!!! \n"
                                    f"Clue {st.session_state['curr_index'] + 1} : {clues[st.session_state['curr_index']]}")
                else:
                    clue_text.write(f"Clue {st.session_state['curr_index'] + 1} : {clues[st.session_state['curr_index']]}")
