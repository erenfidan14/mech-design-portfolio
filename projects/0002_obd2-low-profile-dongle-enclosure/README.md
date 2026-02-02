# 0002 — Low-profile OBD-II Dongle Enclosure (Spec-based)

## 1. Problem
Many OBD-II dongles protrude into the driver footwell. This project designs a low-profile enclosure concept around the standardized SAE J1962 Type A interface, targeting reduced protrusion and robust strain relief.

## 2. Requirements and constraints (from sources)
Interface
- Must mate with SAE J1962 Type A geometry (external test equipment connector vs vehicle connector).

Vehicle clearance
- Must respect connector access / clearance guidance (technician access area + DLC clearance area).

Forces / robustness (baseline)
- Connection/disconnection forces (max) and mis-mating force requirement inform housing strength and latch robustness.

Environment (baseline)
- Temperature class reference: -40 °C to +85 °C.

## 3. Design targets (engineering choices)
- “Protrusion from vehicle port” target: <= 60 mm (design goal, not a standard requirement).
- Right-angle cable exit.
- Strain relief: cable bend support, no sharp edges, relief length >= 25 mm.

## 4. Deliverables (what will exist in this repo)
- Spec file with key dimensions taken from SAE J1962 figures.
- CAD reference envelope (connector mouth + keep-out volumes).
- Enclosure Concept A: two-piece clamshell with screws.
- Enclosure Concept B: snap-fit (serviceable latch).
- Drawing pack PDF (overall + section + critical dims).
- Renders for portfolio page.

## 5. Sources
- SAE J1962:2016 (figures for Type A connector geometry + access/clearance guidance).
- Example connector spec listing forces/durability (secondary baseline).
