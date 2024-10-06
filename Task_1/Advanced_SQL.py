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
    
    #Make use of a JOIN to find out the `AverageIncome` per `CustomerClass`

    qry = """
    -- Select the customer class and the average income of customers within each class
    SELECT 
        cr.CustomerClass, ROUND(AVG(c.Income),2) AS AverageIncome
    FROM 
        customers AS c
    JOIN 
        credit AS cr
            ON c.CustomerID = cr.CustomerID
    GROUP BY 
        cr.CustomerClass
    ORDER BY 
        AverageIncome DESC;
    """
    
    return qry


def question_2():    
    
    #Q2: Make use of a JOIN to return a breakdown of the number of 'RejectedApplications' per 'Province'. 
    qry = """
    -- Clean the 'Region' column in the 'customers' table by standardizing the region names.
    UPDATE 
        customers
    SET 
        Region = CASE
            WHEN Region = 'EC' THEN 'EasternCape'
            WHEN Region = 'FS' THEN 'FreeState'
            WHEN Region = 'GT' THEN 'Gauteng'
            WHEN Region = 'LP' THEN 'Limpopo'
            WHEN Region = 'MP' THEN 'Mpumalanga'
            WHEN Region = 'NC' THEN 'NorthernCape'
            WHEN Region = 'NL' THEN 'Natal'
            WHEN Region = 'NW' THEN 'NorthWest'
            WHEN Region = 'WC' THEN 'WesternCape'
        END
    WHERE 
        Region IN ('EC','FS','GT','LP','MP','NC','NL','NW','WC');

    -- Show the region and count the number of rejected loan applications per region.
    SELECT 
        customers.Region AS Province, 
        COUNT(loans.ApprovalStatus) AS RejectedApplications
    FROM 
        customers
    JOIN loans
        ON customers.CustomerID = loans.CustomerID
    WHERE 
        loans.ApprovalStatus = 'Rejected'
    GROUP BY 
        customers.Region, 
        loans.ApprovalStatus
    ORDER BY 
        Province;
    """
    
    return qry


def question_3():    
    
    # Making use of the `INSERT` function, create a new table called `financing` which will include the following columns:
        # `CustomerID`,`Income`,`LoanAmount`,`LoanTerm`,`InterestRate`,`ApprovalStatus` and `CreditScore`
    # Do not return the new table

    qry = """
    -- Create the financing table to store customer financing details.
    CREATE TABLE financing(
        CustomerID INTEGER,
        Income INTEGER,
        LoanAmount INTEGER,
        LoanTerm INTEGER,
        InterestRate FLOAT,
        ApprovalStatus VARCHAR(10),
        CreditScore INTEGER
    );
    
    -- Insert data into the financing table from the customers, loans, and credit tables.
    INSERT INTO financing(CustomerID, Income, LoanAmount, LoanTerm, InterestRate, ApprovalStatus, CreditScore)
    SELECT
        c.CustomerID,
        c.Income,
        l.LoanAmount,
        l.LoanTerm,
        l.InterestRate,
        l.ApprovalStatus,
        cr.CreditScore
    FROM
        customers AS c
    JOIN
        loans As l
            ON c.CustomerID = l.CustomerID
    JOIN
        credit AS cr
            ON c.CustomerID = cr.CustomerID;
    """
    
    return qry

# Question 4 and 5 are linked

