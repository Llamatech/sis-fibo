$(document).ready(function() {
        $("#deleteBorrow").click(function(event) {
                /* Act on the event */
                var val = $("#borrowClose").val();
                if (val !== '-1') {
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
                                $.ajax({
                                    url: '/cerrar/prestamo',
                                    type: 'DELETE',
                                    data: {
                                        'id': val
                                    },
                                    success: function(response) {
                                        //...
                                        BootstrapDialog.confirm({
                                            type: BootstrapDialog.TYPE_SUCCESS,
                                            title: 'Operación realizada satisfactoriamente',
                                            message: 'El préstamo número ' + val + ' ha sido cerrado.',
                                            closable: true, // <-- Default value is false
                                            draggable: true,
                                            btnOKLabel: 'Cerrar', // <-- Default value is 'OK',
                                            btnOKClass: 'btn-success',
                                            callback: function(result) {

                                            }
                                        });

                                    },
                                    error: function(response){
                                        BootstrapDialog.confirm({
                                            type: BootstrapDialog.TYPE_DANGER,
                                            title: 'Error',
                                            message: 'Un error ha ocurrido mientras la operación era procesada, intente nuevamente.',
                                            closable: true, // <-- Default value is false
                                            draggable: true,
                                            btnOKLabel: 'Volver', // <-- Default value is 'OK',
                                            btnOKClass: 'btn-danger',
                                            callback: function(result) {

                                            }
                                        });
                                    }
                                });
                            } else {

                            }
                        }
                    });
                }
        });
});