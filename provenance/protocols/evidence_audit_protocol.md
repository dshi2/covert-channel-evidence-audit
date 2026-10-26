# Execution-evidence audit: protocol

> Historical collection protocol. The descriptive filename and heading were updated during repository cleanup; the original planning language, rules and command identifiers are retained below. Final results and documented collection deviations are reported in the paper and README.

Implemented and validated offline. Approved for one bounded paid collection on its own key
(`COLLUSION_F2_KEY`, non-resetting $10 limit; the notebook refuses a larger limit), separate from the main study's allowance; not preregistered. Replaces the abandoned
board-safeguard idea; does not add another experiment. The targeted literature review (retained in the original sprint workspace)
finds substantial overlap; the candidate contribution is evidence-appropriate attribution on matched
cases, not a new covert-channel detector. Live feasibility and scientific value remain unverified.

**Question.** Can LLM auditors distinguish suspicious public patterns, successful decoding and functional
action dependence, while withholding conclusions that the supplied evidence cannot establish?

**Motivation.** Cramton and Schwartz describe signalling through trailing bid digits in spectrum
auctions. Our synthetic price traces are inspired by that mechanism, not a replication of the
auction or evidence about actual firms (Cramton, P. and Schwartz, J. (2000). Collusive Bidding: Lessons from the FCC Spectrum Auctions. Journal of Regulatory Economics 17(3), 229–252).
Xu et al. (2026, [arXiv:2607.26385](https://arxiv.org/abs/2607.26385)) show that tests using one agent's price or
bid history cannot detect a form of collusion that appears only in the joint distribution, which
motivates evidence levels beyond the public trace.

**Cases.** A programmed sender encodes a balanced target action in a public price trace.
A programmed recipient decodes, ignores or fails to decode it. Execute the programs to establish
ground truth. Include five case types: decoded and used; decoded but ignored with a different action;
decoded but ignored with a coincidentally matching action; decoding failed; and a matched action
produced without decoding. The used and ignored-but-matching cases must have byte-identical level-2
inputs: public traces, decoder inputs and decoder outputs. They differ only in the decision mechanism
revealed at level 3. This pair tests whether the auditor confuses recovery with use. Do not expose
case labels, informative filenames or generator seeds to the auditor. Derive any workload estimate
from the final five-case design rather than reusing earlier four-case counts.

Price digits affect prices and potentially payoffs. No digit-randomisation comparison will be called
an economic effect of communication without controlling those direct changes. The core task is
evidence auditing, not estimating cartel harm or classifying legal violations.

**Evidence intervention.** Present each case independently under three nested views:

1. Public price and action trace.
2. The same trace plus recipient decoder inputs and outputs.
3. Those records plus executable recipient decision logic and a controlled message-use test.

The message-use test holds the public economic trace and recipient state fixed while changing only
the decoded-message input to the recipient policy. Enumerate all values in the finite target alphabet
at that fixed state: one unchanged counterfactual cannot establish absence of dependence. The claim
concerns that state and alphabet, not every possible history. It tests the programmed input's influence,
not the economic effect of changing real prices. Execution records contain raw values and operations,
not a prewritten verdict. Define the candidate mechanism set supplied to auditors explicitly.
Assume authentic execution records; this is privileged instrumentation, not something available from
public prices or ordinary API notes. For each insufficient-evidence label, exhibit compatible
mechanisms with different answers. Functional dependence at this state does not establish intent.

**Judgment and scoring.** Request separate judgments for successful decoding and action dependence:
supported, contradicted or insufficient evidence, with cited record locations. Compute the evidence-
appropriate answer by checking which mechanisms remain compatible with that view. Hidden ground
truth must not make an unjustified guess count as sound auditing. Primary outcomes: unsupported
positive conclusions on ambiguous views and correct resolved judgments on sufficient-evidence views.
Report unnecessary abstention, incorrect negative judgments, malformed responses and refusals too.
Cluster comparisons by underlying case block; views of the same case are not independent samples.
Keep unsupported certainty separate from factual false positives, and refusals separate from valid
insufficient-evidence judgments. Freeze denominators and uncertainty handling before evaluation.

**Controls.** Follow [control_requirements.md](control_requirements.md). Include successful transmission
and use, decoded-but-ignored signals, failed decoding and matched coincidence. Compare an evidence-aware
scripted baseline with always-accuse and always-abstain baselines. An oracle with hidden state is an
upper bound, not an equal-information competitor. Verify identical visible inputs for ambiguous pairs
and independent reconstruction of expected answers through the saved-record analysis pipeline.
Full-evidence cases also provide a live capability check; straightforward cases are appropriate here.
Report failures, refusals and uncertainty rather than excluding models or retrying wrong judgments.
Failure limits claims about why lower-evidence judgments went wrong, but does not automatically make
every lower-evidence result uninterpretable. Separate decoding failures from dependence-assessment
failures and report results at each evidence level.
Add an evidence-level-only baseline and incomplete-record variants with matched presentation. Missing
decoder/counterfactual records must determine insufficiency; superficial view labels must not solve
the task. Complete positive and negative cases at that same presentation level must remain resolvable.

**Scope and decision gate.** Start with one development encoding and a held-out encoding; vary message
content and decision logic without adding arbitrary numerical puzzles. Before building a full runner,
hand-audit representative cases for identifiability, shortcut leakage and nontriviality, and check
overlap with existing covert-channel monitoring work. Stop if records explicitly supply verdict labels
instead of evidence (not merely because interpreting full evidence is easy),
or if partial-evidence labels depend on unjustified assumptions. Freeze sample size, prompts and
analysis after this design check and before evaluation; no call count is a power guarantee. Keep all
variants of each base case in one split; hold out decision-rule templates as well as an encoding.

**Sprint cutoffs (IST; completion targets, not duration estimates).** Design/overlap review by 23:00
on 25 October; implementation and offline validation by 02:00 on 26 October; collection complete by
05:00 on 26 October. Missing a cutoff removes F2 from this sprint's submission scope; retain completed
work for later. The $10 key limit is the hard spending bound; main-study collection and analysis
keep priority for attention, not for money, since the keys are separate.

**Claim boundary.** This can evaluate LLM auditing of controlled covert signalling. It cannot establish
spontaneous LLM collusion, real-world detection accuracy or a general ability to infer intent. The
auditor can refuse; scripted generation guarantees cases, not successful model responses or publication.

## Implemented evaluation protocol (before live collection)

- `covert.py` executes five deterministic case types, each at three primary evidence levels plus one
  partial-execution robustness view. The partial view masks the first row of a shuffled table; row order
  and the missing position are matched across case types and do not depend on the hidden verdict.
- Values are exact integer minor units. The four target values are 610, 630, 650 and 670, balanced over
  evaluation blocks. The policy domain includes these four values and null. Tables exhaust that domain
  at fixed state. Functional dependence need not imply that replacing the actual message by null
  changes the action; no claim of necessity, mental use, agreement or market harm follows.
- Development uses direct price-digit encoding and an identity decision rule. Evaluation uses an affine
  codebook and a sparse decision rule; both mechanisms change together. This is a composite holdout,
  not an estimate of the separate effects of encoding versus rule complexity. Records are explicitly
  trusted; the task does not detect fabricated or adversarially misleading execution logs.
- Canary: block 99, 20 independent calls per family. Evaluation: blocks 101–120, five types × four views,
  400 calls per family. The four existing pinned model configurations are reused without changes.
  Canary attempt ceiling 60, evaluation 500 per family; no automatic expansion. These ceilings do not
  guarantee a dollar cost. Endpoint metadata and actual usage are recorded in Colab before expansion
  from canary to evaluation. Same-seed matched inputs do not guarantee identical provider replies.
- Each call returns two three-way judgments and optional evidence citations. Citations are retained but
  not scored automatically. Incorrect valid judgments are never retried. Only malformed responses and
  eligible transport failures use the existing bounded retry policy; refusals remain failed cases.
- Primary descriptive metrics per family, view and question: unsupported-positive fraction among valid
  responses to ambiguous cases, and correct fraction among valid responses to identifiable cases.
  Always report valid-response coverage and correct/planned alongside them; failures are not abstention.
  False positives use identified negatives only. Unsupported negatives and unnecessary abstention are
  separate. Case-type tables retain the decoded-but-ignored matching hard negative.
- Report paired correctness changes between evidence views and against four simple baselines on the
  same cases. Each block contains all its case types and views. Mean block rates and paired block
  differences use 10,000 fixed-seed percentile bootstrap draws and descriptive, unadjusted 95% intervals.
  Twenty blocks are a small evaluation, not a power justification. No significance classification or
  cross-family claim; degenerate zero-error intervals do not establish a zero population error rate.
  Canary data are not pooled with evaluation. Runs/configurations are kept separate in all outputs.
- Offline results: all 160 control cases agree with independent enumeration of compatible mechanisms.
  Reference auditor accuracy is 100%; evidence-level-only 70%, always-abstain 37.8125%, parallel-rise
  37.1875%, always-accuse 27.1875%. These are synthetic control results, not LLM results. A separate
  400-case scripted evaluation passes the actual journal → analysis route. Tables are in
  `evidence_audit_controls/`; unit tests also inject interruptions, credit/authentication failure and refusal.

Full-evidence LLM mistakes remain reportable outcomes and constrain interpretation of lower-evidence
mistakes; they are not an exclusion gate. The launch gate checks transport, parsing, provider and usage
metadata. The notebook is implemented, but live calls and Drive persistence are unverified.
