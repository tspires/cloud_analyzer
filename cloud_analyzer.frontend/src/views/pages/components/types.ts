export type ButtonType = {
  text: string;
  disabled: boolean;
};
export type PlanType = {
  name: string;
  price: number;
  period: string;
  ribbon?: string;
  features: string[];
  button: ButtonType;
};

export type HelpType = {
  title: string;
  description: string;
  icon: string;
  author: string;
  videoCount: number;
  image: string;
};

export type FAQType = {
  question: string;
  answer: string;
};

export type EventType = {
  side?: string;
  title: string;
  badge?: string;
  description: string;
};
export type TimelineType = {
  date: string;
  events: EventType[];
};
