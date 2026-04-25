# How to Use and Run Skills, Agents, and Plugins in VS Code

This guide explains how to discover, enable, and use **Skills**, **Agents**, and **Plugins** in Visual Studio Code with the GitHub Copilot and Agent ecosystem.

---

## 1. Skills
- **Definition:** Modular capabilities (e.g., /pdf_service, /analyze-csv-files) that add new commands to your workspace.
- **Location:** Usually found in `.agents/skills/` or `.github/skills/` in your project.
- **How to Use:**
  1. Type `/` in the Copilot chat input to see available skills.
  2. Select a skill (e.g., `/pdf_service`) and follow prompts.
  3. Skills are workspace-scoped and only available if present in your project.

---

## 2. Agents
- **Definition:** Custom AI assistants with specialized roles, found in `.agents/` or configured in your workspace.
- **Location:** `.agents/` folder or via the Agents tab in VS Code.
- **How to Use:**
  1. Open the **Agents** tab in VS Code (usually in the sidebar).
  2. Select an agent to start a chat session.
  3. Agents can use skills and have custom instructions.

---

## 3. Plugins
- **Definition:** Prepackaged bundles from the VS Code marketplace that can provide skills, agents, slash commands, and more. Plugins are global/user-scoped.
- **How to View/Enable Plugins:**
  1. **Extensions Sidebar:**
     - Open Extensions (Ctrl+Shift+X)
     - Search for `@agentPlugins` or use the More Actions (three dots) > Views > Agent Plugins
  2. **Chat Customizations Editor:**
     - Press Ctrl+Shift+P → run `Chat: Open Chat Customizations` → see the Plugins section
  3. **Enable Plugin Support:**
     - In VS Code settings, set `chat.plugins.enabled` to `true` (search in Settings UI)
  4. **Enable/Disable Plugins:**
     - In the Agent Plugins view, enable or disable plugins as needed. Disabled plugins remove their skills/agents from your workspace.

---

## Key Differences
| Feature  | Where Defined         | Scope           |
|----------|----------------------|-----------------|
| Skills   | .agents/skills/      | Workspace       |
| Agents   | .agents/             | Workspace       |
| Plugins  | Marketplace install  | Global/User     |

---

## Troubleshooting
- If a skill or agent is missing, check if its plugin is enabled in the Agent Plugins view.
- Skills from disabled plugins will not appear in the `/` menu.

---

## Quick Reference
- **/skills**: Type `/` in chat to see available skills.
- **Agents Tab**: Use sidebar to switch agents.
- **Plugins**: Manage via Extensions sidebar or Chat Customizations.

---

For more details, see the official documentation or your workspace's README.



# Connecting Claude to Snowflake Using MCP: A Practical Guide

Modern data workflows are rapidly evolving with AI assistants like Claude becoming central to how we interact with data. One of the most powerful integrations emerging today is connecting Claude to Snowflake using the Model Context Protocol (MCP), enabling natural language access to your data warehouse.

In this guide, we’ll walk through how to set up this integration and highlight useful MCP Snowflake server implementations from the community.

---

## Why MCP + Snowflake?

The Model Context Protocol (MCP) standardizes how AI systems connect to external tools and data sources. When combined with Snowflake, it enables:

* Conversational data querying
* Faster analytics workflows
* Reduced SQL dependency
* Secure, role-based access to warehouse data

This makes Snowflake not just a data platform—but an AI-ready data interface.

---

## Useful MCP Snowflake References

Before diving into setup, here are some important MCP implementations you can explore:

### 1. MCP Servers Collection (Multi-database support)

A collection of MCP server implementations for different databases including Snowflake.

👉 https://github.com/anjijava16/mcp_servers.git

---

### 2. Snowflake MCP Server (Active development branch)

A dedicated Snowflake MCP server implementation within the MCP servers repository.

👉 https://github.com/anjijava16/mcp_servers/tree/develop/mcp_snowflake_server

---

### 3. Reference Implementation (Standalone Snowflake MCP server)

A clean, focused MCP Snowflake server implementation that follows MCP standards.

👉 https://github.com/isaacwasserman/mcp-snowflake-server/tree/main

---

These repositories provide the foundation for building and customizing your own MCP integrations with Snowflake.

---

## Prerequisites

Make sure you have:

* Python (≤ 3.12 recommended)
* Snowflake account access
* Credentials:

  * Account
  * Warehouse
  * User
  * Password / Private Key
  * Role
  * Database
  * Schema

---

## Step 1: Create a Python Virtual Environment

It is strongly recommended to isolate dependencies.

```bash id="v7xq92"
python -m venv snowflake_env
```

Activate it:

**Windows**

```bash id="k3p9zq"
snowflake_env\Scripts\activate
```

**macOS/Linux**

```bash id="m1q8ab"
source snowflake_env/bin/activate
```

---

## Step 2: Install MCP Snowflake Server

```bash id="t9zv21"
pip install mcp-snowflake-server
```

This installs the MCP-compatible Snowflake server used to expose your warehouse to Claude.

---

## Step 3: Locate Your Environment Path

On Windows:

```bash id="cd4pqs"
cd
```

Example output:

```
C:\Users\YourName\snowflake_env
```

Your Python path becomes:

```
C:\Users\YourName\snowflake_env\Scripts\python.exe
```

---

## Step 4: Configure MCP Server

Now configure your MCP server connection:

```json id="x9q2lm"
{
  "mcpServers": {
    "snowflake_pip": {
      "command": "C:\\Users\\YourName\\snowflake_env\\Scripts\\python.exe",
      "args": [
        "-m",
        "mcp_snowflake_server",
        "--account", "your_account",
        "--warehouse", "your_warehouse",
        "--user", "your_user",
        "--password", "your_password",
        "--role", "your_role",
        "--database", "your_database",
        "--schema", "your_schema"
      ]
    }
  }
}
```

---

## Step 5: Security Best Practices

Avoid embedding credentials directly in configuration files.

Instead, use environment variables:

**Windows**

```bash id="p2xk81"
set SNOWFLAKE_PASSWORD=your_password
```

**macOS/Linux**

```bash id="q8lmp3"
export SNOWFLAKE_PASSWORD=your_password
```

Then reference them in your runtime setup.

---

## Step 6: Connecting Claude

Once MCP is configured:

* Launch your Claude MCP-compatible environment
* Ensure the Snowflake MCP server is active
* Start querying Snowflake in natural language

### Example queries:

* “Show total revenue by region”
* “List top 5 customers by spend”
* “Analyze monthly sales trends for 2025”

---

## Why This Matters

By combining Claude + MCP + Snowflake, you transform your data warehouse into a conversational analytics engine. This reduces friction between data and decision-making.

Instead of writing SQL, you can simply ask questions—and get structured insights instantly.

---

## Final Thoughts

MCP is quickly becoming a foundational layer for AI-tool integrations. With Snowflake as your backend and Claude as your interface, you unlock a powerful new way to interact with enterprise data.

The repositories listed above provide excellent starting points for experimentation, customization, and production-grade implementations.

---
