$(document).ready(function() {

    // process the form
    $('#nomina-form').submit(function(event) {
        event.preventDefault();
        var formData = {
            'cuenta': $('#comp_acc').val(),
            'cuenta_empl': $('#cuenta_empl').val(),
            'salario': $('#salario').val(),
            'frec': $('#frec_sel').val()
        };
        BootstrapDialog.confirm({
            title: 'Confirmación',
            message: 'Cuenta: ' + formData['cuenta'] + '<br>' +
                'Cuenta Empleado: ' + formData['cuenta_empl'] + '<br>' +
                'Salario: ' + formData['salario'],
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
    });
});