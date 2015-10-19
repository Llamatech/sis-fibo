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
            url: '/usuarios',
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

    $(".itemSearchP").select2({
        // tags: true,
        // multiple: true,
        // tokenSeparators: [',', ' '],
        minimumInputLength: 1,
        minimumResultsForSearch: 20,
        ajax: {
            url: '/cerrar/prestamo',
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
                        var apellido = '';
                        if(item.apellido !== 'null')
                        {
                            apellido = item.apellido;
                        }
                        var obj = {
                            id: item.id,
                            text: item.id+' : '+item.tipo_p+' - '+item.nombre+' '+apellido+' Saldo: $'+item.saldo
                        };
                        console.log(obj);
                        return obj;
                    })
                };
            }
        }
    });
    
    $("#comp_acc").select2();
    $("#frec_sel").select2();

    $(".itemSearchE").select2({
        // tags: true,
        // multiple: true,
        // tokenSeparators: [',', ' '],
        minimumInputLength: 1,
        minimumResultsForSearch: 20,
        ajax: {
            url: '/cuentas/naturales',
            dataType: "json",
            type: "POST",
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
                        var obj = {
                            id: item.numero,
                            text: 'Número Cuenta: '+item.numero
                        };
                        return obj;
                    })
                };
            }
        }
    });
    
    $(".itemSearchNC").select2({
        // tags: true,
        // multiple: true,
        // tokenSeparators: [',', ' '],
        minimumInputLength: 1,
        minimumResultsForSearch: 20,
        ajax: {
            url: '/cuentas/nocerradas',
            dataType: "json",
            type: "POST",
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
                        var obj = {
                            id: item.numero,
                            text: 'Número Cuenta: '+item.numero
                        };
                        return obj;
                    })
                };
            }
        }
    });
    
    $(".itemSearchPNC").select2({
        // tags: true,
        // multiple: true,
        // tokenSeparators: [',', ' '],
        minimumInputLength: 1,
        minimumResultsForSearch: 20,
        ajax: {
            url: '/prestamos/nocerrados',
            dataType: "json",
            type: "POST",
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
                        var obj = {
                            id: item.id,
                            text: 'Número Préstamo: '+item.id
                        };
                        return obj;
                    })
                };
            }
        }
    });
});