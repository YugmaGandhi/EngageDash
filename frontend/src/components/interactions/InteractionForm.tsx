"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { datetimeLocalToISO, toDatetimeLocalValue } from "@/lib/datetime";
import type { CustomerListItem, InteractionCreateInput, InteractionType } from "@/types";

const TYPES: InteractionType[] = ["meeting", "call", "email", "note"];

interface Props {
  customers: CustomerListItem[];
  // When set, the customer is locked (e.g. logging from a customer's page).
  fixedCustomerId?: number;
  initial?: {
    customer_id?: number;
    type?: InteractionType;
    title?: string;
    notes?: string;
    occurred_at?: string;
  };
  submitting: boolean;
  submitLabel: string;
  onSubmit: (values: InteractionCreateInput) => void;
}

export function InteractionForm({
  customers,
  fixedCustomerId,
  initial,
  submitting,
  submitLabel,
  onSubmit,
}: Props) {
  // Stored as a string so the Select is controlled from the first render
  // ("" means nothing selected yet).
  const initialCustomerId = fixedCustomerId ?? initial?.customer_id;
  const [customerId, setCustomerId] = useState<string>(
    initialCustomerId !== undefined ? String(initialCustomerId) : "",
  );
  const [type, setType] = useState<InteractionType>(initial?.type ?? "note");
  const [title, setTitle] = useState(initial?.title ?? "");
  const [notes, setNotes] = useState(initial?.notes ?? "");
  const [occurredLocal, setOccurredLocal] = useState(toDatetimeLocalValue(initial?.occurred_at));
  const [error, setError] = useState<string | null>(null);

  const customerLocked = fixedCustomerId !== undefined || initial?.customer_id !== undefined;

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (customerId === "") {
      setError("Please choose a customer.");
      return;
    }
    if (title.trim() === "" || notes.trim() === "") {
      setError("Title and notes are required.");
      return;
    }
    setError(null);
    onSubmit({
      customer_id: Number(customerId),
      type,
      title: title.trim(),
      notes: notes.trim(),
      occurred_at: datetimeLocalToISO(occurredLocal),
    });
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="customer">Customer *</Label>
        <Select
          value={customerId}
          onValueChange={(v) => setCustomerId(v ?? "")}
          disabled={customerLocked}
        >
          <SelectTrigger id="customer">
            <SelectValue placeholder="Select a customer" />
          </SelectTrigger>
          <SelectContent>
            {customers.map((c) => (
              <SelectItem key={c.id} value={String(c.id)}>
                {c.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="type">Type</Label>
        <Select value={type} onValueChange={(v) => setType(v as InteractionType)}>
          <SelectTrigger id="type">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {TYPES.map((t) => (
              <SelectItem key={t} value={t}>
                {t}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="title">Title *</Label>
        <Input id="title" value={title} onChange={(e) => setTitle(e.target.value)} />
      </div>

      <div className="space-y-2">
        <Label htmlFor="notes">Notes *</Label>
        <Textarea
          id="notes"
          rows={6}
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="What was discussed?"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="occurred_at">Occurred at</Label>
        <Input
          id="occurred_at"
          type="datetime-local"
          value={occurredLocal}
          onChange={(e) => setOccurredLocal(e.target.value)}
        />
      </div>

      {error && <p className="text-destructive text-sm">{error}</p>}

      <Button type="submit" disabled={submitting}>
        {submitting ? "Saving..." : submitLabel}
      </Button>
    </form>
  );
}
