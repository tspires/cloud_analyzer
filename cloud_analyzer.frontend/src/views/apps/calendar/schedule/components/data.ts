import type { ExternalEventType, OptionsType } from '@/views/apps/calendar/schedule/components/types';
import type { EventInput } from '@fullcalendar/core/index.js';

export const initialEvents: EventInput[] = [
  {
    id: '1',
    title: 'Interview - Backend Engineer',
    start: new Date(),
    className: 'bg-primary'
  },
  {
    id: '2',
    title: 'Meeting with CT Team',
    start: new Date(Date.now() + 13000000),
    className: 'bg-warning'
  },
  {
    id: '3',
    title: 'Meeting with Mr. Rasket',
    start: new Date(Date.now() + 308000000),
    end: new Date(Date.now() + 338000000),
    className: 'bg-info'
  },
  {
    id: '4',
    title: 'Interview - Frontend Engineer',
    start: new Date(Date.now() + 60570000),
    end: new Date(Date.now() + 153000000),
    className: 'bg-secondary'
  },
  {
    id: '5',
    title: 'Phone Screen - Frontend Engineer',
    start: new Date(Date.now() + 168000000),
    className: 'bg-success'
  },
  {
    id: '6',
    title: 'Buy Design Assets',
    start: new Date(Date.now() + 330000000),
    end: new Date(Date.now() + 330800000),
    className: 'bg-primary'
  },
  {
    id: '7',
    title: 'Setup Github Repository',
    start: new Date(Date.now() + 1008000000),
    end: new Date(Date.now() + 1108000000),
    className: 'bg-danger'
  },
  {
    id: '8',
    title: 'Meeting with Mr. Shreyu',
    start: new Date(Date.now() + 2508000000),
    end: new Date(Date.now() + 2508000000),
    className: 'bg-dark'
  }
];

// external events
export const externalEvents: ExternalEventType[] = [
  {
    id: 1,
    textClass: 'text-primary',
    className: 'primary',
    title: 'Team Building Retreat Meeting '
  },
  {
    id: 2,
    textClass: 'text-info',
    className: 'info',
    title: 'Product Launch Strategy Meeting'
  },
  {
    id: 3,
    textClass: 'text-success',
    className: 'success',
    title: 'Monthly Sales Review'
  },
  {
    id: 4,
    textClass: 'text-danger',
    className: 'danger',
    title: 'Team Lunch Celebration'
  },
  {
    id: 5,
    textClass: 'text-warning',
    className: 'warning',
    title: 'Marketing Campaign Kickoff'
  }
];

// Options
export const options: OptionsType[] = [
  { value: 'bg-primary', text: 'Blue' },
  { value: 'bg-secondary', text: 'Gray Dark' },
  { value: 'bg-success', text: 'Green' },
  { value: 'bg-info', text: 'Cyan' },
  { value: 'bg-warning', text: 'Yellow' },
  { value: 'bg-danger', text: 'Red' },
  { value: 'bg-dark', text: 'Dark' }
];
