type Customer = {
  img: string;
  name: string;
};

export type InvoiceType = {
  id: string;
  customer: Customer;
  createdDate: string;
  dueDate: string;
  amount: number;
  paymentStatus: string;
  via: string;
};