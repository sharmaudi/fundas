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
    $.notify("Error while getting company details. Please try another company.", {position: "top center"});
});

var gaugeOptions = {

    chart: {
        type: 'solidgauge'
    },

    title: null,

    pane: {
        center: ['50%', '85%'],
        size: '140%',
        startAngle: -90,
        endAngle: 90,
        background: {
            backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
            innerRadius: '60%',
            outerRadius: '100%',
            shape: 'arc'
        }
    },

    tooltip: {
        enabled: false
    },

    // the value axis
    yAxis: {
        stops: [
            [.3, 'red'], // green
            [.7, 'yellow'], // yellow
            [.9, 'green'] // red
        ],
        lineWidth: 0,
        minorTickInterval: null,
        tickPixelInterval: 400,
        tickWidth: 0,
        title: {
            y: -70
        },
        labels: {
            y: 16
        }
    },

    plotOptions: {
        solidgauge: {
            dataLabels: {
                y: 5,
                borderWidth: 0,
                useHTML: true
            }
        }
    }
};


function showRadar(company, valueScore, perfScore, healthScore, divScore, momScore) {
    $('#radar').highcharts({

        chart: {
            polar: true,
            type: 'line'
        },

        title: {
            text: company,
            x: -80
        },

        pane: {
            size: '80%'
        },

        xAxis: {
            categories: ['Valuation', 'Performance', 'Health', 'Dividends', 'Momentum'
            ],
            tickmarkPlacement: 'on',
            lineWidth: 0
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

        legend: {
            align: 'right',
            verticalAlign: 'top',
            y: 70,
            layout: 'vertical'
        },

        series: [{
            name: 'Actual Scores',
            data: [valueScore, perfScore, healthScore, divScore, momScore],
            type:'area',
            pointPlacement: 'on',
            color: 'blue'
        },
            {
                name: 'Acceptable Scores',
                data: [7, 6, 6, 4, 10],
                pointPlacement: 'on',
                color: 'grey',
                dashStyle: 'Dot'
            }
        ]

    });
}

function updateGauge(id, score, subtitle, maxScore) {

    $('#' + id).highcharts(Highcharts.merge(gaugeOptions, {
        yAxis: {
            min: 0,
            max: maxScore,
            title: {
                text: 'Score'
            }
        },

        credits: {
            enabled: false
        },

        series: [{
            name: 'Score',
            data: [score],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                '<span style="font-size:12px;color:silver">' + subtitle + '</span></div>'
            },
            tooltip: {
                valueSuffix: ''
            }
        }]

    }));
}


function renderChecklist(prefix, data) {
    data.forEach(function (obj) {
        var id = "#" + prefix + "_" + obj.id;
        console.log("ID is " + id);
        if (obj.outcome) {
            markChecked($(id));
        } else {
            markUnchecked($(id));
        }
    })

}


function loadPage(company) {
    $('#company').val(company);
    $.ajax({
        url: "/api/v1/analysis/" + company,
        type: 'get',
        success: function (response) {
            var type = $('#type-all').val().toLowerCase();
            console.log(response);

            if (response.error) {
                $.notify("Error while getting company details. Please try another company", {position: "top center"})
                return
            }

            if (type === 'consolidated') {
                if (response['consolidated']['error']) {
                    $.notify("Error while getting consolidated details. Please try standalone", {position: "top center"});
                    return
                }

                renderChecklist("valuation", response.consolidated.valuation_checklist);
                renderChecklist("performance", response.consolidated.performance_checklist);
                renderChecklist("health", response.consolidated.health_checklist);
                renderChecklist("dividends", response.consolidated.dividends_checklist);
                renderChecklist("momentum", response.consolidated.momentum_checklist);

                updateGauge('pe-gauge', response.consolidated.valuation, 'Valuation Score', 10)
                updateGauge('performance-gauge', response.consolidated.performance, 'Performance Score', 10)
                updateGauge('health-gauge', response.consolidated.health, 'Health Score', 10)
                updateGauge('dividends-gauge', response.consolidated.dividends, 'Dividends Score', 10)
                updateGauge('momentum-gauge', response.consolidated.momentum, 'Momentum Score', 10)
                showRadar(company,
                    response.consolidated.valuation,
                    response.consolidated.performance,
                    response.consolidated.health,
                    response.consolidated.dividends,
                    response.consolidated.momentum)


            } else {
                if (response['standalone']['error']) {
                    $.notify("Error while getting standalone details.", {position: "top center"});
                    return
                }

                renderChecklist("valuation", response.standalone.valuation_checklist);
                renderChecklist("performance", response.standalone.performance_checklist);
                renderChecklist("health", response.standalone.health_checklist);
                renderChecklist("dividends", response.standalone.dividends_checklist);
                renderChecklist("momentum", response.standalone.momentum_checklist);

                updateGauge('pe-gauge', response.standalone.valuation, 'Valuation Score', 10)
                updateGauge('performance-gauge', response.standalone.performance, 'Performance Score', 10)
                updateGauge('health-gauge', response.standalone.health, 'Health Score', 10)
                updateGauge('dividends-gauge', response.standalone.dividends, 'Dividends Score', 10)
                updateGauge('momentum-gauge', response.standalone.momentum, 'Momentum Score', 10)
                showRadar(company,
                    response.standalone.valuation,
                    response.standalone.performance,
                    response.standalone.health,
                    response.standalone.dividends,
                    response.standalone.momentum)
            }


        }
    });


}


function markChecked($element) {
    $element.addClass('active');
    $element.children('span').addClass('glyphicon-ok');
    $element.removeClass('list-group-item-danger');
    $element.children('span').removeClass('glyphicon-remove')
}

function markUnchecked($element) {
    $element.removeClass('active');
    $element.children('span').removeClass('glyphicon-ok');
    $element.addClass('list-group-item-danger');
    $element.children('span').addClass('glyphicon-remove')
}


function loadRoute(company, type) {
    if (company.length != 0) {
        loadPage(company)
    }
}

$('#type-all').change(function (e) {
    changeHash(e);
});

$('#addToWatchlist').click(function () {
    company = $('#company').val();
    console.log('Adding ' + company + ' to watchlist');
    $.ajax({
        type: "POST",
        url: '/api/v1/watchlist/',
        cache: false,
        data: JSON.stringify({
            'company': company
        }),
        success: function (response) {

        },
        dataType: 'json',
        contentType: "application/json; charset=utf-8"

    });
});


