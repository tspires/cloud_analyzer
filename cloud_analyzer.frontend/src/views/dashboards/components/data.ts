import { currency } from "@/helpers/constants";
import type { ApexChartType, StatisticCardType } from "@/types";
import type { BrowserType, CountryType, PageType } from "./types";

export const statistic: StatisticCardType[] = [
  {
    title: 'Page View',
    icon: 'solar:leaf-bold-duotone',
    statistic: 13647,
    growth: 2.3,
    variant: 'success',
  },
  {
    title: 'Clicks',
    icon: 'solar:cpu-bolt-line-duotone',
    statistic: 9526,
    growth: 8.1,
    variant: 'success',
  },
  {
    title: 'Conversions',
    icon: 'solar:layers-bold-duotone',
    statistic: 976,
    growth: -0.3,
    variant: 'danger',
  },
  {
    title: 'New Users',
    icon: 'solar:users-group-two-rounded-bold-duotone',
    statistic: 123.6,
    prefix: currency,
    suffix: 'k',
    growth: -10.6,
    variant: 'danger',
  },
];

export const sessionBrowser: BrowserType[] = [
  {
    name: 'Chrome',
    percentage: 62.5,
    amount: 5.06,
  },
  {
    name: 'Firefox',
    percentage: 12.3,
    amount: 1.5,
  },
  {
    name: 'Safari',
    percentage: 9.86,
    amount: 1.03,
  },
  {
    name: 'Brave',
    percentage: 3.15,
    amount: 0.3,
  },
  {
    name: 'Opera',
    percentage: 3.01,
    amount: 1.58,
  },
  {
    name: 'Falkon',
    percentage: 2.8,
    amount: 0.01,
  },
  {
    name: 'Web',
    percentage: 1.05,
    amount: 2.51,
  },
  {
    name: 'Other',
    percentage: 6.38,
    amount: 3.6,
  }
]

export const countries: CountryType[] = [
  {
    icon: 'circle-flags:us',
    name: 'United States',
    value: 82.5,
    amount: 659,
    variant: 'secondary',
  },
  {
    icon: 'circle-flags:ru',
    name: 'Russia',
    value: 70.5,
    amount: 485,
    variant: 'info',
  },
  {
    icon: 'circle-flags:cn',
    name: 'China',
    value: 65.8,
    amount: 355,
    variant: 'warning',
  },
  {
    icon: 'circle-flags:ca',
    name: 'Canada',
    value: 55.8,
    amount: 204,
    variant: 'success',
  },
]

export const topPages: PageType[] = [
  {
    path: 'rasket/dashboard.html',
    views: 4265,
    avgTime: '09m:45s',
    exitRate: 20.4,
    variant: 'danger',
  },
  {
    path: 'rasket/chat.html',
    views: 2584,
    avgTime: '05m:02s',
    exitRate: 12.25,
    variant: 'warning',
  },
  {
    path: 'rasket/auth-login.html',
    views: 3369,
    avgTime: '04m:25s',
    exitRate: 5.2,
    variant: 'success',
  },
  {
    path: 'rasket/email.html',
    views: 985,
    avgTime: '02m:03s',
    exitRate: 64.2,
    variant: 'danger',
  },
  {
    path: 'rasket/social.html',
    views: 653,
    avgTime: '15m:56s',
    exitRate: 2.4,
    variant: 'success',
  },
]

export const performanceChart: ApexChartType = {
  height: 297,
  type: "line",
  series: [
      {
          name: "Page Views",
          type: "bar",
          data: [34, 65, 46, 68, 49, 61, 42, 44, 78, 52, 63, 67],
      },
      {
          name: "Clicks",
          type: "area",
          data: [8, 12, 7, 17, 21, 11, 5, 9, 7, 29, 12, 35],
      },
  ],
  options: {
      chart: {
          height: 313,
          type: "line",
          toolbar: {
              show: false,
          },
      },
      stroke: {
          dashArray: [0, 0],
          width: [0, 2],
          curve: 'smooth'
      },
      fill: {
          opacity: [1, 1],
          type: ['solid', 'gradient'],
          gradient: {
              type: "vertical",
              inverseColors: false,
              opacityFrom: 0.5,
              opacityTo: 0,
              stops: [0, 90]
          },
      },
      markers: {
          size: [0, 0],
          strokeWidth: 2,
          hover: {
              size: 4,
          },
      },
      xaxis: {
          categories: [
              "Jan",
              "Feb",
              "Mar",
              "Apr",
              "May",
              "Jun",
              "Jul",
              "Aug",
              "Sep",
              "Oct",
              "Nov",
              "Dec",
          ],
          axisTicks: {
              show: false,
          },
          axisBorder: {
              show: false,
          },
      },
      yaxis: {
          min: 0,
          axisBorder: {
              show: false,
          }
      },
      grid: {
          show: true,
          strokeDashArray: 3,
          xaxis: {
              lines: {
                  show: false,
              },
          },
          yaxis: {
              lines: {
                  show: true,
              },
          },
          padding: {
              top: 0,
              right: -2,
              bottom: 0,
              left: 10,
          },
      },
      legend: {
          show: true,
          horizontalAlign: "center",
          offsetX: 0,
          offsetY: 5,
          markers: {},
          itemMargin: {
              horizontal: 10,
              vertical: 0,
          },
      },
      plotOptions: {
          bar: {
              columnWidth: "30%",
              barHeight: "70%",
              borderRadius: 3,
          },
      },
      colors: ["#1bb394", "#1e84c4"],
      tooltip: {
          shared: true,
          y: [{
              formatter: function (y: number) {
                  if (typeof y !== "undefined") {
                      return y.toFixed(1) + "k";
                  }
                  return y;
              },
          },
          {
              formatter: function (y: number) {
                  if (typeof y !== "undefined") {
                      return y.toFixed(1) + "k";
                  }
                  return y;
              },
          },
          ],
      },
  }
};

export const conversionsChart: ApexChartType = {
  height: 292,
  type: 'radialBar',
  series: [65.2],
  options: {
      chart: {
          height: 292,
          type: 'radialBar',
      },
      plotOptions: {
          radialBar: {
              startAngle: -135,
              endAngle: 135,
              dataLabels: {
                  name: {
                      fontSize: '14px',
                      color: "undefined",
                      offsetY: 100
                  },
                  value: {
                      offsetY: 55,
                      fontSize: '20px',
                      color: undefined,
                      formatter: function (val) {
                          return val + "%";
                      }
                  }
              },
              track: {
                  background: "rgba(170,184,197, 0.2)",
                  margin: 0
              },
          }
      },
      fill: {
          gradient: {
              // enabled: true,
              shade: 'dark',
              shadeIntensity: 0.2,
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 50, 65, 91]
          },
      },
      stroke: {
          dashArray: 4
      },
      colors: ["#1bb394", "#1bb394"],
      labels: ['Returning Customer'],
      responsive: [{
          breakpoint: 380,
          options: {
              chart: {
                  height: 180
              }
          }
      }],
      grid: {
          padding: {
              top: 0,
              right: 0,
              bottom: 0,
              left: 0
          }
      }
  }
};