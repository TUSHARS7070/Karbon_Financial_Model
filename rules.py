import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  
    WHITE = 4  

def latest_financial_index(data: dict):

    financials = data.get("data", {}).get("financials")
    
    if not financials or not isinstance(financials, list):
        print("Financials data is missing or invalid.")
        return -1  
    
    for index, financial in enumerate(financials):
        if financial.get("nature") == "STANDALONE":
            return index
    
    return 0  


def total_revenue(data: dict, financial_index: int):

    try:
        return data['financials'][financial_index]['pnl']['lineItems']['netRevenue']
    except KeyError:
        return None

def total_borrowing(data: dict, financial_index: int):

    try:
        financial = data['financials'][financial_index]
        long_term_borrowing = financial['bs']['lineItems']['longTermBorrowings']
        short_term_borrowing = financial['bs']['lineItems']['shortTermBorrowings']
        return long_term_borrowing + short_term_borrowing
    except KeyError:
        return None

def iscr(data: dict, financial_index: int):

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

    iscr_value = iscr(data, financial_index)
    if iscr_value is None or iscr_value < 2:
        return FLAGS.RED
    return FLAGS.GREEN

def total_revenue_5cr_flag(data: dict, financial_index: int):

    revenue = total_revenue(data, financial_index)
    if revenue is None or revenue < 50000000:  
        return FLAGS.RED
    return FLAGS.GREEN

def borrowing_to_revenue_flag(data: dict, financial_index: int):

    revenue = total_revenue(data, financial_index)
    total_borrowing_value = total_borrowing(data, financial_index)
    
    if revenue is None or total_borrowing_value is None:
        return FLAGS.WHITE

    borrowing_to_revenue_ratio = total_borrowing_value / revenue

    if borrowing_to_revenue_ratio <= 0.25:
        return FLAGS.GREEN
    return FLAGS.AMBER
