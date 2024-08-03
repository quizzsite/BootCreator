import os, uuid
from bs4 import BeautifulSoup, Comment
from bs4.element import Tag as BS4Tag
from flask import url_for

def htmlToDict(htmlContent):
    soup = BeautifulSoup(htmlContent, 'html.parser')

    def buildTree(node):
        if isinstance(node, Comment):
            return {'tag': '#comment', '#text': node.string}
        elif isinstance(node, BS4Tag):
            tagName = node.name
            attrs = {key: value for key, value in node.attrs.items()}
            children = [buildTree(child) for child in node.children if not isinstance(child, str) or child.strip()]
            text = node.string.strip() if not children and node.string else None
            result = {'tag': tagName, 'attrs': attrs, 'children': children}
            if text:
                result['#text'] = text
            return result
        elif isinstance(node, str):
            return {'tag': '#text', '#text': node.strip() if node.strip() else None}
        return None

    root = soup.find("html")
    return buildTree(root) if root else {'tag': 'html', 'children': [buildTree(child) for child in soup.children]}

def dictToHtml(jsonTree):
    def buildHtml(node):
        if node['tag'] == '#text':
            return node.get('#text') or ''
        if node['tag'] == '#comment':
            return f"<!--{node['#text']}-->"
        
        selfClosingTags = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']
        if node['tag'] in selfClosingTags:
            attrs = ' '.join(f'{attr}="{value}"' for attr, value in node.get('attrs', {}).items())
            return f"<{node['tag']}{' ' + attrs if attrs else ''}>"
        
        attrs = ' '.join(f'{attr}="{value}"' for attr, value in node.get('attrs', {}).items())
        openingTag = f"<{node['tag']}{' ' + attrs if attrs else ''}>"
        childrenHtml = ''.join(buildHtml(child) for child in node.get('children', []))
        text = node.get('#text', '') or ''
        closingTag = f"</{node['tag']}>"
        return openingTag + text + childrenHtml + closingTag

    return buildHtml(jsonTree)


