import apps.commonmodules as cm
import pendulum
import pandas as pd
import datetime
from datequarter import DateQuarter
import dash_bootstrap_components as dbc
from dash import Input, Output, html
import dash_mantine_components as dmc

now = datetime.datetime.now()
q_start = (DateQuarter.from_date(now)-1).start_date()
q_end = (DateQuarter.from_date(now)-1).end_date()
m_end = now.replace(day=1) - datetime.timedelta(days=1)
m_start = m_end.replace(day=1)
y_end = m_end
y_start = m_end.replace(day=1).replace(month=1)


def get_period(num=1):
    d = dict()
    if num==1:
        per_start = datetime.date(2017, 1, 1).strftime("%Y-%m-%d")
        per_end = now.strftime("%Y-%m-%d")
    elif num==2:
        per_start = y_start.strftime("%Y-%m-%d")
        per_end = y_end.strftime("%Y-%m-%d")
    elif num==3:
        per_start = q_start.strftime("%Y-%m-%d")
        per_end = q_end.strftime("%Y-%m-%d")
    else:
        per_start = m_start.strftime("%Y-%m-%d")
        per_end = m_end.strftime("%Y-%m-%d")
    d['start'] = per_start
    d['end'] = per_end
    return d

period_group = html.Div(
    [
        dmc.SegmentedControl(
            id="radios",
            value=1,
            size="sm",
            color="blue",
            data=[
                {"label": "Увесь період", "value": 1},
                {"label": "Поточний рік", "value": 2},
                {"label": "Квартал", "value": 3},
                {"label": "Місяць", "value": 4},
            ],
            mt=10,
        )

    ],
    style={'marginTop': -12},
    className="small",
)
