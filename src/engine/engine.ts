import type {
  Build,
  CalculatedBuild,
  EventCard,
  EventPreview,
  EventResult,
  MissionState,
  PlayerResponse,
  Report,
  ScoreResult,
  StageResult,
  ValidationResult,
  Card,
  MarginTier,
  ResourceKey,
  ResponseKind,
  InstrumentState,
  ReportItem,
} from './types.ts';
import { cardById, events, eventById } from '../data/index.ts';
import { mulberry32, shuffle } from './rng.ts';

// Find an installed card by ID and verify that it belongs in the selected slot.
// Missing selections are allowed while the Build screen is being assembled;
// unknown IDs and wrong card types are configuration/input errors.
function selectedCard<T extends Card['type']>(
  id: string | null,
  expectedType: T
): Extract<Card, { type: T }> | null {
  if (id === null) return null;
  if (typeof id !== 'string' || id.trim() === '') {
    throw new Error(`Invalid ${expectedType} card ID`);
  }
  const card = cardById[id];
  if (!card || card.type !== expectedType) {
    throw new Error(`Unknown or incorrect ${expectedType} card: ${id}`);
  }
  return card as Extract<Card, { type: T }>;
}

function cardList<T extends Card['type']>(
  ids: string[],
  expectedType: T
): Extract<Card, { type: T }>[] {
  if (!Array.isArray(ids)) {
    throw new Error(`Invalid ${expectedType} card list`);
  }
  return ids.map((id) => {
    const card = selectedCard(id, expectedType);
    if (!card) throw new Error(`Missing ${expectedType} card ID in list`);
    return card;
  });
}

function nonnegative(value: number, field: string): number {
  if (typeof value !== 'number' || !Number.isFinite(value) || value < 0) {
    throw new Error(`Invalid numeric card data: ${field}`);
  }
  return value;
}

function margin(used: number, limit: number): number {
  // An unchosen prerequisite gives a zero limit; don't divide by zero.
  return limit > 0 ? (limit - used) / limit : 0;
}

function tier(ratio: number): MarginTier {
  return ratio >= 0.25 ? 'green' : ratio >= 0.10 ? 'yellow' : 'red';
}

// Rule source: Section 15.4 Canonical build calculations.
// No launch validation here; validateBuild handles LV-01..LV-08.
export function calculateBuild(build: Build): CalculatedBuild {
  const mission = selectedCard(build.missionId, 'mission');
  const orbit = selectedCard(build.orbitId, 'orbit');
  const rocket = selectedCard(build.rocketId, 'rocket');
  const bus = selectedCard(build.busId, 'bus');
  const power = selectedCard(build.powerId, 'power');
  const comms = selectedCard(build.commsId, 'comms');
  const propulsion = selectedCard(build.propulsionId, 'propulsion');
  const instruments = cardList(build.instrumentIds, 'instrument');
  const supports = cardList(build.supportIds, 'support');

  const payloadCards: Card[] = [
    ...(bus ? [bus] : []),
    ...(power ? [power] : []),
    ...(comms ? [comms] : []),
    ...(propulsion ? [propulsion] : []),
    ...instruments,
    ...supports,
  ];

  const cost = [
    ...(rocket ? [rocket] : []),
    ...payloadCards,
  ].reduce((sum, card) => sum + nonnegative(card.cost, `${card.id}.cost`), 0);

  // The launch vehicle is not included in payload mass.
  const mass = payloadCards.reduce(
    (sum, card) => sum + nonnegative(card.mass, `${card.id}.mass`),
    0
  );

  // Power-system cards produce energy; only installed consumers draw it.
  const powerDraw = [
    ...(bus ? [bus] : []),
    ...(comms ? [comms] : []),
    ...(propulsion ? [propulsion] : []),
    ...instruments,
    ...supports,
  ].reduce((sum, card) => sum + nonnegative(card.power, `${card.id}.power`), 0);

  const powerOutput = !power
    ? 0
    : nonnegative(power.output, `${power.id}.output`) *
      (power.source === 'rtg' ? 1 : orbit ? nonnegative(orbit.sunFactor, `${orbit.id}.sunFactor`) : 0);

  const dataGenerated = instruments.reduce(
    (sum, instrument) => sum + nonnegative(instrument.data, `${instrument.id}.data`),
    0
  );
  const downlink = comms && orbit
    ? nonnegative(comms.downlink, `${comms.id}.downlink`) *
      nonnegative(orbit.signalFactor, `${orbit.id}.signalFactor`)
    : 0;
  const dataThrottle = dataGenerated === 0
    ? 0
    : Math.min(1, downlink / dataGenerated);

  const instrumentContributions: Record<string, number> = {};
  for (const instrument of instruments) {
    const matchesPriority = mission?.priorityTags.some((tag) => instrument.tags.includes(tag)) ?? false;
    const contribution = nonnegative(instrument.science, `${instrument.id}.science`) *
      (matchesPriority ? 1.5 : 1);
    instrumentContributions[instrument.id] =
      (instrumentContributions[instrument.id] ?? 0) + contribution;
  }
  const potentialScience = Object.values(instrumentContributions).reduce((sum, n) => sum + n, 0);

  const limits = {
    cost: mission ? nonnegative(mission.budgetCap, `${mission.id}.budgetCap`) : 0,
    mass: rocket && orbit
      ? nonnegative(rocket.capacityLEO, `${rocket.id}.capacityLEO`) *
        nonnegative(orbit.reachFactor, `${orbit.id}.reachFactor`)
      : 0,
    power: powerOutput,
    data: downlink,
    deltaV: orbit ? nonnegative(orbit.minDeltaV, `${orbit.id}.minDeltaV`) : 0,
  };
  const totals = {
    cost,
    mass,
    powerDraw,
    powerOutput,
    dataGenerated,
    downlink,
    deltaV: propulsion ? nonnegative(propulsion.deltaV, `${propulsion.id}.deltaV`) : 0,
    potentialScience,
  };
  const margins = {
    cost: margin(totals.cost, limits.cost),
    mass: margin(totals.mass, limits.mass),
    power: margin(totals.powerDraw, limits.power),
    data: margin(totals.dataGenerated, limits.data),
    // Before insertion, ΔV margin is (available − required) / required.
    // ΔV capacity is the available reserve over the orbit's requirement.
    deltaV: limits.deltaV > 0
      ? (totals.deltaV - limits.deltaV) / limits.deltaV
      : 0,
  };

  return {
    totals,
    limits,
    margins,
    tiers: {
      cost: tier(margins.cost),
      mass: tier(margins.mass),
      power: tier(margins.power),
      data: tier(margins.data),
      deltaV: tier(margins.deltaV),
    },
    dataThrottle,
    contingencyAtLaunch: Math.max(0, limits.cost - totals.cost),
    instrumentContributions,
  };
}