def question_4():

    # Using a `CROSS JOIN` and the `months` table, create a new table called `timeline` that sumarizes Repayments per customer per month.
    # Columns should be: `CustomerID`, `MonthName`, `NumberOfRepayments`, `AmountTotal`.
    # Repayments should only occur between 6am and 6pm London Time. 
    # Hint: there should be 12x CustomerID = 1.
    # Null values to be filled with 0.

    qry = """
    -- Note: The implementation of the timezone query faced execution challenges and has not been integrated at this time.

    -- Create table that summarizes the number of repayments and total amount paid each month that each customer pays.
    CREATE TABLE timeline(
        CustomerID INTEGER,
        MonthName VARCHAR(20),
        NumberOfRepayments INTEGER,
        AmountTotal FLOAT);

    -- Insert summarized repayment data into the timeline table.
    INSERT INTO timeline(CustomerID, MonthName, NumberOfRepayments, AmountTotal)
    SELECT
        c.CustomerID,
        m.MonthName,
        COALESCE(COUNT(r.Amount), 0) AS NumberOfRepayments,  
        COALESCE(SUM(r.Amount), 0) AS AmountTotal 
    FROM
        customers AS c -- Include all customers, even those who have not made payments
    CROSS JOIN
        months AS m  -- Generate all combinations of customers and months
    LEFT JOIN 
       repayments AS r
           ON c.CustomerID = r.CustomerID
           AND m.MonthID = MONTH(r.RepaymentDate) 
           AND HOUR(r.RepaymentDate) BETWEEN 6 AND 18  -- Include only payments made between 6 AM and 6 PM
    GROUP BY 
        c.CustomerID, m.MonthID, m.MonthName
    ORDER BY 
        c.CustomerID, m.MonthID, m.MonthName;

   -- Select all records from the timeline table for review.
    SELECT *
    FROM timeline
    
"""

    return qry


def question_5():

    # Make use of conditional aggregation to pivot the `timeline` table such that the columns are as follows:
        # CustomerID, JanuaryRepayments, JanuaryTotal,...,DecemberRepayments, DecemberTotal,...etc
    # MonthRepayments columns (e.g JanuaryRepayments) should be integers
    # Hint: there should be 1x CustomerID = 1

    qry = """
    -- Create a new table that summarizes monthly repayments and totals for each customer.
    SELECT
        CustomerID,
        -- January Repayments and Total
        CAST(SUM(CASE WHEN MonthName = 'January' THEN NumberOfRepayments ELSE 0 END) AS INT) AS JanuaryRepayments,
        SUM(CASE WHEN MonthName = 'January' THEN AmountTotal ELSE 0 END) AS JanuaryTotal,
        
        -- Febraury Repayments and Total
        CAST(SUM(CASE WHEN MonthName = 'February' THEN NumberOfRepayments ELSE 0 END) AS INT) AS FebruaryRepayments,
        SUM(CASE WHEN MonthName = 'February' THEN AmountTotal ELSE 0 END) AS FebruaryTotal,

        -- March Repayments and Total
        CAST(SUM(CASE WHEN MonthName = 'March' THEN NumberOfRepayments ELSE 0 END) AS INT) AS MarchRepayments,
        SUM(CASE WHEN MonthName = 'March' THEN AmountTotal ELSE 0 END) AS MarchTotal,

        -- April Repayments and Total
        CAST(SUM(CASE WHEN MonthName = 'April' THEN NumberOfRepayments ELSE 0 END) AS INT) AS AprilRepayments,
        SUM(CASE WHEN MonthName = 'April' THEN AmountTotal ELSE 0 END) AS AprilTotal,

        -- May Repayments and Total
        CAST(SUM(CASE WHEN MonthName = 'May' THEN NumberOfRepayments ELSE 0 END) AS INT) AS MayRepayments,
        SUM(CASE WHEN MonthName = 'May' THEN AmountTotal ELSE 0 END) AS MayTotal,

        -- June Repayments and Total
        CAST(SUM(CASE WHEN MonthName = 'June' THEN NumberOfRepayments ELSE 0 END) AS INT) AS JuneRepayments,
        SUM(CASE WHEN MonthName = 'June' THEN AmountTotal ELSE 0 END) AS JuneTotal,

        -- July Repayments and Total
        CAST(SUM(CASE WHEN MonthName = 'July' THEN NumberOfRepayments ELSE 0 END) AS INT) AS JulyRepayments,
        SUM(CASE WHEN MonthName = 'July' THEN AmountTotal ELSE 0 END) AS JulyTotal,

        -- August Repayments and Total
        CAST(SUM(CASE WHEN MonthName = 'August' THEN NumberOfRepayments ELSE 0 END) AS INT) AS AugustRepayments,
        SUM(CASE WHEN MonthName = 'August' THEN AmountTotal ELSE 0 END) AS AugustTotal,

        -- September Repayments and Total
        CAST(SUM(CASE WHEN MonthName = 'September' THEN NumberOfRepayments ELSE 0 END) AS INT) AS SeptemberRepayments,
        SUM(CASE WHEN MonthName = 'September' THEN AmountTotal ELSE 0 END) AS SeptemberTotal,
        
        -- October Repayments and Total
        CAST(SUM(CASE WHEN MonthName = 'October' THEN NumberOfRepayments ELSE 0 END) AS INT) AS OctoberRepayments,
        SUM(CASE WHEN MonthName = 'October' THEN AmountTotal ELSE 0 END) AS OctoberTotal,
        
        -- November Repayments and Total
        CAST(SUM(CASE WHEN MonthName = 'November' THEN NumberOfRepayments ELSE 0 END) AS INT) AS NovemberRepayments,
        SUM(CASE WHEN MonthName = 'November' THEN AmountTotal ELSE 0 END) AS NovemberTotal,
        
        -- December Repayments and Total
        CAST(SUM(CASE WHEN MonthName = 'December' THEN NumberOfRepayments ELSE 0 END) AS INT) AS DecemberRepayments,
        SUM(CASE WHEN MonthName = 'December' THEN AmountTotal ELSE 0 END) AS DecemberTotal,
    FROM
        timeline
    GROUP BY
      CustomerID;
    """

    return qry





