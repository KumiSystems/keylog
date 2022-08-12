from django.template.loader import render_to_string

from core.models import Key

from ajax_datatable.views import AjaxDatatableView


class KeyDataView(AjaxDatatableView):
    model = Key
    title = "All Keys"
    initial_order = [["created_at", "asc"], ]

    column_defs = [
        {
            'name': '',
            'visible': True,
            'defaultContent': render_to_string('frontend/datatables/key_list.html'),
            "className": 'dataTables_row-tools',
            'width': 30,
        },
        {'name': 'id', "visible": True},
        {'name': 'application', 'visible': True, },
        {'name': 'key', 'visible': True, },
        {'name': 'created_at', 'visible': True, },
        {'name': 'used_at', 'visible': True, },
    ]
    
