import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # display purpose only
    WHITE = 4  # data is missing for this field

# This is a already written for your reference
def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.
    """
    # Access the 'financials' under 'data'
    financials = data.get("data", {}).get("financials")
    
    # Check if financials exist and is a list
    if not financials or not isinstance(financials, list):
        print("Financials data is missing or invalid.")
        return -1  # Return an error code or handle it differently
    
    for index, financial in enumerate(financials):
        if financial.get("nature") == "STANDALONE":
            return index
    
    return 0  # Default return if no STANDALONE entry is found


def total_revenue(data: dict, financial_index: int):
    """
    Calculate the total revenue from the financial data at the given index.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The net revenue value from the financial data or None if not available.
    """
    try:
        return data['financials'][financial_index]['pnl']['lineItems']['netRevenue']
    except KeyError:
        return None

def total_borrowing(data: dict, financial_index: int):
    """
    Calculate the total borrowings from the balance sheet section of the financial data.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The sum of long-term and short-term borrowings, or None if not available.
    """
    try:
        financial = data['financials'][financial_index]
        long_term_borrowing = financial['bs']['lineItems']['longTermBorrowings']
        short_term_borrowing = financial['bs']['lineItems']['shortTermBorrowings']
        return long_term_borrowing + short_term_borrowing
    except KeyError:
        return None

def iscr(data: dict, financial_index: int):
    """
    Calculate the Interest Service Coverage Ratio (ISCR).

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - float: The ISCR value, or None if data is missing.
    """
    try:
        financial = data['financials'][financial_index]
        profit_before_interest_tax = financial['pnl']['lineItems']['profitBeforeInterestAndTax']
        depreciation = financial['pnl']['lineItems']['depreciation']
        interest_expenses = financial['pnl']['lineItems']['interestExpenses']

        iscr_value = (profit_before_interest_tax + depreciation + 1) / (interest_expenses + 1)
        return iscr_value
    except KeyError:
        return None

def iscr_flag(data: dict, financial_index: int):
    """
    Determine the flag based on ISCR value.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for ISCR calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: Based on the ISCR value.
    """
    iscr_value = iscr(data, financial_index)
    if iscr_value is None or iscr_value < 2:
        return FLAGS.RED
    return FLAGS.GREEN

def total_revenue_5cr_flag(data: dict, financial_index: int):
    """
    Determine the flag based on whether the total revenue exceeds 5 crores (50 million).

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for revenue calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: Based on the total revenue.
    """
    revenue = total_revenue(data, financial_index)
    if revenue is None or revenue < 50000000:  # 5 crores in paise
        return FLAGS.RED
    return FLAGS.GREEN

def borrowing_to_revenue_flag(data: dict, financial_index: int):
    """
    Determine the flag based on the ratio of total borrowings to total revenue.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ratio calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.AMBER: Based on the borrowing to revenue ratio.
    """
    revenue = total_revenue(data, financial_index)
    total_borrowing_value = total_borrowing(data, financial_index)
    
    if revenue is None or total_borrowing_value is None:
        return FLAGS.WHITE

    borrowing_to_revenue_ratio = total_borrowing_value / revenue

    if borrowing_to_revenue_ratio <= 0.25:
        return FLAGS.GREEN
    return FLAGS.AMBER
