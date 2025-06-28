import type { InvoiceType } from '@/views/apps/invoices/components/types';

import avatar1 from '@/assets/images/users/avatar-1.jpg';
import avatar2 from '@/assets/images/users/avatar-2.jpg';
import avatar3 from '@/assets/images/users/avatar-3.jpg';
import avatar4 from '@/assets/images/users/avatar-4.jpg';
import avatar5 from '@/assets/images/users/avatar-5.jpg';
import avatar6 from '@/assets/images/users/avatar-6.jpg';
import avatar7 from '@/assets/images/users/avatar-7.jpg';
import avatar8 from '@/assets/images/users/avatar-8.jpg';
import avatar9 from '@/assets/images/users/avatar-9.jpg';
import avatar10 from '@/assets/images/users/avatar-10.jpg';

export const invoiceList: InvoiceType[] = [
  {
    id: 'RB6985',
    customer: {
      img: avatar2,
      name: 'Sean Kemper'
    },
    createdDate: '23 April, 2024 05:09 PM',
    dueDate: '30 April, 2024',
    amount: 852.25,
    paymentStatus: 'unpaid',
    via: 'PayPal',
  },
  {
    id: 'RB1002',
    customer: {
      img: avatar3,
      name: 'Victoria Sullivan'
    },
    createdDate: '14 May, 2024 10:51 AM',
    dueDate: '25 Aug, 2024',
    amount: 953.00,
    paymentStatus: 'send',
    via: 'PayPal',
  },
  {
    id: 'RB3652',
    customer: {
      img: avatar4,
      name: 'Liam Martinez'
    },
    createdDate: '12 April, 2024 12:09 PM',
    dueDate: '28 April, 2024',
    amount: 99.00,
    paymentStatus: 'unpaid',
    via: 'Swift Transfer',
  },
  {
    id: 'RB7854',
    customer: {
      img: avatar5,
      name: 'Emma Johnson'
    },
    createdDate: '10 April, 2024 10:09 PM',
    dueDate: '15 April, 2024',
    amount: 1250.00,
    paymentStatus: 'paid',
    via: 'PayPal',
  },
  {
    id: 'RB9521',
    customer: {
      img: avatar1,
      name: 'Olivia Thompson'
    },
    createdDate: '22 May, 2024 03:41 PM',
    dueDate: '05 July, 2024',
    amount: 500.00,
    paymentStatus: 'send',
    via: 'Payoneer',
  },
  {
    id: 'RB9634',
    customer: {
      img: avatar6,
      name: 'Noah Garcia'
    },
    createdDate: '18 May, 2024 09:09 AM',
    dueDate: '30 May, 2024',
    amount: 250.00,
    paymentStatus: 'paid',
    via: 'Bank',
  },
  {
    id: 'RB8520',
    customer: {
      img: avatar7,
      name: 'Sophia Davis'
    },
    createdDate: '05 April, 2024 08:50 AM',
    dueDate: '22 April, 2024',
    amount: 29.00,
    paymentStatus: 'paid',
    via: 'PayPal',
  },
  {
    id: 'RB3590',
    customer: {
      img: avatar8,
      name: 'Isabella Lopez'
    },
    createdDate: '15 Jun, 2024 11:09 PM',
    dueDate: '01 Aug, 2024',
    amount: 24.99,
    paymentStatus: 'send',
    via: 'Swift Transfer',
  },
  {
    id: 'RB5872',
    customer: {
      img: avatar9,
      name: 'Ava Wilson'
    },
    createdDate: '22 April, 2024 05:09 PM',
    dueDate: '30 April, 2024',
    amount: 1000.00,
    paymentStatus: 'unpaid',
    via: 'Payoneer',
  },
  {
    id: 'RB1158',
    customer: {
      img: avatar10,
      name: 'Oliver Lee'
    },
    createdDate: '23 April, 2024 12:09 PM',
    dueDate: '30 April, 2024',
    amount: 1999.00,
    paymentStatus: 'unpaid',
    via: 'Wise',
  },
];