"use client";

import { Plus } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

import { ErrorState } from "@/components/common/ErrorState";
import { Loading } from "@/components/common/Loading";
import { buttonVariants } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { formatDateTime } from "@/lib/datetime";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { fetchInteractions } from "@/store/slices/interactionsSlice";
import type { InteractionType } from "@/types";

const TYPE_OPTIONS: { value: InteractionType | "all"; label: string }[] = [
  { value: "all", label: "All types" },
  { value: "meeting", label: "Meeting" },
  { value: "call", label: "Call" },
  { value: "email", label: "Email" },
  { value: "note", label: "Note" },
];

export default function InteractionsPage() {
  const dispatch = useAppDispatch();
  const { items, status, error } = useAppSelector((s) => s.interactions);
  const [typeFilter, setTypeFilter] = useState<InteractionType | "all">("all");

  useEffect(() => {
    dispatch(fetchInteractions({ type: typeFilter === "all" ? undefined : typeFilter }));
  }, [dispatch, typeFilter]);

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Interactions</h1>
        <Link href="/interactions/new" className={buttonVariants()}>
          <Plus className="h-4 w-4" />
          Log interaction
        </Link>
      </div>

      <div className="mb-4">
        <Select
          value={typeFilter}
          onValueChange={(v) => setTypeFilter(v as InteractionType | "all")}
        >
          <SelectTrigger className="sm:w-48">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {TYPE_OPTIONS.map((o) => (
              <SelectItem key={o.value} value={o.value}>
                {o.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {status === "loading" && items.length === 0 ? (
        <Loading label="Loading interactions..." />
      ) : error ? (
        <ErrorState message={error} />
      ) : items.length === 0 ? (
        <p className="text-muted-foreground py-10 text-center">No interactions found.</p>
      ) : (
        <div className="overflow-x-auto rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Title</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Customer</TableHead>
                <TableHead>When</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {items.map((it) => (
                <TableRow key={it.id}>
                  <TableCell className="font-medium">
                    <Link href={`/interactions/${it.id}`} className="hover:underline">
                      {it.title}
                    </Link>
                  </TableCell>
                  <TableCell>{it.type}</TableCell>
                  <TableCell>
                    <Link href={`/customers/${it.customer_id}`} className="hover:underline">
                      #{it.customer_id}
                    </Link>
                  </TableCell>
                  <TableCell>{formatDateTime(it.occurred_at)}</TableCell>
                  <TableCell className="text-right">
                    <Link
                      href={`/interactions/${it.id}`}
                      className={buttonVariants({ variant: "outline", size: "sm" })}
                    >
                      View
                    </Link>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
}
