export type UserType = {
  name: string
  avatar: string
}

export type TodoType = {
  id: number
  taskName: string
  createDate: string
  time: string
  dueDate: string
  assigned: UserType
  status: 'in-progress'| 'pending'| 'completed'| 'new'
  priority: 'high'| 'medium'| 'low'
  checked: boolean
}
