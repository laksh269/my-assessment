"""
The database loan.db consists of 3 tables: 
   1. customers - table containing customer data
   2. loans - table containing loan data pertaining to customers
   3. credit - table containing credit and creditscore data pertaining to customers
   4. repayments - table containing loan repayment data pertaining to customers
   5. months - table containing month name and month ID data
    
You are required to make use of your knowledge in SQL to query the database object (saved as loan.db) and return the requested information.
Simply fill in the vacant space wrapped in triple quotes per question (each function represents a question)

"""

def question_1():    
        
    # Find all name-surname combinations that are duplicated in the customers dataset. 
    # Return `Name` and `Surname` columns

    qry = """
    --- Show all the duplicated names and surname combinations from the customer dataset.
    SELECT 
        Name, Surname 
    FROM 
        customers 
    GROUP BY 
        Name, Surname
    HAVING 
        COUNT(*) > 1
    ORDER BY 
        Surname, Name;
    """
    return qry



def question_2():    
    
    # Return the `Name`, `Surname` and `Income` of all female customers in the dataset in descending order of income

    qry = """
    -- Show the Name, Surname, and Income of female customers in descending order of income.
    SELECT 
        Name, Surname, Income
    FROM 
        customers
    WHERE 
        Gender = 'Female'
    ORDER BY 
        Income DESC;
    """

    return qry


def question_3():    
    
    # Find the `ApprovalPercentage` of loans by `LoanTerm`

    qry = """
    --- Show the Approval Percentage for loans for each LoanTerm.
    SELECT  
        LoanTerm,
        COUNT(CASE WHEN ApprovalStatus = 'Approved' THEN 1 END) * 100.0 / COUNT(*) AS ApprovalPercentage
    FROM 
        loans
    GROUP BY 
        LoanTerm;
    """
    return qry




def question_4():    
    
    # Return a breakdown of the number of customers per CustomerClass in the credit data
    # Return columns `CustomerClass` and `Count`

    qry = """
    --- Show the number of customers in each customer class in the credit dataset.
    SELECT 
        CustomerClass, 
        COUNT(*) AS Count
    FROM 
        credit
    GROUP BY 
        CustomerClass;
    """
    return qry




def question_5():    
    
    # Make use of the UPDATE function to amend/fix the following: Customers with a CreditScore between and including 600 to 650 must be classified as CustomerClass C.
    
    qry = """
    --- Update the credit dataset to include the new customer class.
    UPDATE 
        credit
    SET 
        CustomerClass = 'C'
    WHERE 
        CreditScore BETWEEN 600 AND 650;
    """
    
    return qry

