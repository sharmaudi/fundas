import {typography} from 'material-ui/styles';
import {blue600, grey600} from 'material-ui/styles/colors';

const styles = {
    navigation: {
        fontSize: 15,
        fontWeight: typography.fontWeightLight,
        color: grey600,
        paddingBottom: 15,
        display: 'block'
    },
    title: {
        fontSize: 24,
        fontWeight: typography.fontWeightLight,
        marginBottom: 10
    },
    section: {
      padding:5,
    },
    paper: {
        padding: 30
    },
    toolbar: {
      backgroundColor: blue600,
      fontWeight: typography.fontWeightLight,
    },
    toolbarActive: {
        fontWeight: typography.fontWeightMedium,
        fontSize: 20,
        color:'white'
    },
    toolbarInactive: {
        fontWeight: typography.fontWeightLight,
        color:'white'
    },
    clear: {
        clear: 'both'
    }
};

export default styles;
