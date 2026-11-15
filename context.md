# context.md

## Project
- **Event:** NASA Space Apps Challenge 2026 (hackathon, Nov 14–15, 2026)
- **Team size:** 5
- **Deliverable:** Web-based game
- **Current stage:** Implementation sprint (final day). **Step 0 DONE and deployed.** Simulation & Mission Logic spec (Section 15) merged from owner's fork → canonical v13. Next: Step 1 (contract commit) after A1/A2 acks.
- **Live URL:** https://darling-crisp-b1fb7f.netlify.app/

## Challenge Statement
Create an interactive game where players design, manage, and simulate a complete space mission. Players make engineering decisions, manage limited resources, and see how each choice affects mission success. Trade-offs to cover: mission objectives, spacecraft design, science instruments, launch vehicles, budget, power, mass, communications, orbital constraints.

Note: the official challenge page blocks automated access. Submission requirements below come from the official brief the team already has. A teammate should still skim the official page for anything new.

## Target Audience
Students who rarely get to experiment with a whole mission from concept to operation.

## Output Rules (from user)
- Give only the idea, nothing more.
- Provide an updated `context.md` after every reply.
- All replies and files are in English only.

## DECISION: We are going with Idea 1 only
Idea 2 (Tradeoff: Mission Zero) and the proposed merge are archived at the bottom. They are not part of the build.

## Chosen Idea 1 (from teammate): Card-Based Space Mission Game
Inspired by board games and card games. The player builds their own space mission using different cards. Each choice has its own advantages, disadvantages, and consequences.

Card types:
- **Mission Cards:** Mars exploration, Moon exploration, Earth observation, or asteroid investigation.
- **Spacecraft Cards:** Components and subsystems the spacecraft needs.
- **Scientific Instrument Cards:** Each with its own cost, mass, power consumption, and scientific value.
- **Rocket Cards:** A launch vehicle that can carry the spacecraft and payload.
- **Orbit Cards:** An orbit suited to the mission objective.
- **Event Cards:** Equipment failure, budget cuts, solar storms, communication problems.

---

# LOCKED DECISIONS
- **Stack:** React + Vite + TypeScript + Tailwind CSS v4 (`@tailwindcss/vite` plugin) + Vitest. 100% client-side, no backend, no accounts, no router, no state library. Node 22. Netlify deploy (`netlify.toml`, publish `dist`, SPA redirect). **Step 0 complete; live URL above.**
- **Players:** Single-player only. Multiplayer post-MVP.
- **Mode for MVP:** Learning mode only.
- **Numbers:** Decision C — keep starter numbers; `inspiredBy` credits + README sources (Section 19).
- **Rules:** v7.1 patch P1–P6 approved. **v7.2 amendments A1–A3 (Section 17): A3 adopted; A1/A2 applied as recommended defaults, pending Mechanics owner's one-word ack.** After ack, frozen again.
- **Engine spec:** Section 15 (15.1–15.22), owned by Simulation & Mission Logic, is the authoritative implementation spec. **Interface contract = 15.18. Event JSON schema = 15.19.** Where older text conflicts, Section 15 governs implementation.
- **Art:** PIXEL ART per required-assets.md. Placeholder-first; code never waits on art (Section 22).
- **AI tooling:** OmniRoute in VS Code (fast model). Prompts scope-fenced, self-contained, ending in runnable verification.
- **Canonical file:** one `context.md` at repo root. Section owners propose edits; coordinator merges and bumps the changelog. No forks.

---

# GAME MECHANICS (v7.2, owner: Game Mechanics & Logic — FROZEN after A1/A2 ack)

All numbers are starter values for balancing, simplified and fictional-but-plausible, labeled as such in-game (Section 19). Mechanics owns rules and data; Simulation owns the code (Section 15).

## 1. Core Loop (5 phases)
1. **Briefing:** pick a Mission Card (objective, budget cap, science target, priority instrument tags).
2. **Build:** fill slots with cards. Live gauges: Mass, Power, Cost, Data + margins.
3. **Launch Check:** hard-limit validation. Any red rule blocks launch.
4. **Flight:** 6 stages, Event Cards drawn, player responses.
5. **Report:** score /100 + Trade-off Report explaining what helped or hurt.

One run ≈ 10–15 minutes. Single-player.

