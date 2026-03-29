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
