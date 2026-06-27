"use client";

import { Pencil, Plus, Trash2 } from "lucide-react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { toast } from "sonner";

import { Loading } from "@/components/common/Loading";
import { CustomerStatusBadge } from "@/components/customers/CustomerStatusBadge";
import { Button, buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { listInteractions } from "@/lib/api/interactions";
import { getErrorMessage } from "@/lib/getErrorMessage";
import { canDeleteCustomers } from "@/lib/permissions";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { deleteCustomer, fetchCustomer } from "@/store/slices/customersSlice";
import type { InteractionListItem } from "@/types";

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString();
}

export default function CustomerDetailPage() {
  const params = useParams();
  const id = Number(params.id);
  const dispatch = useAppDispatch();
  const router = useRouter();
  const customer = useAppSelector((s) => s.customers.selected);
  const role = useAppSelector((s) => s.auth.user?.role);

  const [interactions, setInteractions] = useState<InteractionListItem[]>([]);

  useEffect(() => {
    dispatch(fetchCustomer(id));
    listInteractions({ customer_id: id })
      .then(setInteractions)
      .catch((err) => toast.error(getErrorMessage(err)));
  }, [dispatch, id]);

  async function handleDelete() {
    if (!window.confirm("Delete this customer? This cannot be undone.")) return;
    try {
      await dispatch(deleteCustomer(id)).unwrap();
      toast.success("Customer deleted");
      router.push("/customers");
    } catch (err) {
      toast.error(typeof err === "string" ? err : "Could not delete customer");
    }
  }

  if (!customer || customer.id !== id) {
    return <Loading label="Loading customer..." />;
  }

  return (
    <div className="max-w-2xl space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">{customer.name}</h1>
        <div className="flex gap-2">
          <Link
            href={`/customers/${id}/edit`}
            className={buttonVariants({ variant: "outline", size: "sm" })}
          >
            <Pencil className="h-4 w-4" />
            Edit
          </Link>
          {canDeleteCustomers(role) && (
            <Button variant="ghost" size="icon" onClick={handleDelete} aria-label="Delete customer">
              <Trash2 className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            Details
            <CustomerStatusBadge status={customer.status} />
          </CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-2 gap-4 text-sm">
          <Detail label="Company" value={customer.company ?? "—"} />
          <Detail label="Email" value={customer.email ?? "—"} />
          <Detail label="Phone" value={customer.phone ?? "—"} />
          <Detail label="Health score" value={String(customer.health_score)} />
          <Detail label="Assigned CSM" value={customer.assigned_csm_name ?? "—"} />
          <Detail label="Created by" value={customer.created_by_name ?? "—"} />
          <Detail label="Created" value={formatDate(customer.created_at)} />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>Interactions</span>
            <Link
              href={`/interactions/new?customer_id=${id}`}
              className={buttonVariants({ variant: "outline", size: "sm" })}
            >
              <Plus className="h-4 w-4" />
              Log interaction
            </Link>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {interactions.length === 0 ? (
            <p className="text-muted-foreground text-sm">No interactions yet.</p>
          ) : (
            <ul className="divide-y">
              {interactions.map((it) => (
                <li key={it.id} className="flex items-center justify-between py-2">
                  <Link href={`/interactions/${it.id}`} className="hover:underline">
                    {it.title}
                  </Link>
                  <span className="text-muted-foreground text-xs">
                    {it.type} · {formatDate(it.occurred_at)}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-muted-foreground text-xs">{label}</div>
      <div>{value}</div>
    </div>
  );
}