## 2. Build Board (slots)
| Slot | Count | Notes |
|---|---|---|
| Mission | 1 | Chosen first; sets budget cap, target, priority tags, allowed orbits |
| Orbit | 1 | Must be allowed by the Mission |
| Rocket | 1 | Sets payload capacity and launch reliability |
| Bus | 1 | Sets instrument and support slots |
| Power | 1 | Solar or RTG |
| Communications | 1 | Antenna / downlink |
| Propulsion | 1 | Must meet the Orbit's minimum ΔV |
| Instrument | 2–4 | Limited by Bus |
| Support | 1–3 | Limited by Bus |

## 3. Resources and Rules
**Four gauges:** Cost ($M) vs Mission cap; Mass (kg) vs Rocket capacity × Orbit Reach Factor; Power (W) generated (× Sun Factor, RTG exempt) vs total draw; Data (Mbps) generated vs Comms downlink × Orbit Signal Factor. Full formulas in 15.4.

**Hard limits (block launch):** Cost ≤ cap, Mass ≤ capacity, Power ≥ draw, ΔV ≥ Orbit minimum, Orbit allowed by Mission, ≥1 priority-tag instrument. Full rule codes LV-01…LV-08 in 15.6.

**Soft limit:** Data. `Data Throttle = min(1, Downlink / Data Generated)` — throttles science, never blocks launch.

**Margin** = (Limit − Used) / Limit.
| Margin | Tier | Event bonus |
|---|---|---|
| ≥ 25% | Green | +2 |
| 10–<25% | Yellow | +1 |
| < 10% (incl. negative) | Red | 0 |

Margins link Build to Flight: spare capacity buys event safety. Leftover budget = **Contingency Fund**.

## 4. Mission Cards
| Mission | Budget Cap | Science Target | Priority Tags (×1.5) | Allowed Orbits |
|---|---|---|---|---|
| Lunar Ice Hunter (Moon) | 480 | 50 | Subsurface, Composition | Lunar Polar |
| Red Planet Climate Watch (Mars) | 700 | 60 | Imaging, Composition | Mars Orbit |
| Wildfire Watch (Earth Observation) | 300 | 40 | Thermal, Imaging | LEO, Sun-Synchronous |
| Asteroid Rendezvous | 600 | 55 | Composition, Topography | Asteroid Rendezvous |

Difficulty order: Wildfire Watch → Lunar Ice Hunter → Asteroid Rendezvous → Red Planet Climate Watch. MVP: first two only.

## 5. Orbit Cards
| Orbit | Reach | Sun | Signal | Min ΔV (m/s) | Radiation |
|---|---|---|---|---|---|
| LEO | 1.00 | 1.0 | 1.0 | 200 | 1 |
| Sun-Synchronous | 0.85 | 1.0 | 1.0 | 300 | 1 |
| Lunar Polar | 0.35 | 1.0 | 0.8 | 1,500 | 2 |
| Mars Orbit | 0.25 | 0.43 | 0.4 | 1,800 | 2 |
| Asteroid Rendezvous | 0.20 | 0.6 | 0.5 | 2,500 | 3 |

Reach cuts deliverable mass; Sun multiplies solar output (not RTG); Signal multiplies downlink; Radiation raises Solar Storm difficulty (+0/+1/+2).

## 6. Rocket Cards
| Rocket | Capacity to LEO (kg) | Cost | Reliability |
|---|---|---|---|
| Light Lifter | 1,500 | 60 | 85% |
| Medium Lifter | 3,000 | 150 | 92% |
| Heavy Lifter | 10,000 | 300 | 96% |
| Super Heavy Lifter | 30,000 | 500 | 98% |

`Mass Limit = Capacity × Reach`. Rocket mass is NOT payload mass (15.4).

## 7. Spacecraft Cards
**Bus**
| Bus | Mass | Cost | Draw | Instr Slots | Support Slots |
|---|---|---|---|---|---|
| Small | 150 | 40 | 50 | 2 | 1 |
| Medium | 300 | 80 | 80 | 3 | 2 |
| Large | 600 | 150 | 150 | 4 | 3 |

**Power**
| Card | Mass | Cost | Output (W) | Notes |
|---|---|---|---|---|
| Solar Array S | 30 | 10 | 200 | × Sun |
| Solar Array L | 80 | 25 | 600 | × Sun |
| Solar Array XL | 140 | 45 | 1,000 | × Sun |
| RTG | 45 | 90 | 150 | Ignores Sun; tag Radiation-Hardened |

