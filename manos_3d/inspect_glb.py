from pathlib import Path
from pygltflib import GLTF2

path = Path("hand_model_rigged.glb")
if not path.exists():
    print("❌ No se encontró el archivo hand_model_rigged.glb")
else:
    glb = GLTF2().load_binary(path)
    print("✅ Archivo GLB cargado correctamente")
    print(f"👉 Contiene {len(glb.nodes)} nodos totales")

    # Buscar nodos tipo Joint o Armature
    has_skin = any(skin for skin in glb.skins)
    if has_skin:
        print("🦴 Se detectaron estructuras de huesos (Armature).")
    else:
        print("⚠️ No se detectaron huesos. Posiblemente la mano no está riggeada correctamente.")
