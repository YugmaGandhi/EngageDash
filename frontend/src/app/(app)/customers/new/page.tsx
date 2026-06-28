"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { toast } from "sonner";

import { CustomerForm } from "@/components/customers/CustomerForm";
import { useAppDispatch } from "@/store/hooks";
import { createCustomer } from "@/store/slices/customersSlice";
import type { CustomerCreateInput } from "@/types";

export default function NewCustomerPage() {
  const dispatch = useAppDispatch();
  const router = useRouter();
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(values: CustomerCreateInput) {
    setSubmitting(true);
    try {
      const customer = await dispatch(createCustomer(values)).unwrap();
      toast.success("Customer created");
      router.push(`/customers/${customer.id}`);
    } catch (err) {
      toast.error(typeof err === "string" ? err : "Could not create customer");
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-lg">
      <h1 className="mb-4 text-2xl font-bold">New customer</h1>
      <CustomerForm submitting={submitting} submitLabel="Create customer" onSubmit={handleSubmit} />
    </div>
  );
}