// Rule source: Section 15.6 Launch Check (LV-01..LV-08), updated for v7.3 P7 G1-G2.
// All decisions come from the same card data used by calculateBuild().
export function validateBuild(build: Build): ValidationResult {
  const calculatedBuild = calculateBuild(build);
  const { totals, limits, dataThrottle } = calculatedBuild;
  const errors: ValidationResult['errors'] = [];
  const warnings: ValidationResult['warnings'] = [];

  function error(code: string, message: string): void {
    errors.push({ code, message });
  }

  const requiredSlots: Array<[string, string | null]> = [
    ['Mission', build.missionId],
    ['Orbit', build.orbitId],
    ['Rocket', build.rocketId],
    ['Bus', build.busId],
    ['Power', build.powerId],
    ['Communications', build.commsId],
    ['Propulsion', build.propulsionId],
  ];
  const missingSlots = requiredSlots
    .filter(([, id]) => id === null || id === '')
    .map(([slot]) => slot);
  if (missingSlots.length > 0) {
    error('LV-01', `Select the required cards: ${missingSlots.join(', ')}.`);
  }

  // LV-02: v7.3 minimums, bus limits, and no duplicate instrument/support IDs.
  const bus = selectedCard(build.busId, 'bus');
  const instrumentCount = build.instrumentIds.length;
  const supportCount = build.supportIds.length;
  if (instrumentCount < 2) {
    error('LV-02', `At least 2 instruments are required (selected: ${instrumentCount}).`);
  }
  if (supportCount < 1) {
    error('LV-02', 'At least 1 support card is required.');
  }
  if (bus && instrumentCount > bus.instrumentSlots) {
    error('LV-02', `${bus.name} has ${bus.instrumentSlots} instrument slot(s), but ${instrumentCount} instruments were selected.`);
  }
  if (bus && supportCount > bus.supportSlots) {
    error('LV-02', `${bus.name} has ${bus.supportSlots} support slot(s), but ${supportCount} supports were selected.`);
  }
  if (new Set(build.instrumentIds).size !== instrumentCount) {
    error('LV-02', 'Duplicate instrument cards are not allowed.');
  }
  if (new Set(build.supportIds).size !== supportCount) {
    error('LV-02', 'Duplicate support cards are not allowed.');
  }

  // LV-03: require at least one instrument matching a mission priority tag.
  const mission = selectedCard(build.missionId, 'mission');
  if (mission) {
    const hasPriorityInstrument = cardList(build.instrumentIds, 'instrument')
      .some((instrument) => instrument.tags.some((tag) => mission.priorityTags.includes(tag)));
    if (!hasPriorityInstrument) {
      error('LV-03', `Choose an instrument with a mission priority tag: ${mission.priorityTags.join(' or ')}.`);
    }
  }

  // LV-04: mission-specific orbit restriction.
  const orbit = selectedCard(build.orbitId, 'orbit');
  if (mission && orbit && !mission.allowedOrbits.includes(orbit.id)) {
    error('LV-04', `${orbit.name} is not an allowed orbit for ${mission.name}.`);
  }

  // LV-05..LV-08: hard resource constraints. Missing core cards are
  // separately reported by LV-01; avoid misleading resource errors until
  // the cards supplying the corresponding limit have been selected.
  if (mission && totals.cost > limits.cost) {
    error('LV-05', `Cost ${totals.cost} exceeds the mission budget of ${limits.cost} ($M).`);
  }
  if (selectedCard(build.rocketId, 'rocket') && orbit && totals.mass > limits.mass) {
    error('LV-06', `Payload mass ${totals.mass} kg exceeds the rocket/orbit limit of ${limits.mass} kg.`);
  }
  if (selectedCard(build.powerId, 'power') && orbit && totals.powerDraw > totals.powerOutput) {
    error('LV-07', `Power draw ${totals.powerDraw} W exceeds available output of ${totals.powerOutput} W.`);
  }
  if (selectedCard(build.propulsionId, 'propulsion') && orbit && totals.deltaV < limits.deltaV) {
    error('LV-08', `Available ΔV ${totals.deltaV} m/s is below the orbit requirement of ${limits.deltaV} m/s.`);
  }

  // Data is a SOFT constraint: warn about reduced downlink, never block launch.
  if (selectedCard(build.commsId, 'comms') && orbit && totals.dataGenerated > limits.data) {
    warnings.push({
      code: 'DATA-THROTTLE',
      message: `Only ${(dataThrottle * 100).toFixed(1)}% of generated science data can be transmitted.`,
    });
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
    calculatedBuild,
  };
}

