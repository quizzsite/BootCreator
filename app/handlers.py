from .ext import appServer, projMan, emit, jsonify

# Good: {"status": 1, "data": "<html></html>"}

# Error: {"status": 0, "errors": [{"for": "command", "error": "One id to many elements"}]}

def updateProjects(socketio):
    @appServer.on('update_project')
    def handleUpdateProject(data):
        proj, file, s = data['proj'], data['file'], data['s']
        errors = []
        for do in s:
            try:
                result = projMan.update(proj, file, do)
            except IndexError as e:
                errors.append({"for": do, "error": e})
            except ValueError as e:
                errors.append({"for": do, "error": e})
        if errors:
            emit('update_response', jsonify({'status': 0, "errors": errors}))
        else:
            emit('update_response', jsonify({'status': 1, "data": result}))
