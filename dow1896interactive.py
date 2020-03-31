from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Kline, Line, Bar, Grid, Page, Tab
import pandas as pd
import numpy as np
from typing import List, Sequence, Union

def split_data(origin_data) -> dict:
    datas = []
    times = []
    vols = []
    macds = []
    

    for i in range(len(origin_data)):
        datas.append(origin_data[i][1:])
        times.append(origin_data[i][0:1][0])
        vols.append(origin_data[i][5])
        macds.append(origin_data[i][7])
        
    vols = [int(v) for v in vols]

    return {
        "datas": datas,
        "times": times,
        "vols": vols,
        "macds": macds,
       
    }

def calculate_ma1(day_count: int, p):
    result=ta.MA(p,timeperiod=day_count)
    return result
def calculate_ma(day_count: int):
    result: List[Union[float, str]] = []

    for i in range(len(data["times"])):
        if i < day_count:
            result.append("-")
            continue
        sum_total = 0.0
        for j in range(day_count):
            sum_total += float(data["datas"][i - j][1])
        result.append(abs(float("%.2f" % (sum_total / day_count))))
    return result

def get_df(filename):
    global df, price
    df=pd.read_csv(str(filename)+'.csv')
    last=df.last_valid_index()
    df=df.loc[:last]
    #df.Open=np.log10(df.Open)
    #df.Close=np.log10(df.Close)
    #df.Low=np.log10(df.Low)
    #df.High=np.log10(df.High)
    
    price=df.Close.values
    #df.index = df.index.astype('str')
    df=df.fillna(0)
    df=df.values.tolist()
    return df, price
    
def draw_charts(nome,day):
    get_df(nome)
    echarts_data = df
    global data
    data = split_data(origin_data=echarts_data)
    #
    kline = (
        Kline()
        .add_xaxis(xaxis_data=data["times"])
        .add_yaxis(
            series_name="",
            y_axis=data["datas"],
            itemstyle_opts=opts.ItemStyleOpts(
                color="#ef232a",
                color0="#14b143",
                border_color="#ef232a",
                border_color0="#14b143",
            
            ),
            
        )
        
        .set_global_opts(
            title_opts=opts.TitleOpts(title=str(day), pos_left="0"),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                is_scale=True,
                boundary_gap=False,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                split_number=20,
                min_="dataMin",
                max_="dataMax",
            ),
            yaxis_opts=opts.AxisOpts(
                is_scale=True, splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line"),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=False, type_="inside", xaxis_index=[0, 0], range_end=100
                ),
                opts.DataZoomOpts(
                    is_show=True, xaxis_index=[0, 1], pos_top="95%", range_end=100
                ),
                opts.DataZoomOpts(is_show=False, xaxis_index=[0, 2], range_end=100),
            ],
            
        )
    )
    
    kline_line = (
        Line()
        .add_xaxis(xaxis_data=data["times"])
        .add_yaxis(
            series_name="MA20",
            y_axis=calculate_ma(day_count=20),
            
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="MA60",
            y_axis=calculate_ma(day_count=60),
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="MA120",
            y_axis=calculate_ma(day_count=120),
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        ).add_yaxis(
            series_name="MA200",
            y_axis=calculate_ma(day_count=200),
            is_smooth=True,
            linestyle_opts=opts.LineStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
       
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                grid_index=1,
                axislabel_opts=opts.LabelOpts(is_show=False),
            ),
            yaxis_opts=opts.AxisOpts(
                grid_index=1,
                split_number=3,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=False),
            ),
        )
    )
    overlap_kline_line = kline.overlap(kline_line)
    
    bar_1 = (
        Bar()
        .add_xaxis(xaxis_data=data["times"])
        .add_yaxis(
            series_name="Volumn",
            yaxis_data=data["vols"],
            xaxis_index=1,
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            
            itemstyle_opts=opts.ItemStyleOpts(
                color=JsCode(
                    """
                function(params) {
                    var colorList;
                    if (barData[params.dataIndex][1] > barData[params.dataIndex][0]) {
                        colorList = '#ef232a';
                    } else {
                        colorList = '#14b143';
                    }
                    return colorList;
                }
                """
                )
            ),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                grid_index=1,
                axislabel_opts=opts.LabelOpts(is_show=False),
            ),
            yaxis_opts=opts.AxisOpts(
                grid_index=1,
                split_number=2,
                axislabel_opts=opts.LabelOpts(is_show=False),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    
    bar_2 = (
        Bar()
        .add_xaxis(xaxis_data=data["times"])
        .add_yaxis(
            series_name="MACD",
            yaxis_data=data["macds"],
            xaxis_index=2,
            yaxis_index=2,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(
                color=JsCode(
                    """
                        function(params) {
                            var colorList;
                            if (params.data >= 0) {
                              colorList = '#ef232a';
                            } else {
                              colorList = '#14b143';
                            }
                            return colorList;
                        }
                        """
                )
            ),
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="category",
                grid_index=2,
                axislabel_opts=opts.LabelOpts(is_show=False),
            ),
            yaxis_opts=opts.AxisOpts(
                grid_index=2,
                split_number=2,
                axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=True),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    
    line_2 = (
        Line()
        .add_xaxis(xaxis_data=data["times"])
        .add_yaxis(
            series_name="DIF",
            y_axis=[],
            xaxis_index=2,
            yaxis_index=2,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .add_yaxis(
            series_name="DIF",
            y_axis=[],
            xaxis_index=2,
            yaxis_index=2,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
    )
    overlap_bar_line = bar_2.overlap(line_2)
    
    grid_chart = Grid()
    
    grid_chart.add_js_funcs("var barData = {}".format(data["datas"]))
    
    grid_chart.add(
        overlap_kline_line,
        grid_opts=opts.GridOpts(pos_left="10%", pos_right="6%", height="55%"),
    )
    grid_chart.add(
        bar_1,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="6%", pos_top="72%", height="8%"
        ),
    )
    grid_chart.add(
        overlap_bar_line,
        grid_opts=opts.GridOpts(
            pos_left="10%", pos_right="6%", pos_top="83%", height="10%"
        ),
    )


    #page.add(grid_chart)
    tab.add(grid_chart,str(day))


#page=Page(layout=Page.DraggablePageLayout)
tab=Tab()
draw_charts('dji','Daily')
tab.render("Daily1.html")

tab=Tab()
draw_charts('dji_w','Weekly')
tab.render("Weekly1.html")

tab=Tab()
draw_charts('dji_m','Monthly')
tab.render("Monthly1.html")






