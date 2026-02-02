import bpy
import bmesh
import os
import math

# -----------------------------
# Helpers
# -----------------------------
def mm(x: float) -> float:
    """Convert millimeters to meters (Blender base unit)."""
    return x / 1000.0

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def clear_scene() -> None:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def get_or_create_collection(name: str) -> bpy.types.Collection:
    if name in bpy.data.collections:
        return bpy.data.collections[name]
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col

def link_to_collection(obj: bpy.types.Object, col: bpy.types.Collection) -> None:
    # Remove from other collections
    for c in obj.users_collection:
        c.objects.unlink(obj)
    col.objects.link(obj)

def simple_yaml_flat_kv(path: str) -> dict:
    """
    Minimal YAML parser for flat key: value pairs (no nesting).
    Works for the spec file used in this project.
    """
    data = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            # Try numeric
            try:
                if "." in v:
                    data[k] = float(v)
                else:
                    data[k] = int(v)
            except Exception:
                data[k] = v
    return data

def make_mesh_object(name: str, verts, faces) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    return obj

def apply_all_modifiers(obj: bpy.types.Object) -> None:
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    for mod in list(obj.modifiers):
        try:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        except Exception:
            # If apply fails (rare), keep modifier to avoid crash
            pass
    obj.select_set(False)

# -----------------------------
# Paths
# -----------------------------
# Save your .blend in: .../cad/blender/ so "//" resolves correctly
BASE = bpy.path.abspath("//")
SPEC_PATH = os.path.normpath(os.path.join(BASE, "../../spec/j1962_typeA_key_dims.yaml"))
EXPORT_DIR = os.path.normpath(os.path.join(BASE, "../exports"))

