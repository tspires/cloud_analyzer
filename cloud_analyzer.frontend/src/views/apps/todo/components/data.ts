import type { TodoType } from '@/views/apps/todo/components/types'

import avatar1 from '@/assets/images/users/avatar-1.jpg'
import avatar2 from '@/assets/images/users/avatar-2.jpg'
import avatar3 from '@/assets/images/users/avatar-3.jpg'
import avatar4 from '@/assets/images/users/avatar-4.jpg'
import avatar5 from '@/assets/images/users/avatar-5.jpg'
import avatar6 from '@/assets/images/users/avatar-6.jpg'
import avatar7 from '@/assets/images/users/avatar-7.jpg'
import avatar8 from '@/assets/images/users/avatar-8.jpg'
import avatar9 from '@/assets/images/users/avatar-9.jpg'
import avatar10 from '@/assets/images/users/avatar-10.jpg'

export const todosData: TodoType[] = [
  {
    id: 1,
    taskName: 'Review system logs for any reported errors',
    createDate: '23 April, 2024',
    time: '05:09 PM',
    dueDate: '30 April, 2024',
    assigned: {
      name: 'Sean Kemper',
      avatar: avatar2
    },
    status: 'in-progress',
    priority: 'high',
    checked: false
  },
  {
    id: 2,
    taskName: 'Conduct user testing to identify potential bugs',
    createDate: '14 May, 2024',
    time: '10:51 AM',
    dueDate: '25 Aug, 2024',
    assigned: {
      name: 'Victoria Sullivan',
      avatar: avatar3
    },
    status: 'pending',
    priority: 'low',
    checked: true
  },
  {
    id: 3,
    taskName: 'Gather feedback from stakeholders regarding any issues',
    createDate: '12 April, 2024',
    time: '12:09 PM',
    dueDate: '28 April, 2024',
    assigned: {
      name: 'Liam Martinez',
      avatar: avatar4
    },
    status: 'in-progress',
    priority: 'high',
    checked: false
  },
  {
    id: 4,
    taskName: 'Prioritize bugs based on severity and impact',
    createDate: '10 April, 2024',
    time: '10:09 PM',
    dueDate: '15 April, 2024',
    assigned: {
      name: 'Emma Johnson',
      avatar: avatar5
    },
    status: 'completed',
    priority: 'medium',
    checked: false
  },
  {
    id: 5,
    taskName: 'Investigate and analyze the root cause of each bug',
    createDate: '22 May, 2024',
    time: '03:41 PM',
    dueDate: '05 July, 2024',
    assigned: {
      name: 'Olivia Thompson',
      avatar: avatar1
    },
    status: 'pending',
    priority: 'low',
    checked: false
  },
  {
    id: 6,
    taskName: 'Develop and implement fixes for the identified bugs',
    createDate: '18 May, 2024',
    time: '09:09 AM',
    dueDate: '30 April, 2024',
    assigned: {
      name: 'Noah Garcia',
      avatar: avatar6
    },
    status: 'completed',
    priority: 'low',
    checked: false
  },
  {
    id: 7,
    taskName: 'Complete any recurring tasks',
    createDate: '05 April, 2024',
    time: '08:50 AM',
    dueDate: '22 April, 2024',
    assigned: {
      name: 'Sophia Davis',
      avatar: avatar7
    },
    status: 'new',
    priority: 'high',
    checked: false
  },
  {
    id: 8,
    taskName: 'Check emails and respond',
    createDate: '15 Jun, 2024',
    time: '11:09 PM',
    dueDate: '01 Aug, 2024',
    assigned: {
      name: 'Isabella Lopez',
      avatar: avatar8
    },
    status: 'pending',
    priority: 'low',
    checked: false
  },
  {
    id: 9,
    taskName: 'Review schedule for the day',
    createDate: '22 April, 2024',
    time: '05:09 PM',
    dueDate: '30 April, 2024',
    assigned: {
      name: 'Ava Wilson',
      avatar: avatar9
    },
    status: 'in-progress',
    priority: 'medium',
    checked: true
  },
  {
    id: 10,
    taskName: 'Daily stand-up meeting',
    createDate: '23 April, 2024',
    time: '12:09 PM',
    dueDate: '30 April, 2024',
    assigned: {
      name: 'Oliver Lee',
      avatar: avatar10
    },
    status: 'in-progress',
    priority: 'high',
    checked: false
  }
]
