import ReactEcharts from 'echarts-for-react';
import React, { useMemo } from 'react';


const CountryChart = () => {
  const option = useMemo(() => ({
    series: {
      type: 'map',
      mapType: 'RO',
      emphasis: {
        label: {
          show: false,
        },
      },
      data: [
        { name: 'Buzău', value: 213 },
        { name: 'Suceava', value: 400 },
      ],

    },
    visualMap: {
      min: 800,
      max: 50000,
      text: [ 'High', 'Low' ],
      realtime: false,
      calculable: true,
      inRange: {
        color: [ 'lightskyblue', 'yellow', 'orangered' ],
      },
    },
  }), []);

  return <ReactEcharts option={ option } style={ { height: 500, width: '100%' } }/>;
};


export default CountryChart;
