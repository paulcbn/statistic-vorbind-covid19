import API, { keysToCamel } from '../../api';

const loadAgeHistogram = (countyCode) => {
  return (dispatch, getState) => {
    dispatch({ type: 'COUNTY_AGE_HISTOGRAM_LOADING' });
    API.get(`/api/statistics/${countyCode}-age-histogram`)
      .then(({ status, data }) => {
        if (status === 200) {
          dispatch({ type: 'COUNTY_AGE_HISTOGRAM_LOADED', data: keysToCamel(data) });
        } else if (status >= 400 && status < 500) {
          dispatch({ type: 'COUNTY_AGE_HISTOGRAM_ERROR', data: keysToCamel(data) });
        }
      });
  };
};

const loadDeathDateHistogram = (countyCode) => {
  return (dispatch, getState) => {
    dispatch({ type: 'COUNTY_DEATH_DATE_HISTOGRAM_LOADING' });
    API.get(`/api/statistics/${countyCode}-death-date-histogram`)
      .then(({ status, data }) => {
        if (status === 200) {
          dispatch({ type: 'COUNTY_DEATH_DATE_HISTOGRAM_LOADED', data: keysToCamel(data) });
        } else if (status >= 400 && status < 500) {
          dispatch({ type: 'COUNTY_DEATH_DATE_HISTOGRAM_ERROR', data: keysToCamel(data) });
        }
      });
  };
};

const loadGenderHistogram = (countyCode) => {
  return (dispatch, getState) => {
    dispatch({ type: 'COUNTY_GENDER_HISTOGRAM_LOADING' });
    API.get(`/api/statistics/${countyCode}-gender-histogram`)
      .then(({ status, data }) => {
        if (status === 200) {
          dispatch({ type: 'COUNTY_GENDER_HISTOGRAM_LOADED', data: keysToCamel(data) });
        } else if (status >= 400 && status < 500) {
          dispatch({ type: 'COUNTY_GENDER_HISTOGRAM_ERROR', data: keysToCamel(data) });
        }
      });
  };
};

export const loadCountyHistograms = (countyCode) => {
  return (dispatch, getState) => {
    dispatch(loadGenderHistogram(countyCode));
    dispatch(loadDeathDateHistogram(countyCode));
    dispatch(loadAgeHistogram(countyCode));
  };
};