**Communications**
| Card | Mass | Cost | Draw | Downlink (Mbps) |
|---|---|---|---|---|
| Small Antenna | 10 | 8 | 20 | 5 |
| Medium Antenna | 30 | 20 | 60 | 25 |
| Large Dish | 80 | 45 | 150 | 100 |

**Propulsion**
| Card | Mass | Cost | Draw | ΔV (m/s) |
|---|---|---|---|---|
| Chemical Small | 60 | 20 | 0 | 1,000 |
| Chemical Large | 150 | 40 | 0 | 2,000 |
| Ion Drive | 90 | 70 | 150 | 4,000 |

**Support**
| Card | Mass | Cost | Draw | Tag |
|---|---|---|---|---|
| Radiation Shield | 25 | 12 | 0 | Radiation-Hardened |
| Redundant Computer | 10 | 15 | 10 | Redundant |
| Onboard Storage | 8 | 10 | 5 | Storage |
| Thermal Control | 12 | 8 | 10 | Thermal |

## 8. Scientific Instrument Cards
| Instrument | Cost | Mass | Power | Data | Science | Tag |
|---|---|---|---|---|---|---|
| Wide-Field Camera | 15 | 20 | 30 | 10 | 8 | Imaging |
| High-Res Imager | 40 | 60 | 80 | 40 | 15 | Imaging |
| Thermal IR Imager | 30 | 30 | 45 | 10 | 12 | Thermal |
| Spectrometer | 35 | 35 | 50 | 4 | 14 | Composition |
| Radar Sounder | 60 | 80 | 150 | 10 | 18 | Subsurface |
| Neutron Detector | 30 | 25 | 30 | 1 | 12 | Subsurface |
| Laser Altimeter | 45 | 45 | 70 | 4 | 14 | Topography |
| Magnetometer | 10 | 8 | 10 | 0.5 | 6 | Fields |

`Potential Science = Σ (Science × 1.5 if any Mission priority tag, else × 1)` — multiplier applied once per instrument (15.4).

## 9. Flight Phase (6 stages)
| Stage | What happens |
|---|---|
| 1. Launch | Learning mode: always proceeds (optional practice d100 shown). |
| 2. Cruise | Draw 1 Event. No science. |
| 3. Orbit Insertion | Check Current ΔV vs Min; **below → Mission Lost**; else deduct Required ΔV. |
| 4–6. Science Ops 1–3 | Draw 1 Event, then collect science (15.14). |

Post-insertion ΔV reaching 0 does NOT lose the mission; logged as critical condition (15.4). Engine stage behavior: 15.8.

## 10. Event Cards and Resolution
`Result = d6 + Margin Bonus + Tag Bonus + Response Bonus` vs Difficulty. Success ≥ Diff; Partial = Diff−1; Fail ≤ Diff−2. Response Bonus capped +2. Full resolution rules: 15.11. Effect definitions: 15.12–15.13. Response legality: 15.10. Odds shown before every draw (transparency rule; `getEventPreview`).

**MVP deck = the 8 negative events below** (Navigation Error removed per P1; positives and Dust Storm cut for MVP). Drawn without replacement, seeded shuffle, 4 draws per run (15.9).

| Event | Checks | Counter Tag | Diff. | Partial | Fail |
|---|---|---|---|---|---|
| Solar Storm | Power margin | Radiation-Hardened | 4 (+radiation) | science ×0.75 | instrument offline this + next stage |
| Comms Blackout | Data margin | Storage | 4 | science ×0.5 | science ×0 this stage |
| Instrument Fault | Cost margin | Redundant | 5 | instrument offline 1 stage | instrument lost |
| Thruster Glitch | ΔV margin | none | 4 | −300 m/s | −700 m/s |
| Budget Cut | Cost margin | none | 5 | −5% cap from fund | −10% cap; if unpaid, costliest active instrument offline 1 stage |
| Micrometeoroid | Mass margin | Radiation-Hardened | 5 | instrument offline 1 stage | instrument lost |
| Thermal Overheat | Power margin | Thermal | 4 | science ×0.75 | instrument offline 2 stages |
| Software Bug | Cost margin | Redundant | 3 | science ×0.75 | science ×0 this stage |

Post-MVP (not in MVP data/UI): Dust Storm (Mars), Lucky Break, Extended Funding. After each event: 1–2 sentence **Learning Moment**.

