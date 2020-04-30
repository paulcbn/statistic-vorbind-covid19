const initialState = {
  ageHistogram: null,
  ageHistogramLoading: false,
  ageHistogramErrors: null,

  genderHistogram: null,
  genderHistogramLoading: false,
  genderHistogramErrors: null,

  deathDateHistogram: null,
  deathDateHistogramLoading: false,
  deathDateHistogramErrors: null,
};


export default function countyStatistics(state = initialState, action) {
  switch (action.type) {
    case 'COUNTY_AGE_HISTOGRAM_LOADING':
      return {
        ...state,
        ageHistogramLoading: true,
        ageHistogramErrors: null,
      };
    case 'COUNTY_AGE_HISTOGRAM_LOADED':
      return {
        ...state,
        ageHistogram: action.data,
        ageHistogramLoading: false,
        ageHistogramErrors: null,
      };
    case 'COUNTY_AGE_HISTOGRAM_ERROR':
      return {
        ...state,
        ageHistogramLoading: false,
        ageHistogramErrors: action.data,
      };

    case 'COUNTY_GENDER_HISTOGRAM_LOADING':
      return {
        ...state,
        genderHistogramLoading: true,
        genderHistogramErrors: null,
      };
    case 'COUNTY_GENDER_HISTOGRAM_LOADED':
      return {
        ...state,
        genderHistogram: action.data,
        genderHistogramLoading: false,
        genderHistogramErrors: null,
      };
    case 'COUNTY_GENDER_HISTOGRAM_ERROR':
      return {
        ...state,
        genderHistogramLoading: false,
        genderHistogramErrors: null,
      };

    case 'COUNTY_DEATH_DATE_HISTOGRAM_LOADING':
      return {
        ...state,
        deathDateHistogramLoading: true,
        deathDateHistogramErrors: null,
      };
    case 'COUNTY_DEATH_DATE_HISTOGRAM_LOADED':
      return {
        ...state,
        deathDateHistogram: action.data,
        deathDateHistogramLoading: false,
        deathDateHistogramErrors: null,
      };
    case 'COUNTY_DEATH_DATE_HISTOGRAM_ERROR':
      return {
        ...state,
        deathDateHistogramLoading: false,
        deathDateHistogramErrors: null,
      };

    default:
      return state;
  }
}
