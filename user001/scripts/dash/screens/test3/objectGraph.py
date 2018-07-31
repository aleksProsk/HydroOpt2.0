d = [{
    'output': {
        'object': 'myChart',
        'param': 'figure',
        'type': 'CChart',
    },
    'input': [
        {
            'object': 'mySlider',
            'param': 'value',
            'type': 'CRangeSlider',
        }
    ],
    'callback': 'updateGraph',
},
{
    'output': {
        'object': 'mySlider',
        'param': 'value',
        'type': 'CRangeSlider',
    },
    'input': [
        {
            'object': 'myButton',
            'param': 'n_clicks',
            'type': 'CButton',
        }
    ],
    'callback': 'resetSlider',
},
]