import React, { useMemo } from 'react';
import { Redirect, Route } from 'react-router-dom';
import { userTypes } from '../../../lib/constants';
import { deepGet } from '../../../lib/utils';

const CorrespondingRouteRedirecter = ({ patientRoute, doctorRoute, loadingComponent: Loading, authState, errorRedirectRoute, ...otherProps }) => {
  const { isDoctor, isAuthenticated, loading } = useMemo(() => ({
    loading: deepGet(authState, 'loginLoading', false) || deepGet(authState, 'currentUserLoading', false),
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
      if (isDoctor)
        return <Redirect to={ doctorRoute }/>;
      return <Redirect to={ patientRoute }/>;
    } }
  />;
};
export default CorrespondingRouteRedirecter;
