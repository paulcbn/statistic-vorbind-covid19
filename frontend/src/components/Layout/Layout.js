import { Container } from '@material-ui/core';
import Box from '@material-ui/core/Box';
import React from 'react';
import LayoutHeader from './LayoutHeader';

const Layout = ({ children}) => {
  return <Box>
    <LayoutHeader/>
    <Container>
      { children }
    </Container>
  </Box>;
};


export const withLayout = (PageComponent) => {
  return (props) => {
    return <Layout>
      <PageComponent { ...props }/>
    </Layout>;
  };
};
