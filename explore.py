from os import defpath
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 

def shorten_categories(categories, cutoff):
    hashmap = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            hashmap[categories.index[i]] = categories.index[i]
        else:
            hashmap[categories.index[i]] = 'Other'
    return hashmap

def clean_ex(ex):
    if ex == "More than 50 years":
        return 50
    elif ex == "Less than 1 year":
        return 1
    return ex

def clean_edlevel(edlevel):
    if edlevel == "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)":
        return "Master's Degree"
    elif edlevel == 'Bachelor’s degree (B.A., B.S., B.Eng., etc.)':
        return "Bachelor's Degree"
    elif edlevel == 'Professional degree (JD, MD, etc.)' or edlevel == 'Other doctoral degree (Ph.D., Ed.D., etc.)':
        return "Post Grad"
    else:
        return "Less than Bachelors"

@st.cache
def load_data():
    df = pd.read_csv('data/survey_results_public.csv')
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()



    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df["Salary"] <= 200000]
    df = df[df['Salary'] >= 10000]
    df = df[df['Country'] != 'Other']
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_ex)
    df['EdLevel'] = df['EdLevel'].apply(clean_edlevel)

    return df

df = load_data()

def show_explore():
    st.title("Explore Software engineer salaries")

    st.write("""### Stackoverflow Developer Survey 2021""")

    data = df["Country"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")

    st.write("""#### Number of data from different countries""")

    st.pyplot(fig1)

    st.write("""#### Mean salary based on country""")

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""#### Mean Salary based on experience""")
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)



