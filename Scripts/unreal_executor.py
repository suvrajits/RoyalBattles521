import sys
sys.path.append("E:/UE_5.5/Engine/Binaries/Win64")

import unreal
print(unreal.SystemLibrary.get_engine_version())


from flask import Flask, request, jsonify
import unreal

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_task():
    data = request.json
    task = data.get("task", "")
    
    if task == "create_blueprint":
        blueprint_name = data["blueprint_name"]
        blueprint_type = data["blueprint_type"]

        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        package_path = f"/Game/{blueprint_name}"

        if blueprint_type.lower() == "actor":
            blueprint_class = unreal.Blueprint
        else:
            return jsonify({"status": "error", "message": f"Unsupported blueprint type {blueprint_type}"})

        # Create the Blueprint
        blueprint = asset_tools.create_asset(
            blueprint_name, package_path, blueprint_class, unreal.BlueprintFactory()
        )

        # Save and open the Blueprint
        unreal.EditorAssetLibrary.save_asset(package_path)
        unreal.AssetToolsHelpers.get_asset_tools().open_editor_for_assets([blueprint])

        return jsonify({"status": "success", "message": f"Blueprint {blueprint_name} created and opened."})

    return jsonify({"status": "error", "message": "Invalid task"})

if __name__ == '__main__':
    app.run(port=5000)
