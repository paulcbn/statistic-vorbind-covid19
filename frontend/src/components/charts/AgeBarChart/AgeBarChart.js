import ReactEcharts from 'echarts-for-react';
import React, { useMemo } from 'react';


const AgeBarChart = () => {
  const option = useMemo(() => ({
    xAxis: {
      type: 'category',
      data: [ '0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '90-100' ],
      name: 'Varsta',
    },
    yAxis: {
      type: 'value',
    },
    series: [ {
      data: [ 120, 200, 150, 80, 70, 110, 130 ],
      type: 'bar',
    } ],
    visualMap: {
      show: false,
      min: 10,
      max: 200,
      inRange: {
        colorLightness: [ 0.8, 0.2 ],
      },
    },
  }), []);

  return <ReactEcharts option={ option } style={ { height: 500, width: '100%' } }/>;
};


export default AgeBarChart;
