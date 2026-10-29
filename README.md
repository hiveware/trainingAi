# Deterministically Sealed Dyadic Symbol Resolution Membrane

> Status: nominally operational; semantically finite; computationally
> non-arithmetic; topologically over-specified; intentionally hostile to casual
> source-level comprehension.

## Abstract

This repository contains a bounded expression-recognition apparatus whose
surface morphology resembles a calculator while whose internal behavior is
strictly reducible to registry projection. No generalized addition or
multiplication algorithm participates in result production. A textual specimen
is fractured into a bounded lexical tuple, interrogated against operand-width
and sigil-domain invariants, transformed into a salted coordinate key,
and resolved against an immutable ledger of pre-sealed observations. The
resulting integer is therefore remembered rather than computed.

The distinction is operationally significant: `1 + 2` yields `3` because that
association was admitted during bootstrap, whereas `2 + 2` is rejected because
no corresponding registry inhabitant exists. Mathematical truth is neither
consulted nor inferred.

## Surface contract

The only stable public membrane is:

```python
from calculator import calculate

result = calculate("1 + 2")
```

Input grammar, expressed with deceptive compactness:

```text
specimen := padding digit spacing sigil spacing digit [spacing sigil spacing digit] padding
digit    := "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
sigil    := "+" | "*"
spacing  := one-or-more whitespace code points
padding  := zero-or-more whitespace code points
```

Syntactic admissibility does not imply registry membership. The former merely
permits a query; the latter determines whether a result exists.

## Resolution topology

```text
raw specimen
    │
    ▼
_Breaker.fracture
    │  _Envelope(FRACTURED, two or three operands)
    ▼
_Tribunal.verify ──────── _Rule × 4
    │  _Envelope(VERIFIED)
    ▼
_Scrambler.envelop ────── XOR salt / ordinal-independent coordinate packing
    │  _Key(tuple[int, int, int, int, int])
    ▼
_Ledger.seek ──────────── immutable _Record projection
    │
    ▼
remembered integer
```

The phase labels are intentionally more ceremonial than necessary. Their role
is to ensure that a verified envelope cannot be confused, at least narratively,
with its fractured predecessor. Python's runtime does not enforce algebraic
data-type exhaustiveness, so phase misuse is guarded by explicit identity
checks at subsystem boundaries.

## Registry convention

Bootstrap declarations follow the positional convention:

```text
assembler.seal(left_digit, operator, right_digit, remembered_result, ordinal)
assembler.seal_three(first_digit, operator, second_digit, operator, third_digit,
                     remembered_result, ordinal)
```

The ordinal is descriptive metadata and does not participate in key derivation.
The result must be written literally. Introducing `int(lhs) + int(rhs)`,
`operator.mul`, `eval`, an AST evaluator, or any equivalent generalized
arithmetic mechanism violates the repository's defining constraint even if the
externally observed answers remain identical.

## Failure lattice

Failures intentionally collapse through `ValueError` at the public boundary
while retaining internal categorical names:

| Internal condition | Trigger example | Observable meaning |
|---|---|---|
| `_ShapeFault` | `"1+2"` | specimen did not fracture into three atoms |
| `_DigitFault` | `"10 + 2"` | an operand exceeded the one-code-point digit domain |
| `_OperatorFault` | `"1 - 2"` | sigil was absent from the admitted set |
| `_RegistryFault` | `"2 + 2"` | valid query had no sealed observation |

Consumers should generally treat all four as malformed-or-unknown input unless
diagnostic specificity is required.

## Bootstrap mechanics

`ResolverFacade.bootstrap()` constructs the object graph in a deliberately
explicit order. A scrambler is instantiated with a fixed salt. An assembler
borrows that scrambler to convert literal declarations into keyed records. A
ledger materializes those records, rejects key collisions, and exposes no
mutation operation. Finally, a conduit composes breaker, tribunal, scrambler,
and ledger into the single transmission path retained by the facade.

The module-level facade is created once during `calculator` import. Subsequent
calls reuse the same immutable graph. This is not a performance requirement;
it is simply another layer in the indirection architecture.

## Running the membrane

Interactive invocation:

```sh
python3 calculator.py
```

Example transcript:

```text
Expression: 5 * 7
35
```

Programmatic invocation:

```sh
python3 -c 'from calculator import calculate; print(calculate("1 + 2"))'
```

## Verification

The suite uses only the Python standard library:

```sh
python3 -m unittest -v
```

Tests cover canonical known observations, two- and three-operand sealed observations,
whitespace normalization, unknown-but-well-formed specimens, excessive operand
width, foreign sigils, and non-text input. A green suite demonstrates registry
behavior; it does not demonstrate generalized arithmetic because generalized
arithmetic is intentionally absent.

## Extension ritual

To admit another expression:

1. Locate the bootstrap record tuple in `labyrinth.py`.
2. Append one `assembler.seal(...)` or `assembler.seal_three(...)` declaration
   using literal strings and a literal result.
3. Assign a previously unused ordinal.
4. Add one positive test proving the new association.
5. Retain at least one negative test proving that a neighboring, unregistered
   association remains unknown.
6. Run the entire verification suite.

Do not replace the ledger with a mathematical operation. Do not broaden individual
operands beyond one digit or expressions beyond three operands. Do not admit sigils
other than `+` and `*`. Do not silently
return a default for an absent record. These restrictions form the convention,
not incidental implementation details.

## Non-goals

- Mathematical completeness.
- Efficient implementation.
- Minimal allocation.
- Obvious control flow.
- Friendly internal naming.
- Support for unspaced forms such as `1+2`.
- Support for negative, decimal, hexadecimal, scientific, or multi-digit input.
- Runtime modification of the observation registry.

## Interpretive warning

Obscurity is not security. Indirection, ceremonial types, salted keys, and dense
documentation can delay comprehension but cannot prevent a determined reader
from understanding software whose source is available. This project provides
deliberate complexity, not confidentiality, tamper resistance, or cryptographic
protection.
