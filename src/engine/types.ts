export type CardType = 'mission'|'orbit'|'rocket'|'bus'|'power'|'comms'|'propulsion'|'instrument'|'support'|'event';
export type MarginTier = 'green'|'yellow'|'red';
export type ResourceKey = 'cost'|'mass'|'power'|'data'|'deltaV';
export type InstrumentTag = 'Imaging'|'Thermal'|'Composition'|'Subsurface'|'Topography'|'Fields';
export type CounterTag = 'Radiation-Hardened'|'Redundant'|'Storage'|'Thermal';
export type ResponseKind = 'safe_mode'|'spend_contingency'|'throttle_data';
export type Outcome = 'success'|'partial'|'fail';
export type MissionOutcome = 'mission_lost'|'failed'|'partial_success'|'success'|'outstanding';
export type InstrumentStatus = 'active'|'offline'|'lost';
export type EffectType = 'science_multiplier'|'instrument_offline'|'instrument_lost'|'delta_v_loss'|'contingency_loss'|'solar_output_multiplier'|'contingency_gain';
export type EffectTarget = 'random_active'|'most_expensive_active';

export interface Effect {
  type: EffectType;
  value?: number;
  duration?: number;
  target?: EffectTarget;
  condition?: 'if_unpaid';
}
// contingency_loss value = FRACTION OF BUDGET CAP (0.05 = 5% of cap), not an absolute amount.

interface CardBase {
  id: string;
  type: CardType;
  name: string;
  cost: number;
  mass: number;
  flavor?: string;
  inspiredBy?: string;
}

export interface MissionCard extends CardBase {
  type: 'mission';
  budgetCap: number;
  scienceTarget: number;
  priorityTags: InstrumentTag[];
  allowedOrbits: string[];
}

export interface OrbitCard extends CardBase {
  type: 'orbit';
  reachFactor: number;
  sunFactor: number;
  signalFactor: number;
  minDeltaV: number;
  radiation: 1 | 2 | 3;
}

export interface RocketCard extends CardBase {
  type: 'rocket';
  capacityLEO: number;
  reliability: number;
} // reliability 0..1

export interface BusCard extends CardBase {
  type: 'bus';
  power: number;
  instrumentSlots: number;
  supportSlots: number;
}

export interface PowerCard extends CardBase {
  type: 'power';
  output: number;
  source: 'solar' | 'rtg';
  tags: CounterTag[];
}

export interface CommsCard extends CardBase {
  type: 'comms';
  power: number;
  downlink: number;
}

export interface PropulsionCard extends CardBase {
  type: 'propulsion';
  power: number;
  deltaV: number;
}

export interface InstrumentCard extends CardBase {
  type: 'instrument';
  power: number;
  data: number;
  science: number;
  tags: InstrumentTag[];
}

export interface SupportCard extends CardBase {
  type: 'support';
  power: number;
  tags: CounterTag[];
}

export interface EventCard {
  id: string;
  type: 'event';
  name: string;
  checks: ResourceKey;
  counterTag: CounterTag | null;
  baseDifficulty: number;
  allowedResponses: ResponseKind[];
  effects: {
    success: Effect[];
    partial: Effect[];
    fail: Effect[];
  };
  learningMoment: string;
}

export type Card = MissionCard | OrbitCard | RocketCard | BusCard | PowerCard | CommsCard | PropulsionCard | InstrumentCard | SupportCard;
// NOTE: on bus/comms/propulsion/instrument/support, `power` means POWER DRAW (W). Only PowerCard has `output`.

export interface Build {
  missionId: string | null;
  orbitId: string | null;
  rocketId: string | null;
  busId: string | null;
  powerId: string | null;
  commsId: string | null;
  propulsionId: string | null;
  instrumentIds: string[];
  supportIds: string[];
}

export interface Totals {
  cost: number;
  mass: number;
  powerDraw: number;
  powerOutput: number;
  dataGenerated: number;
  downlink: number;
  deltaV: number;
  potentialScience: number;
}

export interface Limits {
  cost: number;
  mass: number;
  power: number;
  data: number;
  deltaV: number;
}

export type RatioMap = Record<ResourceKey, number>;
export type TierMap = Record<ResourceKey, MarginTier>;

export interface CalculatedBuild {
  totals: Totals;
  limits: Limits;
  margins: RatioMap;
  tiers: TierMap;
  dataThrottle: number;
  contingencyAtLaunch: number;
  instrumentContributions: Record<string, number>;
}

export interface ValidationIssue {
  code: string;
  message: string;
} // codes LV-01..LV-08

export interface ValidationResult {
  valid: boolean;
  errors: ValidationIssue[];
  warnings: ValidationIssue[];
  calculatedBuild: CalculatedBuild;
}

export interface PlayerResponse {
  kind: ResponseKind;
  instrumentId?: string;
}

export interface InstrumentState {
  id: string;
  status: InstrumentStatus;
  offlineStagesRemaining: number;
}

export interface ActiveEffect {
  type: EffectType;
  value: number;
  stagesRemaining: number;
  targetInstrumentId?: string;
}

export interface EventResult {
  eventId: string;
  stage: number;
  roll: number;
  checkedResource: ResourceKey;
  marginRatio: number;
  marginBonus: number;
  tagBonus: number;
  responseBonus: number;
  responses: PlayerResponse[];
  finalDifficulty: number;
  total: number;
  outcome: Outcome;
  effects: Effect[];
  learningMoment: string;
  explanation: string;
}

export interface StageResult {
  stage: number;
  scienceCollected: number;
  explanation: string;
}

export interface MissionState {
  runId: string;
  mode: 'learning';
  seed: number;
  status: 'active' | 'completed' | 'lost';
  stage: number;
  buildSnapshot: Build;
  initialGauges: Totals;
  initialMargins: RatioMap;
  currentDeltaV: number;
  remainingDeltaV: number | null;
  contingencyFund: number;
  scienceCollected: number;
  instruments: InstrumentState[];
  temporaryEffects: ActiveEffect[];
  eventDeck: string[];
  eventsDrawn: string[];
  eventResults: EventResult[];
  stageLog: StageResult[];
  score: ScoreResult | null;
  report: Report | null;
}

export interface EventPreview {
  eventId: string;
  finalDifficulty: number;
  marginBonus: number;
  tagBonus: number;
  legalResponses: ResponseKind[];
  outcomeRanges: {
    success: string;
    partial: string;
    fail: string;
  };
  explanation: string;
}

export interface ScoreResult {
  total: number;
  breakdown: {
    science: number;
    resilience: number;
    budget: number;
    margin: number;
  };
  marginByResource: {
    cost: number;
    mass: number;
    power: number;
  };
  outcome: MissionOutcome;
}

export interface ReportItem {
  title: string;
  detail: string;
  whatIf?: string;
}

export interface Report {
  helped: ReportItem[];
  hurt: ReportItem[];
}
