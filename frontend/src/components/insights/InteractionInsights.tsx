"use client";

import { Sparkles } from "lucide-react";
import { useEffect } from "react";
import { toast } from "sonner";

import { Loading } from "@/components/common/Loading";
import { SentimentBadge } from "@/components/insights/SentimentBadge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { clearInsights, fetchInsights, generateInsight } from "@/store/slices/insightsSlice";

export function InteractionInsights({ interactionId }: { interactionId: number }) {
  const dispatch = useAppDispatch();
  const { items, status, generating } = useAppSelector((s) => s.insights);

  useEffect(() => {
    dispatch(fetchInsights(interactionId));
    return () => {
      dispatch(clearInsights());
    };
  }, [dispatch, interactionId]);

  const latest = items[0];

  async function handleGenerate() {
    try {
      await dispatch(generateInsight(interactionId)).unwrap();
      toast.success("Insight generated");
    } catch (err) {
      toast.error(typeof err === "string" ? err : "Could not generate insight");
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span className="flex items-center gap-2">
            <Sparkles className="h-5 w-5" />
            AI Insights
          </span>
          <Button size="sm" onClick={handleGenerate} disabled={generating}>
            {generating ? "Generating..." : latest ? "Regenerate" : "Generate insight"}
          </Button>
        </CardTitle>
      </CardHeader>
      <CardContent>
        {status === "loading" ? (
          <Loading label="Loading insights..." />
        ) : !latest ? (
          <p className="text-muted-foreground text-sm">
            No insights yet. Click “Generate insight” to analyze the notes.
          </p>
        ) : (
          <div className="space-y-4">
            {latest.status === "fallback" && (
              <p className="border-status-at-risk/40 bg-status-at-risk/10 rounded-md border p-2 text-xs">
                AI generation was unavailable, so this is a fallback result.
              </p>
            )}

            <div className="flex items-center gap-2">
              <span className="text-muted-foreground text-xs">Sentiment:</span>
              <SentimentBadge sentiment={latest.sentiment} />
            </div>

            <div>
              <div className="text-muted-foreground mb-1 text-xs">Summary</div>
              <p className="text-sm">{latest.summary}</p>
            </div>

            <InsightList title="Action items" items={latest.action_items} />
            <InsightList title="Risks" items={latest.risks} />
          </div>
        )}
      </CardContent>
    </Card>
  );
}

function InsightList({ title, items }: { title: string; items: string[] }) {
  return (
    <div>
      <div className="text-muted-foreground mb-1 text-xs">{title}</div>
      {items.length === 0 ? (
        <p className="text-muted-foreground text-sm">None</p>
      ) : (
        <ul className="list-inside list-disc space-y-1 text-sm">
          {items.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
