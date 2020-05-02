import ReactEcharts from 'echarts-for-react';
import moment from 'moment';
import React, { useMemo } from 'react';
import { deepGet } from '../../../lib/utils';
import ChartWrapper from '../ChartWrapper/ChartWrapper';


const GENDERS = { 'M': 'Bărbați', 'F': 'Femei' };

const GenderChart = ({ data, loading, title, height }) => {
  const { dateModified, sampleSize, dataList } = useMemo(() => ({
    dateModified: deepGet(data, 'dateModified'),
    sampleSize: deepGet(data, 'content.aggregation.sampleSize'),
    dataList: deepGet(data, 'content.data', []),
  }), [ data ]);
  const chartData = useMemo(() => dataList.map(({ label, value }) => ({ name: GENDERS[label], value })), [ dataList ]);

  const option = useMemo(() => ({
    tooltip: {
      trigger: 'item',
      formatter: 'Decese {b}:<br/> {c} ({d}%)',
    },
    legend: {
      orient: 'vertical',
      bottom: 10,
      left: 10,
    },
    series: [
      {
        type: 'pie',
        data: chartData,
        label: {
          show: false,
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  }), [ chartData ]);


  const metadataList = useMemo(() => [
    { label: 'Numărul cazurilor analizate', value: sampleSize },
    { label: 'Ultima actualizare', value: moment(dateModified).format('DD-MM-YYYY') },
  ], [ sampleSize, dateModified ]);

  return <ChartWrapper title={ title } loading={ loading } metadataList={ metadataList }>
    <ReactEcharts
      option={ option }
      style={ { height, width: '100%' } }
      opts={ { renderer: 'svg' } }
    />
  </ChartWrapper>;
};


export default GenderChart;
