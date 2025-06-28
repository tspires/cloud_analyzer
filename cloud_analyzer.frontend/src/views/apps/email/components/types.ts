export type EmailType = {
  id: string
  sender: string
  subject: string
  message: string
  date: string
  status: string
  isStarred: boolean
  isImportant: boolean
  isSent: boolean
  isTrash: boolean
  attachType?: string
  attachments?: string[]
  badge?: string
  type: string
  isRead: boolean
  categories: string[]
}

export type NavLinkType = {
  title: string
  link?: string
  category?: string
  badge?: string
  badgeVariant?: string
  icon?: string
  variant?: string
  isLabel?: boolean
  isTitle?: boolean
}
