import API, { keysToCamel } from '../../api';

export const loadAgeHistogram = () => {
  return (dispatch, getState) => {
    dispatch({ type: 'AGE_HISTOGRAM_LOADING' });
    API.get(`/api/statistics/?search_string=full-age-histogram`)
      .then(({ status, data }) => {
        if (status === 200) {
          dispatch({ type: 'AGE_HISTOGRAM_LOADED', data: keysToCamel(data) });
        } else if (status >= 400 && status < 500) {
          dispatch({ type: 'AGE_HISTOGRAM_ERROR', data: keysToCamel(data) });
        }
      });
  };
};
