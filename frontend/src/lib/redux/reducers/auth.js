const initialState = {
  data: null,
  dataLoading: false,
  dataErrors: null,
};


export default function auth(state = initialState, action) {
  switch (action.type) {
    case 'AGE_HISTOGRAM_LOADING':
      return {
        ...state,
        data: null,
        dataLoading: true,
        dataErrors: {},
      };
    case 'AGE_HISTOGRAM_LOADED':
      return {
        ...state,
        data: null,
        dataLoading: false,
        dataErrors: action.data,
      };
    case 'AGE_HISTOGRAM_ERROR':
      return {
        ...state,
        data: action.data,
        dataLoading: false,
        dataErrors: {},
      };

    default:
      return state;
  }
}
