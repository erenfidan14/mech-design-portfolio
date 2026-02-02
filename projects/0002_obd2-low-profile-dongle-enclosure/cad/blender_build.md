# Blender build notes — Project 0002 (spec-based)

## Goal
Generate a reference OBD-II mouth envelope + keep-out boxes + an initial two-piece clamshell enclosure concept.

## Recommended setup
- Use Blender 3.6+.
- Units: the script works in mm internally and converts to meters.

## Files
- Spec input:
  ../spec/j1962_typeA_key_dims.yaml
- Script:
  ./blender/obd2_enclosure_generator.py
- Outputs:
  ./exports/*.stl and ./exports/*.glb

## Run steps
1) Open Blender.
2) Save a new file here:
   projects/0002_obd2-low-profile-dongle-enclosure/cad/blender/obd2_enclosure.blend
   (Saving matters so relative paths work.)
3) Go to the Scripting tab.
4) Open the script file:
   projects/0002_obd2-low-profile-dongle-enclosure/cad/blender/obd2_enclosure_generator.py
5) Click Run.

## What gets generated
- Collection "Reference":
  - OBD2_MOUTH_ENVELOPE (approx envelope from SAE J1962 key dims)
  - TECHNICIAN_ACCESS_BOX (80 x 100 mm face, depth default)
- Collection "ConceptA":
  - ENCLOSURE_A_TOP and ENCLOSURE_A_BOTTOM (simple clamshell)
  - screw boss placeholders

## Notes
- This is an envelope-based model (not a full connector model). Without hardware, it’s meant to show design intent, constraints, and documentation quality.
- Blender cannot reliably export STEP; STEP exports belong in the CAD-solid pipeline later (CadQuery/FreeCAD/NX).
