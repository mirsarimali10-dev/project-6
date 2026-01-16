import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 
import streamlit as st 
import plotly.express as px
import numpy as np
import random as rd
st.set_page_config(page_title="Title")
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "About Me"
if "theme" not in st.session_state:
    st.session_state.theme = "Light mode"
themes = {
    "Light mode":{
        "bg_color":"#88D7EF",
        "text_color":"#5D5656",
        "primary": "orange",
        "secondary": "blue"
    },
    "Dark mode":{
        "bg_color":"#000000",
        "text_color":"#ffffff",
        "primary":"orange",
        "secondary":"blue"
    },
    "Natural mode":{
        "bg_color":"#A47148",
        "text_color":"#71D890",
        "primary":"brown",
        "secondary":"green"
    }
}
current_theme = themes[st.session_state.theme]
st.markdown(f"""
<style>
.stApp{{background-color:{current_theme["bg_color"]};
color:{current_theme["text_color"]}}}
.metric-card{{background:linear-gradient(135deg,{current_theme["primary"]}, {current_theme["secondary"]})}}
</style>""",unsafe_allow_html = True)
tab = ["About Me" , "Books" , "Happiness Report"]
navigation = st.columns(len(tab))
i = 0
for tabs in tab:
    with navigation[i]:
        if st.button(f"{tabs}"):
            st.session_state.current_tab = tabs
            st.rerun()
    i += 1 
with st.sidebar.expander("Themes"):
    if "Theme_selected" not in st.session_state:
        st.session_state.Theme_selected = st.session_state.theme
    theme_name = ["Light mode" , "Dark mode" , "Natural mode"]
    current_index = theme_name.index(st.session_state.theme)
    theme_choice = st.radio("Select a theme" , theme_name ,index= current_index, key="theme_radio")
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.session_state.Theme_selected = theme_choice
        st.rerun()
if st.session_state.current_tab == "About Me":
    data = pd.read_csv("Me.csv")
    button_name = st.sidebar.button("Happy New Year")
    button_name2 = st.sidebar.button("Fun Facts")
    if button_name:
        st.balloons()
        st.snow()
    list_name = ["Origami is the art of folding paper" , 
    "Speedcubing is a hobby in which you try to solve a rubiks cube as fast as possible" , 
    "Coding means programing a computer to do something"]
    st.header("About Me")
    if button_name2:
        st.success(np.random.choice(list_name))
    st.title("Visual Representation")
    column1 , columh2 = st.columns(2)
    with column1:
        fig,ax = plt.subplots(figsize = ( 10 , 5 ) )
        ax.barh(data["name"],data["years_done"])
        ax.set_xlabel("Name")
        ax.set_ylabel("Years doing hobby")
        ax.set_title("Comparrison of how many years each hobby has been done")
        st.pyplot(fig)
    with columh2:
        fig = px.scatter(data , x="rating", y="skills_rating", color="name",
        hover_name="name", hover_data = { "rating":True ,"skills_rating":True },
        title = "Rating comparison",
        labels={"rating":"rating" , "rating":"rating"})
        st.plotly_chart(fig)