// Rule source: Section 15.7. A mission always begins with a validated,
// frozen build; its event order is fixed by the seed for reproducible runs.
export function createMissionState(build: Build, mode: 'learning', seed: number): MissionState {
  if (mode !== 'learning') {
    throw new Error('Only Learning mode is supported in the MVP.');
  }
  if (!Number.isFinite(seed) || !Number.isInteger(seed)) {
    throw new Error('Mission seed must be a finite integer.');
  }
  const validation = validateBuild(build);
  if (!validation.valid) {
    const messages = validation.errors.map((issue) => `${issue.code}: ${issue.message}`);
    throw new Error(`Cannot launch an invalid build: ${messages.join(' | ')}`);
  }
  const calculated = validation.calculatedBuild;
  const cardIds = events.map((event) => event.id);
  if (cardIds.length !== 8 || new Set(cardIds).size !== 8) {
    throw new Error('MVP configuration requires exactly 8 unique negative events.');
  }
  // Separate copies ensure subsequent changes to the Build screen cannot alter
  // the frozen flight design or its launch-time scoring margins.
  const buildSnapshot: Build = {
    ...build,
    instrumentIds: [...build.instrumentIds],
    supportIds: [...build.supportIds],
  };
  return {
    runId: `learning-${build.missionId}-${seed}`,
    mode,
    seed,
    status: 'active',
    stage: 1,
    buildSnapshot,
    initialGauges: { ...calculated.totals },
    initialMargins: { ...calculated.margins },
    currentDeltaV: calculated.totals.deltaV,
    remainingDeltaV: null,
    contingencyFund: calculated.contingencyAtLaunch,
    scienceCollected: 0,
    instruments: buildSnapshot.instrumentIds.map((id) => ({
      id,
      status: 'active',
      offlineStagesRemaining: 0,
    })),
    temporaryEffects: [],
    eventDeck: shuffle(cardIds, mulberry32(seed)),
    eventsDrawn: [],
    eventResults: [],
    stageLog: [],
    score: null,
    report: null,
  };
}

