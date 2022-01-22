import { EditorState, EditorView, basicSetup } from "@codemirror/basic-setup"


export function newEditor(parentNode: HTMLDivElement) {
  const editor = new EditorView({
    state: EditorState.create(
      {
        extensions: [basicSetup]
      }
    ),
    parent: parentNode,
  })
}

