import {newEditor} from './editor.js'


function getEditorParentNode() {
  let editorContainer = document.querySelector('#editor-container')

  if (editorContainer == null) {
    throw 'editor container div does not exist'
  }

  return editorContainer
}

newEditor(getEditorParentNode())
