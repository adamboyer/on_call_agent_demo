# MCP notes

You do not need MCP for the base app.

If you add it later, expose existing service functions as tools, for example:
- get_oncall_user
- diagnose_incident
- inspect_code_context
- send_slack_message
- create_pull_request
- queue_restart

Treat MCP as a wrapper over the existing services, not as the core architecture.
