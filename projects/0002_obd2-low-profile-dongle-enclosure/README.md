# 0002 — Low-profile OBD-II Dongle Enclosure (Mechanical Case Study)

## 1. Problem
Many OBD-II dongles and cables protrude into the driver’s knee/footwell volume.
Goal: design a low-profile enclosure concept that reduces protrusion, adds strain relief, and is suitable for prototyping (3D print) and future injection molding.

Context: OBD-II uses a standardized 16-pin diagnostic connector specified by SAE J1962. (Reference link in Sources.)

## 2. Requirements and constraints
Functional
- Must interface with the standard OBD-II connector geometry (J1962 ecosystem).
- Must support a right-angle cable exit concept to reduce protrusion in the footwell.
- Must include strain relief and cable bend protection.

Mechanical / use environment
- Target connector durability: 200 mating cycles (baseline reference).
- Design for insertion force up to 142 N max and extraction force up to 88 N max (baseline reference).
- Temperature range target: −40 to +85 °C (baseline reference).

Envelope targets (starting point)
- Male 16M connector envelope reference: 32.5 L × 19.0 H × 41.1 W mm.
- Female 16F connector envelope reference: 28.0 L × 23.0 H × 61.0 W mm.
- Target “protrusion from vehicle port” ≤ 60 mm (design goal; to be validated on a real vehicle).

Manufacturing
- Prototype: PETG / PA / ABS 3D print, 0.2 mm layers.
- Future: injection-molded PA66 or PBT-GF class materials.

## 3. Approach
- Define interface envelope + keep-out volume.
- Create 2 housing concepts:
  A) Two-piece clamshell with screws
  B) Snap-fit with serviceable latch
- Select concept based on manufacturability, assembly time, and strain-relief performance.

## 4. CAD and documentation (planned)
- Parametric master model (STL exports for quick tests)
- STEP export for NX/Rhino interoperability
- 2D drawing pack (PDF): overall, sections, assembly, and critical dims
- Render for portfolio (clean white background)

## 5. Verification (planned)
- Clearance checks vs envelope + keep-out
- Hand calc / quick estimate for snap-fit stress or screw boss integrity
- Simple pull test plan: ensure housing survives repeated insert/extract loads without cracking

## 6. Results (targets)
- Reduced protrusion vs typical straight dongle
- Robust strain relief
- Clean documentation pack suitable for a hiring portfolio

## 7. Artifacts (folders)
- /cad        STEP, STL exports
- /drawings   PDF drawings
- /analysis   notes + basic calculations
- /renders    images for README
- /assets     reference images (your own photos)

## 8. Sources
- OBD-II standard connector context + 16-pin J1962 note:
  Advanced Vehicle Technologies, “OBD-II Cable and Connector Information” (1999).
- Baseline insertion/extraction forces and cycles (example connector spec):
  ATTEND, OBDII Type A male connector page (226A-1202).
- Baseline connector envelope dimensions (example catalog listing):
  Delphi/Packard Metri-Pack OBD-II catalog page.