#QUESTION 6 and 7 are linked

def question_6():

    # The `customers` table was created by merging two separate tables: one containing data for male customers and the other for female customers.
    # Due to an error, the data in the age columns were misaligned in both original tables, resulting in a shift of two places upwards in
    # relation to the corresponding CustomerID.

    # Utilize a window function to correct this mistake in a new `CorrectedAge` column.
    # Create a table called `corrected_customers` with columns: `CustomerID`, `Age`, `CorrectedAge`, `Gender` 
    # Also return a result set for this table
    # Null values can be input manually

    qry = """
    -- Create a new table with the corrected age.
    CREATE TABLE corrected_customers AS
    SELECT
        CustomerID,
        Age,
        CAST(COALESCE(LAG(Age, 2) OVER (PARTITION BY Gender ORDER BY CustomerID), NULL) AS INT) AS CorrectedAge,
        Gender
    FROM
        customers
    ORDER BY
        CustomerID;
        
    -- Return the result set
    SELECT * FROM corrected_customers;
    
    """

    return qry


def question_7():

    # Create a column called 'AgeCategory' that categorizes customers by age 
    # Age categories should be as follows:
        # Teen: x < 20
        # Young Adult: 20 <= x < 30
        # Adult: 30 <= x < 60
        # Pensioner: x >= 60
    # Make use of a windows function to assign a rank to each customer based on the total number of repayments per age group. Add this into a "Rank" column.
    # The ranking should not skip numbers in the sequence, even when there are ties, i.e. 1,2,2,2,3,4 not 1,2,2,2,5,6 
    # Customers with no repayments should be included as 0 in the result.

    qry = """
    -- Show the age categories for the corrected age and rank customers based on the number of repayments they have made.
    SELECT 
        c.CustomerID,
        c.CorrectedAge,
        CASE
            WHEN c.CorrectedAge < 20 THEN 'Teen'
            WHEN c.CorrectedAge BETWEEN 21 AND 30 THEN 'Young Adult'
            WHEN c.CorrectedAge BETWEEN 31 AND 60 THEN 'Adult'
            WHEN c.CorrectedAge >= 60 THEN 'Pensioner'
            END AS AgeCategory,
        COUNT(r.Amount) AS NumberOfRepayments, 
        DENSE_RANK() OVER(PARTITION BY 
            CASE
                WHEN c.CorrectedAge < 20 THEN 'Teen'
                WHEN c.CorrectedAge BETWEEN 21 AND 30 THEN 'Young Adult'
                WHEN c.CorrectedAge BETWEEN 31 AND 60 THEN 'Adult'
                WHEN c.CorrectedAge >= 60 THEN 'Pensioner'
            END ORDER BY COUNT(r.Amount) DESC) AS Rank  
    FROM 
        corrected_customers AS c
    JOIN
        repayments AS r 
            ON c.CustomerID = r.CustomerID
    GROUP BY 
        c.CustomerID, c.CorrectedAge  
    ORDER BY 
        AgeCategory, Rank; 
"""
    return qry
