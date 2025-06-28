import type { BaseColorVariant } from 'bootstrap-vue-next'

type TableHeaderType = string[]

export type RecentProjectsSummaryTableType = {
  header: TableHeaderType
  body: {
    project: string
    client: string
    team: { avatar: string }[]
    deadline: string
    progress: { data: number; variant: keyof BaseColorVariant | null | undefined }
  }[]
}

export type ScheduleType = {
  task: string
  time: { startAt: string; endAt: string }
  variant: keyof BaseColorVariant | null | undefined
}

export type FriendRequestType = {
  avatar: string
  name: string
  mutualFriends: number
}

export type RecentTransactionType = {
  date: string
  amount: string
  status: 'cr' | 'dr'
  description: string
}
