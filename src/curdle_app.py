import time
import streamlit as st
import pandas as pd
from utils import *

st.title("Curdle : So you think you know your drinks? :beer: ")
final_message = st.empty()
st.subheader("Ingredients")
qna_col, history_col = st.columns([0.75,0.25])

with qna_col:
    clue_text = st.empty()
    ingredients_table = st.empty()
    final_image = st.empty()

def get_animated_image(image):
    for i in range(1, 30):
        new_image = image.resize((10 * i, 10 * i), Image.LANCZOS)
        time.sleep(0.05)
        final_image.image(new_image)

def df_index_from_1(df : pd.DataFrame):
    df.index = [i+1 for i in range(len(df))]
    return df

if 'curr_index' not in st.session_state:
    st.session_state['curr_index'] = 0
    st.session_state['guess_history'] = []
    curr_index = 0
    df = pd.read_csv("../data/cocktail_ingredients.csv")
    row = df.sample(1).reset_index()
    clues = row.loc[0, 'Ingredients'].split("|")
    cocktail = row.loc[0, "Cocktails"]
    st.session_state['clues'] = clues
    st.session_state['cocktail'] = cocktail
    for i in range(len(clues)):
        st.session_state[i] = ""
    clue_text.write(f"Clue {st.session_state['curr_index']+1} : {clues[st.session_state['curr_index']]}")
    print(cocktail)

else:
    clues = st.session_state['clues']
    cocktail = st.session_state['cocktail']
    curr_index = st.session_state['curr_index']
    print(st.session_state.to_dict())

with history_col:
    guess_table = st.empty()


if curr_index<len(clues) and st.session_state[curr_index].lower() == cocktail.lower():
    ingredients_table.table(df_index_from_1(pd.DataFrame(clues, columns=["Ingredient"]).reset_index(drop=True)))
    final_message.markdown(f"Great job! Time to chug that drink :cocktail: ")
    image = get_image(cocktail)
    get_animated_image(image)
    guess_table.table(df_index_from_1(pd.DataFrame(st.session_state['guess_history'], columns=["Guesses"])))

elif st.session_state[curr_index] in st.session_state['guess_history']:
    clue_text.write(f"Bro are you drunk? You can't guess the same drink twice! \n "
                    f"Clue {curr_index + 1} : {clues[curr_index]}")
    guess_table.table(df_index_from_1(pd.DataFrame(st.session_state['guess_history'], columns=["Guesses"])))

else:
    if st.session_state[curr_index] != "":
        st.session_state['guess_history'].append(st.session_state[curr_index])
        guess_table.table(df_index_from_1(pd.DataFrame(st.session_state['guess_history'], columns=["Guesses"])))
        curr_index += 1
        st.session_state['curr_index'] = curr_index
        if curr_index == len(clues):
            ingredients_table.table(df_index_from_1(pd.DataFrame(clues, columns=["Ingredient"]).reset_index(drop=True)))
            final_message.markdown(f"Bro do you even drink? :grin: "
                                   f"The right answer is __{cocktail}__ ")
            image = get_image(cocktail)
            get_animated_image(image)
        else:
            if curr_index < len(clues):
                if levenshtein_distance(cocktail.lower(),st.session_state[curr_index-1].lower())<3:
                    clue_text.write(f"You are very close to the right answer!!! \n"
                                    f"Clue {curr_index + 1} : {clues[curr_index]}")
                else:
                    clue_text.write(f"Clue {curr_index + 1} : {clues[curr_index]}")

with qna_col:
    if curr_index<len(clues) and st.session_state[curr_index].lower() != cocktail.lower():
        response = st.empty()
        response.text_input(label=f"Guess {curr_index+1}", key=curr_index, value="")

