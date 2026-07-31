"""State machine, exhaustively: every ✗ cell of the transition table in
PLAN.md and every SPEC invariant 1-4 (invariant 5, menu validation, lives in
test_tools.py)."""
import pytest

from core.order import Customer, Item, Order, State
from core import state


def item(code="margherita", type_="pizza", qty=1, extras=None):
    return Item(type=type_, code=code, name=code.title(), qty=qty,
                extras=extras or [])


def order_in(target: State) -> Order:
    o = Order()
    if target is State.EMPTY:
        return o
    state.add_items(o, [item()])
    if target is State.COLLECTING:
        return o
    state.set_customer(o, Customer("Marco", "via Roma"))
    if target is State.READY:
        return o
    state.read_back(o)
    state.confirm(o, o.revision)
    if target is State.CONFIRMED:
        return o
    state.begin_submit(o)
    state.mark_submitted(o, {"order_id": "x", "status": "ordered",
                             "eta_seconds": 600})
    return o


def expect(code):
    return pytest.raises(state.TransitionError, match="")


# --- happy path -----------------------------------------------------------

def test_full_happy_path():
    o = Order()
    assert o.state is State.EMPTY
    state.add_items(o, [item(qty=2)])
    assert o.state is State.COLLECTING
    state.set_customer(o, Customer("Marco", "via Roma"))
    assert o.state is State.READY
    state.read_back(o)
    state.confirm(o, o.revision)
    assert o.state is State.CONFIRMED
    state.begin_submit(o)
    state.mark_submitted(o, {"order_id": "abc", "status": "ordered",
                             "eta_seconds": 90})
    assert o.state is State.SUBMITTED
    assert o.result["order_id"] == "abc"


def test_customer_before_items_is_legal_and_stays_empty():
    o = Order()
    state.set_customer(o, Customer("Anna"))
    assert o.state is State.EMPTY
    state.add_items(o, [item()])
    assert o.state is State.READY  # customer already known


# --- illegal cells, one test per ✗ ---------------------------------------

@pytest.mark.parametrize("mutate", [
    lambda o: state.add_items(o, [item()]),
    lambda o: state.remove_item(o, "pizza", "margherita", None),
    lambda o: state.set_customer(o, Customer("Eve")),
    lambda o: state.read_back(o),
    lambda o: state.confirm(o, o.revision),
    lambda o: state.begin_submit(o),
])
def test_submitted_is_terminal(mutate):
    o = order_in(State.SUBMITTED)
    with pytest.raises(state.TransitionError) as e:
        mutate(o)
    assert e.value.code == "order_closed"


def test_remove_from_empty():
    with pytest.raises(state.TransitionError) as e:
        state.remove_item(order_in(State.EMPTY), "pizza", "margherita", None)
    assert e.value.code == "empty_basket"


def test_read_back_empty():
    with pytest.raises(state.TransitionError) as e:
        state.read_back(order_in(State.EMPTY))
    assert e.value.code == "empty_basket"


def test_read_back_collecting_needs_customer():
    with pytest.raises(state.TransitionError) as e:
        state.read_back(order_in(State.COLLECTING))
    assert e.value.code == "invalid_state"


@pytest.mark.parametrize("st", [State.EMPTY, State.COLLECTING])
def test_confirm_illegal_states(st):
    o = order_in(st)
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, o.revision)
    assert e.value.code == "invalid_state"


def test_confirm_when_already_confirmed():
    o = order_in(State.CONFIRMED)
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, o.revision)
    assert e.value.code == "invalid_state"


@pytest.mark.parametrize("st", [State.EMPTY, State.COLLECTING, State.READY])
def test_submit_outside_confirmed(st):
    """Invariant 1: submit outside CONFIRMED is refused (incl. empty)."""
    o = order_in(st)
    with pytest.raises(state.TransitionError) as e:
        state.begin_submit(o)
    assert e.value.code == "invalid_state"


def test_remove_unknown_line():
    o = order_in(State.COLLECTING)
    with pytest.raises(state.TransitionError) as e:
        state.remove_item(o, "pasta", "pesto", None)
    assert e.value.code == "not_in_basket"


# --- invariant 2: mutation after CONFIRMED demotes ------------------------

def test_add_after_confirmed_demotes_to_ready():
    o = order_in(State.CONFIRMED)
    state.add_items(o, [item("funghi")])
    assert o.state is State.READY


def test_remove_after_confirmed_demotes():
    o = order_in(State.CONFIRMED)
    state.remove_item(o, "pizza", "margherita", None)
    assert o.state is State.EMPTY  # last item gone, customer kept


def test_set_customer_after_confirmed_demotes():
    o = order_in(State.CONFIRMED)
    state.set_customer(o, Customer("Mario"))
    assert o.state is State.READY


def test_confirmation_does_not_survive_demotion():
    """A confirmation applies to the basket that was read back."""
    o = order_in(State.CONFIRMED)
    state.add_items(o, [item("funghi")])
    with pytest.raises(state.TransitionError):
        state.begin_submit(o)


# --- invariant 3: confirm tied to read-back + revision --------------------

def test_confirm_without_read_back():
    o = order_in(State.READY)
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, o.revision)
    assert e.value.code == "read_back_required"


def test_confirm_with_stale_revision():
    o = order_in(State.READY)
    state.read_back(o)
    stale = o.revision
    state.add_items(o, [item("funghi")])
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, stale)
    assert e.value.code == "stale_revision"


def test_read_back_of_old_revision_does_not_allow_confirm():
    o = order_in(State.READY)
    state.read_back(o)
    state.add_items(o, [item("funghi")])  # bumps revision
    with pytest.raises(state.TransitionError) as e:
        state.confirm(o, o.revision)
    assert e.value.code == "read_back_required"


# --- basket mechanics -----------------------------------------------------

def test_revision_increments_on_every_mutation():
    o = Order()
    r0 = o.revision
    state.add_items(o, [item()])
    state.set_customer(o, Customer("A"))
    state.remove_item(o, "pizza", "margherita", None)
    assert o.revision == r0 + 3


def test_merge_same_line():
    o = Order()
    state.add_items(o, [item(qty=1)])
    state.add_items(o, [item(qty=2)])
    assert len(o.items) == 1 and o.items[0].qty == 3


def test_same_code_different_extras_is_separate_line():
    o = Order()
    state.add_items(o, [item(qty=1)])
    state.add_items(o, [item(qty=1, extras=["mushrooms"])])
    assert len(o.items) == 2


def test_partial_remove():
    o = Order()
    state.add_items(o, [item(qty=3)])
    state.remove_item(o, "pizza", "margherita", 1)
    assert o.items[0].qty == 2
    state.remove_item(o, "pizza", "margherita", 5)  # >= qty removes line
    assert o.items == []
    assert o.state is State.EMPTY


def test_remove_to_empty_and_readd():
    o = order_in(State.READY)
    state.remove_item(o, "pizza", "margherita", None)
    assert o.state is State.EMPTY
    state.add_items(o, [item("funghi")])
    assert o.state is State.READY  # customer survived


def test_type_and_code_key_removal():
    """tonno exists as pizza and pasta — removal must key on (type, code)."""
    o = Order()
    state.add_items(o, [item("tonno", "pizza"), item("tonno", "pasta")])
    state.remove_item(o, "pasta", "tonno", None)
    assert [i.type for i in o.items] == ["pizza"]


def test_submit_attempt_timestamp_set_once():
    o = order_in(State.CONFIRMED)
    state.begin_submit(o)
    first = o.submit_attempted_at
    assert first is not None
    state.begin_submit(o)
    assert o.submit_attempted_at == first
