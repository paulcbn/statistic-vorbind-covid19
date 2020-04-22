import AppBar from '@material-ui/core/AppBar/AppBar';
import Box from '@material-ui/core/Box';
import IconButton from '@material-ui/core/IconButton';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import AccountIcon from '@material-ui/icons/AccountCircle';
import LogoutIcon from '@material-ui/icons/ExitToApp';
import MenuIcon from '@material-ui/icons/Menu';
import React, { useCallback, useMemo } from 'react';
import { userTypes } from '../../lib/constants';
import { deepGet } from '../../lib/utils';
import { useLayoutHeaderStyle } from './styles';

const LayoutHeader = ({ onLogout, user, onOpenProfile, onOpenMenu, onOpenDashboard }) => {
  const classes = useLayoutHeaderStyle();

  const { userType } = useMemo(() => ({
    userType: deepGet(user, 'userType'),
  }), [ user ]);

  const isLoggedIn = useMemo(() => userType !== undefined, [ userType ]);
  const renderMenuButton = useCallback(() => {
    if (isLoggedIn)
      return <IconButton edge="start" className={ classes.menuButton } color={ 'inherit' } onClick={ onOpenMenu }>
        <MenuIcon/>
      </IconButton>;
    return <></>;
  }, [ isLoggedIn, classes, onOpenMenu ]);

  const renderTitle = useCallback(() => {
    if (userType === userTypes.DOCTOR)
      return <Typography variant="h5">
        Analyzr
        <Typography component='span' variant={ 'h5' } className={ classes.userType }>.Doctor</Typography>
      </Typography>;

    if (userType === userTypes.PATIENT)
      return <Typography variant="h5">
        Analyzr
        <Typography component='span' variant={ 'h5' } className={ classes.userType }>.Patient</Typography>
      </Typography>;

    return <Typography variant="h5">
      Analyzr
    </Typography>;
  }, [ userType, classes ]);

  const renderIconButtons = useCallback(() => {
    if (isLoggedIn)
      return <>
        <IconButton color={ 'inherit' } onClick={ onOpenProfile }>
          <AccountIcon/>
        </IconButton>
        <IconButton color={ 'inherit' } className={ classes.logoutIcon } onClick={ onLogout }>
          <LogoutIcon/>
        </IconButton>
      </>;

    return <></>;
  }, [ isLoggedIn, classes, onOpenProfile, onLogout ]);


  return <AppBar position="static">
    <Toolbar>
      { renderMenuButton() }
      <Box onClick={ onOpenDashboard } className={ classes.title }>
        { renderTitle() }
      </Box>
      <Box className={ classes.flexExpander }/>
      { renderIconButtons() }
    </Toolbar>
  </AppBar>;
};

export default LayoutHeader;
