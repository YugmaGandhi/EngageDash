import Link from "next/link";

import { Badge } from "@/components/ui/badge";
import { buttonVariants } from "@/components/ui/button";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 p-8 text-center">
      <h1 className="text-3xl font-bold">EngageDash</h1>
      <p className="text-muted-foreground">AI-powered Customer Success Insights Dashboard</p>

      {/* Quick check that the design tokens render. */}
      <div className="flex flex-wrap items-center justify-center gap-2">
        <Badge className="bg-status-active text-white">Active</Badge>
        <Badge className="bg-status-at-risk text-white">At risk</Badge>
        <Badge className="bg-status-churned text-white">Churned</Badge>
        <Badge className="bg-sentiment-positive text-white">Positive</Badge>
      </div>

      <div className="flex flex-wrap items-center justify-center gap-3">
        <Link href="/login" className={buttonVariants()}>
          Get started
        </Link>
        <Link href="/register" className={buttonVariants({ variant: "outline" })}>
          Create account
        </Link>
      </div>
    </main>
  );
}
