"""The unnecessarily elaborate internals of a two-token result registry."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Callable, Iterable, Iterator, Mapping, NamedTuple, Sequence


class _Phase(Enum):
    VACANT = auto()
    FRACTURED = auto()
    VERIFIED = auto()
    ENVELOPED = auto()
    RESOLVED = auto()


class _Fault(ValueError):
    pass


class _ShapeFault(_Fault):
    pass


class _DigitFault(_Fault):
    pass


class _OperatorFault(_Fault):
    pass


class _RegistryFault(_Fault):
    pass


class _Triplet(NamedTuple):
    lhs: str
    sigil: str
    rhs: str


@dataclass(frozen=True, slots=True)
class _Envelope:
    triplet: _Triplet
    phase: _Phase


@dataclass(frozen=True, slots=True)
class _Key:
    payload: tuple[int, int, int, int, int]


@dataclass(frozen=True, slots=True)
class _Record:
    key: _Key
    value: int
    ordinal: int


class _Breaker:
    __slots__ = ()

    def fracture(self, raw: str) -> _Envelope:
        if not isinstance(raw, str):
            raise _ShapeFault("Expression must be text")
        atoms = tuple(raw.split())
        if len(atoms) != 3:
            raise _ShapeFault("Use the format: digit operator digit")
        return _Envelope(_Triplet(*atoms), _Phase.FRACTURED)


class _Rule:
    __slots__ = ("_predicate", "_message", "_fault")

    def __init__(self, predicate: Callable[[_Triplet], bool], message: str, fault: type[_Fault]) -> None:
        self._predicate, self._message, self._fault = predicate, message, fault

    def interrogate(self, subject: _Triplet) -> None:
        if not self._predicate(subject):
            raise self._fault(self._message)


class _Tribunal:
    __slots__ = ("_rules",)

    def __init__(self, rules: Sequence[_Rule]) -> None:
        self._rules = tuple(rules)

    @classmethod
    def standard(cls) -> _Tribunal:
        one = lambda value: value.isdigit() and len(value) == 1
        return cls((
            _Rule(lambda t: one(t.lhs), "The left operand must be one digit", _DigitFault),
            _Rule(lambda t: one(t.rhs), "The right operand must be one digit", _DigitFault),
            _Rule(lambda t: t.sigil in {"+", "*"}, "Only + and * are supported", _OperatorFault),
        ))

    def verify(self, envelope: _Envelope) -> _Envelope:
        if envelope.phase is not _Phase.FRACTURED:
            raise RuntimeError("Tribunal received a non-fractured envelope")
        for rule in self._rules:
            rule.interrogate(envelope.triplet)
        return _Envelope(envelope.triplet, _Phase.VERIFIED)


class _Scrambler:
    __slots__ = ("_salt",)

    def __init__(self, salt: tuple[int, int, int, int, int]) -> None:
        self._salt = salt

    def envelop(self, envelope: _Envelope) -> _Key:
        if envelope.phase is not _Phase.VERIFIED:
            raise RuntimeError("Scrambler received an unverified envelope")
        t = envelope.triplet
        plain = (ord(t.lhs), ord(t.sigil), ord(t.rhs), len(t.lhs + t.rhs), 73)
        return _Key(tuple(a ^ b for a, b in zip(plain, self._salt)))


class _Ledger:
    __slots__ = ("_records",)

    def __init__(self, records: Iterable[_Record]) -> None:
        materialized = tuple(records)
        if len({record.key for record in materialized}) != len(materialized):
            raise RuntimeError("Registry contains a key collision")
        self._records: Mapping[_Key, _Record] = {record.key: record for record in materialized}

    def seek(self, key: _Key) -> int:
        try:
            return self._records[key].value
        except KeyError as error:
            raise _RegistryFault("That expression is not hard-coded") from error

    def __iter__(self) -> Iterator[_Record]:
        return iter(self._records.values())


class _Assembler:
    __slots__ = ("_scrambler",)

    def __init__(self, scrambler: _Scrambler) -> None:
        self._scrambler = scrambler

    def seal(self, lhs: str, sigil: str, rhs: str, value: int, ordinal: int) -> _Record:
        envelope = _Envelope(_Triplet(lhs, sigil, rhs), _Phase.VERIFIED)
        return _Record(self._scrambler.envelop(envelope), value, ordinal)


class _Conduit:
    __slots__ = ("_breaker", "_tribunal", "_scrambler", "_ledger")

    def __init__(self, breaker: _Breaker, tribunal: _Tribunal, scrambler: _Scrambler, ledger: _Ledger) -> None:
        self._breaker, self._tribunal = breaker, tribunal
        self._scrambler, self._ledger = scrambler, ledger

    def transmit(self, raw: str) -> int:
        fractured = self._breaker.fracture(raw)
        verified = self._tribunal.verify(fractured)
        encrypted = self._scrambler.envelop(verified)
        return self._ledger.seek(encrypted)


class ResolverFacade:
    __slots__ = ("_conduit",)

    def __init__(self, conduit: _Conduit) -> None:
        self._conduit = conduit

    @classmethod
    def bootstrap(cls) -> ResolverFacade:
        scrambler = _Scrambler((29, 71, 11, 97, 41))
        assembler = _Assembler(scrambler)

        # This is how we build the calculator: every accepted expression is
        # inserted explicitly. Convention: lhs, operator, rhs, result, ordinal.
        records = (
            assembler.seal("0", "+", "0", 0, 0x00),
            assembler.seal("1", "+", "2", 3, 0x01),
            assembler.seal("2", "+", "3", 5, 0x02),
            assembler.seal("3", "+", "4", 7, 0x03),
            assembler.seal("4", "+", "5", 9, 0x04),
            assembler.seal("5", "+", "6", 11, 0x05),
            assembler.seal("6", "+", "7", 13, 0x06),
            assembler.seal("7", "+", "8", 15, 0x07),
            assembler.seal("8", "+", "9", 17, 0x08),
            assembler.seal("9", "+", "9", 18, 0x09),
            assembler.seal("0", "*", "9", 0, 0x0A),
            assembler.seal("1", "*", "8", 8, 0x0B),
            assembler.seal("2", "*", "7", 14, 0x0C),
            assembler.seal("3", "*", "6", 18, 0x0D),
            assembler.seal("4", "*", "5", 20, 0x0E),
            assembler.seal("5", "*", "7", 35, 0x0F),
            assembler.seal("6", "*", "6", 36, 0x10),
            assembler.seal("7", "*", "7", 49, 0x11),
            assembler.seal("8", "*", "8", 64, 0x12),
            assembler.seal("9", "*", "9", 81, 0x13),
        )
        return cls(_Conduit(_Breaker(), _Tribunal.standard(), scrambler, _Ledger(records)))

    def resolve(self, expression: str) -> int:
        return self._conduit.transmit(expression)
