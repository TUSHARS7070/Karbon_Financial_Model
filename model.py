from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, borrowing_to_revenue_flag
import json

def analyze_financial_data(data: dict):
    """
    Analyze financial data and evaluate various flags.
    """
    latest_financial_index_value = latest_financial_index(data)

    # If the latest financial index is -1, handle the error
    if latest_financial_index_value == -1:
        return {
            "error": "Invalid financial data. Could not find valid financial entries."
        }

    total_revenue_5cr_flag_value = total_revenue_5cr_flag(data, latest_financial_index_value)
    borrowing_to_revenue_flag_value = borrowing_to_revenue_flag(data, latest_financial_index_value)
    iscr_flag_value = iscr_flag(data, latest_financial_index_value)

    # Return results formatted for display
    return [
        f"Rule 1: TOTAL_REVENUE_5CR_FLAG - {total_revenue_5cr_flag_value}",
        f"Rule 2: BORROWING_TO_REVENUE_FLAG - {borrowing_to_revenue_flag_value}",
        f"Rule 3: ISCR_FLAG - {iscr_flag_value}",
    ]

if __name__ == "__main__":
    # Read the JSON file
    with open("data.json", "r") as file:
        content = file.read()
        # Convert content to json
        data = json.loads(content)
        
        # Run the analysis on the provided data
        result = analyze_financial_data(data["data"])

        # Output the result in a human-readable format
        for line in result:
            print(line)
