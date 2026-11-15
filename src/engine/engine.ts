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
} from './types.ts';

// Rule source: Section 15.4 Canonical build calculations (totals, limits, margins, tiers, potentialScience, dataThrottle)
export function calculateBuild(_build: Build): CalculatedBuild {
  throw new Error("NotImplemented: calculateBuild");
}

// Rule source: Section 15.6 Launch Check (hard rules LV-01..LV-08 and data warning)
export function validateBuild(_build: Build): ValidationResult {
  throw new Error("NotImplemented: validateBuild");
}

// Rule source: Section 15.7 Authoritative mission state (frozen snapshot at launch)
export function createMissionState(_build: Build, _mode: 'learning', _seed: number): MissionState {
  throw new Error("NotImplemented: createMissionState");
}

// Rule source: Section 15.9 & 15.11 Event preview with difficulty, bonuses, and outcome ranges
export function getEventPreview(_state: MissionState, _event: EventCard): EventPreview {
  throw new Error("NotImplemented: getEventPreview");
}

// Rule source: Section 15.9 Event deck drawing without replacement
export function drawEvent(_state: MissionState): { state: MissionState; event: EventCard } {
  throw new Error("NotImplemented: drawEvent");
}

// Rule source: Section 15.11 Event resolution (d6 + margin bonus + tag bonus + response bonus)
export function resolveEvent(_state: MissionState, _event: EventCard, _responses: PlayerResponse[]): { state: MissionState; result: EventResult } {
  throw new Error("NotImplemented: resolveEvent");
}

// Rule source: Section 15.8 Mission stages progression (Stages 1-6)
export function runStage(_state: MissionState, _input: PlayerResponse[]): { state: MissionState; result: StageResult; nextRequiredAction: string } {
  throw new Error("NotImplemented: runStage");
}

// Rule source: Section 15.14 Science collection (active instruments, data throttle, and multipliers)
export function collectScience(_state: MissionState): { state: MissionState; science: number } {
  throw new Error("NotImplemented: collectScience");
}

// Rule source: Section 15.16 Final scoring (science, resilience, budget efficiency, margin discipline)
export function computeScore(_state: MissionState): ScoreResult {
  throw new Error("NotImplemented: computeScore");
}

// Rule source: Section 15.17 Trade-off Report generation (helped, hurt, what-if)
export function buildReport(_state: MissionState): Report {
  throw new Error("NotImplemented: buildReport");
}