# -----------------------------
# Main build
# -----------------------------
def build():
    clear_scene()
    ensure_dir(EXPORT_DIR)

    spec = {}
    if os.path.exists(SPEC_PATH):
        spec = simple_yaml_flat_kv(SPEC_PATH)
    else:
        print("Spec file not found:", SPEC_PATH)
        print("Proceeding with defaults...")

    # Required keys from your spec file (defaults if missing)
    mouth_w_outer = float(spec.get("mouth_width_outer_mm", 37.55))
    mouth_w_inner = float(spec.get("mouth_width_inner_mm", 29.5))
    side_angle_deg = float(spec.get("side_angle_deg", 15))

    tech_w = float(spec.get("technician_access_area_min_width_mm", 80))
    tech_h = float(spec.get("technician_access_area_min_height_mm", 100))

    # Project design parameters (envelope-based; editable later)
    env_height = float(spec.get("envelope_height_mm", 20.0))     # engineering choice
    env_depth  = float(spec.get("envelope_depth_mm", 45.0))      # engineering choice
    clearance  = float(spec.get("clearance_mm", 1.0))            # engineering choice
    wall       = float(spec.get("wall_thickness_mm", 2.5))       # engineering choice
    split_gap  = float(spec.get("split_gap_mm", 0.2))            # engineering choice

    # Collections
    col_ref = get_or_create_collection("Reference")
    col_a   = get_or_create_collection("ConceptA")

    # -----------------------------
    # 1) Reference: OBD-II mouth envelope (approx trapezoid prism)
    # -----------------------------
    # Build a trapezoid cross-section in X-Z, extrude along Y (depth)
    # Origin: vehicle port plane at Y=0, center at X=0, Z=0
    top_w = mouth_w_outer
    bot_w = mouth_w_inner

    # Side angle can inform trapezoid slope; we keep it simple:
    # trapezoid top at Z=+H/2, bottom at Z=-H/2
    H = env_height
    D = env_depth

    x1 = -top_w/2
    x2 =  top_w/2
    x3 =  bot_w/2
    x4 = -bot_w/2
    zt =  H/2
    zb = -H/2

    # 8 verts of a prism (front face at y=0, back at y=D)
    V = [
        (mm(x1), mm(0), mm(zt)),  # 0
        (mm(x2), mm(0), mm(zt)),  # 1
        (mm(x3), mm(0), mm(zb)),  # 2
        (mm(x4), mm(0), mm(zb)),  # 3
        (mm(x1), mm(D), mm(zt)),  # 4
        (mm(x2), mm(D), mm(zt)),  # 5
        (mm(x3), mm(D), mm(zb)),  # 6
        (mm(x4), mm(D), mm(zb)),  # 7
    ]
    F = [
        (0, 1, 2, 3),  # front
        (4, 5, 6, 7),  # back
        (0, 4, 5, 1),  # top
        (1, 5, 6, 2),  # right
        (2, 6, 7, 3),  # bottom
        (3, 7, 4, 0),  # left
    ]
    env_obj = make_mesh_object("OBD2_MOUTH_ENVELOPE", V, F)
    link_to_collection(env_obj, col_ref)

    # -----------------------------
    # 2) Reference: technician access keep-out box
    # -----------------------------
    # Box centered on the port, extending forward (positive Y)
    tech_depth = float(spec.get("technician_access_depth_mm", 120.0))  # engineering choice
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, mm(tech_depth/2), 0))
    tech = bpy.context.active_object
    tech.name = "TECHNICIAN_ACCESS_BOX"
    tech.scale = (mm(tech_w/2), mm(tech_depth/2), mm(tech_h/2))
    link_to_collection(tech, col_ref)
    tech.display_type = 'WIRE'

    # -----------------------------
    # 3) Concept A: clamshell enclosure around envelope
    # -----------------------------
    # Outer housing as a box around the envelope with wall thickness
    outer_w = top_w + 2*(clearance + wall)
    outer_h = H     + 2*(clearance + wall)
    outer_d = D     + (clearance + wall) + 10.0  # extra for cable/PCB space

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, mm(outer_d/2), 0))
    outer = bpy.context.active_object
    outer.name = "ENCLOSURE_A_OUTER"
    outer.scale = (mm(outer_w/2), mm(outer_d/2), mm(outer_h/2))
    link_to_collection(outer, col_a)

    # Create cavity: slightly inflated envelope
    # Duplicate envelope and scale in X/Z and extend depth slightly
    cavity = env_obj.copy()
    cavity.data = env_obj.data.copy()
    bpy.context.scene.collection.objects.link(cavity)
    cavity.name = "CAVITY_TOOL"
    cavity.scale = (1.0 + clearance/max(1e-6, top_w), 1.0 + clearance/max(1e-6, D), 1.0 + clearance/max(1e-6, H))
    cavity.location = (0, 0, 0)
    link_to_collection(cavity, col_a)

    # Boolean difference outer - cavity
    bool_mod = outer.modifiers.new(name="CAVITY_BOOL", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = cavity
    apply_all_modifiers(outer)

    # Hide cavity tool
    cavity.hide_set(True)
    cavity.hide_render = True

    # Split into TOP/BOTTOM along Z=0 plane (simple: duplicate + bisect)
    def bisect_object(obj, name_a, name_b, plane_co=(0,0,0), plane_no=(0,0,1), gap_mm=0.2):
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        # Duplicate for second half
        bpy.ops.object.duplicate()
        obj_b = bpy.context.active_object
        obj_b.name = name_b

        obj_a = obj
        obj_a.name = name_a

        # Bisect A keep positive side (top)
        bpy.context.view_layer.objects.active = obj_a
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj_a.data)
        bmesh.ops.bisect_plane(
            bm,
            geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
            plane_co=plane_co,
            plane_no=plane_no,
            clear_outer=True,
            clear_inner=False
        )
        bmesh.update_edit_mesh(obj_a.data)
        bpy.ops.object.mode_set(mode='OBJECT')

        # Bisect B keep negative side (bottom)
        bpy.context.view_layer.objects.active = obj_b
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj_b.data)
        bmesh.ops.bisect_plane(
            bm,
            geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
            plane_co=plane_co,
            plane_no=plane_no,
            clear_outer=False,
            clear_inner=True
        )
        bmesh.update_edit_mesh(obj_b.data)
        bpy.ops.object.mode_set(mode='OBJECT')

        # Apply small split gap
        obj_a.location.z += mm(gap_mm/2)
        obj_b.location.z -= mm(gap_mm/2)

        obj_a.select_set(False)
        obj_b.select_set(False)

        return obj_a, obj_b

    top, bottom = bisect_object(
        outer,
        "ENCLOSURE_A_TOP",
        "ENCLOSURE_A_BOTTOM",
        plane_co=(0, 0, 0),
        plane_no=(0, 0, 1),
        gap_mm=split_gap
    )
    link_to_collection(top, col_a)
    link_to_collection(bottom, col_a)

    # Remove the original outer (now renamed to TOP) already handled.

    # -----------------------------
    # 4) Exports (STL + GLB)
    # -----------------------------
    def export_selected(filepath_stl: str, filepath_glb: str):
        bpy.ops.object.select_all(action='DESELECT')
        for o in bpy.context.scene.objects:
            if o.name in {"OBD2_MOUTH_ENVELOPE", "ENCLOSURE_A_TOP", "ENCLOSURE_A_BOTTOM"}:
                o.select_set(True)
        bpy.ops.export_mesh.stl(filepath=filepath_stl, use_selection=True)
        bpy.ops.export_scene.gltf(filepath=filepath_glb, export_format='GLB', use_selection=True)

    export_selected(
        os.path.join(EXPORT_DIR, "project0002_obd2_envelope_and_enclosureA.stl"),
        os.path.join(EXPORT_DIR, "project0002_obd2_envelope_and_enclosureA.glb")
    )

    print("Done. Exports written to:", EXPORT_DIR)
    print("Spec path used:", SPEC_PATH)

build()
