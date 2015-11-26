$(document).ready(function() {
    var dialog;
    var ws = new WebSocket('ws://localhost:8000/ws');
    
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

    $('#op_do').click(function(event) {
        var obj = {
                     op_type:$('#extop_type').val(),
                     amount:parseFloat($('#amount').val()),
                     acc_local:parseInt($('#sel1').val()),
                     acc_remote:parseInt($('#out_acc_val').val())
                  };
        // dialog.setTitle('Transacción externa');
        // dialog.setClosable(true);
        // dialog.setDraggable(true);
        // dialog.setType(BootstrapDialog.TYPE_WARNING);
        // dialog.setMessage('Prueba de conexión al servidor');
        var button = [];
        button.push({
            id: 'btn-1',
            label: "Confirmar Operación",
            cssClass: "btn-success",
            action: function(dialog) {
                var $button = this; // 'this' here is a jQuery object that wrapping the <button> DOM element.
                $button.disable();
                $button.spin();
                ws.send(JSON.stringify(obj));
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
            title:"Transacción externa",
            closable:true,
            draggable:true,
            type: BootstrapDialog.TYPE_WARNING,
            message:'Prueba de conexión al servidor',
            buttons:button
        })
        // dialog.setData('buttons', buttons);
        // dialog.setData('draggable', true);
        dialog.realize();
        dialog.open();
    });
});