var cache = {}

$(document).ajaxError(function myErrorHandler(event, xhr, ajaxOptions, thrownError) {
    console.log("There was an ajax error - " + thrownError);
    $.notify("Error while getting company details. Please try another company.", {position: "top center"});
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


function loadRoute(company, type) {
    console.log("inside LoadRoute");
    $('.select-data-type').each(function () {
        $(this).val(type)
    })

    if (company.length != 0) {
        id = company + '_industry'

        if (localStorage.getItem(id) === null) {
            $.ajax({
                url: "/api/v1/company/industry/" + company,
                type: 'get',
                localCache: true,
                dataType: 'text',
                success: function (response) {
                    localStorage.setItem(id, response)
                    $('.chart-content').each(function () {
                        var config = get_config($(this))
                        config.company = [company]
                        showChart(config);
                    })
                }
            });

        } else {
            $('.chart-content').each(function () {
                var config = get_config($(this))
                config.company = [company]
                showChart(config);
            })
            $('#company').val(company);
        }

    }
}

function get_industry_data(company) {
    var id = company + '_industry';
    var str = localStorage.getItem(id);
    var returnObj = str == null ? str : JSON.parse(str);
    return returnObj;

}

function getChart(renderTo, title, bands, showInvertedBands) {

    var bandList = bands.split(',');


    var bandValues = [];
    if (bandList.length === 2) {
        bandValues.push({
            'from': bandList[0],
            'to': showInvertedBands ? 999999 : -999999,
            'color': 'rgba(227,16,30,.3)'
        })

        bandValues.push({
            'from': parseInt(bandList[0]),
            'to': bandList[1],
            'color': 'rgba(227,227,16,.3)'

        })

        bandValues.push({
            'from': parseInt(bandList[1]),
            'to': showInvertedBands ? -999999 : 999999,
            'color': 'rgba(23,227,16,.3)'

        })
    } else {
    }


    return new Highcharts.Chart({
        chart: {
            zoomType: 'x',
            renderTo: renderTo
        },
        title: {
            text: title
        },
        subtitle: {},
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: 'Value'
            },
            plotBands: bandValues
        },
        legend: {
            enabled: true
        },

        plotOptions: {},
        series: []
    });

}


function showChart(config) {
    if (config.isComparisonChart) {
        showComparisonChart(
            config);
    } else {
        showChartInternal(config)
    }
}

function showChartInternal(config) {
    var renderTo = config.renderTo;
    var title = config.title;
    var type = config.type;
    var indicators = config.indicators;
    var companyList = config.company;

    var chart = getChart(renderTo, title, config.bands, config.showInvertedBands);


    for (c in companyList) {
        var company = companyList[c];

        (function (company) {

            $.ajax({
                url: "/api/v1/company/" + company,
                type: 'get',
                localCache: true,
                data: {
                    i: indicators,
                    p: config.period
                },
                dataType: 'text',
                success: function (response) {

                    var industry_data = get_industry_data(company);


                    var resp = JSON.parse(response);

                    key = company + "_" + indicators.split(",").join("_");

                    var dataobj;

                    if (config.standalone) {
                        dataobj = resp.Standalone;
                    } else {
                        dataobj = resp.Consolidated;
                    }


                    for (var r in dataobj) {
                        var record = dataobj[r];
                        var index = record.Index;
                        var data = record.Data;
                        var mean = record.Mean;
                        var median = record.Median;
                        var metric = record.Metric;
                        var Pctchange1Y = record.PctChange1Y;
                        var Pctchange5Y = record.PctChange5Y;

                        var chart_data = [];
                        var d;
                        for (var i in index) {
                            if (!isNaN(data[i]) && !isNaN(parseInt(data[i]))) {
                                if (config.showPercentage) {
                                    d = data[i] * 100
                                } else {
                                    d = data[i]
                                }
                                chart_data.push({
                                    x: index[i],
                                    y: Math.round(d * 100) / 100
                                })
                            }

                        }

                        var seriesName = metric;

                        if (config.isComparisonChart) {
                            seriesName = company;
                        }

                        if (industry_data !== null) {
                            var data = industry_data[metric.toUpperCase()]
                            if (data != null) {
                                var weighedAvg = Math.round(data['weighed_average'] * 100) / 100
                                var avg = data['average']

                                if (chart_data.length != 0) {
                                    chart.addSeries({
                                        data: [{
                                            x: chart_data[chart_data.length - 1].x,
                                            y: config.showPercentage ? weighedAvg * 100 : weighedAvg
                                        }],
                                        name: metric + ' - Industry Average',
                                        type: 'bar',
                                        zIndex: -1
                                    }, false)
                                }

                            }
                        }


                        chart.addSeries({
                            data: chart_data,
                            name: seriesName,
                            type: type
                        })


                    }


                    $('.hidden-default').show();
                    chart.reflow();

                    if (renderTo == 'modal-chart') {
                        chart.setSize(chart.chartWidth, 550);
                    }


                },
                error: function (xhr) {
                    console.log('Error' + xhr)
                }
            });


        })(company);


    }
};

function showComparisonChart(config) {
    var company = config.company;

    //get related company list from server

    companies = get_industry_data(company)['companies']

    company = companies
    config['company'] = company;
    showChartInternal(config);

}


function get_config($parent) {
    var company = $('#company').val();
    var value = $parent.children('.select-data-type').val();
    var indicators = $parent.attr('data-indicators');
    var type = $parent.attr('data-chart-type');
    var showPercentageAttr = $parent.attr('data-show-percentage');
    var showPercentage = false;
    var period = $parent.attr('data-period');

    var standalone = value.toLowerCase() === 'standalone';
    var target = $parent.attr('data-target');
    var title = $parent.attr('data-title');
    var bands = $parent.attr('data-bands');
    if (showPercentageAttr) {
        showPercentage = showPercentageAttr.toLowerCase() === 'true';
    }

    var invertedBands = $parent.attr('data-inverted-bands');
    var showInvertedBands = false;
    if (invertedBands) {
        showInvertedBands = invertedBands === 'true'
    }

    var doComparison = $parent.find('.compare-peers').prop("checked");


    config = {
        renderTo: target,
        type: type,
        indicators: indicators,
        standalone: standalone,
        company: [company],
        isComparisonChart: doComparison,
        showPercentage: showPercentage,
        bands: bands,
        showInvertedBands: showInvertedBands,
        title: title,
        period: period
    }


    return config;
}


$('.select-data-type').change(function () {
    $parent = $(this).parent();
    config = get_config($parent);
    showChart(config);
})


$('#type-all').change(function (e) {

    /*
     var self = this;
     console.log($(self).val());
     var company = $('#company').val();
     $('.select-data-type').each(function() {
     $(this).val($(self).val())
     })
     loadRoute(company);
     */
    changeHash(e);
})


$('.modal-control').on('click', function () {
    $parent = $(this).parent();
    config = get_config($parent);
    config['renderTo'] = 'modal-chart';
    showChart(config);

});


$('.compare-peers').click(function () {
    $parent = $(this).parent().parent();
    config = get_config($parent);
    showChart(config);

})


var $container = $('#modal-chart')

$('#height-increase').click(function () {
    var chart = $container.highcharts();

    var chartHeight = chart.chartHeight * 1.1;
    chart.setSize(chart.chartWidth, chartHeight);
});
$('#height-decrease').click(function () {
    var chart = $container.highcharts();

    var chartHeight = chart.chartHeight * .9;
    chart.setSize(chart.chartWidth, chartHeight);
});