## 11. Scoring (100 points, v7.2)
| Category | Points | How |
|---|---|---|
| Science Return | 50 | `50 × min(1, Science Collected ÷ Target)` |
| Resilience | 20 | `20 × (Successes + 0.5 × Partials) ÷ negative events drawn`; zero events → 20 |
| Budget Efficiency | 15 | `15 × min(1, FINAL Contingency ÷ (0.15 × cap))` — after responses and event losses |
| Margin Discipline | 15 | Per Cost/Mass/Power, launch-time margins (A1): <0% → 0; 0–<10% → `5×(margin/0.10)`; 10–25% → 5; >25% → `max(0, 5×(1−(margin−0.25)/0.50))` → 0 at ≥75% |

**Outcome (A2):** Mission Lost (failed insertion / all instruments permanently lost) → Margin Discipline only. **Failed:** score <40 OR Science < Target. **Partial Success:** 40–59 AND target met. **Success:** 60–79 AND target met. **Outstanding:** 80+ AND target met. Display to one decimal. Badges post-MVP.

## 12. Trade-off Report (end screen)
Up to 3 helped / 3 hurt / 1 What-if per hurt item, generated from recorded run facts, ranked per 15.17. Score breakdown + one-click Replay (same mission, new seed).

## 13. Game Modes
Learning (MVP): launch never fails, odds shown, gauge hints. Standard / Challenge / Draft Mode: post-MVP.

## 14. Worked Example (ACCEPTANCE TEST)
Lunar Ice Hunter + Lunar Polar + Medium Lifter + Medium Bus + Solar L + Medium Antenna + Chemical Large + Radiation Shield + Radar Sounder + Neutron Detector + Spectrometer:
- Cost **452/480** (5.8%, Red) · Mass **725/1,050** (31%, Green) · Power **370/600** (38%, Green) · Data **15/20**, throttle 1.0 (25%, Green) · ΔV 2,000/1,500 OK · Potential Science **66** vs 50 OK · Contingency 28.
- Light Lifter swap → 525 kg limit < 725 kg → blocked. Full test list: 15.21.

## 15. Simulation & Mission Logic Specification (MVP — owner: Simulation & Mission Logic; adopted v13)

### 15.1 Purpose
The rules engine: converts selected cards + event responses into stats, launch validation, stage outcomes, science, score, and report. Mechanics defines values/formulas; Simulation implements and owns authoritative state; Frontend displays inputs/outputs and must NOT duplicate calculations. Turn-based trade-off sim, not orbital physics.

### 15.2 MVP boundaries
Wildfire Watch + Lunar Ice Hunter only. Learning mode only (launch cannot permanently fail). One build, six stages, four event draws, scoring, report. Browser state + JSON; no accounts/DB/multiplayer/physics. Eight negative non-Mars events; positives cut from data AND UI. Every result explainable: validation errors, bonuses, penalties, losses, scoring changes all return player-facing reasons.

### 15.3 Inputs
Mode; selected Mission/Orbit/Rocket/Bus/Power/Comms/Propulsion cards; Instruments; Supports; random seed; per-event responses. Same build + responses + seed ⇒ identical event order, rolls, damage targets, score, report.

### 15.4 Canonical build calculations (recalc on every card change)
- **Cost** = Rocket + Bus + Power + Comms + Propulsion + Σ Instruments + Σ Supports. Limit = Mission cap. Margin = (Limit−Used)/Limit. **Contingency at launch = max(0, Limit−Used).**
- **Mass** = Bus + Power + Comms + Propulsion + Σ Instruments + Σ Supports (rocket excluded). Limit = Capacity × Reach. Margin likewise.
- **Power:** Solar effective = rated × Sun; RTG = rated. Draw = Bus + Comms + Propulsion + Σ Instruments + Σ Supports. Margin = (Output−Draw)/Output. All installed systems count at Launch Check; Safe Mode cannot make an invalid build valid.
- **Data:** Generated = Σ active instrument rates. Effective downlink = Comms × Signal. Throttle = min(1, downlink/generated); generated 0 → throttle 0. Margin = (downlink−generated)/downlink; negative = Red; never blocks launch.
- **Propulsion:** Required = Orbit Min. Pre-insertion margin = Current − Required; build needs Current ≥ Required. Pre-insertion event losses reduce Current; after insertion, Remaining = Current − Required and losses reduce Remaining. Remaining 0 ≠ mission loss (critical condition logged).
- **Potential Science:** ×1.5 if instrument has ANY priority tag (once), else ×1; sum.

