import Divider from '@material-ui/core/Divider';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import React, { useCallback } from 'react';
import { OverlayCircularProgress } from '../../OverlayCircularProgress';
import { useStyles } from './styles';


const ChartWrapper = ({ title, children, metadataList, loading }) => {
  const classes = useStyles();
  const renderMetadataList = useCallback(() => {
    return <List dense>
      { (metadataList || []).map(({ label, value }) => {
        return <ListItem key={ label }>{ label }:&nbsp;{ value }</ListItem>;
      }) }
    </List>;
  }, [ metadataList ]);

  return <Paper className={ classes.paper }>
    <Typography variant={ 'h5' } className={ classes.title }>
      { title }
    </Typography>
    <Divider variant={ 'middle' }/>
    { children }
    { (metadataList || []).length > 0 && <Divider variant={ 'middle' }/> }
    { renderMetadataList() }
    <OverlayCircularProgress show={ loading } circularSize={ 100 }/>
  </Paper>;
};

export default ChartWrapper;
