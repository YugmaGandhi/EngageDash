"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { toast } from "sonner";

import { CustomerForm } from "@/components/customers/CustomerForm";
import { Loading } from "@/components/common/Loading";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { fetchCustomer, updateCustomer } from "@/store/slices/customersSlice";
import type { CustomerCreateInput } from "@/types";

export default function EditCustomerPage() {
  const params = useParams();
  const id = Number(params.id);
  const dispatch = useAppDispatch();
  const router = useRouter();
  const selected = useAppSelector((s) => s.customers.selected);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    dispatch(fetchCustomer(id));
  }, [dispatch, id]);

  async function handleSubmit(values: CustomerCreateInput) {
    setSubmitting(true);
    try {
      await dispatch(updateCustomer({ id, data: values })).unwrap();
      toast.success("Customer updated");
      router.push(`/customers/${id}`);
    } catch (err) {
      toast.error(typeof err === "string" ? err : "Could not update customer");
      setSubmitting(false);
    }
  }

  // Wait until the right customer is loaded so the form starts with its values.
  if (!selected || selected.id !== id) {
    return <Loading label="Loading customer..." />;
  }

  return (
    <div className="mx-auto max-w-lg">
      <h1 className="mb-4 text-2xl font-bold">Edit customer</h1>
      <CustomerForm
        initial={selected}
        submitting={submitting}
        submitLabel="Save changes"
        onSubmit={handleSubmit}
      />
    </div>
  );
}
