import { Badge } from "@/components/ui/badge";
import type { CustomerStatus } from "@/types";

const labels: Record<CustomerStatus, string> = {
  prospect: "Prospect",
  active: "Active",
  at_risk: "At risk",
  churned: "Churned",
};

// Uses the customer-status design tokens defined in globals.css.
const classes: Record<CustomerStatus, string> = {
  prospect: "bg-status-prospect text-white",
  active: "bg-status-active text-white",
  at_risk: "bg-status-at-risk text-white",
  churned: "bg-status-churned text-white",
};

export function CustomerStatusBadge({ status }: { status: CustomerStatus }) {
  return <Badge className={classes[status]}>{labels[status]}</Badge>;
}
