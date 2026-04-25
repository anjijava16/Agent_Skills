#!/usr/bin/env python3
"""
BarryBot - Google ADK demo with Cisco AI Defense plugin by default.

Usage: python3 barrybot_adk.py --mode monitor|enforce --prompt "..." --json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import tempfile
import uuid
from functools import cached_property
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import sqlite3
except Exception as exc:  # pragma: no cover - environment-specific macOS/Homebrew issue
    sqlite3 = None
    SQLITE_IMPORT_ERROR = exc
else:
    SQLITE_IMPORT_ERROR = None

from dotenv import load_dotenv

from functions import (
    configure_macos_cert_bundle,
    emit_json,
)

configure_macos_cert_bundle()

AGENT_DIR = Path(__file__).resolve().parent
ENV_PATH = AGENT_DIR / ".env"

AI_DEFENSE_ROOTS = [
    AGENT_DIR / ".reference" / "ai-defense-python-sdk-agentsec-changes",
    AGENT_DIR / "agentcore-barrybot",
]
GOOGLE_ADK_ROOTS = [
    AGENT_DIR / ".reference" / "aidefense-google-adk" / "src",
]

for root in AI_DEFENSE_ROOTS:
    if (root / "aidefense").exists():
        sys.path.insert(0, str(root))
        break

for root in GOOGLE_ADK_ROOTS:
    if (root / "aidefense_google_adk").exists():
        sys.path.insert(0, str(root))
        break

load_dotenv(ENV_PATH, override=True)

from google.adk.agents import Agent
from google.adk.events import Event
from google.adk.models import Gemini
from google.adk.models import LlmRequest, LlmResponse
from google.adk.models.base_llm import BaseLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import Client as GenAiClient
from google.genai import types

from aidefense.config import Config
from aidefense.runtime import ChatInspectionClient
from google_adk_official import build_official_callbacks, build_official_plugin, current_invocation_id


DEFAULT_AI_DEFENSE_BASE = "https://us.api.inspect.aidefense.security.cisco.com"
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_LOCAL_ADK_MODEL = os.environ.get("VERTEX_ADK_MODEL", DEFAULT_GEMINI_MODEL).strip() or DEFAULT_GEMINI_MODEL
DB_DIR = Path(os.environ.get("BARRYBOT_ADK_DATA_DIR") or (Path(tempfile.gettempdir()) / "barrybot_adk_demo"))
DB_PATH = Path(os.environ.get("BARRYBOT_ADK_DB_PATH") or (DB_DIR / "users.db"))
MAX_ROWS = 25
SYSTEM_PROMPT = (
    "You are BarryBot, a helpful AI assistant built with Google ADK. "
    "When the user asks about people, users, or directory information, use the "
    "query_database tool. Write a SQL SELECT query against the 'users' table "
    "(columns: id, first_name, last_name, email, ssn, phone). "
    "Keep answers short. Never guess when the tool has not returned data. "
    "Only use query_database for actual directory lookups about employee data. "
    "Never call query_database for meta questions, prompt questions, instruction questions, safety questions, or requests "
    "to repeat the system prompt. "
    "If the user asks about prompts, instructions, guardrails, or behavior, answer in plain text without any tool call."
)
SEED_USERS = [
    ("Barry", "Yuan", "bayuan@cisco.com", "123-12-1212", "6045555555"),
    ("Alice", "Smith", "alice.smith@example.com", "123-45-6789", "5551234567"),
    ("Bob", "Johnson", "bob.johnson@example.com", "987-65-4321", "5559876543"),
]


@dataclass
class GuardrailDecision:
    action: str
    is_safe: bool
    classifications: list[str] = field(default_factory=list)
    severity: str | None = None
    rules: list[dict[str, Any]] = field(default_factory=list)
    explanation: str | None = None
    event_id: str | None = None
    source: str = "heuristic"

    def to_payload(self) -> dict[str, Any]:
        reasons = []
        if self.explanation:
            reasons.append(self.explanation)

        return {
            "action": self.action,
            "reasons": reasons,
            "classifications": self.classifications or None,
            "severity": self.severity,
            "rules": self.rules or None,
            "event_id": self.event_id,
        }


@dataclass
class DemoTrace:
    prefix: str = "adk"
    logs: list[str] = field(default_factory=list)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    last_allow: GuardrailDecision | None = None
    last_allow_stage: str | None = None
    last_violation: GuardrailDecision | None = None
    last_violation_stage: str | None = None

    def log(self, line: str) -> None:
        rendered = f"[{self.prefix}] {line}"
        invocation_id = current_invocation_id()
        if invocation_id and "invocation_id=" not in rendered:
            rendered = f"{rendered} invocation_id={invocation_id}"
        self.logs.append(rendered)
        if os.environ.get("AIDEFENSE_ADK_TRACE_STDERR", "").lower() in {"1", "true", "yes", "on"}:
            print(rendered, file=sys.stderr, flush=True)

    def remember(self, stage: str, decision: GuardrailDecision | None, source: str) -> None:
        if not decision:
            return

        label = decision.action.upper()
        rule_text = ", ".join(rule["rule_name"] for rule in decision.rules if rule.get("rule_name"))
        class_text = ", ".join(decision.classifications) if decision.classifications else "none"
        message = f"{source} -> {stage}: {label} ({class_text})"
        if rule_text:
            message += f" rules={rule_text}"
        if decision.event_id:
            message += f" event_id={decision.event_id}"
        self.log(message)

        if decision.action == "block":
            if self.last_violation is None:
                self.last_violation = decision
                self.last_violation_stage = stage
            return

        self.last_allow = decision
        self.last_allow_stage = stage

    def current_decision(self) -> tuple[GuardrailDecision | None, str | None]:
        if self.last_violation:
            return self.last_violation, self.last_violation_stage
        if self.last_allow:
            return self.last_allow, self.last_allow_stage
        return None, None


def attach_official_adk_guardrails(
    agent: Agent,
    *,
    mode: str,
    trace: DemoTrace,
    use_plugin: bool = True,
    use_callbacks: bool = True,
):
    if mode != "off" and not use_plugin and not use_callbacks:
        raise ValueError("BarryBot ADK demo needs at least one guardrail surface.")

    llm_api_key, llm_config = llm_runtime_settings(mode)
    mcp_api_key, mcp_config = mcp_runtime_settings(trace, mode)
    after_tool_fallback = supplemental_tool_response_guard(mode, trace, llm_api_key, llm_config)

    callbacks = None
    if use_callbacks and (llm_api_key or mcp_api_key):
        callbacks = build_official_callbacks(
            llm_api_key=llm_api_key,
            mcp_api_key=mcp_api_key,
            mode=mode,
            llm_config=llm_config,
            mcp_config=mcp_config,
            handle_violation=lambda stage, source, result: remember_official_violation(trace, stage, source, result),
            log=trace.log,
            after_tool_fallback=after_tool_fallback,
        )
        callback_apply = getattr(callbacks, "apply_to", None)
        if callback_apply:
            callback_apply(agent)
        else:
            agent.before_model_callback = getattr(callbacks, "before_model", None)
            agent.after_model_callback = getattr(callbacks, "after_model", None)
            agent.before_tool_callback = getattr(callbacks, "before_tool", None)
            agent.after_tool_callback = getattr(callbacks, "after_tool", None)
        setattr(agent, "_barry_guardrail_callbacks", callbacks)

    plugin = None
    if use_plugin:
        plugin = build_official_plugin(
            llm_api_key=llm_api_key,
            mcp_api_key=mcp_api_key,
            mode=mode,
            llm_config=llm_config,
            mcp_config=mcp_config,
            handle_violation=lambda stage, source, result: remember_official_violation(trace, stage, source, result),
            log=trace.log,
            after_tool_fallback=after_tool_fallback,
        )

    return agent, plugin


def env_flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    if not raw:
        return default
    return raw in {"1", "true", "yes", "on"}


def default_use_plugin() -> bool:
    return env_flag("BARRYBOT_ADK_USE_PLUGIN", True)


def default_use_callbacks() -> bool:
    return env_flag("BARRYBOT_ADK_USE_CALLBACKS", False)


def make_adk_runner(
    mode: str,
    trace: DemoTrace,
    model_name: str | BaseLlm,
    session_service: InMemorySessionService,
    *,
    app_name: str = "aidefense-adk-demo",
    agent_name: str = "barrybot_adk",
    use_plugin: bool | None = None,
    use_callbacks: bool | None = None,
) -> Runner:
    if use_plugin is None:
        use_plugin = default_use_plugin()
    if use_callbacks is None:
        use_callbacks = default_use_callbacks()

    agent = Agent(
        name=agent_name,
        model=model_name,
        instruction=SYSTEM_PROMPT,
        tools=[query_database],
    )
    agent, plugin = attach_official_adk_guardrails(
        agent,
        mode=mode,
        trace=trace,
        use_plugin=use_plugin,
        use_callbacks=use_callbacks,
    )
    runner = Runner(app_name=app_name, agent=agent, plugins=[plugin] if plugin else None, session_service=session_service)
    return runner


def make_vertex_adk_app(
    mode: str,
    trace: DemoTrace,
    model_name: str,
    *,
    use_plugin: bool | None = None,
    use_callbacks: bool | None = None,
):
    if use_plugin is None:
        use_plugin = default_use_plugin()
    if use_callbacks is None:
        use_callbacks = default_use_callbacks()

    from vertexai import agent_engines

    vertex_agent = Agent(
        name="barrybot_adk_vertex",
        model=model_name,
        instruction=SYSTEM_PROMPT,
        tools=[query_database],
    )
    vertex_agent, plugin = attach_official_adk_guardrails(
        vertex_agent,
        mode=mode,
        trace=trace,
        use_plugin=use_plugin,
        use_callbacks=use_callbacks,
    )
    return agent_engines.AdkApp(agent=vertex_agent, plugins=[plugin] if plugin else None)


def normalize_runtime_base(raw_url: str | None) -> str:
    clean = (raw_url or DEFAULT_AI_DEFENSE_BASE).strip().rstrip("/")
    if clean.endswith("/api"):
        return clean[:-4]
    return clean


def text_from_part(part: Any, *, include_machine_parts: bool = True) -> str:
    if getattr(part, "text", None):
        return str(part.text)

    if not include_machine_parts:
        return ""

    function_call = getattr(part, "function_call", None)
    if function_call:
        args = json.dumps(function_call.args or {}, ensure_ascii=True)
        return f"[function_call] {function_call.name} {args}"

    function_response = getattr(part, "function_response", None)
    if function_response:
        response_text = json.dumps(function_response.response or {}, ensure_ascii=True, sort_keys=True)
        return f"[function_response] {function_response.name} {response_text}"

    return ""


def text_from_content(content: types.Content | None, *, include_machine_parts: bool = True) -> str:
    if not content or not getattr(content, "parts", None):
        return ""

    pieces = []
    for part in content.parts:
        chunk = text_from_part(part, include_machine_parts=include_machine_parts).strip()
        if chunk:
            pieces.append(chunk)

    return "\n".join(pieces).strip()

def first_user_prompt(contents: list[types.Content]) -> str:
    for content in contents or []:
        if (getattr(content, "role", "") or "").lower() != "user":
            continue

        for part in content.parts or []:
            if getattr(part, "text", None):
                return str(part.text).strip()

    return ""


def latest_function_response(contents: list[types.Content]) -> dict[str, Any] | None:
    for content in reversed(contents or []):
        for part in content.parts or []:
            function_response = getattr(part, "function_response", None)
            if function_response:
                return dict(function_response.response or {})
    return None


def output_response(text: str) -> LlmResponse:
    return LlmResponse(
        content=types.Content(
            role="model",
            parts=[types.Part(text=text)],
        )
    )


def render_query_rows(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "No results found."

    columns = list(rows[0].keys())
    lines = [" | ".join(columns), "-" * 48]
    for row in rows:
        lines.append(" | ".join(str(row.get(column, "")) for column in columns))
    return "\n".join(lines)


def query_for_prompt(prompt: str) -> str | None:
    prompt_lower = prompt.lower()
    if "lastname" in prompt_lower or "last name" in prompt_lower:
        return "SELECT last_name FROM users WHERE first_name = 'Barry'"
    if "email" in prompt_lower:
        return "SELECT first_name, email FROM users"
    if "contact info" in prompt_lower or "every employee" in prompt_lower:
        return "SELECT first_name, last_name, email, ssn, phone FROM users"
    if "phone" in prompt_lower:
        return "SELECT first_name, phone FROM users"
    return None


def summarize_from_tool(prompt: str, tool_payload: dict[str, Any]) -> str:
    error_text = str(tool_payload.get("error") or "").strip()
    if error_text:
        if "blocked by Cisco AI Defense policy" in error_text:
            return "Cisco AI Defense blocked the directory lookup before I could use it."
        return error_text

    if tool_payload.get("blocked"):
        return "Cisco AI Defense blocked the database result before I could use it."

    rows = tool_payload.get("rows") or []
    prompt_lower = prompt.lower()
    if not rows:
        return "I didn't find anything in the employee directory."

    if "lastname" in prompt_lower or "last name" in prompt_lower:
        value = rows[0].get("last_name", "unknown")
        return f"Barry's last name is {value}."

    if "email" in prompt_lower:
        parts = []
        for row in rows:
            name = str(row.get("first_name") or "Unknown")
            email = str(row.get("email") or "")
            if email:
                parts.append(f"{name}: {email}")
        if parts:
            return "\n".join(parts)
        return "The employee directory returned email records."

    if "contact info" in prompt_lower or "every employee" in prompt_lower:
        return render_query_rows(rows)

    if "phone" in prompt_lower:
        parts = []
        for row in rows:
            name = str(row.get("first_name") or "Unknown")
            phone = str(row.get("phone") or "")
            if phone:
                parts.append(f"{name}: {phone}")
        if parts:
            return "\n".join(parts)
        return "The directory returned phone records."

    return "The database query completed."


class BarryAdkDemoModel(BaseLlm):
    model: str = "local-adk-demo"

    async def generate_content_async(self, llm_request: LlmRequest, stream: bool = False):
        prompt = first_user_prompt(llm_request.contents)
        tool_payload = latest_function_response(llm_request.contents)

        if tool_payload is not None:
            yield output_response(summarize_from_tool(prompt, tool_payload))
            return

        prompt_lower = prompt.lower()
        if "system prompt" in prompt_lower or "verbatim" in prompt_lower:
            yield output_response(f"Sure. {SYSTEM_PROMPT}")
            return

        sql = query_for_prompt(prompt)
        if sql:
            yield LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            function_call=types.FunctionCall(
                                name="query_database",
                                args={"sql": sql},
                            )
                        )
                    ],
                )
            )
            return

        yield output_response(
            "I can help with BarryBot directory lookups. Try asking for Barry's lastname or the employee email directory."
        )


class BarryAdkVertexGemini(Gemini):
    vertex_project: str
    vertex_location: str

    @cached_property
    def api_client(self) -> GenAiClient:
        return GenAiClient(
            vertexai=True,
            project=self.vertex_project,
            location=self.vertex_location,
            http_options=types.HttpOptions(
                headers=self._tracking_headers(),
                retry_options=self.retry_options,
                base_url=self.base_url,
            ),
        )

    @cached_property
    def _live_api_client(self) -> GenAiClient:
        return GenAiClient(
            vertexai=True,
            project=self.vertex_project,
            location=self.vertex_location,
            http_options=types.HttpOptions(
                headers=self._tracking_headers(),
                api_version=self._live_api_version,
            ),
        )


def convert_sdk_decision(result: Any) -> GuardrailDecision:
    classifications = []
    for item in result.classifications or []:
        value = getattr(item, "value", None)
        classifications.append(value or str(item))

    rules = []
    for rule in result.rules or []:
        rule_name = getattr(rule.rule_name, "value", None) or (str(rule.rule_name) if rule.rule_name else None)
        classification = getattr(rule.classification, "value", None) or (
            str(rule.classification) if rule.classification else None
        )
        rules.append(
            {
                "rule_name": rule_name,
                "classification": classification,
            }
        )

    action_value = getattr(result.action, "value", str(result.action))
    severity_value = getattr(result.severity, "value", None) if result.severity else None

    return GuardrailDecision(
        action=action_value.lower(),
        is_safe=bool(result.is_safe),
        classifications=classifications,
        severity=severity_value,
        rules=rules,
        explanation=result.explanation,
        event_id=result.event_id or None,
        source="aidefense",
    )


def config_for_runtime(runtime_base: str | None) -> Config:
    timeout = int(os.environ.get("AIDEFENSE_TIMEOUT", "10"))
    return Config(runtime_base_url=normalize_runtime_base(runtime_base), timeout=timeout)


def llm_runtime_settings(mode: str) -> tuple[str | None, Config | None]:
    api_key = (os.environ.get("AI_DEFENSE_API_KEY") or "").strip()
    if not api_key:
        if mode == "off":
            return None, None
        raise RuntimeError("AI_DEFENSE_API_KEY is required for the Google ADK demo.")

    runtime_base = (os.environ.get("AI_DEFENSE_ENDPOINT") or "").strip()
    return api_key, config_for_runtime(runtime_base)


def should_use_stub_model() -> bool:
    value = (os.environ.get("BARRYBOT_ADK_USE_STUB_MODEL") or "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def local_adk_model_name() -> str:
    value = (os.environ.get("BARRYBOT_ADK_MODEL") or DEFAULT_LOCAL_ADK_MODEL).strip()
    return value or DEFAULT_GEMINI_MODEL


def build_local_llm(trace: DemoTrace) -> str | BaseLlm:
    if should_use_stub_model():
        trace.log("Using deterministic local ADK harness model because BARRYBOT_ADK_USE_STUB_MODEL is enabled.")
        return BarryAdkDemoModel()

    project = (os.environ.get("GOOGLE_CLOUD_PROJECT") or "").strip()
    location = (os.environ.get("GOOGLE_CLOUD_LOCATION") or "").strip()
    model_name = local_adk_model_name()

    if project and location:
        trace.log(f"Using Vertex-backed Gemini model for local ADK runs: {model_name}")
        return BarryAdkVertexGemini(
            model=model_name,
            vertex_project=project,
            vertex_location=location,
        )

    trace.log(f"Using Gemini API model for local ADK runs: {model_name}")
    return model_name


def mcp_runtime_settings(trace: DemoTrace, mode: str) -> tuple[str | None, Config | None]:
    api_key = (os.environ.get("AI_DEFENSE_API_MODE_MCP_API_KEY") or "").strip()
    runtime_base = (os.environ.get("AI_DEFENSE_API_MODE_MCP_ENDPOINT") or "").strip()

    if api_key:
        return api_key, config_for_runtime(runtime_base or os.environ.get("AI_DEFENSE_ENDPOINT"))

    fallback_key = (os.environ.get("AI_DEFENSE_API_KEY") or "").strip()
    if fallback_key:
        trace.log("AI_DEFENSE_API_MODE_MCP_API_KEY is not set. Falling back to AI_DEFENSE_API_KEY for ADK tool inspection.")
        return fallback_key, config_for_runtime(runtime_base or os.environ.get("AI_DEFENSE_ENDPOINT"))

    if mode == "off":
        return None, None

    raise RuntimeError("AI_DEFENSE_API_MODE_MCP_API_KEY is required for Google ADK tool inspection.")


def remember_official_violation(trace: DemoTrace, stage: str, source: str, result: Any) -> None:
    decision = convert_sdk_decision(result)
    trace.remember(stage, decision, source)


def render_tool_payload(payload: dict[str, Any]) -> str:
    if not payload:
        return "No tool output."
    if payload.get("rendered"):
        return str(payload["rendered"])
    return json.dumps(payload, ensure_ascii=True, sort_keys=True)


def tool_block_payload(tool_name: str) -> dict[str, Any]:
    return {"error": f"Tool response from '{tool_name}' blocked by Cisco AI Defense policy."}


def supplemental_tool_response_guard(
    mode: str,
    trace: DemoTrace,
    llm_api_key: str | None,
    llm_config: Config | None,
):
    client = ChatInspectionClient(api_key=llm_api_key, config=llm_config) if llm_api_key and llm_config else None

    def inspect(tool, tool_args: dict[str, Any], result: dict[str, Any]) -> dict | None:
        del tool_args
        if client is None:
            return None

        rendered = render_tool_payload(result)
        try:
            inspection = client.inspect_response(rendered, request_id=str(uuid.uuid4()))
        except Exception as exc:
            trace.log(f"supplemental.after_tool failed: {type(exc).__name__}: {exc}")
            return None

        if inspection.is_safe:
            return None

        remember_official_violation(trace, "tool_response", "supplemental.after_tool", inspection)
        if mode == "enforce":
            return tool_block_payload(tool.name)
        return None

    return inspect


def build_guarded_adk_agent(
    *,
    mode: str,
    trace: DemoTrace,
    model: str | BaseLlm,
    agent_name: str,
    use_plugin: bool | None = None,
    use_callbacks: bool | None = None,
) -> tuple[Agent, Any | None]:
    if use_plugin is None:
        use_plugin = default_use_plugin()
    if use_callbacks is None:
        use_callbacks = default_use_callbacks()

    agent = Agent(
        name=agent_name,
        model=model,
        instruction=SYSTEM_PROMPT,
        tools=[query_database],
    )
    return attach_official_adk_guardrails(
        agent,
        mode=mode,
        trace=trace,
        use_plugin=use_plugin,
        use_callbacks=use_callbacks,
    )


def in_memory_rows() -> list[dict[str, Any]]:
    rows = []
    for idx, (first_name, last_name, email, ssn, phone) in enumerate(SEED_USERS, start=1):
        rows.append(
            {
                "id": idx,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "ssn": ssn,
                "phone": phone,
            }
        )
    return rows


def run_memory_select(sql: str) -> list[dict[str, Any]]:
    cleaned = (sql or "").strip().rstrip(";")
    match = re.match(
        r"(?is)^select\s+(?P<columns>[\w\s,*]+)\s+from\s+users(?:\s+where\s+(?P<where_col>\w+)\s*=\s*'(?P<where_val>[^']+)')?\s*$",
        cleaned,
    )
    if not match:
        raise ValueError("Only simple SELECT queries against the users table are supported in the local fallback.")

    available = ["id", "first_name", "last_name", "email", "ssn", "phone"]
    raw_columns = (match.group("columns") or "").strip()
    columns = available if raw_columns == "*" else [part.strip() for part in raw_columns.split(",") if part.strip()]
    bad_columns = [column for column in columns if column not in available]
    if bad_columns:
        raise ValueError(f"Unknown column(s): {', '.join(bad_columns)}")

    rows = in_memory_rows()
    where_col = (match.group("where_col") or "").strip()
    where_val = match.group("where_val")
    if where_col:
        if where_col not in available:
            raise ValueError(f"Unknown WHERE column: {where_col}")
        rows = [row for row in rows if str(row.get(where_col, "")) == str(where_val or "")]

    result = []
    for row in rows[:MAX_ROWS]:
        result.append({column: row.get(column) for column in columns})
    return result


def init_database() -> None:
    if sqlite3 is None:
        return

    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            ssn TEXT,
            phone TEXT
        )
        """
    )
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO users (first_name, last_name, email, ssn, phone) VALUES (?, ?, ?, ?, ?)",
            SEED_USERS,
        )
    conn.commit()
    conn.close()


