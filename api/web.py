from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from pywebio.session import set_env

from api.loan_calc import calculate


def home_page():
    set_env(title="房贷计算器")
    put_markdown('### 房贷计算器')
    put_grid([
        [put_text("公积金贷款金额："), put_input(name="hp_loan", type=NUMBER), put_text("万")],
        [put_text("商业贷款金额："), put_input(name="c_loan", type=NUMBER), put_text("万")],
        [put_text("贷款期限："), put_select(name="loan_month", options=[(f"{i}年({i * 12}期)", i * 12) for i in range(1, 31)])],
        [put_text("还款方式："), put_select(name="repaid_method", options=[("等额本息", 1), ("等额本金", 2)])],
        [put_text("公积金余额："), put_input(name="hp_balance", type=FLOAT), put_text("万")],
        [put_text("公积金月收入："), put_input(name="hp_income_per_month", type=FLOAT), put_text("千")]
    ])
    put_button(label="计算", onclick=click_calc)


def click_calc():
    remove("total_repaid")
    remove("result")
    c_loans = pin.c_loan * 10000 if pin.c_loan else 0
    hp_loans = pin.hp_loan * 10000 if pin.hp_loan else 0
    hp_balance = pin.hp_balance * 10000 if pin.hp_balance else 0
    hp_income_per_month = pin.hp_income_per_month * 1000 if pin.hp_income_per_month else 0
    table, total_repaid = calculate(hp_loans, c_loans, pin.loan_month, pin.repaid_method, hp_balance, hp_income_per_month)
    put_scope("total_repaid", content=[put_text(f"总现金还款额：{round(total_repaid / 10000, 2)}万")])
    put_scope("result", content=[put_textarea(name="result", value=str(table), rows=20)])


if __name__ == '__main__':
    start_server(home_page, 80)
