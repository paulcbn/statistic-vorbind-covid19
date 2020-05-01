import Box from '@material-ui/core/Box';
import Grid from '@material-ui/core/Grid';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import AgeBarChart from '../../components/charts/AgeBarChart/AgeBarChart';
import CountryChart from '../../components/charts/CountryChart/CountryChart';
import DeathDateChart from '../../components/charts/DeathDateChart/DeathDateChart';
import { GenderChart } from '../../components/charts/GenderChart';
import { withLayout } from '../../components/Layout';
import { globalStatistics } from '../../lib/redux/actions/';

const Dashboard = ({ loadCharts, ageHistogram, countyHistogram, genderHistogram, deathDateHistogram }) => {
  useEffect(() => loadCharts(), [ loadCharts ]);


  return <Box>
    <Grid container>
      <Grid item xs={ 12 } md={ 7 }>
        <AgeBarChart
          { ...ageHistogram }
          title={ 'Distribuția deceselor pe categorii de vârstă' }
          height={ 400 }
        />
      </Grid>
      <Grid item xs={ 12 } md={ 5 }>
        <GenderChart
          { ...genderHistogram }
          title={ 'Distribuția deceselor pe gen' }
          height={ 400 }
        />
      </Grid>
    </Grid>


    <CountryChart
      { ...countyHistogram }
      title={ 'Distribuția deceselor pe județe' }
      height={ 500 }
    />


    <DeathDateChart
      { ...deathDateHistogram }
      title={ 'Distribuția deceselor pe zile' }
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
    deathDateHistogram: {
      data: state.globalStatistics.deathDateHistogram,
      loading: state.globalStatistics.deathDateHistogramLoading,
      errors: state.globalStatistics.deathDateHistogramErrors,
    },
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadCharts: () => {
      dispatch(globalStatistics.loadGlobalHistograms());
    },
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(withLayout(Dashboard));

