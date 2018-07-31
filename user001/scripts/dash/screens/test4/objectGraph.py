d = [{
    'output': {
        'object': 'myOutput',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myTopologyMap',
            'param': 'clickData',
            'type': 'CTopologyMap',
        }
    ],
    'callback': 'getClickData',
},
{
    'output': {
        'object': 'myOutput1',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myOutput1',
            'param': 'n_clicks',
            'type': 'CText',
        }
    ],
    'state': [
        {
            'object': 'myTopologyMap',
            'param': 'clickData',
            'type': 'CTopologyMap',
        }
    ],
    'callback': 'clickState',
},
{
    'output': {
        'object': 'myZoom',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myInterval',
            'param': 'n_intervals',
            'type': 'CInterval',
        }
    ],
    'state': [
        {
            'object': 'myMap',
            'param': 'figure',
            'type': 'CMap',
        }
    ],
    'callback': 'getZoom',
},
{
    'output': {
        'object': 'selected',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myTopologyMap',
            'param': 'clickData',
            'type': 'CTopologyMap',
        }
    ],
    'callback': 'getClickedInfo',
},
{
    'output': {
        'object': 'myTopologyMap',
        'param': 'figure',
        'type': 'CTopologyMap',
    },
    'input': [
        {
            'object': 'myButton',
            'param': 'n_clicks',
            'type': 'CButton',
        }
    ],
    'state': [
        {
            'object': 'myTopologyMap',
            'param': 'id',
            'type': 'CTopologyMap',
        },
        {
            'object': 'myTopologyMap',
            'param': 'clickData',
            'type': 'CTopologyMap',
        },
        {
            'object': 'inputLat',
            'param': 'value',
            'type': 'CInput',
        },
        {
            'object': 'inputLon',
            'param': 'value',
            'type': 'CInput',
        },
    ],
    'callback': 'setPointCoordinates',
},
]