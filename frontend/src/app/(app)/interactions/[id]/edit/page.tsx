"use client";

import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { toast } from "sonner";

import { Loading } from "@/components/common/Loading";
import { InteractionForm } from "@/components/interactions/InteractionForm";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { fetchCustomers } from "@/store/slices/customersSlice";
import { fetchInteraction, updateInteraction } from "@/store/slices/interactionsSlice";
import type { InteractionCreateInput } from "@/types";

export default function EditInteractionPage() {
  const params = useParams();
  const id = Number(params.id);
  const dispatch = useAppDispatch();
  const router = useRouter();
  const interaction = useAppSelector((s) => s.interactions.selected);
  const customers = useAppSelector((s) => s.customers.items);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    dispatch(fetchInteraction(id));
    dispatch(fetchCustomers(undefined));
  }, [dispatch, id]);

  async function handleSubmit(values: InteractionCreateInput) {
    setSubmitting(true);
    try {
      await dispatch(updateInteraction({ id, data: values })).unwrap();
      toast.success("Interaction updated");
      router.push(`/interactions/${id}`);
    } catch (err) {
      toast.error(typeof err === "string" ? err : "Could not update interaction");
      setSubmitting(false);
    }
  }

  if (!interaction || interaction.id !== id) {
    return <Loading label="Loading interaction..." />;
  }

  return (
    <div className="mx-auto max-w-lg">
      <h1 className="mb-4 text-2xl font-bold">Edit interaction</h1>
      <InteractionForm
        customers={customers}
        initial={interaction}
        submitting={submitting}
        submitLabel="Save changes"
        onSubmit={handleSubmit}
      />
    </div>
  );
}