class ProjectManager:
    def __init__(self, dir="app/static/cache"):
        self.projectDir = dir
        self.nameGen = uuid.uuid4
        self.id = 1
    
    def create(self):
        token = self.nameGen()
        os.makedirs(str(os.path.join(self.projectDir, f"project-{str(token)}")))
        with open(f'{os.path.join(self.projectDir, f"project-{str(token)}")}/index.html', "a+") as f:
            f.close()
        return token
    
    def isProj(self, proj):
        return os.path.isdir(str(os.path.join(self.projectDir, f"project-{str(proj)}")))
    
    def getFile(self, proj, file):
        return open(f'{str(os.path.join(self.projectDir, f"project-{str(proj)}"))}/{file}', "a+")

    def update(self, proj, file, s):
        if self.isProj(proj):
            filePath = f'{str(os.path.join(self.projectDir, f"project-{str(proj)}"))}/{file}'
            with open(filePath, "r+") as f:
                fileContent = f.read()
                self.id = self.findId(fileContent) + 1
                code = htmlToDict(fileContent)
                body = next((node for node in code['children'] if node['tag'] == 'body'), None)
                if not body:
                    raise ValueError('No <body> tag found in HTML')

                task = s.split()
                if len(task) > 0:
                    if task[0] == "Update":
                        if task[1] == "new":
                            if task[2] == "class":
                                if task[3] and task[4] and task[5] and task[6]:  # class widgetId
                                    className = task[3]
                                    widgetId = task[4]
                                    parentId = task[5]
                                    index = int(task[6])
                                    self.addClassToWidget(body, className, widgetId, parentId, index)
                            elif task[2] == "widget":
                                if task[3] and task[4] and task[5]:  # widget parentId index
                                    widgetName = task[3]
                                    parentId = task[4]
                                    index = int(task[5])
                                    self.addWidget(body, widgetName, parentId, index)
                            elif task[2] == "property":
                                if task[3] and task[4] and task[5]:  # property value widgetId
                                    propertyName = task[3]
                                    value = task[4]
                                    widgetId = task[5]
                                    self.addPropertyToWidget(body, propertyName, value, widgetId)
                        elif task[1] == "delete":
                            if task[2] == "class":
                                if task[3] and task[4]:  # class widgetId
                                    className = task[3]
                                    widgetId = task[4]
                                    self.deleteClassFromWidget(body, className, widgetId)
                            elif task[2] == "widget":  # widgetId
                                if task[3]:
                                    widgetId = task[3]
                                    self.deleteWidget(body, widgetId)
                            elif task[2] == "property":  # property widgetId
                                if task[3] and task[4]:
                                    propertyName = task[3]
                                    widgetId = task[4]
                                    self.deletePropertyFromWidget(body, propertyName, widgetId)
                    elif task[0] == "Save":
                        naFile = self.getFile(proj, task[1])
                        if naFile.name == file:
                            pass
                newHtml = dictToHtml(code)
                f.seek(0)
                f.write(newHtml)
                f.truncate()
                return url_for('static', filename=f'cache/project-{proj}/{file}')

    def findId(self, htmlContent):
        soup = BeautifulSoup(htmlContent, 'html.parser')
        maxNumber = float('-inf')

        for element in soup.find_all(id=lambda x: x and x.startswith('widget-')):
            try:
                widgetId = element['id']
                number = int(widgetId.split('-')[1])
                if number > maxNumber:
                    maxNumber = number
            except (IndexError, ValueError):
                continue

        return maxNumber if maxNumber != float('-inf') else 0

    def addWidget(self, body, widgetName, parentId, index):
        widgetId = f'widget-{self.id}'
        widget = {'tag': widgetName, 'attrs': {'id': widgetId}, 'children': []}
        parent = self.findWidget(body, parentId)
        if parent:
            parent["children"].insert(index, widget)
        else:
            raise ValueError(f'Parent with id {parentId} not found')

    def deleteWidget(self, body, widgetId):
        parent, index = self.findParentOfWidget(body, widgetId)
        if parent and index is not None:
            del parent["children"][index]
        else:
            raise ValueError(f'Widget with id {widgetId} not found')

    def addPropertyToWidget(self, body, propertyName, value, widgetId):
        widget = self.findWidget(body, widgetId)
        if widget:
            widget["attrs"][propertyName] = value
        else:
            raise ValueError(f'Widget with id {widgetId} not found')

    def deletePropertyFromWidget(self, body, propertyName, widgetId):
        widget = self.findWidget(body, widgetId)
        if widget and propertyName in widget.attrs:
            del widget["attrs"][propertyName]
        else:
            raise ValueError(f'Widget with id {widgetId} not found or property {propertyName} not found')

    def addClassToWidget(self, body, className, widgetId, parentId, index):
        widget = self.findWidget(body, widgetId)
        if widget:
            if 'class' not in widget['attrs']:
                widget['attrs']['class'] = className
            else:
                widget['attrs']['class'] += f' {className}'
        else:
            raise ValueError(f'Widget with id {widgetId} not found')

    def deleteClassFromWidget(self, body, className, widgetId):
        widget = self.findWidget(body, widgetId)
        if widget and 'class' in widget["attrs"]:
            classes = widget["attrs"]['class'].split()
            if className in classes:
                classes.remove(className)
                widget["attrs"]['class'] = ' '.join(classes)
        else:
            raise ValueError(f'Widget with id {widgetId} not found or class {className} not found')

    def findWidget(self, node, widgetId):
        if widgetId == "body":
            return next((body for body in node['children'] if node['tag'] == 'body'), None)
        if node["attrs"].get('id') == widgetId:
            return node
        for child in node["children"]:
            result = self.findWidget(child, widgetId)
            if result:
                return result
        return None

    def findParentOfWidget(self, node, widgetId):
        for index, child in enumerate(node["children"]):
            if child["attrs"].get('id') == widgetId:
                return node, index
            result = self.findParentOfWidget(child, widgetId)
            if result:
                return result
        return None, None