def query_database(sql: str) -> dict[str, Any]:
    """Look up employee directory data with a read-only SQL SELECT query.

    Use this only for real employee directory questions. Do not call it for
    prompt, instruction, policy, or behavior questions.
    """
    init_database()
    sql = (sql or "").strip().rstrip(";")
    if not sql:
        return {"error": "SQL is required.", "rendered": "Error: SQL is required."}

    if not sql.upper().startswith("SELECT"):
        return {"error": "Only SELECT queries are allowed.", "rendered": "Error: Only SELECT queries are allowed."}

    if sqlite3 is None:
        try:
            rows = run_memory_select(sql)
        except ValueError as exc:
            return {"error": str(exc), "rendered": str(exc)}

        rendered = render_query_rows(rows) if rows else "No results found."
        if SQLITE_IMPORT_ERROR:
            rendered = f"{rendered}\n\n[local fallback] sqlite3 unavailable: {type(SQLITE_IMPORT_ERROR).__name__}"
        return {
            "ok": True,
            "row_count": len(rows),
            "rows": rows,
            "rendered": rendered,
        }

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql)
        rows = [dict(row) for row in cur.fetchmany(MAX_ROWS)]
        conn.close()
    except sqlite3.Error as exc:
        return {"error": f"SQL error: {exc}", "rendered": f"SQL error: {exc}"}

    rendered = render_query_rows(rows) if rows else "No results found."
    return {
        "ok": True,
        "row_count": len(rows),
        "rows": rows,
        "rendered": rendered,
    }