### 15.5 Margin tiers
≥25% Green +2; 10–<25% Yellow +1; <10% incl. negative Red 0. ΔV events: pre-insertion ratio = (Current−Required)/Required; post-insertion = Remaining/Required. Same thresholds.

### 15.6 Launch Check
| ID | Rule | Failure output |
|---|---|---|
| LV-01 | Exactly one of each required core card | list missing slots |
| LV-02 | Instrument/Support counts fit Bus | name exceeded slot type |
| LV-03 | ≥1 priority-tag instrument | recommend compatible tags |
| LV-04 | Orbit allowed by Mission | block |
| LV-05 | Cost ≤ cap | show overrun |
| LV-06 | Mass ≤ limit | show excess |
| LV-07 | Power output ≥ draw | show deficit |
| LV-08 | ΔV ≥ Orbit min | show deficit |

Data = soft warning: "Only [throttle×100]% of generated science data can be transmitted." Return machine-readable codes + player-facing explanations.

### 15.7 Authoritative mission state (frozen build snapshot at launch)
```json
{
  "runId": "generated-id", "mode": "learning", "seed": 12345,
  "status": "active", "stage": 1,
  "buildSnapshot": {}, "initialGauges": {}, "initialMargins": {},
  "currentDeltaV": 2000, "remainingDeltaV": null,
  "contingencyFund": 28, "scienceCollected": 0,
  "instruments": [], "temporaryEffects": [],
  "eventDeck": [], "eventsDrawn": [], "eventResults": [],
  "stageLog": [], "score": null, "report": null
}
```

Build cannot change during Flight.
15.8 Mission stages
1 Launch (Learning always proceeds; optional practice d100) → 2 Cruise (event, no science) → 3 Insertion (check, fail→lost, deduct Required) → 4–6 Science Ops (event, then science) → End (status, score, report). Stage start: tick effect durations, determine active instruments, recalc modifiers. Stage end: log science, choices, rolls, bonuses, effects, next state.
15.9 Event deck
Eight negative MVP events; no Dust Storm; seeded shuffle; draw without replacement; 4 draws (Cruise + 3 Ops). Before response: show Difficulty, Margin Bonus, Tag Bonus, legal responses, outcome ranges.
15.10 Player responses

    Safe Mode: Power/Thermal events only; pick one active instrument off this stage (no science/data/power); +1. Cruise use returns before Insertion.
    Spend Contingency: needs ≥10 in fund; costs 10; +1; max 2 per event. All response bonuses capped +2.
    Throttle Data: Comms events only; stage science ×0.5; +1. Cruise: bonus allowed, no science penalty (Cruise earns none).
    UI disables illegal responses.

15.11 Event resolution
Total = d6 + Margin + Tag + Response (cap +2). Final Difficulty = base + orbit modifier (Solar Storm: radiation 1/2/3 → +0/+1/+2). Tag +2 requires installed, functioning counter-tag card. Success ≥ Diff; Partial = Diff−1; Fail ≤ Diff−2. Log event ID, stage, roll, checked margin, all bonuses, responses/costs, difficulty, total, outcome, effects, Learning Moment.
15.12 Reusable effect types
science_multiplier, instrument_offline, instrument_lost, delta_v_loss, contingency_loss, solar_output_multiplier, contingency_gain. Random targets must be active and not lost; no target → log not-applicable. Offline/lost instruments keep original mass/cost for scoring.
15.13 MVP event effects
Event
	
Partial
	
Fail
Solar Storm
	
science ×0.75
	
random instrument offline this + next stage
Comms Blackout
	
×0.50
	
×0
Instrument Fault
	
offline 1 stage
	
lost
Thruster Glitch
	
−300 ΔV
	
−700 ΔV
Budget Cut
	
−5% cap from fund
	
−10%; if not fully paid, costliest active instrument offline 1 stage
Micrometeoroid
	
offline 1 stage
	
lost
Thermal Overheat
	
×0.75
	
offline 2 stages
Software Bug
	
×0.75
	
