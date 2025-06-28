import type { PlanType, FAQType, HelpType, TimelineType } from '@/views/pages/components/types';

import avatar1 from "@/assets/images/users/avatar-1.jpg";
import avatar2 from "@/assets/images/users/avatar-2.jpg";
import avatar3 from "@/assets/images/users/avatar-3.jpg";
import avatar4 from "@/assets/images/users/avatar-4.jpg";
import avatar5 from "@/assets/images/users/avatar-5.jpg";
import avatar6 from "@/assets/images/users/avatar-6.jpg";
import avatar7 from "@/assets/images/users/avatar-7.jpg";
import avatar8 from "@/assets/images/users/avatar-8.jpg";
import avatar9 from "@/assets/images/users/avatar-9.jpg";

export const pricingPlans: PlanType[] = [
  {
    name: 'Free Pack',
    price: 0,
    period: 'Month',
    features: ['5 GB Storage', '100 GB Bandwidth', '1 Domain', 'No Support', '24x7 Support', '1 User'],
    button: {
      text: 'Get Started',
      disabled: false
    }
  },
  {
    name: 'Professional Pack',
    price: 19,
    period: 'Month',
    ribbon: 'Popular',
    features: ['50 GB Storage', '900 GB Bandwidth', '2 Domains', 'Email Support', '24x7 Support', '5 Users'],
    button: {
      text: 'Current Plan',
      disabled: true
    }
  },
  {
    name: 'Business Pack',
    price: 29,
    period: 'Month',
    features: ['500 GB Storage', '2.5 TB Bandwidth', '5 Domains', 'Email Support', '24x7 Support', '10 Users'],
    button: {
      text: 'Get Started',
      disabled: false
    }
  },
  {
    name: 'Enterprise Pack',
    price: 49,
    period: 'Month',
    features: ['2 TB Storage', 'Unlimited Bandwidth', '50 Domains', 'Email Support', '24x7 Support', 'Unlimited Users'],
    button: {
      text: 'Get Started',
      disabled: false
    }
  }
];

export const helpCenter: HelpType[] = [
  {
    title: "Getting Started with Rasket",
    description: "Welcome to Rasket Dive into basic for a swift on boarding experience",
    icon: "solar:round-arrow-right-bold",
    author: "Aston Martin",
    videoCount: 19,
    image: avatar1
  },
  {
    title: "Admin Settings",
    description: "Learn how to manage your current workspace or your enterprise space",
    icon: "solar:user-circle-bold",
    author: "Michael A. Miner",
    videoCount: 10,
    image: avatar2
  },
  {
    title: "Server Setup",
    description: "Connect, simplify, and automate. Discover the power of apps and tools.",
    icon: "solar:display-bold",
    author: "Theresa T. Brose",
    videoCount: 7,
    image: avatar3
  },
  {
    title: "Login And Verification",
    description: "Read on to learn how to sign in with your email address, or your Apple or Google.",
    icon: "solar:login-3-bold",
    author: "James L. Erickson",
    videoCount: 3,
    image: avatar4
  },
  {
    title: "Account Setup",
    description: "Adjust your profile and preferences to make ChatCloud work just for you",
    icon: "solar:shield-user-bold",
    author: "Lily Wilson",
    videoCount: 11,
    image: avatar5
  },
  {
    title: "Trust & Safety",
    description: "Trust on our current database and learn how we distribute your data.",
    icon: "solar:hand-shake-bold",
    author: "Sarah Brooks",
    videoCount: 9,
    image: avatar6
  },
  {
    title: "Channel Setup",
    description: "From channels to search, learn how ChatCloud works from top to bottom.",
    icon: "solar:settings-bold",
    author: "Joe K. Hall",
    videoCount: 14,
    image: avatar7
  },
  {
    title: "Permissions",
    description: "Permission for you and others to join and work within a workspace",
    icon: "solar:lock-keyhole-minimalistic-bold",
    author: "Robert Leavitt",
    videoCount: 17,
    image: avatar8
  },
  {
    title: "Billing Help",
    description: "That feel when you look at your bank account and billing works.",
    icon: "solar:lock-keyhole-minimalistic-bold",
    author: "Lydia Anderson",
    videoCount: 12,
    image: avatar9
  }
];

