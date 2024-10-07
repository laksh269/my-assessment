import pandas as pd
import numpy as np
import os

"""
To answer the following questions, make use of datasets: 
    'scheduled_loan_repayments.csv'
    'actual_loan_repayments.csv'
These files are located in the 'data' folder. 

All loans have a loan term of 2 years with an annual interest rate of 10%. Repayments are scheduled monthly.
A type 1 default will occur on a loan when a repayment is missed.
A type 2 default will occur on a loan when more than 15% of the expected total payments are unpaid for the year.

"""


def calculate_df_balances(df_scheduled,df_actual):
    """ 
        This is a utility function that creates a merged dataframe that will be used in the following questions. 
        This function will not be graded directly.

        Args:
            df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset
            df_actual (DataFrame): Dataframe created from the 'actual_loan_repayments.csv' dataset
        
        Returns:
            DataFrame: A merged Dataframe 

            Columns after the merge should be: 
            ['RepaymentID', 'LoanID', 'Month', 'ActualRepayment', 'LoanAmount', 'ScheduledRepayment']

            Additional columns to be used in later questions should include: 
            ['UnscheduledPrincipal', 'LoanBalanceStart, 'LoanBalanceEnd'] 
            Note: 'LoanBalanceStart' for the first month of each loan should equal the 'LoanAmount'

            You may create other columns to assist you in your calculations. e.g:
            ['InterestPayment']

    """

    df_merged = pd.merge(df_actual, df_scheduled)

    def calculate_balance(group):
        
        # Monthly interest rate calculated from an annual rate of 10%
        r_monthly = 0.1 / 12  
        
        # Sort the group by 'Month'
        group = group.sort_values('Month')

        # Initialize lists to store balances, interest payments, and starting loan balances
        balances = []  
        interest_payments = []
        loan_start_balances = []

        # Calculate interest payment and new balances
        for index, row in group.iterrows():
            if balances:
                interest_payment = balances[-1] * r_monthly
                balance_with_interest = balances[-1] + interest_payment
            else:
                interest_payment = row['LoanAmount'] * r_monthly
                balance_with_interest = row['LoanAmount'] + interest_payment
                loan_start_balances.append(row['LoanAmount'])

            new_balance = balance_with_interest - row['ActualRepayment']
            interest_payments.append(interest_payment)
            
            # Calculate the new balance after applying the actual repayment
            new_balance = max(0, new_balance)
            balances.append(new_balance)

        # Extend the loan start balances with calculated balances and remove the last entry to avoid misalignment
        loan_start_balances.extend(balances)
        loan_start_balances.pop()
        group['LoanBalanceStart'] = loan_start_balances
        group['LoanBalanceEnd'] = balances
        group['InterestPayment'] = interest_payments
        return group
        
    # Apply the calculate_balance function to each group of loans and reset index
    df_balances = df_merged.groupby('LoanID').apply(calculate_balance).reset_index(drop=True)

    # Round the final balances and interest payments to two decimal places for clarity
    df_balances['LoanBalanceEnd'] = df_balances['LoanBalanceEnd'].round(2)
    df_balances['InterestPayment'] = df_balances['InterestPayment'].round(2)
    df_balances['LoanBalanceStart'] = df_balances['LoanBalanceStart'].round(2)

    # Calculate scheduled principal and unscheduled principal repayments
    df_balances['ScheduledPrincipal'] = df_balances['ScheduledRepayment'] - df_balances['InterestPayment']
    df_balances['UnscheduledPrincipal'] = np.where(df_balances['ActualRepayment'] > df_balances['ScheduledRepayment'], 
                                                   df_balances['ActualRepayment'] - df_balances['ScheduledRepayment'], 0)


    return df_balances


#Do not edit these directories
root = os.getcwd()

if 'Task_2' in root:
    df_scheduled = pd.read_csv('data/scheduled_loan_repayments.csv')
    df_actual = pd.read_csv('data/actual_loan_repayments.csv')
else:
    df_scheduled = pd.read_csv('Task_2/data/scheduled_loan_repayments.csv')
    df_actual = pd.read_csv('Task_2/data/actual_loan_repayments.csv')

