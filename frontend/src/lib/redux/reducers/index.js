import { combineReducers } from 'redux';
import globalStatistics from './globalStatistics';
import countyStatistics from './countyStatistics';
import caseList from './caseList';

export const rootReducer = combineReducers({
  globalStatistics, countyStatistics, caseList
});

