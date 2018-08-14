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
        {
            'object': 'slider1',
            'param': 'value',
            'type': 'CSlider',
        },
    ],
    'callback': 'updateChart',
},
{
    'output': {
        'object': 'modal',
        'param': 'style',
        'type': 'CModal',
    },
    'input': [
        {
            'object': 'btn',
            'param': 'n_clicks',
            'type': 'CButton',
        },
        {
            'object': 'modalCloser',
            'param': 'n_clicks',
            'type': 'CText',
        },
    ],
    'state': [
        {
            'object': 'modal',
            'param': 'style',
            'type': 'CModal',
        },
    ],
    'callback': 'loadModal',
},
{
    'output': {
        'object': 'mySelectList',
        'param': 'children',
        'type': 'CSelectList',
    },
    'input': [
        {
            'object': 'mySelectList',
            'param': 'n_clicks',
            'type': 'CSelectList-labels-3',
        },
    ],
    'callback': 'selectListInteraction',
}]