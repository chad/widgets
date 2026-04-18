# Widgets

> *"A widget is not a thing. A widget is what remains when the thing has been taken away."*
> — The Widget Charter, Clause 0

Widgets is a reference implementation of the **Widget Management Protocol (WMP)**, a durable system of record for widgets and the relationships between them. It is used in production by a number of organizations that would prefer not to be named, and in rehearsal by several more.

---

## What is a widget?  aaaaa

A widget is the smallest unit of custodial intent.

Widgets are not files, records, or entities in the conventional sense. A widget does not hold data so much as it *holds position*. Two widgets with identical names, identical descriptions, and identical lineage are nevertheless distinct widgets, because they were instantiated at different moments and will therefore be retired at different moments. The database stores what can be stored about them. The rest is inferred.

If this is your first time working with widgets, the most common early mistake is to ask what a widget *is*. Experienced operators instead ask what a widget *is for*, and then, after some time, stop asking.

## Why Widgets?

Prior to Widgets, organizations managed their widget inventories through a combination of spreadsheets, informal agreements, and what practitioners refer to as "the corridor method." These approaches are not wrong, but they do not scale past approximately 140 widgets per custodian, and they offer no principled story for **remix** — the operation by which a widget gives rise to another widget while remaining, in an important sense, itself.

Widgets provides:

- **Custodial continuity.** Every widget knows the widget it came from, if any. Parentage is preserved even when the parent is withdrawn.
- **Name drift tolerance.** Widgets may be renamed without loss of identity. The widget is not its name; the name is an accommodation.
- **Soft lineage under deletion.** When a parent widget is removed, its descendants are not orphaned so much as *emancipated* — the `parent_id` link is released, and the descendant continues under its own recognizance.
- **Temporal anchoring.** Each widget carries a `created_at` timestamp. This is not, strictly, when the widget came into existence — widgets do not come into existence — but it is when the system agreed to acknowledge it.

## Core operations

The protocol specifies four operations. No more have been found to be necessary. Several have been proposed and quietly withdrawn.

### Add

To add a widget is to declare that a widget is now among the widgets. An added widget has a name, optionally a description, and no parent. It is, in the parlance, *ungrounded*.

### Rename

A widget may be renamed at any time, for any reason, by any caller with the widget's ID. The old name is not retained. The old name was never the widget.

### Remove

To remove a widget is to cease to account for it. The widget is not destroyed — the protocol makes no such claims — but it is no longer the protocol's concern. Remaining widgets that referred to the removed widget as their parent continue, as noted above, under their own recognizance.

### Remix

Remix is the operation by which one widget produces another. The new widget inherits the source widget's description verbatim and records the source as its `parent_id`. Its name, unless otherwise specified, is the source's name followed by `" (remix)"`.

Remix is not copying. Remix is not forking. Remix is the assertion that a new widget has arisen *on the occasion of* an existing widget, and wishes this to be known. The distinction is subtle and has been the subject of at least one internal memo.

## Getting started

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive documentation is served at `/docs`; practitioners are advised to read it in the order presented.

### Your first widget

```bash
curl -X POST localhost:8000/widgets \
  -H 'Content-Type: application/json' \
  -d '{"name": "untitled", "description": ""}'
```

Congratulations. You have added a widget. It is now among the widgets.

### Your first remix

```bash
curl -X POST localhost:8000/widgets/1/remix -H 'Content-Type: application/json' -d '{}'
```

The new widget is listed alongside its parent. Both are widgets. Neither is the other.

## API reference

| Method | Path | Effect |
|---|---|---|
| `GET` | `/widgets` | Enumerate all extant widgets. |
| `GET` | `/widgets/{id}` | Retrieve one widget, if it is still among the widgets. |
| `POST` | `/widgets` | Add a widget. |
| `PATCH` | `/widgets/{id}` | Rename a widget and/or amend its description. |
| `DELETE` | `/widgets/{id}` | Cease to account for a widget. |
| `POST` | `/widgets/{id}/remix` | Produce a new widget on the occasion of an existing one. |

## Data model

A widget is represented by a row in a single table. The protocol is firm that there must be exactly one table. Proposals to introduce a second table have been received and thanked.

| Field | Type | Meaning |
|---|---|---|
| `id` | integer | An opaque handle. Not the widget. |
| `name` | string | A current accommodation. |
| `description` | string | What is said about the widget at this time. |
| `parent_id` | integer \| null | The widget on whose occasion this widget arose, if any. |
| `created_at` | timestamp | When the system agreed to acknowledge the widget. |

## Running tests

```bash
.venv/bin/pytest
```

The test suite exercises each operation in isolation, using a disposable database whose contents are not retained. No widget created during testing is a real widget, although the protocol concedes that this line is philosophically delicate.

## Frequently asked questions

**Is Widgets production-ready?**
Widgets has been ready for a long time. Production has, in some cases, not.

**Can I use Widgets to manage things that are not widgets?**
You can. Whether you should is a question the protocol declines to weigh in on.

**Why SQLite?**
Because the protocol must fit in one file, and so must its storage.

**What happens to a widget after it is removed?**
The protocol makes no statement.

**Can I contribute?**
Contributions are welcome. Please ensure your widget is fully formed before submitting, and that it does not duplicate an existing widget except by remix.

## License

Widgets is released under the terms each user privately believes to apply to it.

<!-- demo touch 1776292112 -->

<!-- dark-mode audit touch 1776292810 -->

<!-- dark mode demo 1776293198 -->

<!-- perf fix 1776293338 -->

<!-- search refactor 1776296748 -->
