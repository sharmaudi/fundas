$('.table').each(function(){
    $(this).bootstrapTable({});
})

$body = $("body");


$(document).ajaxStop(function () {
    console.log("Done!");
    $body.removeClass("loading");
});

$(document).ajaxStart(function () {
    console.log("Loading data..");
    $body.addClass("loading");
});

$(document).ajaxError(function myErrorHandler(event, xhr, ajaxOptions, thrownError) {
    console.log("There was an ajax error - " + thrownError);
    $.notify("Error while getting company details. Please try another company.", {position:"top center"});
});




function load_table(company,type,indicators,period,$table) {
    $.ajax({
        url: "/api/v1/company/" + company,
        type: 'get',
        data: {
            i: indicators,
            p:period
        },
        dataType: 'text',
        success: function (response) {
            var jsonResponse = JSON.parse(response)
            console.log(jsonResponse);

            var obj;
            if(type === 'Standalone') {
                obj = jsonResponse['Standalone']
            } else {
                obj = jsonResponse['Consolidated']
            }

            var table_data={};


            for(var i in obj){
                for(var j in obj[i].Data){
                    if(!table_data[obj[i].Index[j]]) {
                        table_data[obj[i].Index[j]] = {};
                    }

                     if(!table_data[obj[i].Index[j]][obj[i].Metric]) {
                           table_data[obj[i].Index[j]][obj[i].Metric] = 0
                        }
                    table_data[obj[i].Index[j]][obj[i].Metric] = obj[i].Data[j];
                }
            }


            var table = [];


            console.log(table_data);
            for(var d in table_data) {
                var formattedDate = new Date(parseInt(d)).format("mmm-yyyy");
                var obj = {'period':formattedDate};
                var indicatorList = indicators.split(',');
                for( var i in indicatorList) {
                    var temp = Math.round(table_data[d][indicatorList[i]] * 100)/100;
                    obj[indicatorList[i]] = temp;
                }
                table.push(obj);
            }

            console.log(table)



            $table.bootstrapTable("load", table);





        }


        })
}

function loadRoute(company,type) {
    console.log('Showing balance sheet for company : ' + company + " and type : " + type);
    $('.hidden-default').show();


    $('.table').each(function(){
        var period;
        var is_quarterly = $(this).attr("data-is-quarterly")
        if(is_quarterly && is_quarterly === "true"){
            period = "Q"
        } else {
            period = "A"
        }
    load_table(company, type, $(this).attr("data-indicators"),period,$(this));
    })
}




$('#type-all').change(function (e) {
    changeHash(e);
})

