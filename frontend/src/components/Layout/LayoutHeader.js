import AppBar from '@material-ui/core/AppBar/AppBar';
import Box from '@material-ui/core/Box';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import clsx from 'clsx';
import React, { useCallback } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { useLayoutHeaderStyle } from './styles';

const links = [
  { label: 'Situație zilnică', to: '/situatie-zilnica/' },
  { label: 'Statistici', to: '/statistici/' },
  { label: 'Listă cazuri', to: '/lista-cazuri/' },
];

const CustomNavLink = ({ label, to, exact }) => {
  const classes = useLayoutHeaderStyle();

  return <NavLink
    key={ label }
    exact={ exact }
    to={ to }
    className={ clsx(classes.link, classes.navLink) }
    activeClassName={ classes.navLinkActive }>
    <Typography className={ classes.navText } variant='body1'>
      { label }
    </Typography>
  </NavLink>;
};


const LayoutHeader = () => {
  const classes = useLayoutHeaderStyle();

  const renderAllLinks = useCallback(() => links.map((linkData, index) => <CustomNavLink { ...linkData }/>), []);

  return <AppBar position="static" className={ classes.appBar }>
    <Toolbar>
      <Link to='/' className={ classes.link }>
        <Typography className={ classes.inline } variant='h5'>Situație decese - </Typography>
        <Typography className={ classes.inline } variant='h5' color='secondary'> COVID19 </Typography>
      </Link>
      <Box className={ classes.flexExpander }/>
      { renderAllLinks() }
    </Toolbar>

  </AppBar>;
};

export default LayoutHeader;
