$(document).ready(function() {
	var dialog;
	var ws = new WebSocket('ws://localhost:8000/nominaW');

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
        	dialog.setTitle("Error! Saldo insufiente");
            dialog.setType(BootstrapDialog.TYPE_DANGER);
            var err_msg = "Las siguientes cuentas externas no pudieron ser pagadas <br>";
            var data = info.cuentas;

            for(var i = 0; i < data.length; i++)
            {
                info_err += "<b>Número: </b>"+data[i].numero+"&nbsp; <b>Nombre: </b>"+data[i].nombre+"<br>";
            }
            // dialog.setMessage("Ha ocurrido un error mientras la solicitud era procesada: <br>"+info.msg);

        }
        // console.log("Someone sent: ", str);
    };

    $('#nomina-form').submit(function(event) {
        event.preventDefault();
        var formData = {
            'cuenta': $('#comp_acc').val()
        };
        var button = [];
        button.push({
            id: 'btn-1',
            label: "Confirmar Operación",
            cssClass: "btn-success",
            action: function(dialog) {
                var $button = this; // 'this' here is a jQuery object that wrapping the <button> DOM element.
                $button.disable();
                $button.spin();
                dialog.setMessage("Pagando nómina asociada a LlamAndes");
                // ws.send(JSON.stringify(obj));
                dialog.setClosable(false);
                dialog.getButton('close-diag').disable();
                $.ajax({
                    type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
                    data: formData, // our data object
                    dataType: 'json',
                    encode: true
                }).done(function(data) {
                    console.log(data);
             		dialog.setClosable(true);
             		dialog.getButton('close-diag').enable();
             		if(Array.isArray(data))
             		{
             			dialog.getButton('btn-1').stopSpin();
             			dialog.getButton('btn-1').hide();
                		dialog.setTitle('Error! Saldo insuficiente');
                		var info_err = "No ha sido posible realizar el pago de nómina a las siguientes cuentas: <br>"
                		for(var i = 0; i < data.length; i++)
                		{
                			info_err += "<b>Número: </b>"+data[i].cuenta+"&nbsp; <b>Nombre: </b>"+data[i].nombre+"<br>";
                		}
                		info_err += "Se notificarán a los empleados con cuentas externas a LlamAndes"
                		dialog.setMessage(info_err);
                		dialog.setType(BootstrapDialog.TYPE_DANGER);
             		}
             		else {
             			dialog.setMessage("Pagando nómina asociada a BancAndes <br> <b>Nota: </b> Si cierra esta ventana, recibirá una notificación posteriormente");
             			var obj = {acc : formData['cuenta']};
         				ws.send(JSON.stringify(obj));    			
             		}       
                });
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
            title:"Transacción externa",
            closable:true,
            draggable:true,
            type: BootstrapDialog.TYPE_WARNING,
            message:'¿Desea realizar esta operación?',
            buttons:button
        })
        // dialog.setData('buttons', buttons);
        // dialog.setData('draggable', true);
        dialog.realize();
        dialog.open();
    });

});