from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

# CRUD

tasks = []
task_id_control = 1

@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_control, tasks
    data = request.get_json()

    new_task = Task(
        id=task_id_control, 
        title=data["title"], 
        description=data.get("description", "")
    )

    task_id_control += 1

    tasks.append(new_task)

    print(tasks)
    return jsonify({"menssage": "Nova tarefa criada com sucesso"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]

    output = {
                "tasks": task_list,
                "total_tasks": len(task_list)
            }
    return jsonify(output)

@app.route("/tasks/<int:id>", methods=["GET"])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())

    return jsonify({"menssage": "Não foi possível encontrar a atividade"}), 404

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if task == None:
        return jsonify({"Menssage": "Não foi possível encontrar a atividade"}), 404
    
    data = request.get_json()
    task.title = data["title"]
    task.description = data["description"]
    task.completed = data.get("completed", "")
    print(task)
    return jsonify({"menssage": "Tarefa autlizada com sucesso"})

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break

    if not task:
        return jsonify({"Menssage": "Não foi possível encontrar a atividade"}), 404

    tasks.remove(task)
    return jsonify({"menssage": "Tarefa deletada com sucesso"})

if __name__ == "__main__":
    app.run(debug=True)