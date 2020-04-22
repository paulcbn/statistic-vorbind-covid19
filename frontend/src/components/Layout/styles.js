import makeStyles from '@material-ui/core/styles/makeStyles';

export const useMenuDrawerStyle = makeStyles(theme => ({
  root: {
    width: 600,
  },
  flexExpander: {
    flexGrow: 1,
  },
}));

export const useMenuSectionStyle = makeStyles(theme => ({
  root: {
    margin: theme.spacing(2),
  },
}));

export const useLogoutMenuItemStyle = makeStyles(theme => ({
  root: {
    margin: theme.spacing(2),
  },
  text: {
    color: theme.palette.layout.logoutIcon,
  },
  icon: {
    color: theme.palette.layout.logoutIcon,
  },
}));

export const useLayoutHeaderStyle = makeStyles(theme => ({
  menuButton: {
    marginRight: theme.spacing(2),
  },
  logoutIcon: {
    color: theme.palette.layout.logoutIcon,
  },
  flexExpander: {
    flexGrow: 1,
  },
  title: {
    cursor: 'pointer',
  },
  userType: {
    color: theme.palette.secondary.main,
  },
}));
