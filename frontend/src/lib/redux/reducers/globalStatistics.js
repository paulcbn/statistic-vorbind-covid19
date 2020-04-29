const initialState = {
  ageHistogram: null,
  ageHistogramLoading: false,
  ageHistogramErrors: null,

  countyHistogram: null,
  countyHistogramLoading: false,
  countyHistogramErrors: null,

  genderHistogram: null,
  genderHistogramLoading: false,
  genderHistogramErrors: null,
};


export default function global_statistics(state = initialState, action) {
  switch (action.type) {
    case 'GLOBAL_AGE_HISTOGRAM_LOADING':
      return {
        ...state,
        ageHistogramLoading: true,
        ageHistogramErrors: null,
      };
    case 'GLOBAL_AGE_HISTOGRAM_LOADED':
      return {
        ...state,
        ageHistogram:  action.data,
        ageHistogramLoading: false,
        ageHistogramErrors: null,
      };
    case 'GLOBAL_AGE_HISTOGRAM_ERROR':
      return {
        ...state,
        ageHistogramLoading: false,
        ageHistogramErrors:  action.data,
      };


    case 'GLOBAL_COUNTY_HISTOGRAM_LOADING':
      return {
        ...state,
        countyHistogramLoading: true,
        countyHistogramErrors: null,
      };
    case 'GLOBAL_COUNTY_HISTOGRAM_LOADED':
      return {
        ...state,
        countyHistogram: action.data,
        countyHistogramLoading: false,
        countyHistogramErrors: null,
      };
    case 'GLOBAL_COUNTY_HISTOGRAM_ERROR':
      return {
        ...state,
        countyHistogramLoading: false,
        countyHistogramErrors: action.data,
      };


    case 'GLOBAL_GENDER_HISTOGRAM_LOADING':
      return {
        ...state,
        genderHistogramLoading: true,
        genderHistogramErrors: null,
      };
    case 'GLOBAL_GENDER_HISTOGRAM_LOADED':
      return {
        ...state,
        genderHistogram: action.data,
        genderHistogramLoading: false,
        genderHistogramErrors: null,
      };
    case 'GLOBAL_GENDER_HISTOGRAM_ERROR':
      return {
        ...state,
        genderHistogramLoading: false,
        genderHistogramErrors: null,
      };

    default:
      return state;
  }
}
