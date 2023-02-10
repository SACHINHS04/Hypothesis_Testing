import pandas as pd
import numpy as np
import scipy.stats as stats
import streamlit as st

@st.cache_data
def load_data(file=None):
    if file is None:
        return None
    df = pd.read_csv(file)
    return df

def t_test(df, column1, column2, alpha):
    result = stats.ttest_ind(df[column1], df[column2])
    t_statistic = result[0]
    p_value = result[1]
    if p_value < alpha:
        st.write(f"With a significance level of {alpha}, the two-sample t-test is significant.")
        st.write(f"The t-statistic is {t_statistic:.4f} and the p-value is {p_value:.4f}.")
    else:
        st.write(f"With a significance level of {alpha}, the two-sample t-test is not significant.")
        st.write(f"The t-statistic is {t_statistic:.4f} and the p-value is {p_value:.4f}.")

def anova(df, column, group_column, alpha):
    result = stats.f_oneway(df[df[group_column] == group][column] for group in df[group_column].unique())
    f_statistic = result[0]
    p_value = result[1]
    if p_value < alpha:
        st.write(f"With a significance level of {alpha}, the ANOVA test is significant.")
        st.write(f"The F-statistic is {f_statistic:.4f} and the p-value is {p_value:.4f}.")
    else:
        st.write(f"With a significance level of {alpha}, the ANOVA test is not significant.")
        st.write(f"The F-statistic is {f_statistic:.4f} and the p-value is {p_value:.4f}.")

def chi_squared_test(df, column1, column2, alpha):
    result = stats.chi2_contingency(pd.crosstab(df[column1], df[column2]))
    chi2_statistic = result[0]
    p_value = result[1]
    if p_value < alpha:
        st.write(f"With a significance level of {alpha}, the Chi-Squared test is significant.")
        st.write(f"The Chi-Squared statistic is {chi2_statistic:.4f} and the p-value is {p_value:.4f}.")
    else:
        st.write(f"With a significance level of {alpha}, the Chi-Squared test is not significant.")
        st.write(f"The Chi-Squared statistic is {chi2_statistic:.4f} and the p-value is {p_value:.4f}.")

def main():
    st.write("Upload your data file")
    file = st.file_uploader("Choose a CSV file", type="csv")
    df= load_data(file)
    if df is None:
        st.write("No data was uploaded.")
    return

st.write("Select the test you want to perform:")
test = st.selectbox("Test", ["T-Test", "ANOVA", "Chi-Squared Test"])
st.write("Select the columns you want to use:")
column1 = st.selectbox("Column 1", df.columns)
if test == "T-Test":
    column2 = st.selectbox("Column 2", df.columns)
    alpha = st.slider("Significance level (alpha)", 0.0, 1.0, step=0.01, value=0.05)
    t_test(df, column1, column2, alpha)
elif test == "ANOVA":
    group_column = st.selectbox("Grouping Column", df.columns)
    alpha = st.slider("Significance level (alpha)", 0.0, 1.0, step=0.01, value=0.05)
    anova(df, column1, group_column, alpha)
elif test == "Chi-Squared Test":
    column2 = st.selectbox("Column 2", df.columns)
    alpha = st.slider("Significance level (alpha)", 0.0, 1.0, step=0.01, value=0.05)
    chi_squared_test(df, column1, column2, alpha)
if name == 'main':
main()
