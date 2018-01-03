import {blue600, grey900,} from 'material-ui/styles/colors';
import spacing from 'material-ui/styles/spacing';

import getMuiTheme from 'material-ui/styles/getMuiTheme';


export default getMuiTheme({
    spacing: spacing,
    fontFamily: 'Roboto, sans-serif',
    borderRadius: 2,
    palette: {

    },
    appBar: {
        height: 57,
        color: blue600
    },
    drawer: {
        width: 200,
        color: grey900
    },
    raisedButton: {
        primaryColor: blue600,
    }
});