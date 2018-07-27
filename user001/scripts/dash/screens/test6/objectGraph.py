d = [
{
    'output': {
        'object': 'inputTable',
        'param': 'rows',
        'type': 'CDataTable',
    },
    'input': [
        {
            'object': 'addRow',
            'param': 'n_clicks',
            'type': 'CButton',
        },
    ],
    'callback': 'addRow',
},
{
    'output': {
        'object': 'myChart',
        'param': 'figure',
        'type': 'CChart',
    },
    'input': [
        {
            'object': 'inputTable',
            'param': 'rows',
            'type': 'CDataTable',
        },
        {
            'object': 'slider',
            'param': 'value',
            'type': 'CSlider',
        },
    ],
    'callback': 'updateChart',
},
]