function flightMargin(state: MissionState, resource: ResourceKey): number {
  const calc = calculateBuild(state.buildSnapshot);
  if (resource === 'deltaV') {
    const required = calc.limits.deltaV;
    if (required <= 0) return 0;
    // Before insertion, protect the required burn; after insertion, protect
    // the remaining reserve. This is the special ΔV margin rule in §15.5.
    return state.remainingDeltaV === null
      ? (state.currentDeltaV - required) / required
      : state.remainingDeltaV / required;
  }
  if (resource === 'cost') {
    return calc.limits.cost > 0 ? state.contingencyFund / calc.limits.cost : 0;
  }
  if (resource === 'mass') return state.initialMargins.mass;

  // Data and Power use functioning instrument loads rather than permanently
  // counting lost/offline payloads as operational. The original build totals
  // remain unchanged for the final score.
  const inactiveIds = new Set(state.instruments
    .filter((instrument) => instrument.status !== 'active')
    .map((instrument) => instrument.id));
  const inactivePower = state.buildSnapshot.instrumentIds.reduce((sum, id) => {
    const instrument = selectedCard(id, 'instrument');
    return sum + (inactiveIds.has(id) ? (instrument?.power ?? 0) : 0);
  }, 0);
  if (resource === 'power') {
    const outputMultiplier = state.temporaryEffects
      .filter((effect) => effect.type === 'solar_output_multiplier')
      .reduce((factor, effect) => factor * effect.value, 1);
    const effectiveOutput = calc.totals.powerOutput * outputMultiplier;
    return margin(calc.totals.powerDraw - inactivePower, effectiveOutput);
  }
  const activeData = state.buildSnapshot.instrumentIds.reduce((sum, id) => {
    const instrument = selectedCard(id, 'instrument');
    return sum + (inactiveIds.has(id) ? 0 : (instrument?.data ?? 0));
  }, 0);
  return margin(activeData, calc.totals.downlink);
}

function describeRolls(rolls: number[]): string {
  if (rolls.length === 0) return 'none';
  if (rolls.length === 1) return String(rolls[0]);
  return `${rolls[0]}-${rolls[rolls.length - 1]}`;
}

// Rule source: Sections 15.5, 15.9, 15.10, 15.11.
// Outcome ranges describe the unmodified d6; optional response bonuses are
// added at resolution time, after the player chooses their response.
export function getEventPreview(state: MissionState, event: EventCard): EventPreview {
  if (state.status !== 'active') {
    throw new Error('Cannot preview an event for an inactive mission.');
  }
  if (!eventById[event.id]) {
    throw new Error(`Unknown event: ${event.id}`);
  }
  const ratio = flightMargin(state, event.checks);
  const marginBonus = ratio >= 0.25 ? 2 : ratio >= 0.10 ? 1 : 0;
  const power = selectedCard(state.buildSnapshot.powerId, 'power');
  const supports = cardList(state.buildSnapshot.supportIds, 'support');
  const hasTag = event.counterTag !== null && (
    (power?.tags.includes(event.counterTag) ?? false) ||
    supports.some((support) => support.tags.includes(event.counterTag!))
  );
  const tagBonus = hasTag ? 2 : 0;
  const orbit = selectedCard(state.buildSnapshot.orbitId, 'orbit');
  const radiationAdjustment = event.id === 'event_solar_storm' && orbit
    ? orbit.radiation - 1
    : 0;
  const finalDifficulty = event.baseDifficulty + radiationAdjustment;
  const activeInstrumentCount = state.instruments.filter((instrument) => instrument.status === 'active').length;
  const legalResponses: ResponseKind[] = event.allowedResponses.filter((kind) => {
    if (kind === 'spend_contingency') return state.contingencyFund >= 10;
    if (kind === 'safe_mode') return activeInstrumentCount > 0;
    return true;
  });
  const success: number[] = [];
  const partial: number[] = [];
  const fail: number[] = [];
  for (let d6 = 1; d6 <= 6; d6++) {
    const total = d6 + marginBonus + tagBonus;
    if (total >= finalDifficulty) success.push(d6);
    else if (total === finalDifficulty - 1) partial.push(d6);
    else fail.push(d6);
  }
  const freePractice = state.stage === 2 && legalResponses.some((kind) => kind === 'safe_mode' || kind === 'throttle_data');
  return {
    eventId: event.id,
    finalDifficulty,
    marginBonus,
    tagBonus,
    legalResponses,
    outcomeRanges: {
      success: describeRolls(success),
      partial: describeRolls(partial),
      fail: describeRolls(fail),
    },
    explanation: `d6 + margin ${marginBonus} + counter-tag ${tagBonus} vs difficulty ${finalDifficulty}; ranges shown before response bonuses.` +
      (freePractice ? ' Cruise: free practice (no science is collected during Cruise).' : ''),
  };
}

// Rule source: Section 15.9. Store the seeded deck once and draw in order.
// The original deck remains available for determinism checks and replay logs.
export function drawEvent(state: MissionState): { state: MissionState; event: EventCard } {
  if (state.status !== 'active') {
    throw new Error('Cannot draw events after mission completion.');
  }
  if (state.eventsDrawn.length >= 4) {
    throw new Error('The MVP allows only four event draws per run.');
  }
  const eventId = state.eventDeck[state.eventsDrawn.length];
  if (!eventId || state.eventsDrawn.includes(eventId)) {
    throw new Error('No unique event remains in the seeded deck.');
  }
  const event = eventById[eventId];
  if (!event) throw new Error(`Unknown event in deck: ${eventId}`);
  return {
    state: {
      ...state,
      eventsDrawn: [...state.eventsDrawn, eventId],
    },
    event,
  };
}

