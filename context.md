# context.md

## Project
- **Event:** NASA Space Apps Challenge 2026 (hackathon, Nov 14–15, 2026)
- **Team size:** 5
- **Deliverable:** Web-based game
- **Current stage:** Implementation sprint (final day). Mechanics v7.1 frozen. Art in production (pixel art). Executing Section 23 runbook: **Step 0 prompt issued (scaffold + deploy)**; Steps 1–8 pending.
- **Live URL:** TBD (fill in after Netlify deploy)

## Challenge Statement
Create an interactive game where players design, manage, and simulate a complete space mission. Players make engineering decisions, manage limited resources, and see how each choice affects mission success. Trade-offs to cover: mission objectives, spacecraft design, science instruments, launch vehicles, budget, power, mass, communications, orbital constraints.

Note: the official challenge page (spaceappschallenge.org/2026/challenges/space-mission-design-game/) blocks automated access. Submission requirements below come from the official brief the team already has. A teammate should still skim the official page for anything new.

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

# LOCKED DECISIONS (kickoff)
- **Stack:** React + Vite + TypeScript + Tailwind CSS v4 (`@tailwindcss/vite` plugin, no tailwind.config.js) + Vitest. 100% client-side: JSON card files + browser state, no backend, no accounts, no router, no state library. Node 22. Deploy: Netlify (`netlify.toml`, publish `dist`, SPA redirect). Fallback only if the team cannot debug Vite: vanilla JS ES modules, same contract.
- **Players:** Single-player only (confirmed). Collaboration is optional per the challenge; multiplayer is post-MVP.
- **Mode for MVP:** Learning mode only.
- **Numbers:** Decision C — keep v7 starter numbers; add `inspiredBy` credits + README sources instead of real-spec replacement (Section 19).
- **Rules:** v7.1 patch P1–P6 APPROVED. Mechanics frozen. After the freeze checkpoint, only bug fixes and event-difficulty constants may change.
- **Art:** PIXEL ART per required-assets.md. Placeholder-first: code never waits on art (Section 22).
- **Build start:** Immediate, without assets. Asset delivery runs in parallel.
- **AI tooling:** OmniRoute in VS Code (fast model). Prompts must be explicitly scope-fenced, self-contained, and end with runnable verification.

---

# GAME MECHANICS (v7.1, owner: Game Mechanics & Logic — APPROVED & FROZEN)

All numbers are **starter values for balancing**, simplified and fictional-but-plausible, labeled as such in-game (see Section 19). The Simulation & Mission Logic member implements the formulas; this section defines the rules and data.

## 1. Core Loop (5 phases)
1. **Briefing:** pick a Mission Card (shows objective, budget cap, science target, priority instrument tags).
2. **Build:** fill the slots with cards. Live gauges show Mass, Power, Cost, Data and margins.
3. **Launch Check:** hard-limit validation. Any red rule blocks launch.
4. **Flight:** 6 stages, Event Cards drawn, player makes responses.
5. **Report:** score out of 100 plus a "Trade-off Report" explaining what helped or hurt.

One run takes about 10–15 minutes. Single-player.

## 2. Build Board (slots)
| Slot | Count | Notes |
|---|---|---|
| Mission | 1 | Chosen first; sets budget cap, target, priority tags, allowed orbits |
| Orbit | 1 | Must be allowed by the Mission |
| Rocket | 1 | Sets payload capacity and launch reliability |
| Bus | 1 | Main body; sets instrument and support slots |
| Power | 1 | Solar or RTG |
| Communications | 1 | Antenna / downlink |
| Propulsion | 1 | Must meet the Orbit's minimum ΔV |
| Instrument | 2–4 | Limited by Bus |
| Support | 1–3 | Limited by Bus |

## 3. Resources and Rules

**Four gauges**, always visible while building:
- **Cost ($M):** sum of all card costs. Limit = Mission budget cap.
- **Mass (kg):** sum of all card masses. Limit = Rocket capacity × Orbit Reach Factor.
- **Power (W):** Generated (Power card × Sun Factor, RTG ignores it) must be ≥ total Draw (Bus + Instruments + Comms + Propulsion + Supports).
- **Data (Mbps):** Instruments' total data rate vs. Comms downlink × Orbit Signal Factor.

**Hard limits (block launch):** Cost ≤ cap, Mass ≤ capacity, Power generated ≥ draw, Propulsion ΔV ≥ Orbit minimum, Orbit allowed by Mission, at least one instrument with a Mission priority tag.

**Soft limit (does not block launch):** Data. If instruments produce more than the downlink can send, science is throttled: `Data Throttle = min(1, Downlink / Data Generated)`.

**Margin** per resource = (Limit − Used) / Limit.
| Margin | Tier | Event bonus |
|---|---|---|
| ≥ 25% | Green | +2 |
| 10–24% | Yellow | +1 |
| < 10% | Red | 0 |

