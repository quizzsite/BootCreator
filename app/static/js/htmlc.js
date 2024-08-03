function htmlToDict(htmlContent) {
    // Парсинг HTML
    let parser = new DOMParser();
    let doc = parser.parseFromString(htmlContent, 'text/html');

    function buildTree(node) {
        if (node.nodeType === Node.COMMENT_NODE) {
            return { tag: '#comment', '#text': node.nodeValue };
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            let tagName = node.tagName.toLowerCase();
            let attrs = {};
            for (let attr of node.attributes) {
                attrs[attr.name] = attr.value;
            }
            let children = [];
            for (let child of node.childNodes) {
                let childNode = buildTree(child);
                if (childNode) {
                    children.push(childNode);
                }
            }
            let result = { tag: tagName, attrs: attrs, children: children };
            if (node.childNodes.length === 0 && node.textContent.trim()) {
                result['#text'] = node.textContent.trim();
            }
            return result;
        } else if (node.nodeType === Node.TEXT_NODE) {
            if (node.nodeValue.trim()) {
                return { tag: '#text', '#text': node.nodeValue.trim() };
            }
        }
        return null;
    }

    let root = doc.documentElement;
    return buildTree(root);
}

function dictToHtml(jsonTree) {
    function buildHtml(node) {
        if (node.tag === '#text') {
            return node['#text'] || '';
        }
        if (node.tag === '#comment') {
            return `<!--${node['#text']}-->`;
        }

        let selfClosingTags = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']);
        if (selfClosingTags.has(node.tag)) {
            let attrs = Object.entries(node.attrs || {}).map(([attr, value]) => `${attr}="${value}"`).join(' ');
            return `<${node.tag}${attrs ? ' ' + attrs : ''}>`;
        }

        let attrs = Object.entries(node.attrs || {}).map(([attr, value]) => `${attr}="${value}"`).join(' ');
        let openingTag = `<${node.tag}${attrs ? ' ' + attrs : ''}>`;
        let childrenHtml = (node.children || []).map(buildHtml).join('');
        let text = node['#text'] || '';
        let closingTag = `</${node.tag}>`;

        return openingTag + text + childrenHtml + closingTag;
    }

    return buildHtml(jsonTree);
}
