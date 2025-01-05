# PythonDOMParser

## Notes
+ For HTML5
    + If the ```<!DOCTYPE html>``` goes to standard mode
    + If not, goes into quirks mode
    + These modes are the same in this

## Limitations

### To Do
+ Make CSSOM more robust
+ Make RenderTree more robust
+ Layout
+ Painting 
+ Compositing
+ Refactor the CSS parsing to use grammar rather than state machine
+ Refactor cssom.py method 'get_document_styles' to account for css precedence
+ Clean up render_tree.py add_styles method, make access to methods easier to avoid chaining calls

### Resources

#### Document Object Model (DOM)

#### Cascaded Style Sheets Object Model (CSSOM)
+ https://blog.frankmtaylor.com/2013/10/15/exploring-the-cssom-making-a-css-object-analyzer/
+ https://yalco.notion.site/DOM-CSSOM-13c42af030bd417c832d343a4172b260
+ https://web.dev/articles/critical-rendering-path/render-tree-construction
+ https://www.trevorlasn.com/blog/css-object-model-cssom
+ https://www.hongkiat.com/blog/css-object-model-cssom/
+ https://developer.mozilla.org/en-US/docs/Glossary/CSSOM