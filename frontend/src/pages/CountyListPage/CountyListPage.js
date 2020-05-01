import Box from '@material-ui/core/Box';
import React, { useCallback, useEffect } from 'react';
import { connect } from 'react-redux';
import { useHistory } from 'react-router-dom';
import { CountryChart } from '../../components/charts/CountryChart';
import { withLayout } from '../../components/Layout';
import { globalStatistics } from '../../lib/redux/actions/';
import CountyTable from './CountyTable';


const CountyPage = ({ loadCharts, countyHistogram }) => {
  const history = useHistory();
  useEffect(() => {
    loadCharts();
  }, [ loadCharts ]);

  const navigateToCountyDetails = useCallback((countyCode) => history.push(`/judete/${ countyCode }`), [ history ]);

  return <Box>
    <CountryChart
      { ...countyHistogram }
      title={ 'Distribuția deceselor pe județe' }
      height={ 500 }
    />
    <CountyTable countyHistogram={ countyHistogram } onSelectCounty={ navigateToCountyDetails }/>
  </Box>;
};

const mapStateToProps = state => {
  return {
    countyHistogram: {
      data: state.globalStatistics.countyHistogram,
      loading: state.globalStatistics.countyHistogramLoading,
      errors: state.globalStatistics.countyHistogramErrors,
    },
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadCharts: () => {
      dispatch(globalStatistics.loadGlobalCountyHistogram());
    },
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(withLayout(CountyPage));

