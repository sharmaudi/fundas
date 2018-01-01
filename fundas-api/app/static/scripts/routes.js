$('#fundas-nav').click(function() {
    event.preventDefault();
    window.location = '/fundas#' + window.location.hash.substr(1);
})

$('#valuation-nav').click(function() {
    event.preventDefault();
    window.location = '/fundas/valuation#' + window.location.hash.substr(1);
})

$('#performance-nav').click(function() {
    event.preventDefault();
    window.location = '/fundas/performance#' + window.location.hash.substr(1);
})

$('#health-nav').click(function() {
    event.preventDefault();
    window.location = '/fundas/health#' + window.location.hash.substr(1);
})

$('#dividends-nav').click(function() {
    event.preventDefault();
    window.location = '/fundas/dividends#' + window.location.hash.substr(1);
})

$('#analysis-nav').click(function() {
        event.preventDefault();

    window.location = '/analysis#' + window.location.hash.substr(1);

})

$('#watchlist-nav').click(function() {
        event.preventDefault();

    window.location = '/watchlist#' + window.location.hash.substr(1);

})

$('#portfolio-nav').click(function() {
        event.preventDefault();

    window.location = '/portfolio#' + window.location.hash.substr(1);

});

$('#portfolio-performance-nav').click(function() {
        event.preventDefault();

    window.location = '/portfolio/performance/#' + window.location.hash.substr(1);

});



$('#annual-reports-nav').click(function() {
        event.preventDefault();

    window.location = '/annual#' + window.location.hash.substr(1);

})

$('#quarterly-reports-nav').click(function() {
        event.preventDefault();

    window.location = '/quarterly#' + window.location.hash.substr(1);

})

$('#fin-ratios-nav').click(function() {
        event.preventDefault();

    window.location = '/ratios#' + window.location.hash.substr(1);

})





$('#momentum-nav').click(function() {
        event.preventDefault();
    window.location = '/momentum#' + window.location.hash.substr(1);

})

$('#about-nav').click(function() {
        event.preventDefault();

    window.location = '/about#' + window.location.hash.substr(1);

})

function routeChange() {
    console.log(location.pathname)
    var company = this.company;
    var type = this.type;
     if(type && type.toLowerCase() === "standalone") {
        type = "Standalone"
    } else {
        type = "Consolidated"
    }
    loadRoute(company,type)
}


function handleRouteChange() {
        console.log(location.pathname)

    var company = location.hash.slice(1).split("/")[0];
    var type = location.hash.slice(1).split("/")[1];

    if(type && type.toLowerCase() === "standalone") {
        type = "Standalone"
    } else {
        type = "Consolidated"
    }

    $('#company').val(company);
    $('#type-all').val(type);

    if(!type) {
        type = 'Consolidated'
    }

    loadRoute(company,type);

}



function changeHash(event) {
     event.preventDefault();
    var company = $('#company').val();
    var type = $('#type-all').val();

    if(type && type.toLowerCase() === "standalone") {
        type = "Standalone"
    } else {
        type = "Consolidated"
    }

    var newhash = company + "/" + type;

    console.log("New Hash = " + newhash);

    window.location.hash = newhash;
}

$(window).on('hashchange',handleRouteChange()).trigger('hashchange');


window.addEventListener('hashchange', function() {
   handleRouteChange();
}, false);

$.routes.add('{company:string/{type:string}', routeChange);