import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { auth } from '../../../lib/redux/actions';
import { Loading } from '../../../pages/common/Loading';
import { Login } from '../../../pages/common/Login';
import { NotAllowed } from '../../../pages/common/NotAllowed';
import { NotFound } from '../../../pages/common/NotFound';
import { DoctorDashboard } from '../../../pages/doctor';
import { PatientDashboard } from '../../../pages/patient';
import { CorrespondingRouteRedirecter } from '../CorrespondingRouteRedirecter';
import { PrivateDoctorRoute } from '../PrivateDoctorRoute';
import { PrivatePatientRoute } from '../PrivatePatientRoute';

const RootContainer = ({ loadUser, auth }) => {
  useEffect(() => {
    loadUser();
  }, [ loadUser ]);

  return (
    <BrowserRouter>
      <Switch>
        <CorrespondingRouteRedirecter exact path="/"
                                      patientRoute="/patient"
                                      doctorRoute="/doctor"
                                      loadingComponent={ Loading }
                                      errorRedirectRoute="/login"
                                      authState={ auth }/>

        <PrivatePatientRoute exact path="/patient"
                             pageComponent={ PatientDashboard }
                             loadingComponent={ Loading }
                             notAllowedComponent={ NotAllowed }
                             errorRedirectRoute="/login"
                             authState={ auth }/>

        <PrivateDoctorRoute exact path="/doctor"
                            pageComponent={ DoctorDashboard }
                            loadingComponent={ Loading }
                            notAllowedComponent={ NotAllowed }
                            errorRedirectRoute="/login"
                            authState={ auth }/>


        <Route exact path="/login">
          <Login/>
        </Route>
        <Route>
          <NotFound/>
        </Route>
      </Switch>
    </BrowserRouter>
  );
};

const mapStateToProps = state => {
  return {
    auth: state.auth,
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadUser: () => {
      return dispatch(auth.loadUser());
    },
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(RootContainer);
