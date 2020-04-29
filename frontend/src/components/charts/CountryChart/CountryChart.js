import { ListItemText } from '@material-ui/core';
import Divider from '@material-ui/core/Divider';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import ReactEcharts from 'echarts-for-react';
import moment from 'moment';
import React, { useMemo } from 'react';
import { COUNTIES } from '../../../config/countyInfo';
import { deepGet } from '../../../lib/utils';
import { OverlayCircularProgress } from '../../OverlayCircularProgress';
import { useStyles } from './styles';


const CountryChart = ({ data, loading, title, height }) => {
  const { dateModified, sampleSize, dataList, average, min, max } = useMemo(() => ({
    dateModified: deepGet(data, 'dateModified'),
    searchString: deepGet(data, 'searchString'),
    sampleSize: deepGet(data, 'content.aggregation.sampleSize'),
    min: deepGet(data, 'content.aggregation.min', 0),
    max: deepGet(data, 'content.aggregation.max', 0),
    average: deepGet(data, 'content.aggregation.average', 0),
    dataList: deepGet(data, 'content.data', []),
  }), [ data ]);


  const chartData = useMemo(() => dataList.map(({ label, value }) => ({ name: COUNTIES[label], value })), [ dataList ]);
  const maxDeathCount = useMemo(() => {
    let result = 0;
    dataList.forEach(({ value }) => {
      if (value > result) result = value;
    });
    return result;
  }, [ dataList ]);

  const option = useMemo(() => ({
    series: {
      type: 'map',
      mapType: 'RO',
      emphasis: {
        label: {
          show: false,
        },
      },
      data: chartData,
    },
    tooltip: {
      trigger: 'item',
      formatter: (item) => `<strong>${ item.name }</strong></br>
          Decese: ${ item.value }</br>`,
    },
    visualMap: {
      min: 0,
      max: maxDeathCount,
      calculable: true,
      realtime: false,
      inRange: {
        color: [ '#ddcccc', '#990000', '#330000' ],
      },
    },
  }), [ maxDeathCount, chartData ]);


  const classes = useStyles();

  return <Paper className={ classes.paper }>
    <Typography variant={ 'h5' } className={ classes.title }>
      { title }
    </Typography>
    <Divider variant={ 'middle' }/>
    <ReactEcharts
      option={ option }
      style={ { height, width: '100%' } }
      opts={ { renderer: 'svg' } }

    />
    
    <Divider variant={ 'middle' }/>

    <List dense>
      <ListItem>
        <ListItemText>Vârsta minimă: { min.toFixed(2) }</ListItemText>
      </ListItem>
      <ListItem>
        <ListItemText>Vârsta maximă: { max.toFixed(2) }</ListItemText>
      </ListItem>
      <ListItem>
        <ListItemText>Vârsta medie: { average.toFixed(2) }</ListItemText>
      </ListItem>
      <ListItem>
        <ListItemText>Numărul cazurilor analizate: { sampleSize }</ListItemText>
      </ListItem>
      <ListItem>
        <ListItemText>Ultima actualizare: { moment(dateModified).format('DD-MM-YYYY') }</ListItemText>
      </ListItem>
    </List>
    <OverlayCircularProgress show={ loading } circularSize={ 100 }/>
  </Paper>;
};


export default CountryChart;
