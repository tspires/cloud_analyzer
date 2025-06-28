import type { ApexOptions } from 'apexcharts'
import type { ApexChartType } from '@/types'

export const basicRadarChart: ApexChartType = {
  height: 350,
  type: 'radar',
  series: [
    {
      name: 'Series 1',
      data: [80, 50, 30, 40, 100, 20]
    }
  ],
  options: {
    chart: {
      height: 350,
      type: 'radar',
      toolbar: {
        show: false
      }
    },
    colors: ['#7f56da'],
    labels: ['January', 'February', 'March', 'April', 'May', 'June']
  }
}

export const polygonFillChart: ApexChartType = {
  height: 350,
  type: 'radar',
  series: [
    {
      name: 'Series 1',
      data: [20, 100, 40, 30, 50, 80, 33]
    }
  ],
  options: {
    chart: {
      height: 350,
      type: 'radar',
      toolbar: {
        show: false
      }
    },
    labels: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    plotOptions: {
      radar: {
        size: 140
      }
    },
    colors: ['#ed5565'],
    markers: {
      size: 4,
      colors: ['#fff'],
      strokeColors: ['#ed5565'],
      strokeWidth: 2
    },
    tooltip: {
      y: {
        formatter: function (val: number) {
          return val.toString()
        }
      }
    },
    yaxis: {
      tickAmount: 7,
      labels: {
        formatter: function (val: number, i): string {
          if (i % 2 === 0) {
            return val.toString()
          } else {
            return ''
          }
        }
      }
    }
  }
}

export const multipleSeriesChart: ApexOptions = {
  chart: {
    height: 350,
    type: 'radar',
    toolbar: {
      show: false
    }
  },
  stroke: {
    width: 0
  },
  fill: {
    opacity: 0.4
  },
  markers: {
    size: 0
  },
  legend: {
    offsetY: -10
  },
  colors: ['#1e84c4', '#ed5565', '#1bb394'],
  labels: ['2011', '2012', '2013', '2014', '2015', '2016']
}