elif st.session_state.current_tab == "Books":
    data = pd.read_csv("data.csv")
    st.header("About Books")
    st.title("Visual Representation")
    empty = []
    formula = data.iloc[data["average_rating"].idxmax()]
    formula2 = data.iloc[data["published_year"].idxmin()]
    formula3 = data.iloc[data["num_pages"].idxmax()]
    empty.append(f"{formula3["title"]} has the most amount of pages total with {formula3["num_pages"]} total")
    empty.append(f"{formula2["title"]} is the oldest book which was made in {int(formula2["published_year"])}")
    empty.append(f"{formula["title"]} has the highest average rating with {formula["average_rating"]}")
    random_fact = rd.choice(empty)
    button_name2 = st.sidebar.button("Fun Facts")
    if button_name2:
        st.success(random_fact)
    with st.sidebar.expander("books filter"):
        formula5 = st.selectbox("select a category" , data["categories"].unique()) 
        min_v, max_v = st.slider("select average rating:",
        float(data["average_rating"].min()),
        float(data["average_rating"].max()), (float(data["average_rating"].min()), float(data["average_rating"].max())))
    column1 , column2 = st.columns(2)
    data2 = data[(data["categories"] == formula5) & (data["average_rating"] >= min_v) & (data["average_rating"] <= max_v)]
    with column1:
        fig,ax = plt.subplots(1,1, figsize=(10 , 5))
        formula4 = data2["published_year"].value_counts()
        ax.plot(formula4.index , formula4.values, marker="o", label="Count of books published each year")
        formula6 = data2.groupby("published_year")["num_pages"].mean()
        ax.plot(formula6.index , formula6.values, marker="o", label="Number of Average Pages per Year")
        ax.set_xlabel("Published Year")
        ax.set_ylabel("Count")
        ax.legend()
        st.pyplot(fig)
    with column2:
        fig,ax = plt.subplots(1,1, figsize=(10,5))
        info = data2["authors"].value_counts().head(5)
        ax.pie(info, labels=info.index, autopct="%1.1f%%")
        ax.set_title("Amount of books each author published")
        st.pyplot(fig)
    column3,column4,column5 = st.columns(3)
    column3.metric("Total books in our dataset:" , data2["title"].nunique())
    column4.metric("Total pages in our dataset:" , data2["num_pages"].sum())
    column5.metric("Total authors in our dataset:" , data2["authors"].nunique())
elif st.session_state.current_tab == "Happiness Report":
    data = pd.read_csv("2015.csv")
    st.header("Happiness Report Dashboard")
    empty = []
    column1,column2,column3 = st.columns(3)
    column1.metric("Total Countries in our dataset:" , data["Country"].nunique())
    column2.metric("Total Regions in our dataset:" , data["Region"].nunique())
    column3.metric("Highest Happiness Score:" , data["Happiness Score"].head(1))
    formula = data.iloc[data["Economy (GDP per Capita)"].idxmax()]
    formula1 = data.iloc[data["Trust (Government Corruption)"].idxmax()]
    formula2 = data.iloc[data["Happiness Rank"].idxmax()]
    empty.append(f"The Country With the Highest Economy is {formula["Country"]} which has an economy of {formula["Economy (GDP per Capita)"]}")
    empty.append(f"The Country With the Highest Government Trust is {formula1["Country"]} which has a Government Trust Rate of {formula["Trust (Government Corruption)"]}")
    empty.append(f"The Country With the Lowest Happiness Rank is {formula2["Country"]} Which is {formula2["Happiness Rank"]}th Place")
    random_fact = rd.choice(empty)
    button_name2 = st.sidebar.button("Fun Facts")
    if button_name2:
        st.success(random_fact)
    with st.sidebar.expander("Happiness filters"):
        data2 = st.selectbox("Select A Region" , data["Region"].unique())
        min_hs, max_hs = st.slider("Select A Happiness Score:",
        float(data["Happiness Score"].min()),
        float(data["Happiness Score"].max()), (float(data["Happiness Score"].min()), float(data["Happiness Score"].max())))
    data3 = data[(data["Region"] == data2) & (data["Happiness Score"] <= max_hs) & (data["Happiness Score"] >= min_hs)]
    st.title("Visual Representation")
    column4 , column5 = st.columns(2)
    with column4:
        plt.figure(figsize=(20 , 10))
        sns.countplot(x=data3["Health (Life Expectancy)"].head(10))
        plt.xlabel("Health (Life Expectancy)")
        plt.ylabel("Count")
        plt.title("Count of Health (Life Expectancy)")
        st.pyplot(plt)
    with column5:
        fig,ax = plt.subplots(figsize=(10 , 5))
        ax.hist(data3["Generosity"], bins=10)
        ax.set_xlabel("Generosity")
        ax.set_ylabel("Count")
        ax.set_title("Generosty Comparrison")
        st.pyplot(fig)
