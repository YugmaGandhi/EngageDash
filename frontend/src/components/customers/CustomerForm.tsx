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
import type { CustomerCreateInput, CustomerStatus } from "@/types";

const STATUSES: CustomerStatus[] = ["prospect", "active", "at_risk", "churned"];

// A very simple email check (the backend validates properly too).
function isValidEmail(value: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

interface Props {
  initial?: Partial<CustomerCreateInput>;
  submitting: boolean;
  submitLabel: string;
  onSubmit: (values: CustomerCreateInput) => void;
}

export function CustomerForm({ initial, submitting, submitLabel, onSubmit }: Props) {
  const [name, setName] = useState(initial?.name ?? "");
  const [company, setCompany] = useState(initial?.company ?? "");
  const [email, setEmail] = useState(initial?.email ?? "");
  const [phone, setPhone] = useState(initial?.phone ?? "");
  const [status, setStatus] = useState<CustomerStatus>(initial?.status ?? "prospect");
  const [healthScore, setHealthScore] = useState(String(initial?.health_score ?? 50));
  const [error, setError] = useState<string | null>(null);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (name.trim() === "") {
      setError("Name is required.");
      return;
    }
    if (email && !isValidEmail(email)) {
      setError("Please enter a valid email.");
      return;
    }
    const score = Number(healthScore);
    if (Number.isNaN(score) || score < 0 || score > 100) {
      setError("Health score must be between 0 and 100.");
      return;
    }

    setError(null);
    onSubmit({
      name: name.trim(),
      company: company || null,
      email: email || null,
      phone: phone || null,
      status,
      health_score: score,
    });
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">Name *</Label>
        <Input id="name" value={name} onChange={(e) => setName(e.target.value)} />
      </div>
      <div className="space-y-2">
        <Label htmlFor="company">Company</Label>
        <Input id="company" value={company ?? ""} onChange={(e) => setCompany(e.target.value)} />
      </div>
      <div className="space-y-2">
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          value={email ?? ""}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="phone">Phone</Label>
        <Input id="phone" value={phone ?? ""} onChange={(e) => setPhone(e.target.value)} />
      </div>
      <div className="space-y-2">
        <Label htmlFor="status">Status</Label>
        <Select value={status} onValueChange={(v) => setStatus(v as CustomerStatus)}>
          <SelectTrigger id="status">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {STATUSES.map((s) => (
              <SelectItem key={s} value={s}>
                {s}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="space-y-2">
        <Label htmlFor="health_score">Health score (0–100)</Label>
        <Input
          id="health_score"
          type="number"
          min={0}
          max={100}
          value={healthScore}
          onChange={(e) => setHealthScore(e.target.value)}
        />
      </div>

      {error && <p className="text-destructive text-sm">{error}</p>}

      <Button type="submit" disabled={submitting}>
        {submitting ? "Saving..." : submitLabel}
      </Button>
    </form>
  );
}
