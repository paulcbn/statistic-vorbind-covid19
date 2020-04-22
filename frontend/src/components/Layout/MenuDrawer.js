import { Divider, Drawer } from '@material-ui/core';
import Box from '@material-ui/core/Box';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Typography from '@material-ui/core/Typography';
import LogoutIcon from '@material-ui/icons/ExitToApp';
import { useHistory } from 'react-router-dom';
import React, { useMemo } from 'react';
import { deepGet } from '../../lib/utils';
import { getMenuSections } from './navigationRoutes';
import { useMenuDrawerStyle, useMenuSectionStyle, useLogoutMenuItemStyle } from './styles';

const MenuSection = ({ section, history }) => {
  const classes = useMenuSectionStyle();
  return <Box className={ classes.root }>
    <Typography variant='h6'>
      { section.title }
    </Typography>
    <Divider/>
    <List>
      { section.entries.map(({ name, route, Icon }) => (
        <ListItem button key={ name } onClick={ () => history.push(route) }>
          { Icon && <ListItemIcon><Icon/></ListItemIcon> }
          <ListItemText primary={ name }/>
        </ListItem>
      )) }
    </List>
  </Box>;
};

const LogoutMenuItem = ({ onLogout }) => {
  const classes = useLogoutMenuItemStyle();
  return <List className={ classes.root }>
    <ListItem button onClick={ onLogout }>
      <ListItemIcon className={ classes.icon }>
        <LogoutIcon/>
      </ListItemIcon>
      <ListItemText className={ classes.text }>
        Logout
      </ListItemText>
    </ListItem>
  </List>;
};

const MenuDrawer = ({ user, isOpen, onClose, onLogout }) => {
  const classes = useMenuDrawerStyle();
  const { userType } = useMemo(() => ({
    userType: deepGet(user, 'userType', '-'),
  }), [ user ]);
  const history = useHistory();
  const sections = useMemo(() => getMenuSections(userType), [ userType ]);

  return <Drawer
    open={ isOpen }
    onClose={ onClose }
    className={ classes.root }
  >
    { sections.map(section => <MenuSection key={ section.title } section={ section } history={ history }/>) }
    <Box className={ classes.flexExpander }/>
    <LogoutMenuItem onLogout={ onLogout }/>
  </Drawer>;
};

export default MenuDrawer;
