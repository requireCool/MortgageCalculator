import os
from prettytable import PrettyTable


hp_loan_interest_rate = float(os.environ.get('HOUSE_PROVIDENT_FUND_LOAN_INTEREST_RATE', default=0.031))
c_loan_interest_rate = float(os.environ.get('COMMERCIAL_FUND_LOAN_INTEREST_RATE', default=0.0395))

HOUSE_PROVIDENT_FUND_LOAN_INTEREST_RATE_PER_MONTH = hp_loan_interest_rate / 12
COMMERCIAL_FUND_LOAN_INTEREST_RATE_PER_MONTH = c_loan_interest_rate / 12


def calculate(hp_loans, c_loans, loan_month, repay_method, hp_balance, hp_income_per_month):
    table = PrettyTable()
    table.add_column("月数", [f"第{m + 1}月" for m in range(loan_month)])
    if repay_method == 1:
        hp_linear = linear(hp_loans, HOUSE_PROVIDENT_FUND_LOAN_INTEREST_RATE_PER_MONTH, loan_month)
        c_linear = linear(c_loans, COMMERCIAL_FUND_LOAN_INTEREST_RATE_PER_MONTH, loan_month)
        repaid_data, hp_balance_data = repaid_per_month(hp_linear, c_linear, loan_month, hp_balance, hp_income_per_month)
        table.add_column("商业贷款", c_linear)
        table.add_column("公积金贷款", hp_linear)
        table.add_column("月还款额", repaid_data)
        table.add_column("公积金余额", hp_balance_data)
    elif repay_method == 2:
        hp_annuity = annuity(hp_loans, HOUSE_PROVIDENT_FUND_LOAN_INTEREST_RATE_PER_MONTH, loan_month)
        c_annuity = annuity(c_loans, COMMERCIAL_FUND_LOAN_INTEREST_RATE_PER_MONTH, loan_month)
        repaid_data, hp_balance_data = repaid_per_month(hp_annuity, c_annuity, loan_month, hp_balance, hp_income_per_month)
        table.add_column("商业贷款", c_annuity)
        table.add_column("公积金贷款", hp_annuity)
        table.add_column("月还款额", repaid_data)
        table.add_column("公积金余额", hp_balance_data)
    else:
        return "Error repay method", -1

    return table, sum(repaid_data)


def linear(loan_amount, rate, month):
    """等额本息"""
    repayment = loan_amount * (rate * (1 + rate) ** month) / ((1 + rate) ** month - 1)
    return [round(repayment, 2) for _ in range(month)]


def annuity(loan_amount, rate, month):
    """等额本金 (本金/还款月数) + (本金-已归还本金累计额) * 月利率"""
    monthly_repayment = []
    repaid_loan_per_month = loan_amount / month
    for i in range(month):
        repaid_loan = repaid_loan_per_month * i
        repayment = (loan_amount / month) + (loan_amount - repaid_loan) * rate
        monthly_repayment.append(round(repayment, 2))
    return monthly_repayment


def repaid_per_month(hp_repaid_data, c_repaid_data, months, current_hp_balance, hp_income_per_month):
    repaid_data = []
    hp_balance_data = []
    for i in range(months):
        # hp_repaid是公积金不足时需要偿还的公积金贷款月供
        current_hp_balance = current_hp_balance + hp_income_per_month
        if current_hp_balance > hp_repaid_data[i]:
            hp_repaid = 0
            current_hp_balance -= hp_repaid_data[i]
        else:
            hp_repaid = hp_repaid_data[i] - current_hp_balance
            current_hp_balance = 0

        hp_balance_data.append(round(current_hp_balance, 2))

        total_repaid = hp_repaid + c_repaid_data[i]
        repaid_data.append(round(total_repaid, 2))
    return repaid_data, hp_balance_data


if __name__ == '__main__':
    hp_loans = int(input("公积金贷款金额（万）：")) * 10000
    c_loans = int(input("商业贷款金额（万）：")) * 10000
    repay_method = int(input("还款方式（1-等额本息，2-等额本金）："))
    loan_month = int(input("还款月数："))
    hp_balance = float(input("公积金余额（万）：")) * 10000
    hp_income_per_month = float(input("公积金月收入（千）：")) * 1000
    table, total_interest = calculate(hp_loans, c_loans, loan_month, repay_method, hp_balance, hp_income_per_month)
    print(table)
