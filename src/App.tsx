export default function App() {
  const cardColors = [
    { name: 'mission', color: 'var(--c-mission)' },
    { name: 'orbit', color: 'var(--c-orbit)' },
    { name: 'rocket', color: 'var(--c-rocket)' },
    { name: 'spacecraft', color: 'var(--c-spacecraft)' },
    { name: 'instrument', color: 'var(--c-instrument)' },
    { name: 'event', color: 'var(--c-event)' },
  ]

  return (
    <main className="min-h-screen p-8 flex flex-col items-center justify-center">
      <div className="p-6 border-2 border-[var(--c-text)] rounded-none bg-[var(--c-panel)] flex flex-col items-center gap-4 text-center">
        <div>
          <h1 className="text-2xl font-bold tracking-wider">
            MISSION GAME <span className="text-xs font-normal opacity-70">(working title)</span>
          </h1>
          <p className="text-sm opacity-80 mt-1">
            NASA Space Apps Challenge 2026 — Step 0 scaffold
          </p>
        </div>

        <p className="text-xs tracking-wide">
          Vite + React + TypeScript + Tailwind v4 + Vitest
        </p>

        <div className="flex gap-2 my-2">
          {cardColors.map((c) => (
            <div
              key={c.name}
              title={c.name}
              className="w-6 h-6 border border-white"
              style={{ backgroundColor: c.color }}
            />
          ))}
        </div>

        <div className="w-[128px] h-[192px] border-2 border-dashed border-[var(--c-text)] flex items-center justify-center text-xs p-2">
          card placeholder 64x96 @2x
        </div>
      </div>
    </main>
  )
}

