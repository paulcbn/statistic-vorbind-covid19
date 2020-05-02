import API, { keysToCamel, keysToUnderscore } from '../../api';


const createFilterQueryString = (filters) => {
  if (filters === undefined || filters === null)
    return '';
  const pythonCaseFilters = keysToUnderscore(filters);
  return Object.entries(pythonCaseFilters).map(([ key, value ]) => `${ key }=${ value }`).join('&');
};

export const loadCaseList = (filters) => {
  return (dispatch, getState) => {
    dispatch({ type: 'CASE_LIST_LOADING' });
    const queryString = createFilterQueryString(filters);
    API.get(`/api/case/?${ queryString }`)
      .then(({ status, data }) => {
        if (status === 200) {
          dispatch({ type: 'CASE_LIST_LOADED', data: keysToCamel(data) });
        } else if (status >= 400 && status < 500) {
          dispatch({ type: 'CASE_LIST_ERROR', data: keysToCamel(data) });
        }
      });
  };
};
