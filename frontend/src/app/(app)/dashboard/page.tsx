"use client";

import Link from "next/link";
import { useEffect } from "react";

import { ErrorState } from "@/components/common/ErrorState";
import { Loading } from "@/components/common/Loading";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatDateTime } from "@/lib/datetime";
import { cn } from "@/lib/utils";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { fetchDashboard } from "@/store/slices/dashboardSlice";

export default function DashboardPage() {
  const dispatch = useAppDispatch();
  const { data, status, error } = useAppSelector((s) => s.dashboard);

  useEffect(() => {
    dispatch(fetchDashboard());
  }, [dispatch]);

  if (status === "loading" || (status === "idle" && !data)) {
    return <Loading label="Loading dashboard..." />;
  }
  if (error) return <ErrorState message={error} />;
  if (!data) return null;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      {/* KPI cards */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <Kpi label="Customers" value={data.total_customers} />
        <Kpi label="At risk" value={data.at_risk_customers} />
        <Kpi label="Interactions" value={data.total_interactions} />
        <Kpi label="Last 7 days" value={data.interactions_last_7_days} />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Customers by status</CardTitle>
          </CardHeader>
          <CardContent>
            <Bars
              rows={[
                {
                  label: "Prospect",
                  value: data.customers_by_status.prospect,
                  color: "bg-status-prospect",
                },
                {
                  label: "Active",
                  value: data.customers_by_status.active,
                  color: "bg-status-active",
                },
                {
                  label: "At risk",
                  value: data.customers_by_status.at_risk,
                  color: "bg-status-at-risk",
                },
                {
                  label: "Churned",
                  value: data.customers_by_status.churned,
                  color: "bg-status-churned",
                },
              ]}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Sentiment breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            <Bars
              rows={[
                {
                  label: "Positive",
                  value: data.sentiment_breakdown.positive,
                  color: "bg-sentiment-positive",
                },
                {
                  label: "Neutral",
                  value: data.sentiment_breakdown.neutral,
                  color: "bg-sentiment-neutral",
                },
                {
                  label: "Negative",
                  value: data.sentiment_breakdown.negative,
                  color: "bg-sentiment-negative",
                },
              ]}
            />
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent interactions</CardTitle>
        </CardHeader>
        <CardContent>
          {data.recent_interactions.length === 0 ? (
            <p className="text-muted-foreground text-sm">No recent interactions.</p>
          ) : (
            <ul className="divide-y">
              {data.recent_interactions.map((it) => (
                <li key={it.id} className="flex items-center justify-between py-2">
                  <Link href={`/interactions/${it.id}`} className="hover:underline">
                    {it.title}
                  </Link>
                  <span className="text-muted-foreground text-xs">
                    {it.type} · {formatDateTime(it.occurred_at)}
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

function Kpi({ label, value }: { label: string; value: number }) {
  return (
    <Card>
      <CardContent className="pt-6">
        <div className="text-3xl font-bold">{value}</div>
        <div className="text-muted-foreground text-sm">{label}</div>
      </CardContent>
    </Card>
  );
}

function Bars({ rows }: { rows: { label: string; value: number; color: string }[] }) {
  // The biggest value fills the bar; the rest scale relative to it.
  const max = Math.max(1, ...rows.map((r) => r.value));
  return (
    <div className="space-y-3">
      {rows.map((row) => (
        <div key={row.label} className="flex items-center gap-3">
          <span className="text-muted-foreground w-20 shrink-0 text-sm">{row.label}</span>
          <div className="bg-muted h-3 flex-1 overflow-hidden rounded-full">
            <div
              className={cn("h-full rounded-full", row.color)}
              style={{ width: `${(row.value / max) * 100}%` }}
            />
          </div>
          <span className="w-6 shrink-0 text-right text-sm tabular-nums">{row.value}</span>
        </div>
      ))}
    </div>
  );
}
