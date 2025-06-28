import type { RouteParamsRaw } from 'vue-router';
import type { ApexOptions } from "apexcharts";

export type RouteType = {
    name: string;
    params?: RouteParamsRaw;
    url?: string;
};

export type StatisticType = {
    title: string;
    description?: string;
    statistic: number;
    growth?: number;
    prefix?: string;
    suffix?: string;
    duration?: 'week' | 'month' | 'year';
};

export type StatisticCardType = {
    icon: string;
    variant?: string;
    background?: {
        color?: string;
        icon?: string;
        image?: string;
    };
} & StatisticType;


export type ApexChartType = {
    height: number;
    type?: string;
    series: any[];
    options: ApexOptions;
};