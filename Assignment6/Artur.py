import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

mouse_data = pd.read_csv('Mouse_metadata.csv')
study_results = pd.read_csv('Study_results.csv')
merged_df = pd.merge(mouse_data, study_results, on='Mouse ID')
color_choices = {
    'light-blue': '#7FAB8',
    'light-grey': '#F7EFED',
    'light-red': '#F1485B',
    'dark-blue': '#33546D',
    'middle-blue': '#61D4E2'
}

drug_colors = {
    'Placebo': '#29304E',
    'Capomulin': '#27706B',
    'Ramicane': '#71AB7F',
    'Ceftamin': '#9F4440',
    'Infubinol': '#FFD37B',
    'Ketapril': '#FEADB9',
    'Naftisol': '#B3AB9E',
    'Propriva': '#ED5CD4',
    'Stelasyn': '#97C1DF',
    'Zoniferol': '#8980D4'
}

colors = {
    'full-background': color_choices['light-grey'],
    'chart-background': color_choices['light-grey'],
    'histogram-color-1': color_choices['dark-blue'],
    'histogram-color-2': color_choices['light-red'],
    'block-borders': color_choices['dark-blue']
}

margins = {
    'block-margins': '10px 10px 10px 10px',
    'block-margins': '4px 4px 4px 4px'
}

sizes = {
    'subblock-heights': '290px'
}

drug_group = {
    'Lightweight': ['Ramicane', 'Capomulin'],
    'Heavyweight': ['Infubinol', 'Ceftamin', 'Ketapril', 'Naftisol', 'Propriva', 'Stelasyn', 'Zoniferol'],
    'Placebo': ['Placebo']
}

div_title = html.Div(children=html.H1('Mouse Experiment'),
                     style={
                         'border': '3px {} solid'.format(colors['block-borders']),
                         'margin': margins['block-margins'],
                         'text-align': 'center'
                     }
                     )

div_1_1_button = dcc.Checklist(
    id='weight-histogram-checklist',
    options=[{'label': drug, 'value': drug} for drug in np.unique(mouse_data['Drug Regimen'])],
    value=['Placebo'],
    labelStyle={'display': 'inline-block'}
)

div_1_1_graph = dcc.Graph(
    id='weight-histogram',

)

div_1_1 = html.Div(children=[div_1_1_button, div_1_1_graph],
                   style={
                       'border': '1px {} solid'.format(colors['block-borders']),
                       'margin': margins['block-margins'],
                       'width': '50%',
                   },

                   )

div_1_2_button = dcc.RadioItems(
    id='comparison-histogram-checklist',
    options=[
        {'label': drug, 'value': drug} for drug in np.unique(mouse_data['Drug Regimen'])
    ],
    value='Placebo',
    labelStyle={'display': 'inline-block'}
)
div_1_2_graph = dcc.Graph(
    id='comparison-histogram',
)


div_1_2 = html.Div(children=[div_1_2_button, div_1_2_graph],
                   style={
                       'border': '1px {} solid'.format(colors['block-borders']),
                       'margin': margins['block-margins'],
                       'width': '50%',
                   })
div_1_3_checklist = dcc.Checklist(
    id='main-category-checklist',
    options=[
        {'label': 'Lightweight', 'value': 'Lightweight'},
        {'label': 'Heavyweight', 'value': 'Heavyweight'},
        {'label': 'Placebo', 'value': 'Placebo'}
    ],
    value=[],
    labelStyle={'display': 'inline-block'}
)

div_1_3_sub_checklist = dcc.Checklist(
    id='sub-category-checklist',
    options=[],
    value=[],
    labelStyle={'display': 'inline-block'}
)

div_1_3_graph = dcc.Graph(
    id='drug-effect-graph',
)

div_1_3 = html.Div([
    div_1_3_checklist,
    div_1_3_sub_checklist,
    div_1_3_graph
], style={
    'border': '1px {} solid'.format(colors['block-borders']),
    'margin': margins['block-margins'],
    'width': '50%',
})

div_4_button = dcc.Checklist(
    id='group-selection-checklist',
    options=[{'label': key, 'value': key} for key in drug_group.keys()],
    value=[],
    labelStyle={'display': 'inline-block'}
)
div_4_graph = dcc.Graph(id='survival-function-graph')

div_4 = html.Div(children=[div_4_button, div_4_graph],
                 style={
                     'border': '1px {} solid'.format(colors['block-borders']),
                     'margin': margins['block-margins'],
                     'width': '50%',
                 })

app.layout = html.Div([
    div_title,
    html.Div([div_1_1, div_1_2],
             style={'display': 'flex',
                    'flex-direction': 'row',
                    'border': '3px {} solid'.format(colors['block-borders']),
                    'margin': margins['block-margins']}),
    html.Div([div_1_3, div_4],
             style={'display': 'flex',
                    'flex-direction': 'row',
                    'border': '3px {} solid'.format(colors['block-borders']),
                    'margin': margins['block-margins']}),
],
    style={
        'backgroundColor': colors['full-background']
    }
)


