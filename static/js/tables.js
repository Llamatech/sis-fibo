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
                        BootstrapDialog.alert({
                            title: 'Éxito',
                            message: 'La solicitud ha sido procesada satisfactoriamente.',
                            type: BootstrapDialog.TYPE_SUCCESS, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
                            closable: true, // <-- Default value is false
                            draggable: true, // <-- Default value is false
                            buttonLabel: 'Cerrar', // <-- Default value is 'OK',
                            callback: function(result) {
                                // result will be true if button was click, while it will be false if users close the dialog directly
                            }
                        });
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
                        BootstrapDialog.alert({
                            title: 'Éxito',
                            message: 'La solicitud ha sido procesada satisfactoriamente.',
                            type: BootstrapDialog.TYPE_SUCCESS, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
                            closable: true, // <-- Default value is false
                            draggable: true, // <-- Default value is false
                            buttonLabel: 'Cerrar', // <-- Default value is 'OK',
                            callback: function(result) {
                                // result will be true if button was click, while it will be false if users close the dialog directly
                            }
                        });
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
                        BootstrapDialog.alert({
                            title: 'Éxito',
                            message: 'La solicitud ha sido procesada satisfactoriamente.',
                            type: BootstrapDialog.TYPE_SUCCESS, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
                            closable: true, // <-- Default value is false
                            draggable: true, // <-- Default value is false
                            buttonLabel: 'Cerrar', // <-- Default value is 'OK',
                            callback: function(result) {
                                // result will be true if button was click, while it will be false if users close the dialog directly
                            }
                        });
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
                var param = urlD.split('?')[1]
                $.ajax({
                    type: 'POST',
                    url: '/nomina/migrar?' + param,
                    dataType: 'json',
                    encode: true
                }).done(function(data) {
                    if (data.has) {
                        var acc = data.acc;
                        if (acc.length > 0) {
                            var sel = '<select id="acc_subs"> \n';
                            for (var i = acc.length - 1; i >= 0; i--) {
                                var num = acc[i].numero;
                                sel += '<option value = "' + num + '">' + num + '</option> \n'
                            }
                            sel += '</select>'

                            BootstrapDialog.confirm({
                                title: '¡Atención!',
                                message: 'La cuenta empresarial a eliminar, realiza pagos recurrentes de nómina <br> Por favor, seleccione una cuenta a la cual desea transferir los pagos.' + sel,
                                type: BootstrapDialog.TYPE_WARNING, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
                                closable: true, // <-- Default value is false
                                draggable: true, // <-- Default value is false
                                btnCancelLabel: 'Cancelar', // <-- Default value is 'Cancel',
                                btnOKLabel: 'Transferir', // <-- Default value is 'OK',
                                btnOKClass: 'btn-warning',
                                callback: function(result) {
                                    // result will be true if button was click, while it will be false if users close the dialog directly.
                                    if (result) {
                                        $.ajax({
                                            url: '/nomina/migrar?' + param,
                                            type: 'PUT',
                                            data: {
                                                'numero_acc': $('#acc_subs').val()
                                            },
                                            dataType: 'json',
                                            encode: true

                                        }).done(function(data) {
                                            $.ajax({
                                                url: urlD,
                                                type: 'DELETE',
                                                success: function(response) {
                                                    //...
                                                    BootstrapDialog.alert({
                                                        title: 'Éxito',
                                                        message: 'La solicitud ha sido procesada satisfactoriamente.',
                                                        type: BootstrapDialog.TYPE_SUCCESS, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
                                                        closable: true, // <-- Default value is false
                                                        draggable: true, // <-- Default value is false
                                                        buttonLabel: 'Cerrar', // <-- Default value is 'OK',
                                                        callback: function(result) {
                                                            // result will be true if button was click, while it will be false if users close the dialog directly
                                                        }
                                                    });
                                                    table.search("").draw();
                                                }
                                            });
                                        });
                                    }
                                }
                            });
                        } else {
                            BootstrapDialog.confirm({
                                title: 'Error',
                                message: 'El cliente no cuenta con cuentas adicionales a las cuales pueda delegar el pago de nómina.',
                                type: BootstrapDialog.TYPE_DANGER, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
                                closable: true, // <-- Default value is false
                                draggable: true, // <-- Default value is false
                                btnCancelLabel: 'Cancelar', // <-- Default value is 'Cancel',
                                btnOKLabel: 'Salir', // <-- Default value is 'OK',
                                btnOKClass: 'btn-danger',
                                callback: function(result) {
                                    $(elem).parents('tr').removeClass('selected');
                                }
                            });
                        }
                    } else {
                        $.ajax({
                            url: urlD,
                            type: 'DELETE',
                            success: function(response) {
                                //...
                                BootstrapDialog.alert({
                                    title: 'Éxito',
                                    message: 'La solicitud ha sido procesada satisfactoriamente.',
                                    type: BootstrapDialog.TYPE_SUCCESS, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
                                    closable: true, // <-- Default value is false
                                    draggable: true, // <-- Default value is false
                                    buttonLabel: 'Cerrar', // <-- Default value is 'OK',
                                    callback: function(result) {
                                        // result will be true if button was click, while it will be false if users close the dialog directly
                                    }
                                });
                                table.search("").draw();
                            }
                        });
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
            'colvis', {
                text: 'Buscar por nombre de cliente',
                action: function(e, dt, node, config) {
                    $(this).attr("test_attr", "a");
                    state = "1";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Nombre de cliente');
                    // alert($(this).attr("test_attr")) 
                },
                className: 'info'
            }, {
                text: 'Buscar por Tipo de cuenta',
                action: function(e, dt, node, config) {
                    $(this).attr("test_attr", "a");
                    state = "2";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Tipo de cuenta');
                    // alert($(this).attr("test_attr")) 
                },
                className: 'info'
            }
        ],
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/cuentas",
            "type": "POST",
            "data": function(d) {
                d.test = state,
                d.creacionStart = $("#fromD").val(),
                d.creacionStop = $("#toD").val(),
                d.uMovStart = $("#fromMD").val(),
                d.uMovStop = $("#toMD").val(),
                d.saldoFrom = $("#sumFrom").val(),
                d.saldoTo = $("#sumTo").val()
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
            'colvis', {
                text: 'Buscar por nombre de cliente',
                action: function(e, dt, node, config) {
                    $(this).attr("test_attr", "a");
                    state_o = "1";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Nombre de cliente');
                    // alert($(this).attr("test_attr")) 
                },
                className: 'info'
            }, {
                text: 'Buscar por Tipo de cuenta',
                action: function(e, dt, node, config) {
                    $(this).attr("test_attr", "a");
                    state_o = "2";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Tipo de cuenta');
                    // alert($(this).attr("test_attr")) 
                },
                className: 'info'
            }
        ],
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/cuentas",
            "type": "POST",
            "data": function(d) {
                d.test = state_o,
                d.creacionStart = $("#fromD").val(),
                d.creacionStop = $("#toD").val(),
                d.uMovStart = $("#fromMD").val(),
                d.uMovStop = $("#toMD").val(),
                d.saldoFrom = $("#sumFrom").val(),
                d.saldoTo = $("#sumTo").val()
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
        }, {
            "data": "delete"
        }],
        "columnDefs": [{
            "render": function(data, type, row) {
                console.log(data);
                if (data !== null) {
                    var style = '<div class="row"><div class="col-xs-2"><a onClick="' + 'return deleteFuncC(this)' + '" deleteP="' + data + '"><i class="fa fa-times"></i>Cerrar</a></div>';
                    return style;
                }
                return '';
            },
            "targets": 11
        }]
    });

    var state_p = '1'
    $('#pres_table').DataTable({
        dom: 'Bfrtip',
        stateSave: true,
        buttons: [
            'colvis', {
                text: 'Buscar por nombre de cliente',
                action: function(e, dt, node, config) {
                    $(this).attr("test_attr", "a");
                    state_p = "1";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Nombre de cliente');
                    // alert($(this).attr("test_attr")) 
                },
                className: 'info'
            }, {
                text: 'Buscar por Tipo de prestamo',
                action: function(e, dt, node, config) {
                    $(this).attr("test_attr", "a");
                    state_p = "2";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Tipo de prestamo');
                    // alert($(this).attr("test_attr")) 
                },
                className: 'info'
            }
        ],
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/prestamos",
            "type": "POST",
            "data": function(d) {
                d.test = state,
                d.creacionStart = $("#fromD").val(),
                d.creacionStop = $("#toD").val(),
                d.uMovStart = $("#fromMD").val(),
                d.uMovStop = $("#toMD").val(),
                d.saldoFrom = $("#sumFrom").val(),
                d.saldoTo = $("#sumTo").val()
                // d.custom = $('#myInput').val();
                // etc
            }
        },
        "columns": [{
            "data": "id"
        }, {
            "data": "cerrado"
        }, {
            "data": "monto"
        }, {
            "data": "fecha_creacion"
        }, {
            "data": "num_cuotas"
        }, {
            "data": "valor_cuota"
        }, {
            "data": "interes"
        }, {
            "data": "id_cliente"
        }, {
            "data": "nombre"
        }, {
            "data": "apellido"
        }, {
            "data": "oficina"
        }, {
            "data": "nombre_of"
        }]
    });


    var state_op = '1'
    $('#op_table').DataTable({
        dom: 'Bfrtip',
        stateSave: true,
        buttons: [
            'colvis', {
                text: 'Buscar por nombre de cliente',
                action: function(e, dt, node, config) {
                    $(this).attr("test_attr", "a");
                    state_o = "1";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Nombre de cliente');
                    // alert($(this).attr("test_attr")) 
                },
                className: 'info'
            }, {
                text: 'Buscar por número de cuenta',
                action: function(e, dt, node, config) {
                    $(this).attr("test_attr", "a");
                    state_op = "2";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Número de cuenta');
                    // alert($(this).attr("test_attr")) 
                },
                className: 'info'
            }, {
                text: 'Buscar por número de préstamo',
                action: function(e, dt, node, config) {
                    $(this).attr("test_attr", "a");
                    state_op = "3";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Número de préstamo');
                    // alert($(this).attr("test_attr")) 
                },
                className: 'info'
            }
        ],
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/operaciones",
            "type": "POST",
            "data": function(d) {
                d.test = state_op,
                d.tipoOp = $("#tOperacion").val(),
                d.uMovStart = $("#fromMD").val(),
                d.uMovStop = $("#toMD").val(),
                d.saldoFrom = $("#sumFrom").val(),
                d.saldoTo = $("#sumTo").val(),
                d.pa1 = $('#pa1').val(),
                d.pa2 = $('#pa2').val(),
                d.negate = $('#ad-busq').is(':checked').toString().charAt(0).toUpperCase() + $('#ad-busq').is(':checked').toString().slice(1)
                // d.custom = $('#myInput').val();
                // etc
            }
        },
        "columns": [{
            "data": "numero"
        }, {
            "data": "fecha"
        }, {
            "data": "tipo"
        }, {
            "data": "id_cliente"
        }, {
            "data": "nombre"
        }, {
            "data": "apellido"
        }, {
            "data": "cuenta"
        }, {
            "data": "prestamo"
        }, {
            "data": "valor"
        }, {
            "data": "punto_atencion"
        }, {
            "data": "tipo_pa"
        }, {
            "data": "id_oficina"
        }, {
            "data": "nombre_oficina"
        }, {
            "data": "cajero"
        }, {
            "data": "nombre_emp"
        }, {
            "data": "apellido_emp"
        }]
    });

    var state_cons = '1'
    $('#cons_table').DataTable({
        dom: 'Bfrtip',
        stateSave: true,
        buttons: [
            'colvis', {
                text: 'Buscar por nombre de cliente',
                action: function(e, dt, node, config) {
                    $(this).attr("test_attr", "a");
                    state_cons = "1";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Nombre de cliente');
                    // alert($(this).attr("test_attr")) 
                },
                className: 'info'
            }, {
                text: 'Buscar por número de cuenta',
                action: function(e, dt, node, config) {
                    $(this).attr("test_attr", "a");
                    state_cons = "2";
                    // console.log(state);
                    $("#paramF").text('Buscando por: Número de cuenta');
                    // alert($(this).attr("test_attr")) 
                },
                className: 'info'
            }
        ],
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/consignaciones",
            "type": "POST",
            "data": function(d) {
                d.test = state_op,
                d.tPrestamo = $("#tPrestamo").val(),
                d.saldoFrom = $("#sumFrom").val(),
                d.saldoTo = $("#sumTo").val()
                // d.custom = $('#myInput').val();
                // etc
            }
        },
        "columns": [{
            "data": "numero"
        }, {
            "data": "fecha"
        },  {
            "data": "id_cliente"
        }, {
            "data": "nombre"
        }, {
            "data": "apellido"
        }, {
            "data": "cuenta"
        }, {
            "data": "prestamo"
        }, {
            "data": "valor"
        }, {
            "data": "punto_atencion"
        }, {
            "data": "tipo_pa"
        }, {
            "data": "id_oficina"
        }, {
            "data": "nombre_oficina"
        }, {
            "data": "cajero"
        }, {
            "data": "nombre_emp"
        }, {
            "data": "apellido_emp"
        }]
    });


    var dtsettings = {
        "processing": true,
        "serverSide": true,
        "ajax": "doesntMatter/IsNotUsed",
        "fnServerData": function (sSource, aoData, fnCallback) {
            var ws = new WebSocket("ws://localhost:8000/operacionesext");
            ws.onmessage = function (d) {
                fnCallback(d);
            }
 
            ws.onopen = function (e) {
                ws.send(JSON.stringify({
                    uMovStart : $("#fromMD").val(),
                    uMovStop : $("#toMD").val(),
                    saldoFrom : $("#sumFrom").val(),
                    saldoTo : $("#sumTo").val(),
                    pa1 = $('#pa1').val(),
                    pa2 = $('#pa2').val(),
                    data: aoData
                })); 
            }
        },
        "columns": [{
            "data": "fecha"
        }, {
            "data": "tipo"
        },  {
            "data": "id_cliente"
        }, {
            "data": "valor"
        }, {
            "data": "nombre"
        }, {
            "data": "apellido"
        }, {
            "data": "cuenta"
        }, {
            "data": "punto_atencion"
        }]
    };

    $('#op_table_ext').DataTable(dtsettings);

    $('#acc_search_btn').click(function() {
        var table = $('#acc_tableggeneral').DataTable();
        table.search("").draw();
    });

    $('#op_search_btn').click(function() {
        var table = $('#op_table').DataTable();
        table.search("").draw();
    });

    $('#p_search_btn').click(function() {
        var table = $('#pres_table').DataTable();
        table.search("").draw();
    });

    $('#cons_search_btn').click(function() {
        var table = $('#cons_table').DataTable();
        table.search("").draw();
    });


    // $('#ad-busq').click(function() {
    //     if($('#ad-busq').is(':checked')){
    //         $('#fromMD').prop('disabled', false);
    //         $('#toMD').prop('disabled', false);
    //         $('#sumFrom').prop('disabled', false);
    //         $('#sumTo').prop('disabled', false);
    //     }
    //     else 
    //     {
    //         $('#fromMD').prop('disabled', true);
    //         $('#toMD').prop('disabled', true);
    //         $('#sumFrom').prop('disabled', true);
    //         $('#sumTo').prop('disabled', true);
    //     }
    // });
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