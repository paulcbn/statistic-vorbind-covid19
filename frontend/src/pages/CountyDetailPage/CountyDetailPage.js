import Box from '@material-ui/core/Box';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { useParams } from 'react-router-dom';
import AgeBarChart from '../../components/charts/AgeBarChart/AgeBarChart';
import DeathDateChart from '../../components/charts/DeathDateChart/DeathDateChart';
import { GenderChart } from '../../components/charts/GenderChart';
import { withLayout } from '../../components/Layout';
import { COUNTIES, isValidCountyCode } from '../../config/countyInfo';
import { countyStatistics } from '../../lib/redux/actions/';
import { useStyles } from './styles';


const CountyPage = ({ loadCharts, ageHistogram, genderHistogram, deathDateHistogram }) => {
  const { countyCode } = useParams();
  useEffect(() => {
    if (isValidCountyCode(countyCode))
      loadCharts(countyCode);
  }, [ loadCharts, countyCode ]);
  const classes = useStyles();

  if (!isValidCountyCode(countyCode))
    return <Typography variant='h4' align='center'>
      Cod de județ invalid!
    </Typography>;

  return <Box>
    <Paper className={ classes.titlePaper }>
      <Typography variant='h4' component={ 'span' } className={classes.whiteText}>
        Județul&nbsp;
      </Typography>
      <Typography component={ 'span' } variant={ 'h4' } color={'secondary'}>
        { COUNTIES[countyCode] }
      </Typography>
    </Paper>

    <AgeBarChart
      { ...ageHistogram }
      title={ 'Distribuția deceselor pe categorii de vârstă' }
      height={ 500 }
    />

    <GenderChart
      { ...genderHistogram }
      title={ 'Distribuția deceselor pe gen' }
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
      data: state.countyStatistics.genderHistogram,
      loading: state.countyStatistics.genderHistogramLoading,
      errors: state.countyStatistics.genderHistogramErrors,
    },
    ageHistogram: {
      data: state.countyStatistics.ageHistogram,
      loading: state.countyStatistics.ageHistogramLoading,
      errors: state.countyStatistics.ageHistogramErrors,
    },
    deathDateHistogram: {
      data: state.countyStatistics.deathDateHistogram,
      loading: state.countyStatistics.deathDateHistogramLoading,
      errors: state.countyStatistics.deathDateHistogramErrors,
    },
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadCharts: (countyCode) => {
      dispatch(countyStatistics.loadCountyHistograms(countyCode));
    },
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(withLayout(CountyPage));

