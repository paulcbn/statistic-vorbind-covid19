import ReactEcharts from 'echarts-for-react';
import moment from 'moment';
import React, { useMemo } from 'react';
import { deepGet } from '../../../lib/utils';
import ChartWrapper from '../ChartWrapper/ChartWrapper';


const DeathDateChart = ({ data, loading, title, height }) => {
  const { dateModified, sampleSize, dataList, maxGroupValue, averageGroupValue } = useMemo(() => ({
    dateModified: deepGet(data, 'dateModified'),
    sampleSize: deepGet(data, 'content.aggregation.sampleSize', 0),
    averageGroupValue: deepGet(data, 'content.aggregation.averageGroupValue', 0),
    maxGroupValue: deepGet(data, 'content.aggregation.maxGroupValue', 0),
    dataList: deepGet(data, 'content.data', []),
  }), [ data ]);

  const chartData = useMemo(() => {
    let result = dataList.slice();
    for (let i = 0; i < result.length - 1; i++) {
      const currentDate = moment(deepGet(result[i], 'label'));
      const nextDate = moment(deepGet(result[i + 1], 'label'));
      const duration = moment.duration(nextDate.diff(currentDate));

      let delta = duration.asDays();
      let addedDayIndex = 0;
      while (addedDayIndex < delta - 1) {
        addedDayIndex++;
        result.splice(i + addedDayIndex, 0, {
          label: moment(currentDate).add(addedDayIndex, 'day').format('YYYY-MM-DD'),
          value: 0,
        });
      }
      i += addedDayIndex;
    }
    return result;
  }, [ dataList ]);
  const xAxisData = useMemo(() => chartData.map(({ label }) => label), [ chartData ]);

  const initialSliderLength = 30;
  const startValue = useMemo(() => {
    if (chartData.length < initialSliderLength)
      return undefined;
    return chartData.length - initialSliderLength;
  }, [ chartData ]);

  const option = useMemo(() => ({
    tooltip: {
      trigger: 'axis',
      formatter: 'Decese {b}:<br/> {c}',
    },
    xAxis: {
      data: xAxisData,
    },
    yAxis: {
      splitLine: {
        show: false,
      },
    },
    dataZoom: [ {
      type: 'slider',
      minValueSpan: 7,
      maxValueSpan: 30,
      startValue: startValue,
      xAxisIndex: [ 0 ],
      filterMode: 'filter',
    } ],
    visualMap: {
      show: false,
      type: 'continuous',
      min: 0,
      max: maxGroupValue,
      inRange: {
        color: [ '#ddcccc', '#990000', '#330000' ],
      },
    },
    series: {
      type: 'line',
      data: chartData,
      smooth: true,
      smoothMonotone: 'x',
      areaStyle: {
        color: {
          type: 'linear',
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: 'rgb(77,0,3)' },
            { offset: 0.6, color: 'rgba(169,4,0,0.66)' },
            { offset: 1, color: 'rgba(254,217,217,0.33)' },
          ],
        },
      },
    },
  }), [ chartData, xAxisData, maxGroupValue, startValue ]);


  const metadataList = useMemo(() => [
    { label: 'Numărul maxim/zi', value: maxGroupValue },
    { label: 'Numărul mediu/zi (WIP)', value: averageGroupValue.toFixed(2) },
    { label: 'Numărul cazurilor analizate', value: sampleSize },
    { label: 'Ultima actualizare', value: moment(dateModified).format('DD-MM-YYYY') },
  ], [ sampleSize, dateModified, maxGroupValue, averageGroupValue ]);

  return <ChartWrapper title={ title } loading={ loading } metadataList={ metadataList }>
    <ReactEcharts
      option={ option }
      style={ { height, width: '100%' } }
      // opts={ { renderer: 'svg' } }
    />
  </ChartWrapper>;
};


export default DeathDateChart;
