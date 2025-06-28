import smallImg1 from '@/assets/images/small/img-1.jpg'
import smallImg2 from '@/assets/images/small/img-2.jpg'
import smallImg3 from '@/assets/images/small/img-3.jpg'

import avatar2 from '@/assets/images/users/avatar-2.jpg'
import avatar3 from '@/assets/images/users/avatar-3.jpg'
import avatar4 from '@/assets/images/users/avatar-4.jpg'
import avatar5 from '@/assets/images/users/avatar-5.jpg'
import avatar6 from '@/assets/images/users/avatar-6.jpg'
import avatar7 from '@/assets/images/users/avatar-7.jpg'
import avatar8 from '@/assets/images/users/avatar-8.jpg'
import avatar9 from '@/assets/images/users/avatar-9.jpg'
import avatar10 from '@/assets/images/users/avatar-10.jpg'

import type { ChatMsgType, ContactType, DropdownItemType, GroupType, UserContactType } from '@/views/apps/chat/components/types'

export const chatMsg: ChatMsgType[] = [
  {
    id: 1,
    msg: [{ text: 'Hey 😊' }],
    timeStamp: '8:20 am',
    isSender: false
  },
  {
    id: 2,
    msg: [{ text: 'Hi' }],
    timeStamp: '8:20 am',
    isSender: true,
    isRead: true
  },
  {
    id: 3,
    msg: [{ text: "Hi Gaston, thanks for joining the meeting. Let's dive into our quarterly performance review." }],
    isSender: false
  },
  {
    id: 4,
    msg: [{ text: `Hi Gilbert, thanks for having me. I'm ready to discuss how things have been going.` }],
    timeStamp: '8:25 am',
    isSender: true,
    isRead: true
  },
  {
    id: 5,
    msg: [{ img: [smallImg1, smallImg2, smallImg3] }],
    timeStamp: '8:26 am',
    isSender: false
  },
  {
    id: 6,
    msg: [{ isMedia: true, mediaContend: { title: 'financial-report-2024.zip', type: 'bxs-file-archive', size: '2.3 MB' } }, { text: 'I appreciate your honesty. Can you elaborate on some of those challenges? I want to understand how we can support you better in the future.' }],
    timeStamp: '8:27 am',
    isSender: true,
    isRead: true
  },
  {
    id: 7,
    msg: [{ text: `Thanks, Emily. I appreciate your support. Overall, I'm optimistic about our team's performance and looking forward to tackling new challenges in the next quarter.` }],
    timeStamp: '8:29 am',
    isSender: false
  }
]

export const contactList: ContactType[] = [
  {
    image: avatar2,
    name: 'Gaston Lapierre',
    lastMsg: 'How are you today?',
    timeStamp: '10:20am',
    isRead: true
  },
  {
    image: avatar3,
    name: 'Fantina LeBatelier',
    timeStamp: '11:03am',
    lastMsg: "Hey! a reminder for tomorrow's meeting...",
    isRead: true
  },
  {
    image: avatar4,
    name: 'Gilbert Chicoine',
    timeStamp: 'now',
    lastMsg: 'typing...',
    isRead: false
  },
  {
    image: avatar5,
    name: 'Mignonette Brodeur',
    timeStamp: 'Yesterday',
    lastMsg: "Are we going to have this week's planning meeting today?",
    isRead: true
  },
  {
    image: avatar6,
    name: 'Thomas Menard',
    timeStamp: 'Yesterday',
    lastMsg: 'Please check this template...',
    isRead: true
  },
  {
    name: 'Melisande Lapointe',
    timeStamp: 'Yesterday',
    lastMsg: 'Are free for 10 minutes? would like to discuss something...',
    image: avatar7,
    isRead: true
  },
  {
    image: avatar8,
    name: 'Danielle Despins',
    timeStamp: '7/8/21',
    lastMsg: 'How are you?',
    isRead: true
  },
  {
    image: avatar9,
    name: 'Onfroi Pichette',
    timeStamp: '7/8/21',
    lastMsg: 'whats going on?',
    isRead: true
  },
  {
    image: avatar10,
    name: 'Kari Boisvert',
    timeStamp: '7/8/21',
    lastMsg: 'Would you like to join us?',
    isRead: false
  }
]

export const groupList: GroupType[] = [
  {
    name: 'General'
  },
  {
    name: 'Company',
    badge: 33
  },
  {
    name: 'Life Suckers',
    badge: 17
  },
  {
    name: 'Drama Club'
  },
  {
    name: 'Unknown Friends'
  },
  {
    name: 'Family Ties',
    badge: 65
  },
  {
    name: '2Good4U'
  }
]

export const userContact: UserContactType[] = [
  {
    name: 'Gaston Lapierre',
    avatar: avatar2,
    status: ''
  },
  {
    name: 'Fantina LeBatelier',
    avatar: avatar3,
    status: '** no status **'
  },
  {
    name: 'Gilbert Chicoine',
    avatar: avatar4,
    status: '|| Karma ||'
  },
  {
    name: 'Mignonette Brodeur',
    avatar: avatar5,
    status: 'Hey there! I am using Chat.'
  },
  {
    name: 'Thomas Menard',
    avatar: avatar6,
    status: 'TM'
  },
  {
    name: 'Melisande Lapointe',
    avatar: avatar7,
    status: 'Available'
  },
  {
    name: 'Danielle Despins',
    avatar: avatar8,
    status: 'Hey there! I am using Chat.'
  }
]

export const dropdownItem: DropdownItemType[] = [
  { icon: 'bx-share', title: 'Reply' },
  { icon: 'bx-share-alt', title: 'Forward' },
  { icon: 'bx-copy', title: 'Copy' },
  { icon: 'bx-bookmark', title: 'Bookmark' },
  { icon: 'bx-star', title: 'Starred' },
  { icon: 'bx-info-square', title: 'Mark as Unread' },
  { icon: 'bx-trash', title: 'Delete' }
]
