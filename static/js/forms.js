$(document).ready(function() {
    // process the form
    var dialog;
    var ws = new WebSocket('ws://localhost:8000/associate');

     ws.onmessage = function(str) {
        console.log("Message!");
        var info = JSON.parse(str.data);
        console.log(info);
        dialog.setClosable(true);
        var $button = dialog.getButton('btn-1');
        // $button.enable();
        $button.stopSpin();
        $button.hide();
        if(info.estado === 'confirmacion')
        {
            dialog.setType(BootstrapDialog.TYPE_SUCCESS);
            dialog.setMessage("La solicitud ha sido realizada satisfactoriamente<br><b>Código de la operación: "+info.id);
        }
        else
        {
            dialog.setType(BootstrapDialog.TYPE_DANGER);
            dialog.setMessage("Ha ocurrido un error mientras la solicitud era procesada: <br>"+info.msg);
        }
        // console.log("Someone sent: ", str);
    };

    $('#ext-acc').click(function() {
        if($('#ext-acc').is(':checked'))
        {
            $('#acc_label').text("Cuenta BancAndes Empleado");
            $('#esconder').hide();
            $('#mostrar').show();
            // $('#cuenta_empl').replaceWith('<input id="cuenta_empl" name="cuenta_empl style="width:100%>"');
        }
        else
        {
            $('#acc_label').text("Cuenta LlamAndes Empleado");
            $('#esconder').show();
            $('#mostrar').hide();
            // $('#cuenta_empl').replaceWith('<select id="cuenta_empl" name="cuenta_empl" class="itemSearchE" style="width:100%"><option value="-1" selected="selected">Buscar una cuenta</option></select>');
        }
    });

    $('#nomina-form').submit(function(event) {
        event.preventDefault();
        var opt = $('#cuenta_empl').val();
        if($('#ext-acc').is(':checked'))
        {
            opt = $('#cuenta_empl2').val();
        }
        var formData = {
            'cuenta': $('#comp_acc').val(),
            'cuenta_empl': opt,
            'salario': $('#salario').val(),
            'frec': $('#frec_sel').val(),
            'external': $('#ext-acc').is(':checked')
        };
        var msg = 'Cuenta: ' + formData['cuenta'] + '<br>' +
                'Cuenta Empleado: ' + formData['cuenta_empl'] + '<br>' +
                'Salario: ' + formData['salario'] + '<br>';
        if(!formData['external'])
        { 
            msg += 'Cuenta externa asociada a LlamAndes';
            BootstrapDialog.confirm({
            title: 'Confirmación',
            message: msg,
            type: BootstrapDialog.TYPE_WARNING, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
            closable: true, // <-- Default value is false
            draggable: true,
            autospin: true, // <-- Default value is false
            btnCancelLabel: 'Cancelar', // <-- Default value is 'Cancel',
            btnOKLabel: 'Inscribir', // <-- Default value is 'OK',
            btnOKClass: 'btn-warning', // <-- If you didn't specify it, dialog type will be used,
            callback: function(result) {
                if (result) {
                    // result will be true if button was click, while it will be false if users close the dialog directly.
                    $.ajax({
                        type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
                        data: formData, // our data object
                        dataType: 'json',
                        encode: true
                    }).done(function(data) {
                        console.log(data);
                        if (data.succ) {
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
                        } else {
                            BootstrapDialog.alert({
                                title: '¡Error!',
                                message: 'Ha ocurrido un error mientras su solicitud era procesada, por favor, intente de nuevo <br> ' + data['msg'],
                                type: BootstrapDialog.TYPE_DANGER, // <-- Default value is BootstrapDialog.TYPE_PRIMARY
                                closable: true, // <-- Default value is false
                                draggable: true, // <-- Default value is false
                                buttonLabel: 'Cerrar', // <-- Default value is 'OK',
                                callback: function(result) {
                                    // result will be true if button was click, while it will be false if users close the dialog directly
                                }
                            });
                        }
                    });
                }
            }
        });
        }
        else
        {
            msg += 'Cuenta externa asociada a BancAndes';
            var button = [];

        button.push({
            id: 'btn-1',
            label: "Confirmar Operación",
            cssClass: "btn-success",
            action: function(dialog) {
                var $button = this; // 'this' here is a jQuery object that wrapping the <button> DOM element.
                $button.disable();
                $button.spin();
                ws.send(JSON.stringify(formData));
                dialog.setClosable(false);
                // dialog.getButton('close-diag').disable();
            }
        })
        button.push({
            id : 'close-diag',
            label: "Cerrar diálogo",
            cssClass: "btn-danger",
            action: function(dialog) {
                dialog.close();
            }
        })
        dialog = new BootstrapDialog({
            title:"Confirmación",
            closable:true,
            draggable:true,
            type: BootstrapDialog.TYPE_WARNING,
            message:msg,
            buttons:button
        })
        // dialog.setData('buttons', buttons);
        // dialog.setData('draggable', true);
        dialog.realize();
        dialog.open();   
        }
 
    });
});