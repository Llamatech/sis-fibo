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

function deleteFuncP(elem) {
    BootstrapDialog.confirm({
        title: 'Advertencia',
        message: '¿Desea eliminar este punto de atención?',
        type: BootstrapDialog.TYPE_WARNING, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
        closable: true, // <-- Default value is false
        draggable: true, // <-- Default value is false
        btnCancelLabel: 'Cancelar', // <-- Default value is 'Cancel',
        btnOKLabel: 'Eliminar', // <-- Default value is 'OK',
        btnOKClass: 'btn-warning', // <-- If you didn't specify it, dialog type will be used,
        callback: function(result) {
            // result will be true if button was click, while it will be false if users close the dialog directly.
            if (result) {
                var urlD = $(elem).attr('deleteP');
                console.log(urlD);
                var table = $("#pa_table").DataTable();
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


function deleteFuncC(elem) {
    BootstrapDialog.confirm({
        title: 'Advertencia',
        message: '¿Desea cerrar esta cuenta?',
        type: BootstrapDialog.TYPE_WARNING, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
        closable: true, // <-- Default value is false
        draggable: true, // <-- Default value is false
        btnCancelLabel: 'Cancelar', // <-- Default value is 'Cancel',
        btnOKLabel: 'Cerrar', // <-- Default value is 'OK',
        btnOKClass: 'btn-warning', // <-- If you didn't specify it, dialog type will be used,
        callback: function(result) {
            // result will be true if button was click, while it will be false if users close the dialog directly.
            if (result) {
                var urlD = $(elem).attr('deleteP');
                console.log(urlD);
                var table = $("#acc_tablegoficina").DataTable();
                // console.log(table);
                console.log($(elem).parents('tr'));
                $(elem).parents('tr').addClass('selected');
                $.ajax({
                    url: urlD,
                    type: 'DELETE',
                    success: function(response) {
                        //...
                        table.search("").draw();
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

	$('#pa_table').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/puntosAtencion",
            "type": "POST"
        },
        "columns": [{
            "data": "id"
        }, {
            "data": "localizacion"
        }, {
            "data": "tipo_pa"
        }, {
            "data": "oficina"
        }, {
            "data": "nombre"
        }, {
            "data": "delete"
        }],
        "columnDefs": [{
            "render": function(data, type, row) {
                var values = data.split('|')
                var style = '<div class="row"><div class="col-xs-2"><a onClick="' + 'return deleteFuncP(this)' + '" deleteP="' + values[0] + '"><i class="fa fa-trash"></i></a></div><div class="col-xs-2"><a href="' + values[1] + '"><i class="fa fa-pencil-square-o"></i></a></div></div>';
                return style;
            },
            "targets": 5
        }]
    });

    var state = '1'
    $('#acc_tableggeneral').DataTable({
        dom: 'Bfrtip',
        stateSave: true,
        buttons: [
            'colvis',
            {
                text: 'Buscar por nombre de cliente',
                action: function ( e, dt, node, config ) {
                    $(this).attr("test_attr", "a");
                    state = "1";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Nombre de cliente');
                    // alert($(this).attr("test_attr")) 
                },
                className:'info'
            },
            {
                text: 'Buscar por Tipo de cuenta',
                action: function ( e, dt, node, config ) {
                    $(this).attr("test_attr", "a");
                    state = "2";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Tipo de cuenta');
                    // alert($(this).attr("test_attr")) 
                },
                className:'info'
            }
        ],
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/cuentas",
            "type": "POST",
            "data": function ( d ) {
                d.test = state,
                d.creacionStart = $("#fromD").val(),
                d.creacionStop = $("#toD").val(),
                d.uMovStart = $("#fromMD").val(),
                d.uMovStop = $("#toMD").val(),
                d.saldoFrom = $("#sumFrom").val(),
                d.saldoTo =  $("#sumTo").val()
                // d.custom = $('#myInput').val();
                // etc
            }
        },
        "columns": [{
            "data": "numero"
        }, {
            "data": "fecha_creacion"
        }, {
            "data": "saldo"
        }, {
            "data": "tipo"
        }, {
            "data": "cerrada"
        }, {
            "data": "id_cliente"
        }, {
            "data": "nom_cliente"
        }, {
            "data": "ap_cliente"
        }, {
            "data": "id_of"
        }, {
            "data": "of_nombre"
        }, {
            "data": "fecha_umov"
        }]
    });

    var state_o = '1'
    $('#acc_tablegoficina').DataTable({
        dom: 'Bfrtip',
        stateSave: true,
        buttons: [
            'colvis',
            {
                text: 'Buscar por nombre de cliente',
                action: function ( e, dt, node, config ) {
                    $(this).attr("test_attr", "a");
                    state_o = "1";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Nombre de cliente');
                    // alert($(this).attr("test_attr")) 
                },
                className:'info'
            },
            {
                text: 'Buscar por Tipo de cuenta',
                action: function ( e, dt, node, config ) {
                    $(this).attr("test_attr", "a");
                    state_o = "2";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Tipo de cuenta');
                    // alert($(this).attr("test_attr")) 
                },
                className:'info'
            }
        ],
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/cuentas",
            "type": "POST",
            "data": function ( d ) {
                d.test = state_o,
                d.creacionStart = $("#fromD").val(),
                d.creacionStop = $("#toD").val(),
                d.uMovStart = $("#fromMD").val(),
                d.uMovStop = $("#toMD").val(),
                d.saldoFrom = $("#sumFrom").val(),
                d.saldoTo =  $("#sumTo").val()
                // d.custom = $('#myInput').val();
                // etc
            }
        },
        "columns": [{
            "data": "numero"
        }, {
            "data": "fecha_creacion"
        }, {
            "data": "saldo"
        }, {
            "data": "tipo"
        }, {
            "data": "cerrada"
        }, {
            "data": "id_cliente"
        }, {
            "data": "nom_cliente"
        }, {
            "data": "ap_cliente"
        }, {
            "data": "id_of"
        }, {
            "data": "of_nombre"
        }, {
            "data": "fecha_umov"
        },
        {"data": "delete"}],
        "columnDefs": [{
            "render": function(data, type, row) {
            	console.log(data);
            	if(data !== null)
                {
                   var style = '<div class="row"><div class="col-xs-2"><a onClick="' + 'return deleteFuncC(this)' + '" deleteP="' + data + '"><i class="fa fa-times"></i>Cerrar</a></div>';
                   return style;
                }
                return '';
            },
            "targets": 11
    }]
});

	$('#acc_search_btn').click(function() {
        var table = $('#acc_tableggeneral').DataTable();
        table.search("").draw();
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
