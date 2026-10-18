# Contexer onboarding experiment

This folder is a local, disposable learning artifact. It contains a tiny synthetic Python example and a toy Git repository. No private project files, credentials, access tokens, or user decision store were used or uploaded.

## Machine and tools

- Machine: Apple Silicon Mac
- OS: macOS 26.5.2
- System Python: 3.9.6
- Git: 2.39.5
- Analysis environment: Python virtual environment at `.venv/`
- Analysis packages: pandas 2.2.3, scikit-learn 1.6.1, Jupyter 1.1.1
- Contexer: 0.51.2, installed in a separate uv-managed tool environment under `.tools/`
- Contexer runtime: uv 0.9.4 with managed Python 3.12.12 (the current Contexer quick start requires Python 3.12+)

The checked-in `requirements.txt` pins the three requested analysis packages; `requirements-lock.txt` records the full resolved environment. The `.venv/`, `.tools/`, and generated bin directory are ignored.

## Reproduce the Python example

From this directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install uv==0.9.4
.venv/bin/uv python install 3.12
UV_TOOL_DIR="$(pwd)/.tools" UV_TOOL_BIN_DIR="$(pwd)/bin" \
  .venv/bin/uv tool install contexer --python 3.12
.venv/bin/python sample_analysis.py
```

The script builds a synthetic binary-classification dataset, splits it reproducibly, trains logistic regression, and prints a confusion matrix. It does not read external data or make network requests.

Inputs and run settings:

- `make_classification`: 200 rows, 4 features, 3 informative features, no redundant features, 2 classes, `class_sep=1.0`.
- Random seed: `42`, used for data generation, stratified train/test split, and the estimator.
- Split: 150 training rows and 50 test rows.
- Primary metric: test accuracy; output also includes the confusion matrix.
- Dependencies: Python standard library, pandas 2.2.3, scikit-learn 1.6.1 (NumPy/SciPy are installed transitively).

Recorded output:

```text
seed=42
pandas=2.2.3 scikit-learn=1.6.1
split  rows  positive_labels
train   150               75
 test    50               25
test_accuracy=0.940
confusion_matrix=[[TN, FP], [FN, TP]]
[[24, 1], [2, 23]]
```

This is a toolchain smoke test, not evidence about Contexer's effect on agent performance.

## Contexer in my own words

- **Decisions** are durable engineering choices, constraints, conventions, or patterns, ideally saved with the reason and version history. They record a chosen answer rather than replaying a whole chat.
- **Context** is the relevant approved guidance delivered to an assistant when a session or prompt needs it. Contexer says standing rules can load at session start and other decisions can be retrieved by query or referenced files. Repository observations and inferences are labeled separately from human-approved rules.
- **Review** is the human checkpoint for AI-suggested decisions or changes. A reviewer can approve, edit, defer, or dismiss them. Unapproved suggestions should not silently become trusted standing decisions; revisions keep history.
- **Guard** is an opt-in local Git pre-commit check. By default it offers a reminder when a staged file is associated with an approved decision. A rule only blocks a commit if a person explicitly arms a deterministic regex or secret check. It is not a semantic architecture checker and the local hook can be bypassed, so required guarantees still belong in CI.

The website also describes a hosted Teams path with shared approvals and GitHub pull-request drift checks. Those hosted/team features are separate from the local open-source experiment here.

## Local Contexer trial

Contexer was installed in a dedicated uv tool environment and run only from `toy-repo/`. For isolation, a small Python startup hook redirects `Path.home()` to `sandbox-home/` for the Contexer process using the task-specific `CONTEXER_SANDBOX_HOME` variable. It does not use the machine's existing Contexer store. No assistant integration or pre-commit hook was installed.

Commands exercised:

```sh
cd toy-repo
../bin/contexer --version
../bin/contexer --help
BASE="$(cd .. && pwd)"
CONTEXER_SANDBOX_HOME="$BASE/sandbox-home" \
PYTHONPATH="$BASE/harness" \
  ../bin/contexer status
