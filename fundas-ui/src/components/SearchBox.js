import React from 'react';
import {white} from 'material-ui/styles/colors';
import AutoComplete from 'material-ui/AutoComplete';


const filter = (searchText, key) =>  searchText !== '' && key.toUpperCase().startsWith(searchText.toUpperCase());


const SearchBox = ({data, onSelect}) => {


    const styles = {
        iconButton: {
            float: 'right',
            paddingTop: 17
        },
        textField: {
            float:'right',
            color: white,
            borderRadius: 2
        },
        inputStyle: {
            textColor:white,
            color: white,
            paddingLeft: 5
        },
        hintStyle: {
            height: 16,
            paddingLeft: 5,
            color: white
        }
    };
    return (
        <div>

                <AutoComplete
                    style={styles.textField}
                    hintText="Search for a company"
                    textFieldStyle={styles.inputStyle}
                    dataSource={data}
                    filter={filter}
                    onNewRequest={onSelect}
                />

        </div>
    );
};

export default SearchBox;
