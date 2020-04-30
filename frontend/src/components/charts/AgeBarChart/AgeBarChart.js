import ReactEcharts from 'echarts-for-react';
import moment from 'moment';
import React, { useMemo } from 'react';
import { deepGet } from '../../../lib/utils';
import ChartWrapper from '../ChartWrapper/ChartWrapper';


const AgeBarChart = ({ data, loading, title, height }) => {
  const { dateModified, sampleSize, dataList, averageValue, minValue, maxValue, maxGroupValue } = useMemo(() => ({
    dateModified: deepGet(data, 'dateModified'),
    searchString: deepGet(data, 'searchString'),
    sampleSize: deepGet(data, 'content.aggregation.sampleSize'),
    minValue: deepGet(data, 'content.aggregation.minFieldValue', 0),
    maxValue: deepGet(data, 'content.aggregation.maxFieldValue', 0),
    maxGroupValue: deepGet(data, 'content.aggregation.maxGroupValue', 0),
    averageValue: deepGet(data, 'content.aggregation.averageFieldValue', 0),
    dataList: deepGet(data, 'content.data', []),
  }), [ data ]);

  const sortedDataList = useMemo(() => dataList.sort(({ key: key1 }, { key: key2 }) => key1 - key2), [ dataList ]);
  const xAxisData = useMemo(() => sortedDataList.map(({ label }) => label), [ sortedDataList ]);

  const option = useMemo(() => ({
    xAxis: [ {
      type: 'category',
      data: xAxisData,
      name: 'Vârsta',
    } ],
    yAxis: [ {
      type: 'value',
      name: 'Număr decese',
    } ],
    tooltip: [ {
      trigger: 'axis',
      axisPointer: {
        type: 'line',
      },
    } ],
    formatter: (params) => {
      const value = deepGet(params, '0.data.value');
      const label = deepGet(params, '0.data.label');
      return (
        '<span style="color: white">' + label +
        ' ani: <br/>' + value + ' decese</span>'
      );
    },
    series: [ {
      data: sortedDataList,
      type: 'bar',
    } ],
    visualMap: [ {
      show: false,
      max: maxGroupValue,
      inRange: {
        colorLightness: [ 0.6, 0.1 ],
      },
    } ],
  }), [ xAxisData, sortedDataList, maxGroupValue]);


  const metadataList = useMemo(() => [
    { label: 'Vârsta minimă', value: minValue.toFixed(2) },
    { label: 'Vârsta maximă', value: maxValue.toFixed(2) },
    { label: 'Vârsta medie', value: averageValue.toFixed(2) },
    { label: 'Numărul cazurilor analizate', value: sampleSize },
    { label: 'Ultima actualizare', value: moment(dateModified).format('DD-MM-YYYY') },
  ], [ minValue, maxValue, sampleSize, dateModified, averageValue ]);

  return <ChartWrapper title={ title } loading={ loading } metadataList={ metadataList }>
    <ReactEcharts
      option={ option }
      style={ { height, width: '100%' } }
      opts={ { renderer: 'svg' } }
    />
  </ChartWrapper>;
};


export default AgeBarChart;
