$(document).ready(function() {
$(".itemSearch").select2({
        // tags: true,
        // multiple: true,
        // tokenSeparators: [',', ' '],
        minimumInputLength: 2,
        minimumResultsForSearch: 20,
        ajax: {
            url: '/empleados',
            dataType: "json",
            type: "PUT",
            delay:250,
            data: function(params) {

                var queryParameters = {
                    term: params.term
                }
                return queryParameters;
            },
            processResults: function(data) {
                return {
                    results: $.map(data, function(item) {
                    	console.log(item);
                    	var obj = {
                            id: item.id,
                            text: item.id+' : '+item.email + ' - '+item.num_documento
                        };
                        console.log(obj);
                        return obj;
                    })
                };
            }
        }
    });


    $(".itemSearchO").select2({
        // tags: true,
        // multiple: true,
        // tokenSeparators: [',', ' '],
        minimumInputLength: 2,
        minimumResultsForSearch: 20,
        ajax: {
            url: '/oficinas',
            dataType: "json",
            type: "PUT",
            delay:250,
            data: function(params) {

                var queryParameters = {
                    term: params.term
                }
                return queryParameters;
            },
            processResults: function(data) {
                return {
                    results: $.map(data, function(item) {
                        console.log(item);
                        var obj = {
                            id: item.id,
                            text: item.id+' : '+item.nombre
                        };
                        console.log(obj);
                        return obj;
                    })
                };
            }
        }
    });

    $(".itemSearchC").select2({
        // tags: true,
        // multiple: true,
        // tokenSeparators: [',', ' '],
        minimumInputLength: 2,
        minimumResultsForSearch: 20,
        ajax: {
            url: '/clientes',
            dataType: "json",
            type: "PUT",
            delay:250,
            data: function(params) {

                var queryParameters = {
                    term: params.term
                }
                return queryParameters;
            },
            processResults: function(data) {
                return {
                    results: $.map(data, function(item) {
                        console.log(item);
                        var obj = {
                            id: item.id,
                            text: item.id+' : '+item.nombre+' '+item.apellido
                        };
                        console.log(obj);
                        return obj;
                    })
                };
            }
        }
    });
});