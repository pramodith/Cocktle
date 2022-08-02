from datetime import datetime
import streamlit as st
import pandas as pd
from utils import *
import time
from constants import *
import streamlit.components.v1 as components
from cookie_manager import *

cookie_manager = get_manager()
st.title("Cocktle : Can you hold your liquor long enough to name your drinks? :beer:")
question_status_message = st.empty()
question_progress_bar = st.empty()
final_message = st.empty()
clue_text = st.empty()
response = st.empty()
qna_col, history_col, img_col = st.columns([0.3, 0.5, 0.2], gap="medium")
curr_date = str(datetime.datetime.now().strftime("%d-%m-%Y")).replace("-", "")
curr_date = int(curr_date)

with qna_col:
    ingredients_table = st.empty()

with img_col:
    final_image = st.empty()


def update_cookie_state(key, value):
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    #print(cookie_manager.get_all())
    #if key in cookie_manager.get_all():
    #    cookie_manager.delete(key)
    create_cookie(cookie_manager, key, value, datetime=datetime.datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day))


def get_twitter_post_widget():
    components.html(f"""
        <a
        class ="twitter-share-button"
        href = "https://twitter.com/intent/tweet"
        data-size = "large"
        data-text = "I scored {st.session_state['correct_answers']}/{NUM_OF_QUESTIONS_PER_DAY} on today's cocktle! 🍺"
        data-url = "http://localhost:8501"
        data-hashtags = "cocktle"
        >
        Tweet
        </a>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        """,height=100,width=100)

def refresh_screen():
    global clues, cocktail, curr_question_num, curr_index
    curr_question_num += 1
    st.session_state['curr_question'] = curr_question_num
    st.session_state['curr_index'] = curr_index = 0
    st.session_state['guess_history'] = []
    row = st.session_state['rows']
    clues = row.loc[curr_question_num, 'Ingredients'].split("|")
    clues = [c.title() for c in clues]
    cocktail = row.loc[curr_question_num, "Cocktails"]
    st.session_state['clues'] = clues
    st.session_state['cocktail'] = cocktail
    for i in range(len(clues)):
        st.session_state[i] = ""
    clue_text.text(f"Clue {st.session_state['curr_index'] + 1} : {clues[st.session_state['curr_index']]}")

def get_animated_image(image):
    for i in range(1, 30):
        new_image = image.resize((10 * i, 10 * i), Image.LANCZOS)
        time.sleep(0.05)
        final_image.image(new_image)


def df_index_from_1(df : pd.DataFrame):
    df.index = [i+1 for i in range(len(df))]
    return df


if 'curr_index' not in st.session_state:
    if 'curr_index' not in cookie_manager.get_all():
        st.session_state['curr_index'] = curr_index = 0
        st.session_state['correct_answers'] = 0
        st.session_state['curr_question'] = curr_question_num = 0
        st.session_state['guess_history'] = []
        df = pd.read_csv("../data/cocktail_ingredients.csv")
        df = df[df["Selected"] == False]
        row = df.sample(NUM_OF_QUESTIONS_PER_DAY, random_state=curr_date).reset_index()
        st.session_state['rows'] = row
        clues = row.loc[curr_question_num, 'Ingredients'].split("|")
        clues = [c.title() for c in clues]
        cocktail = row.loc[curr_question_num, "Cocktails"]
        st.session_state['clues'] = clues
        st.session_state['cocktail'] = cocktail
        print(f"Drink is {cocktail}")
    else:
        for key in COOKIE_KEYS:
            st.session_state[key] = get_cookie(cookie_manager,key)
        clues = st.session_state['clues']
        cocktail = st.session_state['cocktail']
        curr_index = st.session_state['curr_index']
        curr_question_num = st.session_state['curr_question']
        row = st.session_state['rows']

else:
    clues = st.session_state['clues']
    cocktail = st.session_state['cocktail']
    curr_index = st.session_state['curr_index']
    curr_question_num = st.session_state['curr_question']
    #cookie_manager.set("test","test")
    #for key in COOKIE_KEYS:
    #    update_cookie_state(key, st.session_state[key])

for i in range(len(clues)):
    st.session_state[i] = ""
clue_text.text(f"Clue {st.session_state['curr_index'] + 1} : {clues[st.session_state['curr_index']]}")


with history_col:
    guess_table = st.empty()

question_status_message.text(f"{DRINK_PROGRESS_MSG} {curr_question_num+1}/{NUM_OF_QUESTIONS_PER_DAY}")
question_progress_bar.progress((curr_question_num+1)/NUM_OF_QUESTIONS_PER_DAY)

if curr_index<len(clues) and st.session_state[curr_index].lower() == cocktail.lower():
    ingredients_table.table(df_index_from_1(pd.DataFrame(clues, columns=["Ingredients"]).reset_index(drop=True)))
    final_message.markdown(f"Great job! Time to chug that drink :cocktail: ")
    st.session_state['correct_answers'] += 1
    image = get_image(cocktail)
    get_animated_image(image)
    guess_table.table(df_index_from_1(pd.DataFrame(st.session_state['guess_history'], columns=["Guesses"])))
    if curr_question_num < NUM_OF_QUESTIONS_PER_DAY:
        st.button(BUTTON_TEXT, on_click=refresh_screen)
    else:
        st.subheader(f"{GAME_CLOSE_TEXT} {st.session_state['correct_answers']/NUM_OF_QUESTIONS_PER_DAY}")
        get_twitter_post_widget()


elif st.session_state[curr_index] in st.session_state['guess_history']:
    clue_text.text(f"Bro are you drunk? You can't guess the same drink twice! \n "
                    f"Clue {curr_index + 1} : {clues[curr_index]}")
    guess_table.table(df_index_from_1(pd.DataFrame(st.session_state['guess_history'], columns=["Guesses"])))

else:
    if st.session_state[curr_index] != "":
        st.session_state['guess_history'].append(st.session_state[curr_index].title())
        ingredients_table.table(df_index_from_1(pd.DataFrame(clues[:curr_index+1], columns=["Ingredients"]).reset_index(drop=True)))
        guess_table.table(df_index_from_1(pd.DataFrame(st.session_state['guess_history'], columns=["Guesses"])))
        curr_index += 1
        st.session_state['curr_index'] = curr_index
        if curr_index == len(clues):
            ingredients_table.table(df_index_from_1(pd.DataFrame(clues, columns=["Ingredients"]).reset_index(drop=True)))
            final_message.markdown(f"Bro do you even drink? :grin: "
                                   f"The right answer is __{cocktail}__ ")
            image = get_image(cocktail)
            get_animated_image(image)
            if (curr_question_num+1) < NUM_OF_QUESTIONS_PER_DAY:
                st.button(BUTTON_TEXT, on_click=refresh_screen)
            else:
                st.subheader(f"{GAME_CLOSE_TEXT} {st.session_state['correct_answers']} / {NUM_OF_QUESTIONS_PER_DAY} "
                             f":wine_glass: ")
                get_twitter_post_widget()

        else:
            if curr_index < len(clues):
                if levenshtein_distance(cocktail.lower(),st.session_state[curr_index-1].lower())<3:
                    clue_text.text(f"You are very close to the right answer!!! \n"
                                    f"Clue {curr_index + 1} : {clues[curr_index]}")
                else:
                    clue_text.text(f"Clue {curr_index + 1} : {clues[curr_index]}")

if curr_index < len(clues) and st.session_state[curr_index].lower() != cocktail.lower():
    response.text_input(label=f"Guess {curr_index+1}/{len(clues)}", key=curr_index, value="")