Margins are the main link between Build and Flight: what you leave spare is what saves you later. Leftover budget becomes the **Contingency Fund**.

## 4. Mission Cards
| Mission | Budget Cap | Science Target | Priority Tags (×1.5 science) | Allowed Orbits |
|---|---|---|---|---|
| Lunar Ice Hunter (Moon) | 480 | 50 | Subsurface, Composition | Lunar Polar |
| Red Planet Climate Watch (Mars) | 700 | 60 | Imaging, Composition | Mars Orbit |
| Wildfire Watch (Earth Observation) | 300 | 40 | Thermal, Imaging | LEO, Sun-Synchronous |
| Asteroid Rendezvous | 600 | 55 | Composition, Topography | Asteroid Rendezvous |

Suggested order for tutorial and difficulty: Wildfire Watch (easy) → Lunar Ice Hunter → Asteroid Rendezvous → Red Planet Climate Watch (hard).

## 5. Orbit Cards
| Orbit | Reach Factor | Sun Factor | Signal Factor | Min ΔV (m/s) | Radiation |
|---|---|---|---|---|---|
| Low Earth Orbit (LEO) | 1.00 | 1.0 | 1.0 | 200 | 1 |
| Sun-Synchronous (SSO) | 0.85 | 1.0 | 1.0 | 300 | 1 |
| Lunar Polar | 0.35 | 1.0 | 0.8 | 1,500 | 2 |
| Mars Orbit | 0.25 | 0.43 | 0.4 | 1,800 | 2 |
| Asteroid Rendezvous | 0.20 | 0.6 | 0.5 | 2,500 | 3 |

- **Reach Factor:** farther destinations cut how much mass the rocket can deliver.
- **Sun Factor:** multiplies solar panel output (not RTG).
- **Signal Factor:** multiplies Comms downlink (distance weakens signal).
- **Radiation:** raises Solar Storm difficulty (+0 / +1 / +2 for level 1 / 2 / 3).

## 6. Rocket Cards
| Rocket | Capacity to LEO (kg) | Cost | Launch Reliability |
|---|---|---|---|
| Light Lifter | 1,500 | 60 | 85% |
| Medium Lifter | 3,000 | 150 | 92% |
| Heavy Lifter | 10,000 | 300 | 96% |
| Super Heavy Lifter | 30,000 | 500 | 98% |

`Mass Limit = Capacity × Orbit Reach Factor`

## 7. Spacecraft Cards

**Bus**
| Bus | Mass | Cost | Power Draw | Instrument Slots | Support Slots |
|---|---|---|---|---|---|
| Small Bus | 150 | 40 | 50 | 2 | 1 |
| Medium Bus | 300 | 80 | 80 | 3 | 2 |
| Large Bus | 600 | 150 | 150 | 4 | 3 |

**Power**
| Card | Mass | Cost | Output (W) | Notes |
|---|---|---|---|---|
| Solar Array S | 30 | 10 | 200 | × Sun Factor |
| Solar Array L | 80 | 25 | 600 | × Sun Factor |
| Solar Array XL | 140 | 45 | 1,000 | × Sun Factor |
| RTG | 45 | 90 | 150 | Ignores Sun Factor; tag: Radiation-Hardened |

**Communications**
| Card | Mass | Cost | Power Draw | Downlink (Mbps) |
|---|---|---|---|---|
| Small Antenna | 10 | 8 | 20 | 5 |
| Medium Antenna | 30 | 20 | 60 | 25 |
| Large Dish | 80 | 45 | 150 | 100 |

**Propulsion**
| Card | Mass | Cost | Power Draw | ΔV (m/s) |
|---|---|---|---|---|
| Chemical Small | 60 | 20 | 0 | 1,000 |
| Chemical Large | 150 | 40 | 0 | 2,000 |
| Ion Drive | 90 | 70 | 150 | 4,000 |

**Support (event counters)**
| Card | Mass | Cost | Power Draw | Tag |
|---|---|---|---|---|
| Radiation Shield | 25 | 12 | 0 | Radiation-Hardened |
| Redundant Computer | 10 | 15 | 10 | Redundant |
| Onboard Storage | 8 | 10 | 5 | Storage |
| Thermal Control | 12 | 8 | 10 | Thermal |

## 8. Scientific Instrument Cards
| Instrument | Cost | Mass | Power | Data (Mbps) | Science | Tag |
|---|---|---|---|---|---|---|
| Wide-Field Camera | 15 | 20 | 30 | 10 | 8 | Imaging |
| High-Res Imager | 40 | 60 | 80 | 40 | 15 | Imaging |
| Thermal IR Imager | 30 | 30 | 45 | 10 | 12 | Thermal |
| Spectrometer | 35 | 35 | 50 | 4 | 14 | Composition |
| Radar Sounder | 60 | 80 | 150 | 10 | 18 | Subsurface |
| Neutron Detector | 30 | 25 | 30 | 1 | 12 | Subsurface |
| Laser Altimeter | 45 | 45 | 70 | 4 | 14 | Topography |
| Magnetometer | 10 | 8 | 10 | 0.5 | 6 | Fields |