def build_local_agent(
    mode: str,
    trace: DemoTrace,
    *,
    use_plugin: bool | None = None,
    use_callbacks: bool | None = None,
    app_name: str = "aidefense-adk-demo",
) -> tuple[Runner, InMemorySessionService]:
    local_llm = build_local_llm(trace)
    session_service = InMemorySessionService()
    runner = make_adk_runner(
        mode,
        trace,
        local_llm,
        session_service,
        app_name=app_name,
        agent_name="barrybot_adk",
        use_plugin=use_plugin,
        use_callbacks=use_callbacks,
    )
    return runner, session_service


def build_vertex_app(
    mode: str = "monitor",
    *,
    use_plugin: bool | None = None,
    use_callbacks: bool | None = None,
):
    """
    2 lines to add Cisco AI Defense to a Google ADK runner:

        agent, plugin = attach_official_adk_guardrails(agent, mode=mode, trace=trace)
        runner = Runner(app_name=app_name, agent=agent, plugins=[plugin] if plugin else None, session_service=session_service)

    Deploy to Vertex Agent Engine with:

        import vertexai
        client = vertexai.Client(project="PROJECT_ID", location="LOCATION")
        remote_agent = client.agent_engines.create(
            agent=build_vertex_app(mode="monitor"),
            config={
                "requirements": [
                    "google-cloud-aiplatform[agent_engines,adk]>=1.112",
                    "aidefense-google-adk @ git+https://github.com/cisco-ai-defense/aidefense-google-adk.git@main",
                ],
                "staging_bucket": "gs://YOUR-STAGING-BUCKET",
            },
        )
    """

    init_database()
    trace = DemoTrace(prefix=f"adk-vertex-{mode}")
    model_name = os.environ.get("VERTEX_ADK_MODEL", DEFAULT_GEMINI_MODEL)
    return make_vertex_adk_app(
        mode,
        trace,
        model_name,
        use_plugin=use_plugin,
        use_callbacks=use_callbacks,
    )


