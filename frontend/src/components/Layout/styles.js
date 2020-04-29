import makeStyles from '@material-ui/core/styles/makeStyles';

export const useLayoutHeaderStyle = makeStyles(theme => ({
  appBar: {
    padding: theme.spacing(1, 1),
  },
  inline: {
    display: 'inline',
  },
  link: {
    '&$link': {
      textDecoration: 'none',
      color: 'inherit',
    },
  },
  navLink: {
    '&:hover': {
      color: theme.palette.secondary.light,
    },
  },
  navLinkActive: {
    '&$link': {
      color: theme.palette.secondary.main,
    },
  },
  flexExpander: {
    flex: 1,
  },
  navText: {
    padding: theme.spacing(0, 1),
  },
}));
