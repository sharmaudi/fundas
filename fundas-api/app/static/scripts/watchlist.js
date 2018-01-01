/**
 * Created by Udit on 7/01/2016.
 */

$body = $("body");


$(document).ajaxStop(function () {
    console.log("Done!");
    $body.removeClass("loading");
});

$(document).ajaxStart(function () {
    console.log("Loading data..");
    $body.addClass("loading");
});

$('#table').bootstrapTable({});

$(document).ajaxError(function myErrorHandler(event, xhr, ajaxOptions, thrownError) {
    console.log("There was an ajax error - " + thrownError);
    $.notify(thrownError, {position: "top center"});
});

function showRadar(company, counter, type, valueScore, perfScore, healthScore, divScore, momScore) {
    var chart = $('#radar_' + counter);
    var typeStr = type == "consolidated" ? "/Consolidated" : "/Standalone";
    if(chart.highcharts()) {
        chart.highcharts().destroy();
    }

    var link = "<a href='/analysis/#" + company + typeStr + "'>" + company + "</a>";
    chart.highcharts({

        chart: {
            polar: true,
            // Edit chart spacing
            spacingBottom: 15,
            spacingTop: 10,
            spacingLeft: 10,
            spacingRight: 10,

            // Explicitly tell the width and height of a chart
            width: 300,
            height: 300
        },

        title: {
            useHTML: true,
            text: link

        },

        pane: {
            size: '80%'
        },

        xAxis: {
            categories: ['Valuation', 'Performance', 'Health', 'Dividends', 'Momentum'
            ],
            labels: {
                style: {
                    color: '#000',
                    font: '8px Nunito'
                }
            }

        },

        yAxis: {
            gridLineInterpolation: 'polygon',
            lineWidth: 0,
            min: 0,
            max: 10
        },

        tooltip: {
            shared: true,
            pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.0f}</b><br/>'
        },


        series: [{
            showInLegend: false,
            name: 'Actual Scores',
            type: 'area',
            data: [valueScore, perfScore, healthScore, divScore, momScore],
            color: 'blue'
        },
            {
                showInLegend: false,
                name: 'Acceptable Scores',
                data: [7, 6, 6, 4, 10],
                pointPlacement: 'on',
                color: 'grey',
                dashStyle: 'Dot'
            }
        ]

    });
}


$('#type-all').change(function () {

    loadRoute(company);
});
function loadRoute(company) {
    $.ajax({
        url: "/api/v1/watchlist/",
        type: 'get',
        success: function (response) {
            console.log(response);
            var type = $('#type-all').val();
            console.log("type is " + type);
            if (type.toLowerCase() === 'consolidated') {
                console.log(response['consolidated_list']);
                response['consolidated_list'].forEach(function(value, i) {
                    var obj = response['consolidated'][value];
                    showRadar(value, (i+1), 'consolidated', obj['valuation'], obj['performance'], obj['health'], obj['dividends'], obj['momentum']);
                });

            } else {

                console.log(response['standalone_list']);

                response['standalone_list'].forEach(function(value, i) {
                    var obj = response['standalone'][value];
                    showRadar(value, (i+1), 'standalone', obj['valuation'], obj['performance'], obj['health'], obj['dividends'], obj['momentum']);
                });

            }

        }
    });


}


