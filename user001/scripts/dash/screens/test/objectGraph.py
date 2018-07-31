d = [{
    'output': {
        'object': 'myOutput',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myDatePicker',
            'param': 'start_date',
            'type': 'CDatePickerRange',
        },
        {
            'object': 'myDatePicker',
            'param': 'end_date',
            'type': 'CDatePickerRange',
        }
    ],
    'callback': 'simpleExample',
},
{
    'output': {
        'object': 'dropdownText',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myDropdown',
            'param': 'value',
            'type': 'CDropdown',
        }
    ],
    'callback': 'displayValue',
},
{
    'output': {
        'object': 'sliderText',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'mySlider',
            'param': 'value',
            'type': 'CSlider',
        }
    ],
    'callback': 'displayValue',
},
{
    'output': {
        'object': 'rangeSliderText',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myRangeSlider',
            'param': 'value',
            'type': 'CRangeSlider',
        }
    ],
    'callback': 'displayValue',
},
{
    'output': {
        'object': 'inputText',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myInput',
            'param': 'value',
            'type': 'CInput',
        }
    ],
    'callback': 'displayValue',
},
{
    'output': {
        'object': 'textAreaText',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myTextArea',
            'param': 'value',
            'type': 'CTextArea',
        }
    ],
    'callback': 'displayValue',
},
{
    'output': {
        'object': 'checklistText',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myChecklist',
            'param': 'values',
            'type': 'CChecklist',
        }
    ],
    'callback': 'displayValue',
},
{
    'output': {
        'object': 'radioItemsText',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myRadioItems',
            'param': 'value',
            'type': 'CRadioItems',
        }
    ],
    'callback': 'displayValue',
},
{
    'output': {
        'object': 'buttonText',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myButton',
            'param': 'n_clicks',
            'type': 'CButton',
        }
    ],
    'callback': 'displayValue',
},
{
    'output': {
        'object': 'singleText',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myDatePicker1',
            'param': 'date',
            'type': 'CDatePickerSingle',
        }
    ],
    'callback': 'displayValue',
},
{
    'output': {
        'object': 'uploadText',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myUpload',
            'param': 'contents',
            'type': 'CUpload',
        },
        {
            'object': 'myUpload',
            'param': 'filename',
            'type': 'CUpload',
        }
    ],
    'callback': 'readFile',
},
{
    'output': {
        'object': 'tabsText',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myTabs',
            'param': 'value',
            'type': 'CTabs',
        }
    ],
    'callback': 'displayValue',
},
{
    'output': {
        'object': 'myDataTable',
        'param': 'rows',
        'type': 'CDataTable',
    },
    'input': [
        {
            'object': 'myUploadTable',
            'param': 'contents',
            'type': 'CUpload',
        },
        {
            'object': 'myUploadTable',
            'param': 'filename',
            'type': 'CUpload',
        }
    ],
    'callback': 'loadDataTable',
},
{
    'output': {
        'object': 'outputTable',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myInputTable',
            'param': 'rows',
            'type': 'CDataTable',
        },
    ],
    'callback': 'updateTableContent',
},
{
    'output': {
        'object': 'persons',
        'param': 'children',
        'type': 'CText',
    },
    'input': [
        {
            'object': 'myInputTable',
            'param': 'selected_row_indices',
            'type': 'CDataTable',
        },
    ],
    'callback': 'getPersons',
}]