// A deterministic independent roll for each event resolution. The random
// stream does NOT depend on global Math.random or mutable module state.
// Repeating the same state + event + responses yields identical results.
function hashText(value: string): number {
  let hash = 2166136261;
  for (const char of value) {
    hash = Math.imul(hash ^ char.charCodeAt(0), 16777619);
  }
  return hash >>> 0;
}

function eventRandom(state: MissionState, event: EventCard): () => number {
  const combined = state.seed ^ hashText(event.id) ^
    Math.imul(state.eventResults.length + 1, 0x9e3779b1) ^
    Math.imul(state.stage, 0x85ebca6b);
  return mulberry32(combined >>> 0);
}

function cloneState(state: MissionState): MissionState {
  return {
    ...state,
    instruments: state.instruments.map((instrument) => ({ ...instrument })),
    temporaryEffects: state.temporaryEffects.map((effect) => ({ ...effect })),
    eventsDrawn: [...state.eventsDrawn],
    eventResults: [...state.eventResults],
    stageLog: [...state.stageLog],
  };
}

function offlineInstrument(instrument: InstrumentState, stages: number): void {
  if (instrument.status === 'lost') return;
  instrument.status = 'offline';
  instrument.offlineStagesRemaining = Math.max(instrument.offlineStagesRemaining, stages);
}

