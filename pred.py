import streamlit as st
import pickle
import numpy as np

def load():
    with open('data/saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
        return data
data = load()

regressor = data["model"]
le_country = data["le_country"]
lableEncoder_ed = data["le_education"]

def show_pred():
    st.title("Salary Prediction of Software developer")

    st.write("""### Kindly add some information to predict the salary""")

    countries = (
        "United States of America","India","Germany","United Kingdom","Canada","France","Brazil","Spain","Netherlands","Australia","Poland","Italy","Russia","Sweden","Turkey","Switzerland","Israel ",)
    education = (
        "Less than Bachelors", "Bachelor's Degree", "Master's Degree", "Post Grad",
    )
    country = st.selectbox("Country", countries)
    edu = st.selectbox("Education Level", education)

    experi = st.slider("Years of Experience", 0, 50, 3)
    ok = st.button("Calculate salary")
    if ok:
        X = np.array([[country, edu, experi ]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = lableEncoder_ed.transform(X[:,1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")