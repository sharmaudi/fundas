var companies;
$.ajax({
    url: '/api/v1/companies',
    success: function (data) {
        companies = data.companies;
        console.log(companies);

        var comp_bloodhound = new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.whitespace,
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            // `states` is an array of state names defined in "The Basics"
            local: companies
        });

        $('#company-div .typeahead').typeahead({
                hint: true,
                highlight: true,
                minLength: 1
            },
            {
                name: 'companies',
                source: comp_bloodhound
            })
                .on('typeahead:selected', onSelected);

    }
});


function onSelected($e, datum) {
  console.log('selected');
  console.log(datum);
  window.location = '/fundas#'+datum;
}