// Event outcomes and effects follow Sections 15.10-15.13. The response cost
// is paid AFTER the preview's margin bonus is calculated, so the number shown
// to the player remains the number used in this roll.
export function resolveEvent(
  state: MissionState,
  event: EventCard,
  responses: PlayerResponse[]
): { state: MissionState; result: EventResult } {
  if (state.status !== 'active') throw new Error('Cannot resolve an event after the mission ends.');
  if (!Array.isArray(responses)) throw new Error('Invalid event responses.');
  const preview = getEventPreview(state, event);
  const maxSpends = responses.filter((response) => response.kind === 'spend_contingency').length;
  if (maxSpends > 2) throw new Error('Spend Contingency may be used at most twice per event.');
  if (responses.filter((response) => response.kind === 'safe_mode').length > 1 ||
      responses.filter((response) => response.kind === 'throttle_data').length > 1) {
    throw new Error('A response may be selected at most once (except Spend Contingency).');
  }
  for (const response of responses) {
    if (!event.allowedResponses.includes(response.kind) || !preview.legalResponses.includes(response.kind)) {
      throw new Error(`Response ${response.kind} is illegal for ${event.id}.`);
    }
  }
  if (maxSpends * 10 > state.contingencyFund) {
    throw new Error('Insufficient contingency for the requested responses.');
  }

  const next = cloneState(state);
  const messages: string[] = [];
  for (const response of responses) {
    if (response.kind === 'spend_contingency') {
      next.contingencyFund -= 10;
      messages.push('Spent $10M contingency for +1.');
    } else if (response.kind === 'safe_mode') {
      const selected = next.instruments.find((instrument) =>
        instrument.id === response.instrumentId && instrument.status === 'active');
      if (!selected) throw new Error('Safe Mode requires a selected active instrument.');
      offlineInstrument(selected, 1);
      messages.push(`Safe Mode temporarily disabled ${selected.id} for +1.`);
    } else if (response.kind === 'throttle_data') {
      next.temporaryEffects.push({ type: 'science_multiplier', value: 0.5, stagesRemaining: 1 });
      messages.push('Throttled science data this stage for +1.');
    }
  }
  const responseBonus = Math.min(2, responses.length);
  const rand = eventRandom(state, event);
  const roll = Math.floor(rand() * 6) + 1;
  const total = roll + preview.marginBonus + preview.tagBonus + responseBonus;
  const outcome = total >= preview.finalDifficulty ? 'success'
    : total === preview.finalDifficulty - 1 ? 'partial' : 'fail';
  const effects = event.effects[outcome].map((effect) => ({ ...effect }));
  const mission = selectedCard(state.buildSnapshot.missionId, 'mission');
  if (!mission) throw new Error('Mission card missing from launched state.');
  let budgetUnpaid = false;

  for (const effect of effects) {
    if (effect.condition === 'if_unpaid' && !budgetUnpaid) continue;
    if (effect.type === 'science_multiplier' || effect.type === 'solar_output_multiplier') {
      if (effect.value === undefined || !Number.isFinite(effect.value) || effect.value < 0) {
        throw new Error(`Invalid ${effect.type} effect value.`);
      }
      next.temporaryEffects.push({
        type: effect.type,
        value: effect.value,
        stagesRemaining: Math.max(1, effect.duration ?? 1),
      });
      messages.push(`${effect.type}: ×${effect.value}.`);
    } else if (effect.type === 'delta_v_loss') {
      const loss = nonnegative(effect.value ?? NaN, `${event.id}.delta_v_loss`);
      if (next.remainingDeltaV === null) next.currentDeltaV = Math.max(0, next.currentDeltaV - loss);
      else next.remainingDeltaV = Math.max(0, next.remainingDeltaV - loss);
      messages.push(`Lost ${loss} m/s ΔV.`);
    } else if (effect.type === 'contingency_loss') {
      const fraction = nonnegative(effect.value ?? NaN, `${event.id}.contingency_loss`);
      const requested = fraction * mission.budgetCap;
      const paid = Math.min(next.contingencyFund, requested);
      next.contingencyFund = Math.max(0, next.contingencyFund - requested);
      budgetUnpaid = requested > paid;
      messages.push(`Budget cut $${requested.toFixed(1)}M; paid $${paid.toFixed(1)}M from contingency.`);
    } else if (effect.type === 'contingency_gain') {
      next.contingencyFund += nonnegative(effect.value ?? NaN, `${event.id}.contingency_gain`);
    } else if (effect.type === 'instrument_offline' || effect.type === 'instrument_lost') {
      const active = next.instruments.filter((instrument) => instrument.status === 'active');
      if (active.length === 0) {
        messages.push(`${effect.type}: no active instrument to affect.`);
        continue;
      }
      let target: InstrumentState;
      if (effect.target === 'most_expensive_active') {
        const maxCost = Math.max(...active.map((instrument) =>
          selectedCard(instrument.id, 'instrument')?.cost ?? 0));
        const tied = active.filter((instrument) =>
          selectedCard(instrument.id, 'instrument')?.cost === maxCost);
        target = tied[Math.floor(rand() * tied.length)]!;
      } else {
        target = active[Math.floor(rand() * active.length)]!;
      }
      if (effect.type === 'instrument_lost') {
        target.status = 'lost';
        target.offlineStagesRemaining = 0;
        messages.push(`${target.id} permanently lost.`);
      } else {
        offlineInstrument(target, Math.max(1, effect.duration ?? 1));
        messages.push(`${target.id} offline for ${effect.duration ?? 1} stage(s).`);
      }
    } else {
      const neverEffect: never = effect.type;
      throw new Error(`Unhandled effect type: ${neverEffect}`);
    }
  }
  next.contingencyFund = Math.max(0, next.contingencyFund);
  const result: EventResult = {
    eventId: event.id,
    stage: state.stage,
    roll,
    checkedResource: event.checks,
    marginRatio: flightMargin(state, event.checks),
    marginBonus: preview.marginBonus,
    tagBonus: preview.tagBonus,
    responseBonus,
    responses: responses.map((response) => ({ ...response })),
    finalDifficulty: preview.finalDifficulty,
    total,
    outcome,
    effects,
    learningMoment: event.learningMoment,
    explanation: `${event.name}: d6 ${roll} + margin ${preview.marginBonus} + tag ${preview.tagBonus} ` +
      `+ response ${responseBonus} = ${total} vs difficulty ${preview.finalDifficulty} (${outcome}). ` +
      messages.join(' '),
  };
  next.eventResults.push(result);
  return { state: next, result };
}

// Science is collected only at Ops stages 4-6, AFTER event and player-response
// effects. Instrument outages affect both downlink usage and science potential.
export function collectScience(state: MissionState): { state: MissionState; science: number } {
  if (state.status !== 'active' || state.stage < 4 || state.stage > 6) {
    throw new Error('Science can only be collected during an active Science Ops stage.');
  }
  const calc = calculateBuild(state.buildSnapshot);
  const active = state.instruments.filter((instrument) => instrument.status === 'active');
  const activePotential = active.reduce((sum, instrument) =>
    sum + (calc.instrumentContributions[instrument.id] ?? 0), 0);
  const dataGenerated = active.reduce((sum, instrument) => {
    const card = selectedCard(instrument.id, 'instrument');
    return sum + (card?.data ?? 0);
  }, 0);
  const throttle = dataGenerated > 0 ? Math.min(1, calc.totals.downlink / dataGenerated) : 0;
  const multipliers = state.temporaryEffects
    .filter((effect) => effect.type === 'science_multiplier' && effect.stagesRemaining > 0)
    .reduce((factor, effect) => factor * effect.value, 1);
  const science = Math.max(0, (activePotential / 3) * throttle * multipliers);
  return {
    state: { ...state, scienceCollected: state.scienceCollected + science },
    science,
  };
}

