"use strict";
exports.__esModule = true;
var editor_ts_1 = require("./editor.ts");
function getEditorParentNode() {
    var editorContainer = document.querySelector('#editor-container');
    var foo = 3;
    var bar = 'asdf';
    foo = bar;
    if (editorContainer == null) {
        throw 'editor container div does not exist';
    }
    return editorContainer;
}
(0, editor_ts_1.newEditor)(getEditorParentNode());
