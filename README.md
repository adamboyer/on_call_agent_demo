# Oncall Agent Demo (Simple Scaffold)

This is a lightweight Python scaffold for your Slack + AWS on-call agent demo.

It is intentionally simple:
- no Terraform or infra code
- no heavy enterprise layering
- clear files you can edit quickly during a demo build
- placeholders where real AWS / Slack / GitHub integration will go

## What this project is for

This demo handles two main flows:

1. **Known issue flow**
   - an incident arrives from SQS
   - the app finds the on-call user from an S3-backed JSON schedule
   - it asks the on-call user in Slack whether the agent should restart the app
   - only the on-call user is allowed to approve
   - if approved, the app enqueues a restart job

2. **Unknown issue flow**
   - an incident arrives with a stack trace
   - the app analyzes the exception
   - it inspects the related code in GitHub
   - it summarizes what it found in Slack
   - if confidence is high, it can ask the on-call user whether to create a PR

## Simple project layout

```text
oncall-agent-simple/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ app/
│  ├─ main.py
│  ├─ config.py
│  ├─ models/
│  │  ├─ incident.py
│  │  ├─ oncall.py
│  │  └─ approval.py
│  ├─ services/
│  │  ├─ incident_service.py
│  │  ├─ oncall_service.py
│  │  ├─ approval_service.py
│  │  └─ diagnosis_service.py
│  ├─ clients/
│  │  ├─ slack_client.py
│  │  ├─ aws_client.py
│  │  └─ github_client.py
│  ├─ routes/
│  │  └─ slack_actions.py
│  ├─ mcp/
│  │  └─ tool_notes.md
│  └─ utils/
│     └─ stacktrace.py
├─ examples/
│  ├─ incident_known.json
│  ├─ incident_unknown.json
│  └─ oncall_schedule.json
└─ tests/
   ├─ test_oncall_service.py
   └─ test_approval_service.py
```

## How to think about the folders

### `app/main.py`
The local entry point. Right now it simulates receiving incidents and shows how the services fit together.

### `app/models/`
Simple data models for:
- incident payloads
- on-call schedule entries
- approval state

### `app/services/`
This is where the business logic lives.

- `incident_service.py` orchestrates the main flow
- `oncall_service.py` figures out who is on call
- `approval_service.py` stores and validates who is allowed to approve
- `diagnosis_service.py` handles known-vs-unknown issue logic

### `app/clients/`
These are wrappers for external systems.

- `slack_client.py` sends Slack messages
- `aws_client.py` stands in for S3 / SQS calls
- `github_client.py` stands in for repo inspection and PR creation

These are deliberately thin so they are easy to swap from fake implementations to real ones.

### `app/routes/`
HTTP handlers for Slack callbacks. This is where button clicks or slash commands should land.

### `app/utils/`
Small helpers. Right now it includes stack trace parsing.

### `app/mcp/`
A small placeholder explaining where MCP fits if your partner wants to expose internal app capabilities as tools.

## Suggested ownership split

### You
Own the deterministic backend:
- incident workflow
- AWS integration points
- Slack approval checks
- restart queueing
- overall app wiring

### Your partner
Own the agentic and repo-inspection path:
- stack trace analysis
- GitHub code lookup
- fix suggestion logic
- PR proposal flow
- MCP layer if you decide to use one

## Recommended build order

### Phase 1
Get the known issue path working:
- read incident
- resolve on-call user
- send Slack approval message
- validate approver
- queue restart

### Phase 2
Add unknown issue diagnosis:
- parse stack trace
- inspect repo file context
- summarize possible fix in Slack

### Phase 3
Add PR creation:
- ask for approval
- create branch/commit/PR
- post result to Slack

### Phase 4
Add MCP if needed:
- expose on-call lookup
- expose Slack posting
- expose GitHub inspection
- expose PR creation

## Environment variables

Copy `.env.example` to `.env` and fill in values later.

Main ones you will probably use:
- `SLACK_BOT_TOKEN`
- `SLACK_SIGNING_SECRET`
- `SLACK_CHANNEL_ID`
- `AWS_REGION`
- `ONCALL_S3_BUCKET`
- `ONCALL_S3_KEY`
- `INCIDENT_QUEUE_URL`
- `RESTART_QUEUE_URL`
- `GITHUB_TOKEN`
- `GITHUB_REPO`
- `GITHUB_BRANCH`

## Running locally

Create a virtualenv and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the sample flow:

```bash
python -m app.main
```

Run tests:

```bash
pytest
```

## Where to put the real integrations

### Real S3 on-call file lookup
Replace the stub in `app/clients/aws_client.py` with boto3 calls.

### Real SQS receive / send
Also wire boto3 into `app/clients/aws_client.py`.

### Real Slack messages
Replace the print-based stub in `app/clients/slack_client.py` with the Slack SDK or HTTP Web API calls.

### Real GitHub inspection / PR creation
Replace the stub in `app/clients/github_client.py` with GitHub API calls and local repo checkout logic.

## Approval model

The important rule in this demo is:

**Only the on-call Slack user can approve an action.**

The scaffold stores an in-memory approval record with:
- incident id
- allowed Slack user id
- allowed action
- expiration timestamp

When Slack sends an action callback, your route should:
1. verify Slack signature
2. read the acting Slack user id
3. compare it to the stored approval record
4. allow or deny

## MCP note

You do not need MCP to make this demo work.

If your partner wants MCP, add it after the base flows work. MCP would sit on top of the existing services and expose tool-like actions such as:
- get current on-call user
- inspect stack trace
- read GitHub file context
- post Slack summary
- create PR
- enqueue restart

## Keep it simple

For the first working demo, keep these constraints:
- one Slack workspace
- one channel
- one repo
- one on-call schedule file
- one restart action
- in-memory approvals for local testing

Once that works, you can replace the in-memory storage with DynamoDB or another persistent store.
