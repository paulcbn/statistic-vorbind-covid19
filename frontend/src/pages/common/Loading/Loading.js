import Box from '@material-ui/core/Box';
import React from 'react';
import { withLayout } from '../../../components/Layout';
import { OverlayCircularProgress } from '../../../components/OverlayCircularProgress';
import { useStyle } from './styles.js';

const Loading = () => {
  const classes = useStyle();
  return <Box className={ classes.root }>
    <OverlayCircularProgress show={ true }/>
  </Box>;
};

export default withLayout(Loading);
