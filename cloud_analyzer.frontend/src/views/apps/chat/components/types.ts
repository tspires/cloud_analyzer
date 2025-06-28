type MediaContendType = {
  title: string
  type: string
  size: string
}

type MessageType = {
  text?: string
  img?: string[]
  isMedia?: boolean
  mediaContend?: MediaContendType
}

export type ChatMsgType = {
  id: number
  msg: MessageType[]
  timeStamp?: string
  isSender: boolean
  isRead?: boolean
}

export type ContactType = {
  image: string
  name: string
  lastMsg: string
  timeStamp: string
  isRead: boolean
}

export type GroupType = {
  name: string
  badge?: number
}

export type UserContactType = {
  name: string
  avatar: string
  status: string
}

export type DropdownItemType = {
  icon: string
  title: string
}
