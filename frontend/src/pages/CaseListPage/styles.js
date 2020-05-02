import makeStyles from '@material-ui/core/styles/makeStyles';

export const useStyles = makeStyles(theme => ({
  titlePaper: {
    margin: theme.spacing(1, 0),
    padding: theme.spacing(3),
    background: theme.palette.primary.main,
  },
  whiteText: {
    color: theme.palette.primary.contrastText,
  },
  tableHeaderCell: {
    fontWeight: 'bold',
  },
  contentPaper: {
    display: 'flex',
    position: 'relative',
    flexGrow: 1,
    flexDirection: 'column',
    margin: theme.spacing(1, 0),
  },
  dividerBox: {
    marginBottom: theme.spacing(3),
  },
  buttonBox: {
    display: 'flex',
    justifyContent: 'space-between',
    margin: theme.spacing(2),
  },
  tableBox: {
    flexGrow: 1,
  },
  filterPaper: {
    margin: theme.spacing(1, 0),
  },
  gridItems: {
    padding: theme.spacing(1),
  },
  selectControl: {
    width: '100%',
  },
}));
