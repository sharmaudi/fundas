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

$(document).ajaxError(function myErrorHandler(event, xhr, ajaxOptions, thrownError) {
    console.log("There was an ajax error - " + thrownError);
    $.notify(thrownError, {position: "top center"});
});


$('#type-all').change(function () {

    loadRoute(company);
});
function loadRoute(company) {
    $.ajax({
        url: "/api/v1/portfolio/performance",
        type: 'get',
        success: function (response) {
            console.log(response);

            var openPositions = response['openPositions'];

            console.log(openPositions);

            tableCols = [];

            openPositions.columns.forEach(function (val, i) {
                if (val === 'buyDate') {
                    tableCols.push({
                        'title': 'Buy Date',
                        'type': 'date',
                        'render': function (value) {
                            if (value === null) return "";
                            var dt = new Date(parseFloat(value));
                            return (dt.getMonth() + 1) + "/" + dt.getDate() + "/" + dt.getFullYear();
                        }
                    })
                } else if (val === 'index') {
                    tableCols.push({
                        'title': 'Symbol',
                        'type': 'string'
                    })
                } else {
                    tableCols.push({
                        'type':'num',
                        'title': val,
                        'render': function (value) {

                            val = parseFloat(value);

                            if (isNaN(val)) {
                                return value
                            } else {
                                return parseFloat(Math.round(value * 100) / 100).toFixed(2)
                            }


                        }


                    })

                }

            });

            $(document).ready(function () {
                $('#holdings').DataTable({
                    data: openPositions.data,
                    columns: tableCols
                });
            });


            var stats = response.stats;
            var current_profit = parseFloat(stats.profit);
            var closed_profit = parseFloat(stats.closedProfit);
            var profit = parseFloat(stats.totalProfit);

            var  profitPercentage = stats.profitPercentage;
            var  maxDrawdown = stats.maxDrawdown;
            var maxDrawdownPercentage = stats.maxDrawdownPercentage;
            var cagr = stats.cagr;


             $('#profit').text('Current Profit: ' + current_profit);

            $('#closedProfit').text('Closed Profit: ' + closed_profit);

            $('#totalProfit').text('Overall Profit: ' + profit);

            $('#profitPercentage').text('Profit Percentage: ' + profitPercentage + '%');

            $('#cagr').text('CAGR: ' + cagr + '%');

            $('#maxDrawdown').text('Max Drawdown: ' + maxDrawdown);

            $('#maxDrawdownPercentage').text('Max Drawdown %: ' + maxDrawdownPercentage + '%');



            var closedPositions = response['closedPositions'];

            console.log(closedPositions);

            tableCols = [];

            closedPositions.columns.forEach(function (val, i) {
                if (val === 'BuyDate') {
                    tableCols.push({
                        'title': 'Buy Date',
                        'type': 'date',
                        'render': function (value) {
                            if (value === null) return "";
                            var dt = new Date(parseFloat(value));
                            return (dt.getMonth() + 1) + "/" + dt.getDate() + "/" + dt.getFullYear();
                        }
                    })
                } else if (val === 'SellDate') {
                    tableCols.push({
                        'title': 'Sell Date',
                        'type': 'date',
                        'render': function (value) {
                            if (value === null) return "";
                            var dt = new Date(parseFloat(value));
                            return (dt.getMonth() + 1) + "/" + dt.getDate() + "/" + dt.getFullYear();
                        }
                    })
                } else if (val === 'Symbol') {
                    tableCols.push({
                        'title': 'Symbol',
                        'type': 'string'
                    })
                } else {
                    tableCols.push({
                        'type':'num',
                        'title': val,
                        'render': function (value) {

                            val = parseFloat(value);

                            if (isNaN(val)) {
                                return value
                            } else {
                                return parseFloat(Math.round(value * 100) / 100).toFixed(2)
                            }


                        }


                    })

                }

            });

            $(document).ready(function () {
                $('#closedPositions').DataTable({
                    data: closedPositions.data,
                    columns: tableCols
                });
            });




            Highcharts.chart('chart', {
    chart: {
        type: 'line'
    },
    title: {
        text: 'Portfolio performance against indices'
    },
    subtitle: {
        text: 'Portfolio performance against indices'
    },
    xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: { // don't display the dummy year
            month: '%e. %b',
            year: '%b'
        },
        title: {
            text: 'Date'
        }
    },
    yAxis: {
        title: {
            text: 'Equity'
        },
        min: response.equityCurveMinValue,
        max: response.equityCurveMaxValue
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br>',
        pointFormat: '{point.x:%e. %b}: {point.y:.2f} %'
    },

    plotOptions: {
        spline: {
            marker: {
                enabled: true
            }
        }
    },

    series: [{
        name: 'Portfolio',
        // Define the data points. All series have a dummy year
        // of 1970/71 in order to be compared on the same x axis. Note
        // that in JavaScript, months start at 0 for January, 1 for February etc.
        data: response.equityCurve
    }, {
        name: 'JUNIORBEES',
        data: response.equityCurveJNF
    }, {
        name: 'NIFTYBEES',
        data: response.equityCurveNF
    }]
});


        }
    });


}


