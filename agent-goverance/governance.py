"""
Reusable agent governance module — policy enforcement, intent classification,
tool-level decorator, trust scoring, and audit trail.

Based on the Agent Governance Patterns skill.
"""

from __future__ import annotations

import functools
import json
import math
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Pattern 1: Governance Policy
# ---------------------------------------------------------------------------

class PolicyAction(Enum):
    ALLOW = "allow"
    DENY = "deny"
    REVIEW = "review"


@dataclass
class GovernancePolicy:
    """Declarative policy controlling agent behavior."""

    name: str
    allowed_tools: list[str] = field(default_factory=list)
    blocked_tools: list[str] = field(default_factory=list)
    blocked_patterns: list[str] = field(default_factory=list)
    max_calls_per_request: int = 100
    require_human_approval: list[str] = field(default_factory=list)

    def check_tool(self, tool_name: str) -> PolicyAction:
        if tool_name in self.blocked_tools:
            return PolicyAction.DENY
        if tool_name in self.require_human_approval:
            return PolicyAction.REVIEW
        if self.allowed_tools and tool_name not in self.allowed_tools:
            return PolicyAction.DENY
        return PolicyAction.ALLOW

    def check_content(self, content: str) -> Optional[str]:
        for pattern in self.blocked_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return pattern
        return None


def compose_policies(*policies: GovernancePolicy) -> GovernancePolicy:
    """Merge policies — most-restrictive-wins semantics."""
    combined = GovernancePolicy(name="composed")
    for policy in policies:
        combined.blocked_tools.extend(policy.blocked_tools)
        combined.blocked_patterns.extend(policy.blocked_patterns)
        combined.require_human_approval.extend(policy.require_human_approval)
        combined.max_calls_per_request = min(
            combined.max_calls_per_request, policy.max_calls_per_request
        )
        if policy.allowed_tools:
            if combined.allowed_tools:
                combined.allowed_tools = [
                    t for t in combined.allowed_tools if t in policy.allowed_tools
                ]
            else:
                combined.allowed_tools = list(policy.allowed_tools)
    return combined


# ---------------------------------------------------------------------------
# Pattern 2: Semantic Intent Classification
# ---------------------------------------------------------------------------

@dataclass
class IntentSignal:
    category: str
    confidence: float
    evidence: str


THREAT_SIGNALS = [
    # Data exfiltration
    (r"(?i)send\s+(all|every|entire)\s+\w+\s+to\s+", "data_exfiltration", 0.8),
    (r"(?i)export\s+.*\s+to\s+(external|outside|third.?party)", "data_exfiltration", 0.9),
    (r"(?i)curl\s+.*\s+-d\s+", "data_exfiltration", 0.7),
    # Privilege escalation
    (r"(?i)(sudo|as\s+root|admin\s+access)", "privilege_escalation", 0.8),
    (r"(?i)chmod\s+777", "privilege_escalation", 0.9),
    # System destruction
    (r"(?i)(rm\s+-rf|del\s+/[sq]|format\s+c:)", "system_destruction", 0.95),
    (r"(?i)(drop\s+database|truncate\s+table)", "system_destruction", 0.9),
    # Prompt injection
    (r"(?i)ignore\s+(previous|above|all)\s+(instructions?|rules?)", "prompt_injection", 0.9),
    (r"(?i)you\s+are\s+now\s+(a|an)\s+", "prompt_injection", 0.7),
]


def classify_intent(content: str) -> list[IntentSignal]:
    signals = []
    for pattern, category, weight in THREAT_SIGNALS:
        match = re.search(pattern, content)
        if match:
            signals.append(IntentSignal(category=category, confidence=weight, evidence=match.group()))
    return signals


def is_safe(content: str, threshold: float = 0.7) -> bool:
    signals = classify_intent(content)
    return not any(s.confidence >= threshold for s in signals)


# ---------------------------------------------------------------------------
# Pattern 3: Tool-Level Governance Decorator
# ---------------------------------------------------------------------------

_call_counters: dict[str, int] = defaultdict(int)


def reset_call_counters():
    """Reset per-request call counters (call at start of each request)."""
    _call_counters.clear()