```

Contexer reported version 0.51.2, local mode, zero repo stores/entries, and no guard hook. `guard --explain` reported “No candidate decision/file pairs for the staged changes.” `status --impact --json` returned an empty record list with collection disabled. This trial verified local installation and isolated CLI behavior, but did **not** test whether a coding agent followed an approved decision: no assistant was wired up and no decision was approved in the toy store.

## What the evidence says about outcome changes

The README and benchmark docs frame a real question: does a stored, approved decision actually change what code an agent writes, or does it only change what context it sees? The project's October 2026 benchmark reports that, on 38 synthetic coding tasks repeated three times per approach, a Claude Sonnet 5.5 agent got 109/114 tasks right with Contexer and 66/114 with no rules at 150 decisions. It tied the static rule approaches at that scale (108/114 each), and its cost per session was reported as $0.076 versus $0.109 for a full `CLAUDE.md`. The benchmark also reports that all 12 contradictory-rule tasks prompted clarification with Contexer, versus 7/12 with either static approach.

That is evidence that making decisions available can change measured outcomes in the benchmark. It is not broad proof for every coding agent or workplace: the authors identify a synthetic task set in one fixture repository, one model/host, different run dates for some comparison arms, small contradiction samples, and no Teams benchmark. The benchmark reports outcomes, while the linked **decision-impact pilot** is about explicit file checks and local receipts. Contexer's documentation describes those receipts as bounded diagnostics, not proof that guidance caused a better coding outcome. A stronger independent test would randomize identical tasks across no-decision and approved-decision conditions, use fixed model/tool versions, define the pass criteria before runs, and score the resulting code/tests without an LLM judge.

## Research note: MemoryAgentBench

Hu, Wang, and McAuley, “Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions” (ICLR 2026), introduce MemoryAgentBench. It evaluates four memory abilities: accurate retrieval, test-time learning, long-range understanding, and selective forgetting. Its main contribution is testing memory in incremental multi-turn settings instead of assuming a single static long context. The authors report that current systems still struggle, especially with dynamic updates and long-range consistency.

Limitations: the paper says budget constraints limited the number of memory systems tested. Its benchmark focuses on text-based memory tasks; it does not directly test software coding outcomes, human approval workflows, or whether a specific approved architecture decision changes generated code. It is a useful benchmark for memory capability, but only indirect evidence for Contexer.

## Terms for evaluating the claim

- **Hypothesis:** a testable prediction, for example “the agent follows the approved rule more often when it is surfaced.”
- **Baseline:** the comparison condition, such as the same tasks and model with no decisions available.
- **Metric:** the measured quantity, such as task pass rate, rule-compliance rate, clarifications before coding, or tokens/cost per session.
- **Ground truth:** the independently specified correct outcome for each task, such as an expected behavior checked by tests or a human-authored rubric. It must be defined before looking at which condition wins.

## Git workflow evidence

`toy-repo/` is a disposable local repository with a `main` branch and a `codex/sample-pr` branch containing a small README update and a one-line staged-change fixture. The comparison is reproducible with:

```sh
cd toy-repo
git diff main...codex/sample-pr
```

This is a local pull-request-shaped diff, not a published GitHub PR. No repository link or PR URL exists yet.

## References

- [Contexer public repository](https://github.com/bhargavamin/contexer)
- [Contexer website](https://contexer.ai/)
- [Contexer benchmark documentation](https://github.com/bhargavamin/contexer/blob/main/docs/benchmark.md)
- Hu, Wang, and McAuley, [MemoryAgentBench paper](https://arxiv.org/abs/2507.05257)

## Evidence still requiring the learner

- Notion access screenshot: not captured; this workspace has no connected Notion session visible to me.
- Local version-check screenshot: commands and outputs are documented above; capture a screenshot from your own desktop for submission.
- Sample pull-request screenshot and repository link: local branch only; publish/fork it only if your mentor requires a hosted PR and you choose where it should live.
- Short screen recording in your own voice: not recorded. Use the setup/run commands above and explain what each output means in your own words.
- Mentor review and requested fixes: not requested or recorded yet.

Before sharing screenshots or recordings, inspect them for emails, usernames, tokens, and unrelated private desktop content. Keep this artifact local until you choose an approved submission destination.