// Expire short-lived effects AFTER a stage is processed: an outage of duration
// two affects the stage where it happens and the next stage.
function finishStage(state: MissionState): MissionState {
  const next = cloneState(state);
  next.instruments = next.instruments.map((instrument) => {
    if (instrument.status !== 'offline') return instrument;
    const remaining = Math.max(0, instrument.offlineStagesRemaining - 1);
    return {
      ...instrument,
      offlineStagesRemaining: remaining,
      status: remaining === 0 ? 'active' : 'offline',
    };
  });
  next.temporaryEffects = next.temporaryEffects
    .map((effect) => ({ ...effect, stagesRemaining: effect.stagesRemaining - 1 }))
    .filter((effect) => effect.stagesRemaining > 0);
  return next;
}

function finishMission(state: MissionState, status: 'lost' | 'completed'): MissionState {
  const final: MissionState = { ...state, status };
  const score = computeScore(final);
  return { ...final, score, report: buildReport(final) };
}

// Six named stages; Flight UI calls once per stage. At the end of Cruise we
// pre-check insertion viability so a depleted spacecraft cannot enter Orbit
// Insertion as active (required by existing acceptance test #9).
export function runStage(
  state: MissionState,
  input: PlayerResponse[]
): { state: MissionState; result: StageResult; nextRequiredAction: string } {
  if (state.status !== 'active') throw new Error('The mission has already ended.');
  if (!Array.isArray(input)) throw new Error('Invalid player responses.');
  if (!Number.isInteger(state.stage) || state.stage < 1 || state.stage > 6) {
    throw new Error(`Invalid flight stage ${state.stage}.`);
  }
  const stage = state.stage;
  let next = cloneState(state);
  let explanation = '';
  let scienceCollected = 0;

  if (stage === 1) {
    if (input.length > 0) throw new Error('Launch has no event response.');
    explanation = 'Learning-mode launch proceeds, regardless of the optional practice roll.';
    next = finishStage(next);
    next.stage = 2;
  } else if (stage === 2 || stage >= 4) {
    const draw = drawEvent(next);
    const resolved = resolveEvent(draw.state, draw.event, input);
    next = resolved.state;
    explanation = resolved.result.explanation;
    if (stage >= 4) {
      const collected = collectScience(next);
      next = collected.state;
      scienceCollected = collected.science;
      explanation += ` Science collected: ${scienceCollected.toFixed(1)}.`;
    }
    next = finishStage(next);
    if (next.instruments.every((instrument) => instrument.status === 'lost')) {
      next = finishMission(next, 'lost');
      explanation += ' All instruments permanently lost: mission lost.';
    } else if (stage === 2) {
      const required = calculateBuild(next.buildSnapshot).limits.deltaV;
      if (next.currentDeltaV < required) {
        next = finishMission(next, 'lost');
        explanation += ' Insufficient ΔV at the insertion boundary: mission lost.';
      } else {
        next.stage = 3;
      }
    } else if (stage === 6) {
      next = finishMission(next, 'completed');
      explanation += ' Mission completed.';
    } else {
      next.stage = stage + 1;
    }
  } else { // Stage 3 Orbit Insertion
    if (input.length > 0) throw new Error('Orbit Insertion has no event response.');
    const required = calculateBuild(next.buildSnapshot).limits.deltaV;
    if (next.currentDeltaV < required) {
      next = finishMission(next, 'lost');
      explanation = `Insufficient ΔV: ${next.currentDeltaV} < ${required} m/s. Mission lost.`;
    } else {
      next.remainingDeltaV = next.currentDeltaV - required;
      explanation = `Orbit inserted using ${required} m/s ΔV; ${next.remainingDeltaV} m/s reserve remains.`;
      next = finishStage(next);
      next.stage = 4;
    }
  }

  const result: StageResult = { stage, scienceCollected, explanation };
  next.stageLog = [...next.stageLog, result];
  return {
    state: next,
    result,
    nextRequiredAction: next.status !== 'active' ? 'report'
      : (next.stage === 2 || next.stage >= 4 ? 'event_response' : 'advance'),
  };
}

function disciplinePoints(m: number): number {
  if (m < 0) return 0;
  if (m < 0.1) return 5 * (m / 0.1);
  if (m <= 0.25) return 5;
  return Math.max(0, 5 * (1 - (m - 0.25) / 0.50));
}

