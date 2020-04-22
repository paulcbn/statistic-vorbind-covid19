import { Container } from '@material-ui/core';
import Box from '@material-ui/core/Box';
import React, { useCallback, useMemo, useState } from 'react';
import { connect } from 'react-redux';
import { useHistory } from 'react-router-dom';
import { auth } from '../../lib/redux/actions';
import { deepGet } from '../../lib/utils';
import LayoutHeader from './LayoutHeader';
import MenuDrawer from './MenuDrawer';
import { getProfileRoute, getDashboardRoute } from './navigationRoutes';

const LayoutComponent = ({ children, logout, user }) => {
  const userType = useMemo(() => deepGet(user, 'userType'), [ user ]);

  const [ drawerOpen, setDrawerOpen ] = useState(false);
  const handleCloseMenu = useCallback(() => setDrawerOpen(false), [ setDrawerOpen ]);
  const handleOpenMenu = useCallback(() => setDrawerOpen(true), []);
  const history = useHistory();
  const profileRoute = useMemo(() => getProfileRoute(userType), [ userType ]);
  const dashboardRoute = useMemo(() => getDashboardRoute(userType), [ userType ]);
  const handleOpenProfile = useCallback(() => history.push(profileRoute), [ history, profileRoute ]);
  const handleOpenDashboard = useCallback(() => history.push(dashboardRoute), [ history, dashboardRoute ]);
  return <Box>
    <LayoutHeader
      user={ user }
      onLogout={ logout }
      onOpenMenu={ handleOpenMenu }
      onOpenDashboard={ handleOpenDashboard }
      onOpenProfile={ handleOpenProfile }
    />
    <MenuDrawer
      user={ user }
      isOpen={ drawerOpen }
      onClose={ handleCloseMenu }
      onLogout={ logout }
    />
    <Container>
      { children }
    </Container>
  </Box>;
};

const mapStateToProps = (state) => ({
  user: state.auth.currentUser,
});
const mapDispatchToProps = (dispatch) => ({
  logout: () => dispatch(auth.logout()),
});

const Layout = connect(mapStateToProps, mapDispatchToProps)(LayoutComponent);

export const withLayout = (PageComponent) => {
  return (props) => {
    return <Layout>
      <PageComponent { ...props }/>
    </Layout>;
  };
};
