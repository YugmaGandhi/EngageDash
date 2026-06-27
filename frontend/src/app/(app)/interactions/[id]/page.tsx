"use client";

import { Pencil } from "lucide-react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect } from "react";

import { Loading } from "@/components/common/Loading";
import { InteractionInsights } from "@/components/insights/InteractionInsights";
import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatDateTime } from "@/lib/datetime";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { fetchInteraction } from "@/store/slices/interactionsSlice";

export default function InteractionDetailPage() {
  const params = useParams();
  const id = Number(params.id);
  const dispatch = useAppDispatch();
  const interaction = useAppSelector((s) => s.interactions.selected);

  useEffect(() => {
    dispatch(fetchInteraction(id));
  }, [dispatch, id]);

  if (!interaction || interaction.id !== id) {
    return <Loading label="Loading interaction..." />;
  }

  return (
    <div className="max-w-2xl space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">{interaction.title}</h1>
        <Link
          href={`/interactions/${id}/edit`}
          className={buttonVariants({ variant: "outline", size: "sm" })}
        >
          <Pencil className="h-4 w-4" />
          Edit
        </Link>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Badge variant="secondary">{interaction.type}</Badge>
            <span className="text-muted-foreground text-sm font-normal">
              {formatDateTime(interaction.occurred_at)}
            </span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <div className="text-muted-foreground text-xs">Customer</div>
            <Link href={`/customers/${interaction.customer_id}`} className="hover:underline">
              #{interaction.customer_id}
            </Link>
          </div>
          <div>
            <div className="text-muted-foreground mb-1 text-xs">Notes</div>
            <p className="whitespace-pre-wrap">{interaction.notes}</p>
          </div>
        </CardContent>
      </Card>

      <InteractionInsights interactionId={id} />
    </div>
  );
}
