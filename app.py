import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

st.title("Hypothesis Testing with Streamlit")

@st.cache_data
def load_data(file=None):
    if file is None:
        return None
    df = pd.read_csv(file)
    return df



data = load_data()

if data is not None:
    df = pd.read_csv(data)
    st.dataframe(df.head())

    hypothesis_options = ['Two-Sample T-Test', 'Paired T-Test', 'One-Sample T-Test', 'ANOVA', '2-Way ANOVA', 'Chi-Square Test']
    hypothesis_choice = st.selectbox("Select a hypothesis test to perform", hypothesis_options)

    alpha = st.slider("Specify the significance level (alpha)", 0.01, 0.1, 0.05)

    columns = df.columns
    selected_columns = st.multiselect("Select columns to use for hypothesis testing", columns)
    if len(selected_columns) >= 2:
        x = df[selected_columns[0]]
        y = df[selected_columns[1]]
        if hypothesis_choice == 'Two-Sample T-Test':
            result = stats.ttest_ind(x, y)
            st.write("The T-statistic is %.3f and the p-value is %.3f." % result)
            if result[1] < alpha:
                st.write("We reject the null hypothesis. There is a significant difference between the two groups.")
            else:
                st.write("We fail to reject the null hypothesis. There is not enough evidence to conclude that there is a difference between the two groups.")
        elif hypothesis_choice == 'Paired T-Test':
            result = stats.ttest_rel(x, y)
            st.write("The T-statistic is %.3f and the p-value is %.3f." % result)
            if result[1] < alpha:
                st.write("We reject the null hypothesis. There is a significant difference between the paired observations.")
            else:
                st.write("We fail to reject the null hypothesis. There is not enough evidence to conclude that there is a difference between the paired observations.")
        elif hypothesis_choice == 'One-Sample T-Test':
            mean = st.number_input("Enter the hypothesized mean", value=0)
            result = stats.ttest_1samp(x, mean)
            st.write("The T-statistic is %.3f and the p-value is %.3f." % result)
            if result[1] < alpha:
                st.write("We reject the null hypothesis. The sample mean is significantly different from the hypothesized mean.")
            else:
                st.write("We fail to reject the null hypothesis. The sample mean is not significantly different from the hypothesized mean.")
        elif hypothesis_choice == 'ANOVA':
            result = stats.f_oneway(df[selected_columns].values)
            st.write("The F-statistic is %.3f and the p-value is %.3f." % result)
            if result[1] < alpha:
                st.write("We reject the null hypothesis. There is a significant difference among the means of the groups.")
            else:
                st.write("We fail to reject the null hypothesis. There is not enough evidence to conclude that there is a difference among the means of the groups.")
        elif hypothesis_choice == '2-Way ANOVA':
            result = stats.f_oneway(*[df[col] for col in selected_columns])
            st.write("The F-statistic is %.3f and the p-value is %.3f." % result)
            if result[1] < alpha:
                st.write("We reject the null hypothesis. There is a significant difference among the means of the groups.")
            else:
                st.write("We fail to reject the null hypothesis. There is not enough evidence to conclude that there is a difference among the means of the groups.")
        elif hypothesis_choice == 'Chi-Square Test':
            result = stats.chisquare(x, y)
            st.write("The chi-square statistic is %.3f and the p-value is %.3f." % result)
            if result[1] < alpha:
                st.write("We reject the null hypothesis. The two variables are dependent.")
            else:
                st.write("We fail to reject the null hypothesis. The two variables are independent.")
    else:
        st.write("Please select at least 2 columns for hypothesis testing.")
else:
    st.write("Please upload a data file.")
