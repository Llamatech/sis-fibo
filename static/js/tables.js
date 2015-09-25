// var table;

function deleteFunc(elem) {
    BootstrapDialog.confirm({
        title: 'Advertencia',
        message: '¿Desea eliminar a este empleado?',
        type: BootstrapDialog.TYPE_WARNING, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
        closable: true, // <-- Default value is false
        draggable: true, // <-- Default value is false
        btnCancelLabel: 'Cancelar', // <-- Default value is 'Cancel',
        btnOKLabel: 'Eliminar', // <-- Default value is 'OK',
        btnOKClass: 'btn-warning', // <-- If you didn't specify it, dialog type will be used,
        callback: function(result) {
            // result will be true if button was click, while it will be false if users close the dialog directly.
            if (result) {
                var urlD = $(elem).attr('deleteE');
                console.log(urlD);
                var table = $("#emp_table").DataTable();
                // console.log(table);
                console.log($(elem).parents('tr'));
                $(elem).parents('tr').addClass('selected');
                $.ajax({
                    url: urlD,
                    type: 'DELETE',
                    success: function(response) {
                        //...
                        table.rows('.selected').remove().draw();
                    }
                });
            } else {
                //alert('Nope.');
            }
        }
    });
}

function deleteFuncO(elem) {
    BootstrapDialog.confirm({
        title: 'Advertencia',
        message: '¿Desea eliminar esta oficina?',
        type: BootstrapDialog.TYPE_WARNING, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
        closable: true, // <-- Default value is false
        draggable: true, // <-- Default value is false
        btnCancelLabel: 'Cancelar', // <-- Default value is 'Cancel',
        btnOKLabel: 'Eliminar', // <-- Default value is 'OK',
        btnOKClass: 'btn-warning', // <-- If you didn't specify it, dialog type will be used,
        callback: function(result) {
            // result will be true if button was click, while it will be false if users close the dialog directly.
            if (result) {
                var urlD = $(elem).attr('deleteO');
                console.log(urlD);
                var table = $("#office_table").DataTable();
                // console.log(table);
                console.log($(elem).parents('tr'));
                $(elem).parents('tr').addClass('selected');
                $.ajax({
                    url: urlD,
                    type: 'DELETE',
                    success: function(response) {
                        //...
                        table.rows('.selected').remove().draw();
                    }
                });
            } else {

            }
        }
    });
}

$(document).ready(function() {

    var table = $('#emp_table').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/empleados",
            "type": "POST"
        },
        "columns": [{
            "data": "id"
        }, {
            "data": "email"
        }, {
            "data": "tipo_un"
        }, {
            "data": "tipo_doc"
        }, {
            "data": "num_documento"
        }, {
            "data": "nombre"
        }, {
            "data": "apellido"
        }, {
            "data": "ciudad"
        }, {
            "data": "nombre_oficina"
        }, {
            "data": "delete"
        }],
        "columnDefs": [{
            "render": function(data, type, row) {
                var values = data.split('|')
                var style = '<div class="row"><div class="col-xs-2"><a onClick="' + 'return deleteFunc(this)' + '" deleteE="' + values[0] + '"><i class="fa fa-trash"></i></a></div><div class="col-xs-2"><a href="' + values[1] + '"><i class="fa fa-pencil-square-o"></i></a></div></div>';
                return style;
            },
            "targets": 9
        }]
    });

    $('#office_table').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/oficinas",
            "type": "POST"
        },
        "columns": [{
            "data": "id"
        }, {
            "data": "localizacion"
        }, {
            "data": "nombre"
        }, {
            "data": "direccion"
        }, {
            "data": "telefono"
        }, {
            "data": "id_gerente"
        }, {
            "data": "gerente"
        }, {
            "data": "delete"
        }],
        "columnDefs": [{
            "render": function(data, type, row) {
                var values = data.split('|')
                var style = '<div class="row"><div class="col-xs-2"><a onClick="' + 'return deleteFuncO(this)' + '" deleteO="' + values[0] + '"><i class="fa fa-trash"></i></a></div><div class="col-xs-2"><a href="' + values[1] + '"><i class="fa fa-pencil-square-o"></i></a></div></div>';
                return style;
            },
            "targets": 7
        }]
    });

    // $('#example tbody').on( 'click', 'tr', function () {
    //         if ( $(this).hasClass('selected') ) {
    //             $(this).removeClass('selected');
    //         }
    //         else {
    //             table.$('tr.selected').removeClass('selected');
    //             $(this).addClass('selected');
    //         }
    //     } );



});