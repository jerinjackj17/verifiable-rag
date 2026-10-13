"""Synthetic corpus: Acme Cloud docs. Every fact is invented for the demo.

Deliberately incomplete: there is NO document about 2021 enterprise refund
terms, NO document about the CEO, and only one oblique mention of API key
rotation — the abstention and rewrite demos need gaps to be honest.
"""
from __future__ import annotations

DOCS: list[dict] = [
    {"id": "pricing-01", "title": "Plans and pricing",
     "text": "Acme Cloud has three plans. Starter is free for up to 3 seats. "
             "Pro costs $49 per seat per month billed annually, or $59 month to month. "
             "Enterprise is custom priced with annual contracts."},
    {"id": "pricing-02", "title": "Pro plan limits",
     "text": "The Pro plan includes 500 GB of storage, 10 million API calls per month, "
             "and priority support with a 4-hour response SLA. Overage is $0.02 per GB "
             "and $10 per extra million API calls."},
    {"id": "pricing-03", "title": "Enterprise contracts",
     "text": "Enterprise contracts are annual, paid upfront, with custom storage and "
             "API quotas. All enterprise plans include a 99.99% uptime SLA and a "
             "dedicated success manager. Contact sales for a quote."},
    {"id": "billing-01", "title": "Refund policy",
     "text": "Monthly plans can be cancelled anytime; the current month is not refunded. "
             "Annual plans cancelled within the first 30 days receive a pro-rated refund. "
             "After 30 days, annual plans are non-refundable."},
    {"id": "billing-02", "title": "Invoices and receipts",
     "text": "Invoices are emailed on the first of each month. Receipts are available "
             "in the billing dashboard under Settings, then Billing. We accept all major "
             "credit cards and ACH transfers for annual plans."},
    {"id": "sla-01", "title": "Uptime SLA",
     "text": "Acme Cloud targets 99.95% monthly uptime for Pro and 99.99% for Enterprise. "
             "Scheduled maintenance windows are excluded and announced 7 days ahead. "
             "Downtime credits are 10% of the monthly fee per 0.1% below target."},
    {"id": "api-01", "title": "Getting started with the API",
     "text": "Create an API key in Settings, then API Keys. Authenticate with a Bearer "
             "token in the Authorization header. The base URL is https://api.acme.example/v1. "
             "Rate limits are 100 requests per second per key on Pro."},
    {"id": "api-02", "title": "API key rotation",
     "text": "Keys should be rotated every 90 days. Generate a new key, deploy it alongside "
             "the old one, then revoke the old key after 48 hours. Revoked keys stop working "
             "immediately and cannot be restored."},
    {"id": "api-03", "title": "Webhooks",
     "text": "Webhooks deliver event notifications to your URL as POST requests. Available "
             "events include invoice.paid, usage.threshold, and deploy.finished. "
             "Webhook deliveries retry with exponential backoff for 24 hours."},
    {"id": "api-04", "title": "Error codes",
     "text": "The API returns standard HTTP codes. 429 means you hit the rate limit; back "
             "off and retry after the Retry-After header. 401 means your key is missing, "
             "expired, or revoked."},
    {"id": "security-01", "title": "Data encryption",
     "text": "Data is encrypted at rest with AES-256 and in transit with TLS 1.3. "
             "Enterprise customers can bring their own KMS keys. We never store "
             "plaintext credentials."},
    {"id": "security-02", "title": "SOC 2 and compliance",
     "text": "Acme Cloud is SOC 2 Type II certified, renewed annually. GDPR data "
             "processing agreements are available on Enterprise. Data residency options "
             "include US and EU regions."},
    {"id": "security-03", "title": "SSO and MFA",
     "text": "SSO via SAML and OIDC is available on Pro and Enterprise. Enforce MFA for "
             "all members from Settings, then Security. SCIM provisioning is Enterprise only."},
    {"id": "data-01", "title": "Data retention",
     "text": "Event data is retained for 90 days on Pro and 400 days on Enterprise. "
             "Raw request logs are kept for 30 days. Deleted workspaces are purged "
             "after a 14-day grace period."},
    {"id": "data-02", "title": "Backups",
     "text": "Backups run every 6 hours and are replicated across two regions. "
             "Point-in-time recovery covers the last 7 days on Pro and 30 days on "
             "Enterprise. Restore requests go through support."},
    {"id": "data-03", "title": "Exporting your data",
     "text": "Export workspace data anytime from Settings, then Data, then Export. "
             "Exports include JSON and CSV formats and complete within 24 hours for "
             "workspaces under 100 GB."},
    {"id": "support-01", "title": "Support channels",
     "text": "Starter gets community forum support. Pro gets email support with a "
             "4-hour response SLA on business days. Enterprise gets 24/7 phone and a "
             "dedicated Slack channel."},
    {"id": "support-02", "title": "Status page",
     "text": "Live status is at status.acme.example. Subscribe for incident alerts by "
             "email, SMS, or webhook. Postmortems are published within 5 business days."},
    {"id": "support-03", "title": "Migrating from competitors",
     "text": "Our migration tool imports from the three major competitors. Typical "
             "migrations complete over a weekend. Enterprise migrations include a "
             "dedicated engineer and a rollback plan."},
    {"id": "deploy-01", "title": "Deployments",
     "text": "Connect a Git repository and push to deploy. Preview deployments are "
             "created for every pull request. Production deploys require a passing "
             "CI check on Pro and above."},
    {"id": "deploy-02", "title": "Rollback",
     "text": "Roll back to any deployment from the last 30 days in one click. "
             "Database migrations are not auto-rolled-back; snapshot before risky "
             "migrations."},
    {"id": "deploy-03", "title": "Custom domains",
     "text": "Add a custom domain from Settings, then Domains. Point a CNAME at "
             "cname.acme.example. TLS certificates are provisioned automatically "
             "within minutes."},
    {"id": "team-01", "title": "Roles and permissions",
     "text": "Roles are Owner, Admin, Developer, and Viewer. Only Owners can delete "
             "the workspace or manage billing. API keys inherit the creator's role."},
    {"id": "team-02", "title": "Audit logs",
     "text": "Every settings change, login, and API key event is recorded. Audit logs "
             "are retained for 1 year on Pro and 7 years on Enterprise, and cannot be "
             "edited or deleted."},
    {"id": "usage-01", "title": "Usage alerts",
     "text": "Set usage alerts at 50%, 80% and 100% of your API quota. Alerts fire by "
             "email and webhook. Overage protection can pause non-critical workloads "
             "automatically on Enterprise."},
    {"id": "usage-02", "title": "Fair use",
     "text": "Starter workspaces are limited to 100k API calls per month. Sustained "
             "traffic above your quota for 7 days triggers an automatic plan review "
             "with our team."},
    {"id": "integrations-01", "title": "Slack integration",
     "text": "Connect Slack to receive deploy and incident notifications. Use /acme "
             "status for a quick health check. Notification rules are per channel."},
    {"id": "integrations-02", "title": "GitHub integration",
     "text": "Install the GitHub app to get preview deployments on pull requests. "
             "Required status checks can block merges on failing builds."},
    {"id": "mobile-01", "title": "Mobile app",
     "text": "The iOS and Android apps cover dashboards and incident ack. Deploys and "
             "billing changes require the web app."},
    {"id": "glossary-01", "title": "What is a workspace",
     "text": "A workspace is the top-level container: members, projects, billing, and "
             "settings all live under it. Most companies run one workspace per team."},
]

# Demo questions: each exercises a different pipeline behavior.
QUESTIONS = [
    {"id": "q1", "label": "Straightforward",
     "q": "How much does the Pro plan cost per seat?",
     "expect": "answered from pricing-01"},
    {"id": "q2", "label": "Needs a rewrite",
     "q": "How do I reset it?",
     "expect": "ambiguous 'it' — rewrite targets API key rotation (api-02)"},
    {"id": "q3", "label": "Unanswerable",
     "q": "What was the enterprise refund policy for contracts signed in 2021?",
     "expect": "no doc covers this — verifiable abstains, naive hallucinates"},
    {"id": "q4", "label": "Absurd",
     "q": "What is the CEO's favorite color?",
     "expect": "nothing in the corpus — must abstain"},
    {"id": "q5", "label": "Multi-fact",
     "q": "What is the uptime SLA and what credit do I get for downtime?",
     "expect": "answered from sla-01 with citation"},
]