×0
Budget Cut: deduct as much as available; ties for costliest → seeded random.
15.14 Science collection (Stages 4–6 only)
Recalculate from ACTIVE instruments after event/response effects: Stage Science = (Active Potential ÷ 3) × Current Throttle × Event Multiplier × Response Multiplier. Active Data 0 → science 0. Multipliers multiply, never add. Full precision internally; round for display only.
15.15 Mission loss / completion
Lost: Current ΔV < requirement at Insertion, OR every instrument permanently lost. Temporary outages don't count; all-offline stage = 0 science, mission continues. Survivor → completed after Ops 3.
15.16 Final scoring (v7.2 A1/A2 applied)
Science 50×min(1, collected/target). Resilience 20×(S+0.5P)/negative events drawn. Budget 15×min(1, final fund/(0.15×cap)). Margin Discipline per Cost/Mass/Power at launch: <0→0; 0–<10%→5×(m/0.10); 10–25%→5; >25%→max(0, 5×(1−(m−0.25)/0.50)); ≥75%→0. Outcome: Lost → Margin only; Failed if score <40 OR target missed; Partial 40–59, Success 60–79, Outstanding 80+ — all require target met. One decimal display.
15.17 Trade-off Report
From run facts, ≤3 per category. Helped candidates: Green margin changed an event; counter tag +2; throttle stayed 1.0; contingency improved an event; priority-tag match; ΔV reserve saved insertion. Hurt: throttled science; Red margin; missing counter tag; insufficient contingency; low ΔV; instrument lost/offline; over-engineering penalty. Rank: loss cause > science impact > event impact > score impact > margin size. Each hurt item: one data-based What-if vs an available card.
15.18 Interface contract (THE contract — v7.2 A3, supersedes old 8-function list)

calculateBuild(build)    -> totals, limits, margins, tiers, potentialScience, dataThrottle
validateBuild(build)     -> valid, errors[], warnings[], calculatedBuild
createMissionState(build, mode, seed) -> missionState
getEventPreview(state, event) -> difficulty, bonuses, legalResponses[], outcomeRanges
drawEvent(state)         -> updatedState, event
resolveEvent(state, event, responses[]) -> updatedState, eventResult
runStage(state, playerInput) -> updatedState, stageResult, nextRequiredAction
collectScience(state)    -> updatedState, scienceResult
computeScore(state)      -> total, breakdown, outcome
buildReport(state)       -> helped[], hurt[], whatIf[]

Pure TypeScript, zero React imports. Every public result includes player-facing explanation strings; frontend never recreates rules.
15.19 Data format examples

json
{ "id": "instr_radar_sounder", "type": "instrument", "name": "Radar Sounder",
  "cost": 60, "mass": 80, "power": 150, "data": 10, "science": 18,
  "tags": ["Subsurface"], "flavor": "Sees below the surface using radio waves.",
  "inspiredBy": "Radar sounders flown on lunar orbiters" }

json
{ "id": "event_comms_blackout", "name": "Communications Blackout",
  "checks": "data", "counterTag": "Storage", "baseDifficulty": 4,
  "allowedResponses": ["spend_contingency", "throttle_data"],
  "effects": { "success": [],
    "partial": [{"type":"science_multiplier","value":0.5,"duration":1}],
    "fail":    [{"type":"science_multiplier","value":0,"duration":1}] },
  "learningMoment": "Spacecraft may store data onboard when a communication link is unavailable and transmit it later." }

15.20 Error / edge rules
Reject missing/unknown/malformed/disallowed-duplicate IDs. No division by zero. Clamp fund/science/ΔV at 0. Never repeat an event in a run. Never target a lost instrument. Multiply simultaneous modifiers. Effects past Stage 6 logged, mission ends normally. Bad config numbers → configuration error, never silent 0.
15.21 Minimum acceptance tests (Step 1 writes these RED)

    Lunar build (§14): 452/480, 725/1,050, 370/600, 15/20, throttle 1.0, ΔV 2,000/1,500, science 66.
    Light Lifter swap → 525 kg limit, blocks 725 kg build.
    Data over-capacity warns + throttles, doesn't block.
    Power draw > output blocks.
    No priority instrument blocks.
    Failed practice launch roll still proceeds (Learning).
    Radiation Shield +2 vs Solar Storm; Lunar Polar +1 difficulty.
    Comms Blackout Partial halves stage science; Fail zeroes it.
    Pre-insertion ΔV loss below requirement → Mission Lost.
    Same build + responses + seed → identical full run.
    Plus runbook edges: margin-discipline at 9.9/10/25/26/50/75%; deck never repeats.

