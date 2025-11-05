import bpy
import os
import math

# ============================
# CONFIGURACIÓN DE RUTAS
# ============================
input_path = r"C:\Users\DELL\OneDrive\Documentos\2do Semestre\manos_3d\hand_model.glb"
output_path = r"C:\Users\DELL\OneDrive\Documentos\2do Semestre\manos_3d\hand_model_rigged.glb"

if not os.path.exists(input_path):
    raise FileNotFoundError(f"No se encontró {input_path}. Coloca hand_model.glb aquí.")

print(f"✅ Importando modelo desde: {input_path}")

# ============================
# LIMPIAR ESCENA
# ============================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ============================
# IMPORTAR MODELO .GLB
# ============================
bpy.ops.import_scene.gltf(filepath=input_path)
mesh = None
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        mesh = obj
        break

if mesh is None:
    raise RuntimeError("❌ No se encontró un objeto MESH en el modelo importado.")

bpy.context.view_layer.objects.active = mesh

# ============================
# CREAR ARMATURE (ESQUELETO)
# ============================
bpy.ops.object.armature_add(enter_editmode=True)
armature = bpy.context.object
armature.name = "Hand_Armature"
armature.show_in_front = True  # visible en vista 3D

# Eliminar hueso base
bpy.ops.armature.select_all(action='SELECT')
bpy.ops.armature.delete()

# Crear huesos principales
bones = {
    "wrist": (0, 0, 0, 0, 0.2, 0),
    "palm": (0, 0.2, 0, 0, 0.5, 0),
}

# Dedo base positions (espaciados en eje X)
finger_spacing = 0.05
finger_names = ["thumb", "index", "middle", "ring", "pinky"]

for i, name in enumerate(finger_names):
    x = (i - 2) * finger_spacing
    for j in range(4):
        bones[f"{name}_{j+1}"] = (x, 0.5 + j*0.15, 0, x, 0.5 + (j+1)*0.15, 0)

# Crear huesos en Edit Mode
amt = armature.data
for name, (x1, y1, z1, x2, y2, z2) in bones.items():
    bone = amt.edit_bones.new(name)
    bone.head = (x1, y1, z1)
    bone.tail = (x2, y2, z2)

# Vincular jerarquía
for name in finger_names:
    amt.edit_bones[f"{name}_1"].parent = amt.edit_bones["palm"]
    amt.edit_bones[f"{name}_2"].parent = amt.edit_bones[f"{name}_1"]
    amt.edit_bones[f"{name}_3"].parent = amt.edit_bones[f"{name}_2"]
    amt.edit_bones[f"{name}_4"].parent = amt.edit_bones[f"{name}_3"]

amt.edit_bones["palm"].parent = amt.edit_bones["wrist"]

bpy.ops.object.mode_set(mode='OBJECT')

# ============================
# EMPAREJAR CON PESOS AUTOMÁTICOS
# ============================
mesh.select_set(True)
armature.select_set(True)
bpy.context.view_layer.objects.active = armature
bpy.ops.object.parent_set(type='ARMATURE_AUTO')

print("✅ Armature creada y vinculada con pesos automáticos")

# ============================
# EXPORTAR MODELO FINAL
# ============================
bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    use_selection=False,
    export_apply=True,
    export_skins=True,
)

print(f"✅ Exportado correctamente: {output_path}")
print("🦴 Huesos creados:")
for bone in bones.keys():
    print(f"  - {bone}")

print("🎉 SCRIPT FINALIZADO CON ÉXITO 🎉")
