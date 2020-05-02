const initialState = {
  caseList: null,
  caseListLoading: false,
  caseListErrors: null,
};


export default function caseList(state = initialState, action) {
  switch (action.type) {
    case 'CASE_LIST_LOADING':
      return {
        ...state,
        caseListLoading: true,
        caseListErrors: null,
      };
    case 'CASE_LIST_LOADED':
      return {
        ...state,
        caseList: action.data,
        caseListLoading: false,
        caseListErrors: null,
      };
    case 'CASE_LIST_ERROR':
      return {
        ...state,
        caseListLoading: false,
        caseListErrors: action.data,
      };


    default:
      return state;
  }
}
