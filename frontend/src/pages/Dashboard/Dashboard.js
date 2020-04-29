import Box from '@material-ui/core/Box';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import AgeBarChart from '../../components/charts/AgeBarChart/AgeBarChart';
import CountryChart from '../../components/charts/CountryChart/CountryChart';
import { withLayout } from '../../components/Layout';
import { globalStatistics } from '../../lib/redux/actions/';

const Dashboard = ({ loadCharts, ageHistogram, countyHistogram, genderHistogram }) => {
  useEffect(() => loadCharts(), [ loadCharts ]);

  return <Box>
    <AgeBarChart
      { ...ageHistogram }
      title={ 'Distribuția deceselor pe categorii de vârstă' }
      height={ 500 }
    />

    <CountryChart
      { ...countyHistogram }
      title={ 'Distribuția deceselor pe județe' }
      height={ 500 }
    />
  </Box>;
};

const mapStateToProps = state => {
  return {
    genderHistogram: {
      data: state.globalStatistics.genderHistogram,
      loading: state.globalStatistics.genderHistogramLoading,
      errors: state.globalStatistics.genderHistogramErrors,
    },
    ageHistogram: {
      data: state.globalStatistics.ageHistogram,
      loading: state.globalStatistics.ageHistogramLoading,
      errors: state.globalStatistics.ageHistogramErrors,
    },
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
      dispatch(globalStatistics.loadGlobalAgeHistogram());
      dispatch(globalStatistics.loadGlobalCountyHistogram());
      dispatch(globalStatistics.loadGlobalGenderHistogram());
    },
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(withLayout(Dashboard));