export const generalFAQs: FAQType[] = [
  {
    question: 'Can I use Dummy FAQs for my website or project?',
    answer: 'Yes, you can use Dummy FAQs to populate your website or project during development or testing phases. They help simulate the appearance and functionality of a real FAQ section without requiring actual content.',
  },
  {
    question: 'Are Dummy FAQs suitable for customer support purposes?',
    answer: 'While Dummy FAQs can be used internally for training customer support teams, they are not suitable for public-facing customer support. Real FAQs should be based on genuine customer inquiries to provide accurate and helpful information.',
  },
  {
    question: 'Do Dummy FAQs require attribution?',
    answer: 'No, Dummy FAQs do not require attribution since they are not based on real questions or contributed by individuals. You can use them freely for internal testing or demonstration purposes.',
  },
];

export const paymentsFAQs: FAQType[] = [
  {
    question: 'Can I test my website/app with Dummy Payments?',
    answer: 'Yes, Dummy Payments are commonly used by developers and businesses to test the functionality of e-commerce platforms, mobile apps, and payment gateways. They help identify and resolve issues without risking real transactions.',
  },
  {
    question: 'Are Dummy Payments secure?',
    answer: `Dummy Payments used in controlled environments for training or demonstration purposes are generally secure. However, it's crucial not to confuse them with real transactions and avoid entering genuine financial information.`,
  },
  {
    question: 'How can I differentiate between a Dummy Payment and a real one?',
    answer: 'Real payments involve the transfer of actual funds, resulting in a change in financial balances. Dummy Payments, on the other hand, do not involve any monetary exchange and are typically labeled or indicated as test transactions. Always verify the authenticity of transactions before proceeding with any action.',
  },
];

export const refundsFAQs: FAQType[] = [
  {
    question: 'How do I request a refund?',
    answer: 'To request a refund, simply contact our customer support team through email or phone and provide details about your purchase and reason for the refund. Our representatives will guide you through the process.',
  },
  {
    question: 'What is the refund policy?',
    answer: "Our refund policy allows customers to request a refund within 30 days of purchase for eligible products or services. Certain restrictions may apply, so it's essential to review the terms and conditions specific to your purchase.",
  },
  {
    question: 'How long does it take to process a refund?',
    answer: 'Refunds are typically processed within 3-5 business days after the request is approved. However, it may take longer depending on the payment method and financial institution involved.',
  }
];

export const supportFAQs: FAQType[] = [
  {
    question: 'How do I contact customer support?',
    answer: 'You can contact our customer support team via email, phone, or live chat. Our representatives are available to assist you during business hours, Monday through Friday.',
  },
  {
    question: 'Is customer support available 24/7?',
    answer: "Our customer support is available during regular business hours, Monday through Friday. However, you can leave us a message outside of these hours, and we'll respond to you as soon as possible.",
  },
  {
    question: 'How long does it take to receive a response from customer support?',
    answer: 'We strive to respond to all customer inquiries within 24 hours during regular business hours. Response times may vary depending on the volume of inquiries received.',
  },
];

export const timelineData: TimelineType[] = [
  {
    date: 'Today',
    events: [
      {
        side: 'left',
        title: 'Completed UX design project for our client',
        badge: 'important',
        description: 'Dolorum provident rerum aut hic quasi placeat iure tempora laudantium ipsa ad debitis unde?'
      },
      {
        side: 'right',
        title: 'Yes! We are celebrating our first admin release.',
        description: 'Consectetur adipisicing elit. Iusto, optio, dolorum John deon provident.'
      },
      {
        side: 'left',
        title: 'We released new version of our theme Rasket.',
        description: '3 new photo Uploaded on facebook fan page'
      }
    ]
  },
  {
    date: 'Yesterday',
    events: [
      {
        side: 'right',
        title: 'We have archieved 25k sales in our themes',
        description: 'Dolorum provident rerum aut hic quasi placeat iure tempora laudantium ipsa ad debitis unde?'
      },
      {
        side: 'left',
        title: 'Yes! We are celebrating our first admin release.',
        description: 'Outdoor visit at California State Route 85 with John Boltana & Harry Piterson.'
      }
    ]
  }
];