// var table;

function deleteFunc(elem)
{
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
			table.rows( '.selected' ).remove().draw();
   		}
	});
}

function deleteFuncO(elem)
{
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
			table.rows( '.selected' ).remove().draw();
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
        "columns": [
            { "data": "id" },
            { "data": "email" },
            { "data": "tipo_un" },
            { "data": "tipo_doc" },
            { "data": "num_documento" },
            { "data": "nombre" },
            { "data": "apellido" },
            { "data": "ciudad"},
            { "data": "nombre_oficina"},
            { "data": "delete"}
        ],
        "columnDefs": [
            {
                "render": function ( data, type, row ) {
                	var values = data.split('|')
                	var style = '<div class="row"><div class="col-xs-2"><a onClick="'+'return deleteFunc(this)'+'" deleteE="'+values[0]+'"><i class="fa fa-trash"></i></a></div><div class="col-xs-2"><a href="'+values[1]+'"><i class="fa fa-pencil-square-o"></i></a></div></div>';
                    return style;
                },
                "targets": 9
            }
        ]
    });

     $('#office_table').DataTable({
    	"processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/oficinas",
            "type": "POST"
        },
        "columns": [
            { "data": "id" },
            { "data": "localizacion" },
            { "data": "nombre" },
            { "data": "direccion" },
            { "data": "telefono" },
            { "data": "id_gerente" },
            { "data": "gerente" },
            { "data": "delete"}
        ],
        "columnDefs": [
            {
                "render": function ( data, type, row ) {
                	var values = data.split('|')
                	var style = '<div class="row"><div class="col-xs-2"><a onClick="'+'return deleteFuncO(this)'+'" deleteO="'+values[0]+'"><i class="fa fa-trash"></i></a></div><div class="col-xs-2"><a href="'+values[1]+'"><i class="fa fa-pencil-square-o"></i></a></div></div>';
                    return style;
                },
                "targets": 7
            }
        ]
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



} );