import React, { useMemo } from 'react';
import { Redirect, Route } from 'react-router-dom';
import { userTypes } from '../../../lib/constants';
import { deepGet } from '../../../lib/utils';

const PrivateDoctorRoute = ({ pageComponent: Page, loadingComponent: Loading, notAllowedComponent: NotAllowed, errorRedirectRoute, authState, ...otherProps }) => {
  const { loading, isAuthenticated, isDoctor } = useMemo(() => ({
    loading: deepGet(authState, 'loginLoading', false),
    isAuthenticated: deepGet(authState, 'isAuthenticated', false),
    isDoctor: deepGet(authState, 'currentUser.userType', userTypes.PATIENT) === userTypes.DOCTOR,
  }), [ authState ]);

  return <Route
    { ...otherProps }

    render={ props => {
      if (loading)
        return <Loading { ...props }/>;
      if (!isAuthenticated)
        return <Redirect to={ errorRedirectRoute }/>;
      if (!isDoctor)
        return <NotAllowed/>;

      return <Page { ...props } />;
    } }
  />;
};

export default PrivateDoctorRoute;
