import streamlit as st
import pandas as pd
import scipy.stats as stats

@st.cache_data
def load_data(file):
    if file is None:
        return None
    df = pd.read_csv(file)
    return df

def t_test(df, column1, column2, alpha):
    t, p = stats.ttest_ind(df[column1], df[column2])
    if p < alpha:
        st.write(f"With a p-value of {p:.4f}, we reject the null hypothesis that the means of {column1} and {column2} are equal.")
    else:
        st.write(f"With a p-value of {p:.4f}, we fail to reject the null hypothesis that the means of {column1} and {column2} are equal.")

def anova(df, column1, group_column, alpha):
    groups = df.groupby(group_column)
    f, p = stats.f_oneway(*[group[1][column1] for group in groups])
    if p < alpha:
        st.write(f"With a p-value of {p:.4f}, we reject the null hypothesis that the means of {column1} are equal among the different groups defined by {group_column}.")
    else:
        st.write(f"With a p-value of {p:.4f}, we fail to reject the null hypothesis that the means of {column1} are equal among the different groups defined by {group_column}.")

def chi_squared_test(df, column1, column2, alpha):
    contingency_table = pd.crosstab(df[column1], df[column2])
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
    if p < alpha:
        st.write(f"With a p-value of {p:.4f}, we reject the null hypothesis that {column1} and {column2} are independent.")
    else:
        st.write(f"With a p-value of {p:.4f}, we fail to reject the null hypothesis that {column1} and {column2} are independent.")

def main():
    st.write("Upload a file to perform hypothesis testing:")
    file = st.file_uploader("", type=["csv"])
    df = load_data(file)

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

if __name__ == "__main__":
    main()