15.22 Outside MVP
No orbital propagation/physics, real-time movement, multiplayer/accounts/saves/leaderboards, Mars/Asteroid missions, lifetime sim, Draft/Challenge/badges/positives, AI-generated scoring, exact real-vehicle performance.
16. MVP Scope
Must: 2 missions, their orbits, 4 rockets, 3 buses, power/comms/propulsion, 8 instruments, 4 supports, 8 negative events, scoring, report, Learning mode.
Cut if short: Mars/Asteroid, Draft, badges, Standard/Challenge, positives.
Emergency cut: miss mid-sprint checkpoint → Wildfire Watch only, polished.
17. Patch Records
v7.1 (approved): P1 Navigation Error removed (8+2 base; MVP 8 negatives). P2 insertion failure = Mission Lost. P3 margin formula (superseded by A1). P4 positives = auto-successes; zero events → 20. P5 science-gate (superseded by A2). P6 multipliers 1.0/0.75/0.5/0.
v7.2 (this merge): A1 Margin Discipline — negative clamp + decay to zero at 75% (was 50%); recommended-adopt, pending Mechanics ack. A2 science-below-target = Failed (was Partial cap); recommended-adopt, pending ack. A3 contract = 15.18 (adopted; nothing built on old list). Also adopted from sim spec: ΔV margin ratios, active-instrument science recalc, final-fund Budget Efficiency, effect taxonomy, seeded reproducibility, edge rules, 15.21 tests.
18. Build Plan
Tracks (claim, don't assign): 1 Mechanics & card data (+art normalization); 2 Frontend A (Build screen); 3 Frontend B (Flight+Report); 4 Simulation & state; 5 Visuals & pitch.
Mid-sprint checkpoint: full Wildfire Watch on live URL; miss → emergency cut. 30-min outsider playtest; confusion + difficulty constants only. T−3h freeze (bugs + balance only; unready art stays placeholder). T−2h submission block (demo, links, incognito check, submit early).
19. Decision C — Starter Numbers + NASA Credits
Keep starter numbers; inspiredBy per card + README Sources + demo line: "Rules modeled on NASA's Concept Maturity Level process; hardware inspired by real missions; numbers simplified for gameplay." Realism lives in the rules: CML 1–4 loop (Briefing=Cocktail Napkin, Build=Feasibility/Trade Space, Launch Check=Point Design with margins/reserves), four mission segments, requirements-with-verification (BioNutrients "<250 g container" verified by weighing). Credits: Ion Drive↔Dawn; Super Heavy↔SLS; Wide-Field Camera↔PUNCH imagers; Laser Altimeter↔LOLA; Neutron Detector↔LEND; Thermal IR↔Landsat TIRS. Sources: science.nasa.gov; NASA "Design and Develop Science Missions" webinar (Mar 2025); Wessen et al., CML paper (JPL, AIAA 2013). Real-spec mode post-event.
20. Submission Checklist

    Demo ≤30s video OR ≤7 slides; over-limit = ineligible for Global Judging.
    Externally hosted, public; test incognito.
    English page + materials; non-English narration needs English subtitles.
    Video beats: team 0:00 → problem 0:02 → name+tagline 0:05 → gameplay + NASA data 0:10 → future 0:20–0:30.
    Slides: title/team → problem → concept → gameplay → NASA data/tech → impact → live link.
    README: how to play, live URL, sources, CML mapping, credits, license.
    Judging self-check: Impact, Creativity, Validity, Relevance, Presentation.
    Teammate skims official page.

21. Vibe-Coding Protocol

    Contract first: 15.18 types + 15.19 schemas committed before UI; paste into EVERY prompt.
    One file, one owner. One canonical context.md at repo root; owners propose section edits, coordinator merges + bumps changelog; forks archived under docs/archive/.
    Engine sacred: pure TS, no React, 15.18 signatures frozen; 15.21 tests green before merge.
    AI implements spec exactly; reject invented mechanics.
    Small prompts, small commits; no late giant rewrites.
    Mock-first UI; integration = one import swap.
    Fix loop fails twice → revert, re-prompt with error + contract.
    Fast-model prompt template: role → context (reference) → HARD SCOPE FENCE → numbered tasks w/ exact contents → DO NOT ADD → verification w/ real output → short report → STOP. Save as prompts/stepN.md.

22. Asset Integration Protocol
Placeholder-first; engine has zero asset deps. Drop-point public/assets/{cards,icons,bg,ui}/, filenames = ids (required-assets.md + JSON). <CardArt>/<Icon> fall back to type-color placeholders (gold/blue/orange/teal/purple/magenta); real PNGs appear with zero code changes. DOM UI, image-rendering: pixelated, integer scaling, 16:9 letterbox. Wireframes before art. Designer triage: event_navigation_error REMOVED — do not draw; mode-select trio → P2; P1 order style→frames→icons→build screen; reuse base shapes. Normalization ~20 min (sizes, ≤32-color palette, transparent PNG, nearest-neighbor); inconsistent → placeholder stays. T−3h: unready art stays placeholder. Step 0 palette tokens in index.css are placeholders; designer's final palette replaces values only.
23. Parallel Build Runbook

    Step 0 — DONE. Scaffold + Tailwind v4 + Vitest + folders + netlify.toml deployed: https://darling-crisp-b1fb7f.netlify.app/ . Tag step-0.
    Step 1 — Contract commit (next, Engine, ~30 min): types.ts modeling 15.7 state, 15.12 effects, 15.18 signatures; stubs; 15.21 tests written RED; src/data/*.json with 15.19 schemas (events include allowedResponses/effects/learningMoment). Attach canonical v13. DONE: npm test runs, tests red.
    Step 2 — Placeholder art system (Frontend A, 30 min): CardArt/Icon/CardView/Gauge, type-color fallbacks, pixelated scaling, tier shape symbols. DONE: drop-in PNG works with zero code changes.
    Step 3 — Build screen (Frontend A, 60–90 min): mission pick → slots → 6-tab catalog → click-to-place → gauges via calculateBuild/validateBuild → Launch Check LV-01…08 → Launch disabled until valid. DONE: §14 build assembles; gauges match exactly.
    Step 4 — Full engine (Engine, parallel): implement 15.4–15.17 in order; mulberry32 seeded RNG. DONE: 15.21 green incl. headless end-to-end Wildfire Watch.
    Step 5 — Flight + Report (Frontend B, parallel): mock RunLog first; stage tracker, event reveal, odds via getEventPreview, response buttons with legality states, instrument strip, science counter, Learning Moment; report breakdown, rank, helped/hurt/what-if, Replay. DONE: complete on mocks; engine swap = one import.
    Step 6 — Integration gate: full Wildfire Watch on live URL; replay twice, no state corruption; miss → emergency cut; then playtest.
    Step 7 — Asset drop-in (continuous, Data).
    Step 8 — Freeze T−3h; submit T−2h.

Open Decisions

    A1/A2 one-word ack from Mechanics owner (blocking Step 1 freeze, defaults applied).
    Working project title + team name (logo + demo).
    Decision C final ack.
    Official page check → pitch track.

Areas to Explore (Team Roles)

    Game Mechanics & Logic: rules, cards, resources, scoring.
    Frontend Development: interface and interactions.
    Backend & Game Systems: state, JSON configs, browser state; no accounts.
    Simulation & Mission Logic: implements Section 15.

Suggested Split for 5 People (claim)
1 Mechanics & card data · 2 Frontend (Build; Flight/Report) · 1 Simulation + state · 1 NASA research, art, pitch, demo.
Archived: Idea 2 — "Tradeoff: Mission Zero" (condensed)
Build-then-fly simulator, four gauges, real-time flight events, score + report. More depth, more sim work. Not part of the build.
Archived: Proposed Merge (condensed)
Cards in build + gauges + Event Cards in flight + helped/hurt report — effectively what the mechanics implement on Idea 1's base.
Change Log

    v1–v6: idea capture → translation → roles → Idea 2 expansion → Idea 1 only.
    v7: full mechanics + contract + MVP scope.
    v8: sprint plan, proposed v7.1 patch, credits, submission checklist, acceptance test.
    v9: stack/single-player/Learning locked; v7.1 approved; Decision C; vibe protocol.
    v10: placeholder-first; pixel art; asset protocol + designer triage.
    v11: parallel runbook (8 steps, gates).
    v12: Step 0 prompt; tooling pinned; fast-model prompt template.
    v13: Step 0 done + live URL recorded. Merged Simulation owner's Section 15 fork (their "v8", based on pre-patch v7) into canonical: full 15.1–15.22 adopted; contract = 15.18 (A3); event schema = 15.19; v7.2 amendments A1 (margin clamp + 75% decay) and A2 (science-below-target = Failed) applied as recommended defaults pending Mechanics ack; Sections 9–11 updated to match; canonical-file rule added; Step 1 now targets 15.7/15.12/15.18/15.19/15.21. Their file archived to docs/archive/.