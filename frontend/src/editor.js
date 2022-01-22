import { EditorState, EditorView, basicSetup } from "@codemirror/basic-setup"


export function newEditor() {
  let n = document.createElement('p')
  n.innerHTML = 'You can type in the editor below'
  let editorContainer = document.querySelector('#editor-container')

  if (editorContainer == null) {
    throw 'editor container div does not exist'
  }

  let editor = new EditorView({
    state: EditorState.create(
      {
        extensions: [basicSetup]
      }
    ),
    parent: editorContainer,
  })
}

