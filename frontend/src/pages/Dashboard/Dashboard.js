import Typography from '@material-ui/core/Typography';
import React from 'react';
import AgeBarChart from '../../components/charts/AgeBarChart/AgeBarChart';
import CountryChart from '../../components/charts/CountryChart/CountryChart';
import { withLayout } from '../../components/Layout';

const Dashboard = () => {
  return <Typography>
    <AgeBarChart/>
    <CountryChart/>
  </Typography>;
};

export default withLayout(Dashboard);

