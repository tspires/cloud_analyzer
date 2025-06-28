import type { BaseColorVariant } from "bootstrap-vue-next";

export type BrowserType = {
  name: string
  percentage: number
  amount: number
}

export type CountryType = {
  icon: string
  name: string
  value: number
  amount: number
  variant: keyof BaseColorVariant | null | undefined
}

export type PageType = {
  path: string
  views: number
  avgTime: string
  exitRate: number
  variant: string
}
