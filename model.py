from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, borrowing_to_revenue_flag
import json

def analyze_financial_data(data: dict):

    latest_financial_index_value = latest_financial_index(data)

    if latest_financial_index_value == -1:
        return {
            "error": "Invalid financial data. Could not find valid financial entries."
        }

    total_revenue_5cr_flag_value = total_revenue_5cr_flag(data, latest_financial_index_value)
    borrowing_to_revenue_flag_value = borrowing_to_revenue_flag(data, latest_financial_index_value)
    iscr_flag_value = iscr_flag(data, latest_financial_index_value)

    return [
        f"Rule 1: TOTAL_REVENUE_5CR_FLAG - {total_revenue_5cr_flag_value}",
        f"Rule 2: BORROWING_TO_REVENUE_FLAG - {borrowing_to_revenue_flag_value}",
        f"Rule 3: ISCR_FLAG - {iscr_flag_value}",
    ]

if __name__ == "__main__":
    with open("data.json", "r") as file:
        content = file.read()
        data = json.loads(content)
        
        result = analyze_financial_data(data["data"])

        for line in result:
            print(line)