@app.callback(
    Output(component_id='weight-histogram', component_property='figure'),
    [Input(component_id='weight-histogram-checklist', component_property='value')]
)
def update_weight_histogram(drug_names):
    traces = []
    for drug in drug_names:
        traces.append(go.Histogram(x=mouse_data[mouse_data['Drug Regimen'] == drug]['Weight (g)'],
                                   name=drug,
                                   opacity=0.9,
                                   marker=dict(color=drug_colors[drug]))
                      )

    return {
        'data': traces,
        'layout': dict(
            barmode='stack',
            xaxis={'title': 'mouse weight',
                   'range': [merged_df['Weight (g)'].min(), merged_df['Weight (g)'].max()],
                   'showgrid': False
                   },
            yaxis={'title': 'number of mice',
                   'showgrid': False,
                   'showticklabels': True
                   },
            autosize=False,
            paper_bgcolor=colors['chart-background'],
            plot_bgcolor=colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            end={'x': 0, 'y': 1},
        )
    }


@app.callback(
    Output(component_id='comparison-histogram', component_property='figure'),
    [Input(component_id='comparison-histogram-checklist', component_property='value')]
)
def update_comparison_histogram(drug_names):
    traces = []

    if not isinstance(drug_names, list):
        drug_names = [drug_names]

    traces.append(go.Histogram(
        x=merged_df['Weight (g)'],
        name='all mice',
        opacity=0.5,
        marker=dict(color='lightgrey')
    ))

    for drug in drug_names:
        traces.append(go.Histogram(
            x=merged_df[merged_df['Drug Regimen'] == drug]['Weight (g)'],
            name=drug,
            opacity=0.75,
            marker=dict(color=drug_colors[drug])
        ))

    return {
        'data': traces,
        'layout': dict(
            barmode='overlay',
            xaxis={'title': 'mouse weight',
                   'range': [merged_df['Weight (g)'].min(), merged_df['Weight (g)'].max()],
                   'showgrid': False
                   },
            yaxis={'title': 'number of mice',
                   'showgrid': False,
                   'showticklabels': True
                   },
            autosize=False,
            paper_bgcolor=colors['chart-background'],
            plot_bgcolor=colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
        )
    }


@app.callback(
    [Output('sub-category-checklist', 'options'),
     Output('sub-category-checklist', 'value')],
    [Input('main-category-checklist', 'value')]
)
def update_subcategories(selected_main_categories):
    options = []
    values = []
    for category in selected_main_categories:
        subcategories = drug_group.get(category, [])
        for sub in subcategories:
            options.append({'label': sub, 'value': sub})
            values.append(sub)
    return options, values


@app.callback(
    Output('drug-effect-graph', 'figure'),
    [Input('sub-category-checklist', 'value')]
)
def update_graph(selected_drugs):
    traces = []
    for drug in selected_drugs:
        filtered_data = merged_df[merged_df['Drug Regimen'] == drug]
        if not filtered_data.empty:
            traces.append(go.Histogram(
                x=filtered_data['Weight (g)'],
                name=drug,
                opacity=0.75,
                marker=dict(color=drug_colors[drug])
            ))

    return {
        'data': traces,
        'layout': go.Layout(
            barmode='stack',
            xaxis={
                'title': 'mouse weight',
                'range': [merged_df['Weight (g)'].min(), merged_df['Weight (g)'].max()],
                'showgrid': False
            },
            yaxis={
                'title': 'number of mice',
                'showticklabels': False,
                'showgrid': False
            },
            autosize=True,
            paper_bgcolor=colors['chart-background'],
            plot_bgcolor=colors['chart-background'],
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
        )
    }


survival_data = merged_df.groupby(['Drug Regimen', 'Timepoint']).agg(Alive_Mice=('Mouse ID', 'nunique')).reset_index()


@app.callback(
    Output('survival-function-graph', 'figure'),
    [Input('group-selection-checklist', 'value')]
)
def update_survival_graph(selected_groups):
    traces = []
    for group in selected_groups:
        for drug in drug_group[group]:
            drug_data = survival_data[survival_data['Drug Regimen'] == drug]
            traces.append(go.Scatter(
                x=drug_data['Timepoint'],
                y=drug_data['Alive_Mice'],
                mode='lines+markers',
                name=drug,
                line=dict(width=2, color=drug_colors.get(drug, '#000')),
                marker=dict(size=6)
            ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'time point'},
            yaxis={'title': 'number of alive mice',
                   'showgrid': False},
            paper_bgcolor=colors['chart-background'],
            plot_bgcolor=colors['chart-background'],
            legend={'x': 1, 'y': 1},
            showlegend=True
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True, port=8001)
