var companies;
$.ajax({
    url: '/api/v1/companies',
    success: function (data) {
        companies = data.companies;
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
                .on('typeahead:selected', changeHash);

        $('#company-div-index .typeahead-index').typeahead({
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

function onOpened($e) {
  console.log('opened');
}

function onAutocompleted($e, datum) {
  console.log('autocompleted');
  console.log(datum);
}

function onSelected($e, datum) {
  console.log('selected');
  console.log(datum);
}