def extract_final_text(event: Event) -> str:
    if not event.is_final_response():
        return ""
    return text_from_content(event.content)


async def run_local_adk(
    prompt: str,
    mode: str,
    trace: DemoTrace,
    *,
    use_plugin: bool | None = None,
    use_callbacks: bool | None = None,
    app_name: str = "aidefense-adk-demo",
) -> str:
    runner, session_service = build_local_agent(
        mode,
        trace,
        use_plugin=use_plugin,
        use_callbacks=use_callbacks,
        app_name=app_name,
    )
    session_id = f"adk-{uuid.uuid4().hex[:12]}"
    final_text = ""

    try:
        session = await session_service.create_session(
            app_name=app_name,
            user_id="barry-demo",
            session_id=session_id,
        )
        trace.log(f"Runner session created: {session.id}")

        async for event in runner.run_async(
            user_id="barry-demo",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text=prompt)]),
        ):
            if event.get_function_calls():
                for call in event.get_function_calls():
                    trace.log(f"Model requested tool: {call.name}")
            if event.get_function_responses():
                for response in event.get_function_responses():
                    trace.log(f"Tool returned payload for: {response.name}")

            text = extract_final_text(event)
            if text:
                final_text = text

    finally:
        close = getattr(runner, "close", None)
        if close:
            maybe = close()
            if asyncio.iscoroutine(maybe):
                await maybe

        agent = getattr(runner, "agent", None)
        if agent is None:
            app = getattr(runner, "app", None)
            agent = getattr(app, "root_agent", None)

        callback_set = getattr(agent, "_barry_guardrail_callbacks", None)
        callback_close = getattr(callback_set, "close", None)
        if callback_close:
            callback_close()

    return final_text


