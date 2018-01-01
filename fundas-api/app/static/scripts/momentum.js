/**
 * Created by Udit on 14/01/2016.
 */
var technicals;


$(document).ajaxError(function myErrorHandler(event, xhr, ajaxOptions, thrownError) {
    console.log("There was an ajax error - " + thrownError);
    $.notify("Error while getting company details. Please try another company.", {position:"top center"});
});

$body = $("body");


$(document).ajaxStop(function () {
    console.log("Done!");
    $body.removeClass("loading");
});

$(document).ajaxStart(function () {
    console.log("Loading data..");
    $body.addClass("loading");
});

function loadRoute(company) {
    if (company.length != 0) {
            $.ajax({
                url: "/api/v1/momentum/" + company,
                type: 'get',
                localCache: true,
                dataType: 'text',
                success: function (response) {
                    technicals = JSON.parse(response);
                    console.log(technicals)

                    $('#company').val(company);
                    showChart(company);
                }
            });

    }
}

function showChart(company) {

    var data = technicals['Technicals'];
    var fundas = technicals['Standalone'];
    var rocVal;
    var npVal;
    var srVal;

    console.log(technicals)

    var high_52 = data['52WHigh'];
    console.log(high_52);


            var price = [];
            var roc = [];
            var revenue_growth = [];
            var np_growth = [];
            var dataLength = data['Price'].length,
            // set the allowed units for data grouping
            groupingUnits = [[
                'week',                         // unit name
                [1]                             // allowed multiples
            ], [
                'month',
                [1, 2, 3, 4, 6]
            ]],

            i = 0;



        for (i; i < dataLength; i += 1) {
            price.push([
                data['Date'][i], // the date
                data['Price'][i] // close
            ]);

            rocVal = Math.round(data['Momentum'][i] * 100)/100;

            roc.push([
                data['Date'][i], // the date
                rocVal // the ROC


            ]);

        }

        for(i = 0; i <fundas['SR_G'].length;i++) {
            srVal = Math.round(fundas['SR_G'][i] * 100)/100;
            npVal = Math.round(fundas['NP_G'][i] * 100)/100;

            revenue_growth.push([
                fundas['Date'][i],
                srVal
            ])

             np_growth.push([
                fundas['Date'][i],
                npVal
            ])
        }



        // create the chart
        $('#tech-chart').highcharts('StockChart', {

            chart: {
                zoomType: 'xy',
                height:600
            },

            rangeSelector: {
                selected: 4
            },

            title: {
                text: company + " Momentum"
            },


            plotOptions: {
                line: {
                    marker: {
                        enabled: true
                    }
                }},

            yAxis: [{ // Primary yAxis
            labels: {
                format: '{value}',
                style: {
                    color: Highcharts.getOptions().colors[2]
                }
            },
            title: {
                text: 'Price',
                style: {
                    color: Highcharts.getOptions().colors[2]
                }
            },
            opposite: true,
                plotLines: [{
                    value: high_52,
                    color: 'green',
                    dashStyle: 'shortdash',
                    width: 2,
                    label: {
                        text: '52 Weeks high'
                    }
                }]

        }],

            series: [{
                type: 'area',
                name: company,
                data: price,
                negativeColor: '#00FFFF',
                dataGrouping: {
                    units: groupingUnits
                }
            }


            ]
        });


     $('#rocChart').highcharts('StockChart', {

            chart: {
            zoomType: 'x',
        },
        title: {
            text: "ROC"
        },
          rangeSelector: {
                selected: 4
            },

        subtitle: {

        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value}',
                style: {
                    color: Highcharts.getOptions().colors[2]
                }
            },
            title: {
                text: 'ROC',
                style: {
                    color: Highcharts.getOptions().colors[2]
                }
            },
            opposite: true

        }, { // Secondary yAxis
            gridLineWidth: 0,
            title: {
                text: 'Quarterly Growth',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                format: '{value}%',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            }

        }],
        legend: {
            enabled: true
        },

        plotOptions: {

        },


            series: [{
                type: 'area',
                name: 'ROC',
                data: roc,
                color:'green',
                negativeColor: 'red',

                dataGrouping: {
                    units: groupingUnits
                }
            },{
                type: 'line',
                name: 'Rev Grth',
                data: revenue_growth,
                marker: {
                    symbol: 'square'
                },
                plotOptions: {
                line: {
                    marker: {
                        enabled: true,
                        radius:6

                    }
                }
                },
                yAxis: 1,
                dataGrouping: {
                    units: groupingUnits
                }
            },
                {
                type: 'line',
                name: 'NP Grth.',
                    marker: {
                    symbol: 'triangle',
                    radius:6
                },
                data: np_growth,
                yAxis: 1,
                dataGrouping: {
                    units: groupingUnits
                }
            }
            ]
        });


}