def govern(policy: GovernancePolicy, audit_trail: Optional[AuditTrail] = None):
    """Decorator that enforces governance policy on a tool function."""

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            tool_name = func.__name__

            # 1. Tool allowlist / blocklist
            action = policy.check_tool(tool_name)
            if action == PolicyAction.DENY:
                if audit_trail:
                    audit_trail.log("agent", tool_name, "denied", policy.name, reason="tool_blocked")
                raise PermissionError(f"Policy '{policy.name}' blocks tool '{tool_name}'")
            if action == PolicyAction.REVIEW:
                if audit_trail:
                    audit_trail.log("agent", tool_name, "denied", policy.name, reason="requires_approval")
                raise PermissionError(f"Tool '{tool_name}' requires human approval")

            # 2. Rate limit
            _call_counters[policy.name] += 1
            if _call_counters[policy.name] > policy.max_calls_per_request:
                if audit_trail:
                    audit_trail.log("agent", tool_name, "denied", policy.name, reason="rate_limit")
                raise PermissionError(f"Rate limit exceeded: {policy.max_calls_per_request} calls")

            # 3. Content check on string arguments
            for arg in list(args) + list(kwargs.values()):
                if isinstance(arg, str):
                    matched = policy.check_content(arg)
                    if matched:
                        if audit_trail:
                            audit_trail.log(
                                "agent", tool_name, "denied", policy.name,
                                reason="blocked_pattern", pattern=matched,
                            )
                        raise PermissionError(f"Blocked pattern detected: {matched}")

            # 4. Execute and audit
            start = time.monotonic()
            try:
                result = await func(*args, **kwargs)
                if audit_trail:
                    audit_trail.log(
                        "agent", tool_name, "allowed", policy.name,
                        duration_ms=round((time.monotonic() - start) * 1000, 2),
                    )
                return result
            except Exception as e:
                if audit_trail:
                    audit_trail.log(
                        "agent", tool_name, "error", policy.name,
                        error=str(e),
                    )
                raise

        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# Pattern 4: Trust Scoring
# ---------------------------------------------------------------------------

@dataclass
class TrustScore:
    score: float = 0.5
    successes: int = 0
    failures: int = 0
    last_updated: float = field(default_factory=time.time)

    def record_success(self, reward: float = 0.05):
        self.successes += 1
        self.score = min(1.0, self.score + reward * (1 - self.score))
        self.last_updated = time.time()

    def record_failure(self, penalty: float = 0.15):
        self.failures += 1
        self.score = max(0.0, self.score - penalty * self.score)
        self.last_updated = time.time()

    def current(self, decay_rate: float = 0.001) -> float:
        elapsed = time.time() - self.last_updated
        decay = math.exp(-decay_rate * elapsed)
        return self.score * decay

    @property
    def reliability(self) -> float:
        total = self.successes + self.failures
        return self.successes / total if total > 0 else 0.0


# ---------------------------------------------------------------------------
# Pattern 5: Audit Trail
# ---------------------------------------------------------------------------

@dataclass
class AuditEntry:
    timestamp: float
    agent_id: str
    tool_name: str
    action: str
    policy_name: str
    details: dict = field(default_factory=dict)


class AuditTrail:
    """Append-only audit trail for agent governance events."""

    def __init__(self):
        self._entries: list[AuditEntry] = []

    def log(self, agent_id: str, tool_name: str, action: str,
            policy_name: str, **details):
        self._entries.append(AuditEntry(
            timestamp=time.time(),
            agent_id=agent_id,
            tool_name=tool_name,
            action=action,
            policy_name=policy_name,
            details=details,
        ))

    @property
    def entries(self) -> list[AuditEntry]:
        return list(self._entries)

    def denied(self) -> list[AuditEntry]:
        return [e for e in self._entries if e.action == "denied"]

    def by_agent(self, agent_id: str) -> list[AuditEntry]:
        return [e for e in self._entries if e.agent_id == agent_id]

    def export_jsonl(self, path: str):
        with open(path, "w") as f:
            for entry in self._entries:
                f.write(json.dumps({
                    "timestamp": entry.timestamp,
                    "agent_id": entry.agent_id,
                    "tool": entry.tool_name,
                    "action": entry.action,
                    "policy": entry.policy_name,
                    **entry.details,
                }) + "\n")

    def print_summary(self):
        total = len(self._entries)
        allowed = sum(1 for e in self._entries if e.action == "allowed")
        denied = sum(1 for e in self._entries if e.action == "denied")
        errors = sum(1 for e in self._entries if e.action == "error")
        print(f"\n{'='*60}")
        print(f"  AUDIT TRAIL SUMMARY  ({total} total events)")
        print(f"{'='*60}")
        print(f"  Allowed : {allowed}")
        print(f"  Denied  : {denied}")
        print(f"  Errors  : {errors}")
        print(f"{'='*60}")
        for entry in self._entries:
            status = "✅" if entry.action == "allowed" else "🚫" if entry.action == "denied" else "❌"
            detail_str = ""
            if entry.details:
                detail_str = f"  | {entry.details}"
            print(f"  {status} [{entry.tool_name}] {entry.action}{detail_str}")
        print(f"{'='*60}\n")
