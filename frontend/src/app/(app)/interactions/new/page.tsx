"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";
import { toast } from "sonner";

import { Loading } from "@/components/common/Loading";
import { InteractionForm } from "@/components/interactions/InteractionForm";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { fetchCustomers } from "@/store/slices/customersSlice";
import { createInteraction } from "@/store/slices/interactionsSlice";
import type { InteractionCreateInput } from "@/types";

// useSearchParams must be inside a Suspense boundary.
export default function NewInteractionPage() {
  return (
    <Suspense fallback={<Loading />}>
      <NewInteractionInner />
    </Suspense>
  );
}

function NewInteractionInner() {
  const dispatch = useAppDispatch();
  const router = useRouter();
  const searchParams = useSearchParams();
  const customers = useAppSelector((s) => s.customers.items);
  const [submitting, setSubmitting] = useState(false);

  // Load customers for the picker.
  useEffect(() => {
    dispatch(fetchCustomers(undefined));
  }, [dispatch]);

  // If we arrived from a customer's page, lock to that customer.
  const customerIdParam = searchParams.get("customer_id");
  const fixedCustomerId = customerIdParam ? Number(customerIdParam) : undefined;

  async function handleSubmit(values: InteractionCreateInput) {
    setSubmitting(true);
    try {
      const interaction = await dispatch(createInteraction(values)).unwrap();
      toast.success("Interaction logged");
      router.push(`/interactions/${interaction.id}`);
    } catch (err) {
      toast.error(typeof err === "string" ? err : "Could not log interaction");
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-lg">
      <h1 className="mb-4 text-2xl font-bold">Log interaction</h1>
      <InteractionForm
        customers={customers}
        fixedCustomerId={fixedCustomerId}
        submitting={submitting}
        submitLabel="Save interaction"
        onSubmit={handleSubmit}
      />
    </div>
  );
}
