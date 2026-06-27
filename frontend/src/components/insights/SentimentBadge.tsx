import { Badge } from "@/components/ui/badge";
import type { Sentiment } from "@/types";

// Uses the sentiment design tokens defined in globals.css.
const classes: Record<Sentiment, string> = {
  positive: "bg-sentiment-positive text-white",
  neutral: "bg-sentiment-neutral text-white",
  negative: "bg-sentiment-negative text-white",
};

export function SentimentBadge({ sentiment }: { sentiment: Sentiment }) {
  return <Badge className={classes[sentiment]}>{sentiment}</Badge>;
}
