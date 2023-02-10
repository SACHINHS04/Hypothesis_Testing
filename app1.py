import pandas as pd
import numpy as np
import scipy.stats as stats
import streamlit as st

def load_data(file):
    df = pd.read_csv(file)
    return df

def t_test(df, column1, column2, alpha, test_type):
    group1 = df[column1].dropna()
    group2 = df[column2].dropna()
    
    if test_type == "Two-Sample T-Test":
        t_statistic, p_value = stats.ttest_ind(group1, group2, equal_var=False)
    elif test_type == "Paired T-Test":
        t_statistic, p_value = stats.ttest_rel(group1, group2)
    elif test_type == "One-Sample T-Test":
        t_statistic, p_value = stats.ttest_1samp(group1, np.mean(group2))
        
    if p_value < alpha:
        st.write("Reject Null Hypothesis. Data is likely not from a normal distribution.")
    else:
        st.write("Fail to Reject Null Hypothesis. Data is likely from a normal distribution.")
    st.write("T-Statistic:", t_statistic)
    st.write("P-Value:", p_value)

def anova(df, column1, group_column, alpha):
    group1 = df[df[group_column] == df[group_column].unique()[0]][column1].dropna()
    group2 = df[df[group_column] == df[group_column].unique()[1]][column1].dropna()
    group3 = df[df[group_column] == df[group_column].unique()[2]][column1].dropna()
    
    F_statistic, p_value = stats.f_oneway(group1, group2, group3)
    
    if p_value < alpha:
        st.write("Reject Null Hypothesis. Data is likely not from a normal distribution.")
    else:
        st.write("Fail to Reject Null Hypothesis. Data is likely from a normal distribution.")
    st.write("F-Statistic:", F_statistic)
    st.write("P-Value:", p_value)
    
def two_way_anova(df, column1, group1_column, group2_column, alpha):
    formula = column1 + "~C(" + group1_column + ")+C(" + group2_column + ")+C(" + group1_column + "):C(" + group2_column + ")"
    model = ols(formula, df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    
    if anova_table['PR(>F)'][-1] < alpha:
        st.write("Reject Null Hypothesis. There is a significant interaction between", group1_column, "and", group2_column, "on", column1)
    else:
        st.write("Fail to Reject Null Hypothesis. There is no significant interaction between", group1_column, "and", group2_column, "on", column1)
    st.write("ANOVA Table:")
    st.write(anova_table)

def chi_square_test(df, column1, column2, alpha):
    contingency_table = pd.crosstab(df[column1], df[column2])
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    if p_value < alpha:
        st.write("Reject Null Hypothesis. There is a relationship between", column1, "and", column2)
    else:
        st.write("Fail to Reject Null Hypothesis. There is no relationship between", column1, "and", column2)
    st.write("Chi-Square Statistic:", chi2)
    st.write("P-Value:", p_value)

st.title("Hypothesis Testing with Streamlit")

file = st.file_uploader("Upload your data file", type=["csv"])
if file is not None:
    df = pd.read_csv(file)
    st.write("Data Loaded Successfully")
    st.write("Number of rows:", df.shape[0])
    st.write("Number of columns:", df.shape[1])
    st.write("Column Names:", df.columns)
    
    alpha = st.sidebar.slider("Choose the Alpha Level", 0.01, 0.05, 0.05)
    test_type = st.sidebar.selectbox("Choose the Test Type", ["Two-Sample T-Test", "Paired T-Test", "One-Sample T-Test", "ANOVA", "2-Way ANOVA", "Chi-Square Test"])
    
    if test_type in ["Two-Sample T-Test", "Paired T-Test", "One-Sample T-Test"]:
        column1 = st.selectbox("Choose the first column", df.columns)
        column2 = st.selectbox("Choose the second column", df.columns)
        t_test(df, column1, column2, alpha, test_type)
    elif test_type == "ANOVA":
        column1 = st.selectbox("Choose the dependent variable column", df.columns)
        group_column = st.selectbox("Choose the independent variable column", df.columns)
        anova(df, column1, group_column, alpha)
    elif test_type == "2-Way ANOVA":
        column1 = st.selectbox("Choose the dependent variable column", df.columns)
        group1_column = st.selectbox("Choose the first independent variable column", df.columns)
        group2_column = st.selectbox("Choose the second independent variable column", df.columns)
        two_way_anova(df, column1, group1_column, group2_column, alpha)
    elif test_type == "Chi-Square Test":
        column1 = st.selectbox("Choose the first column", df.columns)
        column2 = st.selectbox("Choosethe second column", df.columns)
        chi_square_test(df, column1, column2, alpha)