export function computeScore(state: MissionState): ScoreResult {
  const mission = selectedCard(state.buildSnapshot.missionId, 'mission');
  if (!mission) throw new Error('Cannot score an unknown mission.');
  const marginByResource = {
    cost: disciplinePoints(state.initialMargins.cost),
    mass: disciplinePoints(state.initialMargins.mass),
    power: disciplinePoints(state.initialMargins.power),
  };
  const marginScore = Object.values(marginByResource).reduce((sum, value) => sum + value, 0);
  if (state.status === 'lost') {
    return {
      total: marginScore,
      breakdown: { science: 0, resilience: 0, budget: 0, margin: marginScore },
      marginByResource,
      outcome: 'mission_lost',
    };
  }
  const science = 50 * Math.min(1, state.scienceCollected / mission.scienceTarget);
  const resolvedCount = state.eventResults.length;
  const success = state.eventResults.filter((event) => event.outcome === 'success').length;
  const partial = state.eventResults.filter((event) => event.outcome === 'partial').length;
  const resilience = resolvedCount === 0 ? 20 : 20 * (success + 0.5 * partial) / resolvedCount;
  const budget = 15 * Math.min(1, Math.max(0, state.contingencyFund) / (mission.budgetCap * 0.15));
  const total = science + resilience + budget + marginScore;
  const outcome = total < 40 || state.scienceCollected < mission.scienceTarget ? 'failed'
    : total < 60 ? 'partial_success' : total < 80 ? 'success' : 'outstanding';
  return {
    total,
    breakdown: { science, resilience, budget, margin: marginScore },
    marginByResource,
    outcome,
  };
}

// This first report implementation only describes causes present in the actual
// run log. A separate content review can refine the wording/what-if templates.
export function buildReport(state: MissionState): Report {
  const build = calculateBuild(state.buildSnapshot);
  const helped: ReportItem[] = [];
  const hurt: ReportItem[] = [];
  const mission = selectedCard(state.buildSnapshot.missionId, 'mission');
  if (!mission) throw new Error('Cannot build a report without a mission.');

  const countered = state.eventResults.filter((event) => event.tagBonus === 2);
  if (countered.length > 0) {
    helped.push({ title: 'Protective systems', detail: `${countered.length} event(s) received a +2 counter-tag bonus.` });
  }
  const greenEvents = state.eventResults.filter((event) => event.marginBonus === 2);
  if (greenEvents.length > 0) {
    helped.push({ title: 'Healthy reserves', detail: `${greenEvents.length} event(s) received +2 from a Green resource margin.` });
  }
  if (build.dataThrottle === 1) {
    helped.push({ title: 'Full data downlink', detail: `Initial data ${build.totals.dataGenerated} Mbps fits ${build.totals.downlink} Mbps downlink.` });
  }
  const prioritized = Object.values(build.instrumentContributions)
    .reduce((sum, value) => sum + value, 0);
  if (prioritized > 0) {
    helped.push({ title: 'Mission-aligned instruments', detail: `Installed instruments provide ${prioritized} potential science against a target of ${mission.scienceTarget}.` });
  }
  if (build.dataThrottle < 1) {
    hurt.push({
      title: 'Data bottleneck',
      detail: `At launch, ${build.totals.dataGenerated} Mbps generated exceeded ${build.totals.downlink} Mbps downlink (throttle ${(build.dataThrottle * 100).toFixed(1)}%).`,
      whatIf: `A communications card with at least ${build.totals.dataGenerated} Mbps effective downlink would eliminate this initial throttle, if the build remains valid.`,
    });
  }
  for (const resource of ['cost', 'mass', 'power'] as const) {
    if (build.margins[resource] < 0.1) {
      hurt.push({
        title: `Tight ${resource} margin`,
        detail: `Initial ${resource} margin was ${(build.margins[resource] * 100).toFixed(1)}%, below the 10% Yellow threshold.`,
        whatIf: `Compare another allowed component combination that brings ${resource} margin to at least 10%; verify the alternative with Launch Check.`,
      });
    }
  }
  const losses = state.instruments.filter((instrument) => instrument.status === 'lost');
  if (losses.length > 0) {
    hurt.push({
      title: 'Instrument damage',
      detail: `${losses.length} instrument(s) were permanently lost during the mission.`,
      whatIf: `Review event counters for the recorded faults to reduce the chance of another instrument loss.`,
    });
  }
  if (state.status === 'lost' && state.currentDeltaV < build.limits.deltaV && state.remainingDeltaV === null) {
    hurt.unshift({
      title: 'Insufficient insertion reserve',
      detail: `Only ${state.currentDeltaV} m/s ΔV remained against ${build.limits.deltaV} m/s required.`,
      whatIf: `An alternate propulsion card providing at least ${build.limits.deltaV} m/s after recorded losses would allow insertion, subject to build limits.`,
    });
  }
  return { helped: helped.slice(0, 3), hurt: hurt.slice(0, 3) };
}
