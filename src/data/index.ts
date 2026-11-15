import type {
  BusCard,
  Card,
  CommsCard,
  EventCard,
  InstrumentCard,
  MissionCard,
  OrbitCard,
  PowerCard,
  PropulsionCard,
  RocketCard,
  SupportCard,
} from '../engine/types.ts';

import busesData from './buses.json';
import commsData from './comms.json';
import eventsData from './events.json';
import instrumentsData from './instruments.json';
import missionsData from './missions.json';
import orbitsData from './orbits.json';
import powerData from './power.json';
import propulsionData from './propulsion.json';
import rocketsData from './rockets.json';
import supportsData from './supports.json';

export const missions: MissionCard[] = missionsData as MissionCard[];
export const orbits: OrbitCard[] = orbitsData as OrbitCard[];
export const rockets: RocketCard[] = rocketsData as RocketCard[];
export const buses: BusCard[] = busesData as BusCard[];
export const power: PowerCard[] = powerData as PowerCard[];
export const comms: CommsCard[] = commsData as CommsCard[];
export const propulsion: PropulsionCard[] = propulsionData as PropulsionCard[];
export const supports: SupportCard[] = supportsData as SupportCard[];
export const instruments: InstrumentCard[] = instrumentsData as InstrumentCard[];
export const events: EventCard[] = eventsData as EventCard[];

export const allCards: Card[] = [
  ...missions,
  ...orbits,
  ...rockets,
  ...buses,
  ...power,
  ...comms,
  ...propulsion,
  ...supports,
  ...instruments,
];

export const cardById: Record<string, Card> = Object.fromEntries(
  allCards.map((card) => [card.id, card])
);

export const eventById: Record<string, EventCard> = Object.fromEntries(
  events.map((event) => [event.id, event])
);