`Potential Science = Σ (instrument Science × 1.5 if its tag is a Mission priority tag, else × 1)`

## 9. Flight Phase (6 stages)
| Stage | What happens |
|---|---|
| 1. Launch | Roll d100 against Rocket Launch Reliability. Fail = mission lost (see Modes). |
| 2. Cruise | Draw 1 Event Card. |
| 3. Orbit Insertion | Auto-check: Propulsion ΔV vs. Orbit Min ΔV. Leftover ΔV = fuel margin (used by thruster events). **If ΔV < Min ΔV here (e.g., after a Stage-2 Thruster Glitch): Mission Lost** (v7.1 P2). |
| 4. Science Ops 1 | Draw 1 Event Card, then collect science. |
| 5. Science Ops 2 | Draw 1 Event Card, then collect science. |
| 6. Science Ops 3 | Draw 1 Event Card, then collect science. |

**Science per Ops stage** = `Potential Science ÷ 3 × Data Throttle × Event Multiplier`. Instruments switched off by an event or by the player produce nothing that stage.

**Event Multiplier mapping (v7.1 P6):** Success = 1.0; Partial/Fail per card text (−25% → 0.75, −50% → 0.5, stage lost → 0). Instrument offline effects apply on top, per instrument.

## 10. Event Cards and Resolution

**Resolution (same for every event):**
`Result = d6 + Margin Bonus + Tag Bonus + Response Bonus`, compared with the event's **Difficulty**.
- Margin Bonus: Green +2, Yellow +1, Red 0, using the margin of the resource the event checks.
- Tag Bonus: +2 if the build has the counter tag listed on the card.
- Response Bonus: from player responses below (max +2 total).
- **Success:** Result ≥ Difficulty, no loss.
- **Partial:** Result = Difficulty − 1, minor loss.
- **Fail:** Result ≤ Difficulty − 2, major loss.

**Transparency rule:** before each draw, show the player their current odds per event type (teaches that margins buy safety).

**Player Responses (only with what was built in):**
- **Safe Mode:** switch off one instrument this stage (it earns 0 science). +1 on Power and Thermal events.
- **Spend Contingency:** pay 10 from leftover budget. +1 on any event (max twice per event).
- **Throttle Data:** halve science this stage. +1 on Communications events.

**Event deck (v7.1 — Navigation Error removed per P1)**
| Event | Checks | Counter Tag | Diff. | Partial | Fail |
|---|---|---|---|---|---|
| Solar Storm | Power margin | Radiation-Hardened | 4 (+orbit radiation) | −25% science this stage | Random instrument offline this + next stage |
| Communications Blackout | Data margin | Storage | 4 | −50% science this stage | Science this stage lost |
| Instrument Fault | Cost margin (spare parts) | Redundant | 5 | One instrument off 1 stage | One instrument lost for the rest of the mission |
| Thruster Glitch | ΔV margin | none | 4 | Lose 300 m/s ΔV | Lose 700 m/s ΔV (insertion fails if below Min ΔV) |
| Budget Cut | Cost margin | none | 5 | Pay 5% of cap from Contingency | Pay 10% of cap; if unpaid, most expensive instrument off 1 stage |
| Micrometeoroid Strike | Mass margin (shielding mass) | Radiation-Hardened | 5 | Random instrument off 1 stage | Random instrument lost |
| Thermal Overheat | Power margin | Thermal | 4 | −25% science this stage | Random instrument offline 2 stages |
| Software Bug | Cost margin | Redundant | 3 | −25% science this stage | All science this stage lost |
| Dust Storm (Mars Orbit only) | Power margin | none | 5 | Solar output −15% this stage | Solar output −30% for 2 stages |
| Lucky Break (positive) | none | none | auto | +10% science this stage | n/a |
| Extended Funding (positive) | none | none | auto | +15 to Contingency Fund | n/a |

Draw rules (v7.1 P1): base deck = **8 negative + 2 positive = 10**, drawn without replacement; Mars adds Dust Storm (9+2). MVP cuts positives → exactly 8 event cards. After each event, show a short **Learning Moment** (1–2 sentences on the real-world equivalent).

