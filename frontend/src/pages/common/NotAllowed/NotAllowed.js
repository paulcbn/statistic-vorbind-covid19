import Box from '@material-ui/core/Box';
import React from 'react';
import { withLayout } from '../../../components/Layout';
import { useStyle } from './styles.js';

const NotAllowed = () => {
  const classes = useStyle();
  return <Box className={ classes.root }>
  </Box>;
};

export default withLayout(NotAllowed);
