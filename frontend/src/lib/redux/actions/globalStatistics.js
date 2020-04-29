import API, { keysToCamel } from '../../api';

export const loadGlobalAgeHistogram = () => {
  return (dispatch, getState) => {
    dispatch({ type: 'GLOBAL_AGE_HISTOGRAM_LOADING' });
    API.get(`/api/statistics/global-age-histogram`)
      .then(({ status, data }) => {
        if (status === 200) {
          dispatch({ type: 'GLOBAL_AGE_HISTOGRAM_LOADED', data: keysToCamel(data) });
        } else if (status >= 400 && status < 500) {
          dispatch({ type: 'GLOBAL_AGE_HISTOGRAM_ERROR', data: keysToCamel(data) });
        }
      });
  };
};

export const loadGlobalGenderHistogram = () => {
  return (dispatch, getState) => {
    dispatch({ type: 'GLOBAL_GENDER_HISTOGRAM_LOADING' });
    API.get(`/api/statistics/global-gender-histogram`)
      .then(({ status, data }) => {
        if (status === 200) {
          dispatch({ type: 'GLOBAL_GENDER_HISTOGRAM_LOADED', data: keysToCamel(data) });
        } else if (status >= 400 && status < 500) {
          dispatch({ type: 'GLOBAL_GENDER_HISTOGRAM_ERROR', data: keysToCamel(data) });
        }
      });
  };
};

export const loadGlobalCountyHistogram = () => {
  return (dispatch, getState) => {
    dispatch({ type: 'GLOBAL_COUNTY_HISTOGRAM_LOADING' });
    API.get(`/api/statistics/global-county-histogram`)
      .then(({ status, data }) => {
        if (status === 200) {
          dispatch({ type: 'GLOBAL_COUNTY_HISTOGRAM_LOADED', data: keysToCamel(data) });
        } else if (status >= 400 && status < 500) {
          dispatch({ type: 'GLOBAL_COUNTY_HISTOGRAM_ERROR', data: keysToCamel(data) });
        }
      });
  };
};