## 11. Scoring (100 points, v7.1 formulas)
| Category | Points | How |
|---|---|---|
| Science Return | 50 | `50 × min(1, Science Collected ÷ Target)` |
| Resilience | 20 | `20 × (Successes + 0.5 × Partials) ÷ Events drawn`. Positive events count as automatic successes (P4). If positives are cut, denominator = negative events drawn. Zero events drawn → full 20. |
| Budget Efficiency | 15 | `15 × min(1, Leftover Budget ÷ (15% of cap))` (rewards a 15% reserve, nothing extra beyond that) |
| Margin Discipline | 15 | 5 pts each for Cost, Mass, Power (P3): margin < 10% → `5 × (margin / 0.10)`; 10–25% → `5`; > 25% → `5 × max(0, 1 − (margin − 0.25) / 0.25)` (0 at ≥ 50%; over-engineering is waste) |

**Mission outcome (v7.1 P5)**
- **Mission Lost:** launch failure, failed orbit insertion, or all instruments lost. Score = Margin Discipline only.
- **Failed** (< 40), **Partial Success** (40–59), **Success** (60–79), **Outstanding** (80+). **Both Success and Outstanding require Science Collected ≥ Target**; otherwise the outcome is capped at Partial Success regardless of score.

**Badges (optional, cheap to build):** Frugal Explorer (≥ 20% budget left), Minimalist (fewest cards in its mission), No Close Calls (all events Success), Against the Odds (Success with a Red margin).

## 12. Trade-off Report (end screen)
Auto-generated from the run:
- Top 3 decisions that helped (e.g., "Your 28% power margin turned a Solar Storm into a non-event").
- Top 3 decisions that hurt (e.g., "Small Antenna throttled science to 27%").
- A "What if" line per hurt decision (e.g., "A Medium Antenna costs 12 more and weighs 20 kg more").
- Score breakdown and a one-click **Replay with same mission**.

## 13. Game Modes
| Mode | Changes |
|---|---|
| Learning (default, MVP) | Launch never fails; odds always shown; hints on gauges |
| Standard (post-MVP) | Launch can fail; odds shown |
| Challenge (post-MVP) | Budget cap −10%; event deck hidden; launch can fail |

**Optional replay variety (post-MVP):** Draft Mode, where the player gets a random hand of 5 cards per category instead of the full catalog.

## 14. Worked Example (THE ENGINE'S ACCEPTANCE TEST)
Cards: Mission Lunar Ice Hunter, Orbit Lunar Polar, Rocket Medium Lifter, Medium Bus, Solar Array L, Medium Antenna, Chemical Large, Radiation Shield, instruments Radar Sounder + Neutron Detector + Spectrometer.
- **Cost:** 80 + 25 + 20 + 40 + 12 + (60 + 30 + 35) + 150 = **452 / 480** → margin 5.8% (Red)
- **Mass:** 300 + 80 + 30 + 150 + 25 + (80 + 25 + 35) = **725 / 1,050** (3,000 × 0.35) → margin 31% (Green)
- **Power draw:** 80 (bus) + 60 (comms) + (150 + 30 + 50) = **370 / 600 W** → margin 38% (Green)
- **Data:** 10 + 1 + 4 = 15 Mbps vs. 25 × 0.8 = **20 Mbps** → throttle 1.0, margin 25% (Green)
- **ΔV:** 2,000 vs. 1,500 required → OK
- **Potential Science:** Radar 18×1.5 + Neutron 12×1.5 + Spectrometer 14×1.5 = **66** vs. target 50 → OK
- Trade-off visible: Budget margin is Red, so a Budget Cut event is dangerous, while Power and Mass margins are strong.
- Light Lifter fails here (1,500 × 0.35 = 525 kg < 725 kg) — second unit test: `validateBuild` must reject it.

## 15. Interface Contract for Simulation & Mission Logic (FROZEN)
The Simulation member implements these functions. Mechanics owns the data and rules; Simulation owns the code. **`engine.ts` is pure TypeScript — zero React imports — so it runs and tests standalone.** Frontend builds against this contract with mock data from Hour 1.
- `validateBuild(build) → { valid, errors[], gauges{cost,mass,power,data}, margins{}, tiers{} }`
- `potentialScience(build) → number`
- `dataThrottle(build) → number (0–1)`
- `drawEvent(deck, mission) → eventCard`
- `resolveEvent(event, build, responses[]) → { roll, total, outcome: success|partial|fail, effects[] }`
- `runStage(state, stage) → state`
- `computeScore(runLog) → { total, breakdown{}, outcome, badges[] }`
- `buildReport(runLog) → { helped[], hurt[], whatIf[] }`

**Card data format (JSON, one file per card type; `inspiredBy` added per Section 19):**
```json
{
  "id": "instr_radar_sounder",
  "type": "instrument",
  "name": "Radar Sounder",
  "cost": 60,
  "mass": 80,
  "power": 150,
  "data": 10,
  "science": 18,
  "tags": ["Subsurface"],
  "flavor": "Sees below the surface using radio waves.",
  "inspiredBy": "Radar sounders flown on lunar orbiters"
}