df_balances = calculate_df_balances(df_scheduled,df_actual)


def question_1(df_balances):
    """ 
        Calculate the percent of loans that defaulted as per the type 1 default definition 
        
        Args:
            df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function
        
        Returns:
            float: The percentage of defaulted loans (type 1)

    """
     # Find loans where at least one repayment was missed (ActualRepayment == 0)
    defaulted_loans = df_balances[df_balances['ActualRepayment'] == 0]['LoanID'].unique()
    
    # Total number of unique loans in the dataset
    total_loans = df_balances['LoanID'].nunique()
    
    # Calculate default rate as a percentage
    default_rate_percent = round((len(defaulted_loans) / total_loans) * 100, 2)
    
    return default_rate_percent






def question_2(df_balances):
    """ 
        Calculate the percent of loans that defaulted as per the type 2 default definition 
        
        Args:
            df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function
        
        Returns:
            float: The percentage of defaulted loans (type 2)

    """
        
    # Calculate the total scheduled and actual repayments on each loan.
    total_scheduled = df_balances.groupby('LoanID')['ScheduledRepayment'].sum()
    total_actual = df_balances.groupby('LoanID')['ActualRepayment'].sum()
    
    # Calculate the percentage unpaid repayments.
    repayment_diff_percent = (total_scheduled - total_actual)/ total_scheduled
    
    # Count loans where more than 15% of the expected total payments are unpaid.
    n_defaulted_loans = (repayment_diff_percent > 0.15).sum()
    
    # Total number of loans
    n_total_loans = df_balances['LoanID'].nunique()
    
    # Calculate the percentage of loans that defaulted as per the type 2 definition
    default_rate_percent = (n_defaulted_loans/n_total_loans) * 100


    return default_rate_percent





def question_3(df_balances):
    """ 
        Calculate the anualized CPR (As a %) from the geometric mean SMM.
        SMM is calculated as: (Unscheduled Principal)/(Start of Month Loan Balance)
        CPR is calcualted as: 1 - (1- SMM_mean)^12  

        Args:
            df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

        Returns:
            float: The anualized CPR of the loan portfolio as a percent.
            
    """
   # Calculate total Unscheduled Principal and Starting Loan Balance for all loans for each month
    df_total_monthly = df_balances.groupby('Month')[['UnscheduledPrincipal', 'LoanBalanceStart']].sum().reset_index()

    # Calculate the SMM for each month.
    df_total_monthly['SMM'] = df_total_monthly['UnscheduledPrincipal']/df_total_monthly['LoanBalanceStart']

    # Calculate the geometric mean SMM.
    def geo_mean(iterable):
        a = np.array(iterable)
        return a.prod()**(1.0/len(a))
    smm_mean = geo_mean(df_total_monthly['SMM'])

    # Calculate the annual CPR rate of the loan.
    cpr_percent = round((1 - (1 - smm_mean)**12)*100, 2)
    
    return cpr_percent


def question_4(df_balances):
    """ 
        Calculate the predicted total loss for the second year in the loan term.
        Use the equation: probability_of_default * total_loan_balance * (1 - recovery_rate).
        The probability_of_default value must be taken from either your question_1 or question_2 answer. 
        Decide between the two answers based on which default definition you believe to be the more useful metric.
        Assume a recovery rate of 80% 
        
        Args:
            df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function
        
        Returns:
            float: The predicted total loss for the second year in the loan term.
            
    """

    # Type 2 default is being used in this equation as I believe it gives a more accurate representation of the entire year.
    # Probability of default as shown as a rate.
    prob_of_default = question_2(df_balances)/100
    
    # Assume recovery rate is 80%
    recovery_rate = 0.80
    
    # Total loan balance for the second year (LoanBalanceStart)
    total_loan_balance = df_balances[df_balances['Month'] == 12]['LoanBalanceEnd'].sum()
    
    # Apply the total loss equation
    total_loss = round(prob_of_default * total_loan_balance * (1 - recovery_rate), 2)
    

    return total_loss