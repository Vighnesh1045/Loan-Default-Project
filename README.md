# Loan Default & Financial Metrics Dashboard
### Dashboard Link: https://app.powerbi.com/view?r=eyJrIjoiZmMwMTQyOGUtMzZiZS00YjQyLWI3OTgtYjZmNDkxYjI3MjdhIiwidCI6ImVjMTQyODJlLTkzZjAtNGI1Mi1hNzkwLWZkOGMwN2Y2MGQ1OCJ9 

## Problem Statement
This dashboard provides a comprehensive analysis of loan distribution, applicant demographics, and financial risk factors. It helps financial institutions understand the relationship between employment status, income levels, and default rates. By identifying that unemployed individuals have the highest default rate (3.39%) while full-time employees have the lowest (2.36%), the organization can refine its lending criteria.





Additionally, the dashboard tracks year-over-year (YOY) changes in loan amounts and defaults. This data allows stakeholders to monitor market trends and manage the total loan portfolio, which currently stands at a sum of 32.58 billion.

## What is in this folder?
- app.py : 
    The web app you can run to interact with the model.

- loan_default_pipeline.pkl : 
    The trained AI model (Large File).

- Loan_default_dataset.csv : 
    The raw data used for training and dashboarding.


- Reports & Dashboards.pdf : 
    A full report of findings and visual analysis.


- requirements.txt : 
    The list of Python tools needed for execution.

## How to use it
- Install the tools : 
    pip install -r requirements.txt

- Run the app : 
    streamlit run app.py

### Steps Followed

- Step 1: Loaded data into Power BI Desktop and performed initial data profiling.


- Step 2: Created Calculated Columns for categorization, such as Income Bracket (Low, Medium, High) and Credit Score Bins (Very Low, Low, Medium, High).






- Step 3: Defined Age Groups using DAX to segment the population into Teens, Adults, Middle Age Adults, and Senior Citizens.


- Step 4: Developed a "Loan Amount by Purpose" visual to show the hierarchy of loan volume, with Home loans leading at 6,545M.




- Step 5: Implemented "Default Rate (%) by Employment Type" to correlate job stability with risk.


- Step 6: Created an "Average Income by Employment Type" chart to validate earning potential across segments, with Full-time workers highest at 82,890.




- Step 7: Built an "Average Loan Amount by Age Group" visual, showing Adults borrow the most on average (127,901).


- Step 8: Added time-series analysis for "Default Rate (%) by Year," noting historical trends across 2013-2018.


- Step 9: Implemented median analysis for loan amounts by credit score category.


- Step 10: Created a "Total Loan (Adults) by Credit Score Bins" chart, showing Medium score adults hold the most debt (4.6bn).


- Step 11: Designed a Decomposition Tree to break down the 32.58bn total loan amount by Income Bracket and Employment Type.





- Step 12: Calculated complex YOY measures to visualize percentage changes in loan amounts and default counts.


### DAX Measures & Columns
1. Age Groups (Column)
Code snippet

    Age Groups = 
    IF('Loan_default'[Age]<=19" Teen" 
    IF('Loan_default' [Age]<=39,"Adults", 
    IF('Loan_default' [Age]<=59,"Middle Age Adults","Senior Citizens")))

2. Default Rate by Employment (Measure)
Code snippet

    Default Rate by Employment type = 
    Var totalrecords = COUNTROWS(ALL('Loan_default'))
    Var DefaultCases = COUNTROWS(FILTER('Loan_default', 'Loan_default'[Default]=TRUE()))
    RETURN
    CALCULATE (DIVIDE(DefaultCases, totalrecords), 
    ALLEXCEPT('Loan_default', 'Loan_default'[EmploymentType])) *100



### Insights
#### Following inferences can be drawn from the dashboard:

[1] Portfolio Composition
    
    The total loan amount across the portfolio is 32.58 billion.

    Home loans represent the largest purpose-based segment by value at 6,545M.

    High Income individuals account for the vast majority of the loan volume at 21.73bn.


[2] Employment & Risk Profile

    Unemployed individuals exhibit the highest risk with a 3.39% default rate.

    Full-time employees present the lowest risk with a 2.36% default rate.

    Average income is highest for Full-time employees (82,890) and lowest for Unemployed individuals (82,272).



[3] Demographic Borrowing Habits

    Adults have the highest average loan amount at 127,901.

    For Middle Age Adults, the total loan amount is split equally between those with and without dependents at 3.1bn each.

    Education-wise, Bachelor's degree holders account for the highest number of loans (64,366).


[4] Yearly Trends (2013-2018)
    The peak default rate occurred in 2016 at 11.75%.

    By 2018, the YOY Loan Amount Change rebounded to a growth of 1.72877%.

    The default rate in 2018 was 11.60%.
