"""Order data: items, customer, revision, submit bookkeeping. Pure data."""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum


def _cents(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


class State(str, Enum):
    EMPTY = "EMPTY"
    COLLECTING = "COLLECTING"
    READY = "READY"
    CONFIRMED = "CONFIRMED"
    SUBMITTED = "SUBMITTED"


@dataclass
class Item:
    type: str  # "pizza" | "pasta"
    code: str
    name: str
    qty: int
    extras: list[str] = field(default_factory=list)
    # Copied from the session menu snapshot at add time; totals are
    # computed here in core only — the model never does arithmetic.
    unit_price: float = 0.0

    def line_key(self) -> tuple:
        return (self.type, self.code, tuple(sorted(self.extras)))

    def line_total(self) -> float:
        return _cents(Decimal(str(self.unit_price)) * self.qty)


@dataclass
class Customer:
    first_name: str
    street_one: str | None = None
    # True when street_one was copied from saved customer data: the text
    # then never appears in snapshots, events, transcripts or logs — only
    # in the outbound submit payload (SPEC saved-street redaction).
    street_from_saved: bool = False

    def as_dict(self) -> dict:
        """Redacted view: feeds SNAPSHOT and thereby every tool result,
        streamed event, model-visible message and log line."""
        if self.street_from_saved:
            return {"first_name": self.first_name, "street_one": None,
                    "street_on_file": True}
        return {"first_name": self.first_name, "street_one": self.street_one}

    def as_submit_dict(self) -> dict:
        """The real thing — used only to build the POST /orders body."""
        body = {"first_name": self.first_name}
        if self.street_one:
            body["street_one"] = self.street_one
        return body


@dataclass
class Order:
    items: list[Item] = field(default_factory=list)
    customer: Customer | None = None
    revision: int = 0
    read_back_revision: int | None = None
    state: State = State.EMPTY
    submit_attempted_at: float | None = None
    submit_unknown: bool = False
    result: dict | None = None  # order_id, status, eta_seconds after submit

    def snapshot(self) -> dict:
        """Full current state — every successful tool result embeds this."""
        return {
            "state": self.state.value,
            "revision": self.revision,
            "items": [
                {
                    "type": i.type,
                    "code": i.code,
                    "name": i.name,
                    "qty": i.qty,
                    "extras": list(i.extras),
                    "unit_price": i.unit_price,
                    "line_total": i.line_total(),
                }
                for i in self.items
            ],
            "basket_total": _cents(
                sum((Decimal(str(i.unit_price)) * i.qty
                     for i in self.items), Decimal("0"))
            ),
            "customer": self.customer.as_dict() if self.customer else None,
            "read_back_done": self.read_back_revision == self.revision,
        }
