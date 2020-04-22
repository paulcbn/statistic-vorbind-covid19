import { makeStyles } from '@material-ui/core';

const useStyles = makeStyles(theme => ({
  loginPaper: {
    position: 'relative',
    padding: theme.spacing(2),
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
  },
  loginInput: {
    margin: theme.spacing(1, 0),
  },
  loginContainer: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    minHeight: '80vh',
  },
  buttonBox: {
    display: 'flex',
    marginTop: theme.spacing(1),
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  captchaAndLoadingBox: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    height: theme.spacing(13),
    overflow: 'hidden',
  },
  errorPaper: {
    marginTop: theme.spacing(2),
    padding: theme.spacing(2),
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
  },
}));

export default useStyles;
