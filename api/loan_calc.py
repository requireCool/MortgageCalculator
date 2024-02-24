import os
from prettytable import PrettyTable


af_loan_interest_rate = float(os.environ.get('AF_LOAN_INTEREST_RATE', default=0.031))
cf_loan_interest_rate = float(os.environ.get('CF_LOAN_INTEREST_RATE', default=0.0395))

ACCUMULATION_FUND_LOAN_INTEREST_RATE_PER_MONTH = af_loan_interest_rate / 12
COMMERCIAL_FUND_LOAN_INTEREST_RATE_PER_MONTH = cf_loan_interest_rate / 12


def calculate(af_loan_amount, cf_loan_amount, loan_month, repay_method, current_af_balance, af_income_per_month):
    table = PrettyTable()
    table.add_column("月数", [f"第{m + 1}月" for m in range(loan_month)])
    if repay_method == 1:
        af_linear = linear(af_loan_amount, ACCUMULATION_FUND_LOAN_INTEREST_RATE_PER_MONTH, loan_month)
        cf_linear = linear(cf_loan_amount, COMMERCIAL_FUND_LOAN_INTEREST_RATE_PER_MONTH, loan_month)
        monthly_repaid = repaid_per_month(af_linear, cf_linear, loan_month, current_af_balance, af_income_per_month)
        table.add_column("商业贷款", cf_linear)
        table.add_column("公积金贷款", af_linear)
        table.add_column("月还款额", monthly_repaid)
    elif repay_method == 2:
        af_annuity = annuity(af_loan_amount, ACCUMULATION_FUND_LOAN_INTEREST_RATE_PER_MONTH, loan_month)
        cf_annuity = annuity(cf_loan_amount, COMMERCIAL_FUND_LOAN_INTEREST_RATE_PER_MONTH, loan_month)
        monthly_repaid = repaid_per_month(af_annuity, cf_annuity, loan_month, current_af_balance, af_income_per_month)
        table.add_column("商业贷款", cf_annuity)
        table.add_column("公积金贷款", af_annuity)
        table.add_column("月还款额", monthly_repaid)
    else:
        return "Error repay method", -1
    total_interest = sum(monthly_repaid)
    return table, total_interest


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


def repaid_per_month(af_annuity, cf_annuity, months, current_af_balance, af_income_per_month):
    result = []
    for i in range(months):
        # af_repaid是公积金不足时需要偿还的公积金贷款月供
        current_af_balance = current_af_balance + af_income_per_month
        if current_af_balance > af_annuity[i]:
            af_repaid = 0
            current_af_balance -= af_annuity[i]
        else:
            af_repaid = af_annuity[i] - current_af_balance
            current_af_balance = 0

        total_repaid = af_repaid + cf_annuity[i]
        result.append(round(total_repaid, 2))
    return result


if __name__ == '__main__':
    af_loan_amount = int(input("公积金贷款金额（万）：")) * 10000
    cf_loan_amount = int(input("商业贷款金额（万）：")) * 10000
    repay_method = int(input("还款方式（1-等额本息，2-等额本金）："))
    loan_month = int(input("还款月数："))
    current_af_balance = float(input("公积金余额（万）：")) * 10000
    af_income_per_month = float(input("公积金月收入（千）：")) * 1000
    calc = calculate(af_loan_amount, cf_loan_amount, loan_month, repay_method, current_af_balance, af_income_per_month)
    print(calc)