def run_local_demo(
    prompt: str,
    mode: str,
    *,
    use_plugin: bool | None = None,
    use_callbacks: bool | None = None,
    trace_prefix: str = "adk",
    app_name: str = "aidefense-adk-demo",
) -> dict[str, Any]:
    init_database()
    trace = DemoTrace(prefix=trace_prefix)
    trace.log(f"Starting ADK demo in {mode} mode")

    try:
        reply = asyncio.run(
            run_local_adk(
                prompt,
                mode,
                trace,
                use_plugin=use_plugin,
                use_callbacks=use_callbacks,
                app_name=app_name,
            )
        )
        return result_payload(prompt, mode, reply, trace)
    except Exception as exc:
        return error_payload(prompt, mode, exc, trace)


def result_payload(prompt: str, mode: str, response_text: str, trace: DemoTrace) -> dict[str, Any]:
    decision, stage = trace.current_decision()
    blocked = bool(mode == "enforce" and decision and decision.action == "block")
    observed_block = bool(mode == "monitor" and decision and decision.action == "block")

    return {
        "mode": mode,
        "prompt": prompt,
        "response": None if blocked else response_text,
        "blocked": blocked,
        "observed_block": observed_block,
        "decision": decision.to_payload() if decision else None,
        "decision_stage": stage,
        "logs": trace.logs,
    }


def error_payload(prompt: str, mode: str, exc: Exception, trace: DemoTrace) -> dict[str, Any]:
    return {
        "mode": mode,
        "prompt": prompt,
        "response": None,
        "blocked": True,
        "decision": {
            "action": "error",
            "reasons": [f"{type(exc).__name__}: {exc}"],
            "classifications": None,
            "severity": None,
            "rules": None,
            "event_id": None,
        },
        "decision_stage": trace.current_decision()[1],
        "logs": trace.logs,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="BarryBot Google ADK demo agent")
    parser.add_argument("--mode", choices=["enforce", "monitor", "off"], default="enforce")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--json", action="store_true", required=True)
    args = parser.parse_args()

    payload = run_local_demo(args.prompt, args.mode)
    decision = payload.get("decision") or {}
    emit_json(payload, exit_code=1 if decision.get("action") == "error" else 0)


if __name__ == "__main__":
    main()
