# PythonDOMParser

## Notes
+ For HTML5
    + If the ```<!DOCTYPE html>``` goes to standard mode
    + If not, goes into quirks mode
    + These modes are the same in this
+ Used ChatGPT and other web resources

## Limitations
+ style tag doesn't get rendered
+ Simplified block layout
+ Default height and width is 100%
+ Can only use px or % for measurements
+ If the height is on the root and uses percentages, bases percentages off of the default value
+ Shortcuts and one liners in css is not supported
+ No videos or images currently supported

### To Do
+ Make CSSOM more robust
+ Make RenderTree more robust
+ Layout (browser engine / reflow) of the render tree
+ Painting of the render tree
+ Compositing
+ Refactor the CSS parsing to use grammar rather than state machine
+ Refactor cssom.py method 'get_document_styles' to account for css precedence
+ Clean up render_tree.py add_styles method, make access to methods easier to avoid chaining calls
+ Set up flask local server to serve html and css
+ Set limits on the padding-left, padding-right ....

### Resources

#### Document Object Model (DOM)

#### Cascaded Style Sheets Object Model (CSSOM)
+ https://blog.frankmtaylor.com/2013/10/15/exploring-the-cssom-making-a-css-object-analyzer/
+ https://yalco.notion.site/DOM-CSSOM-13c42af030bd417c832d343a4172b260
+ https://web.dev/articles/critical-rendering-path/render-tree-construction
+ https://www.trevorlasn.com/blog/css-object-model-cssom
+ https://www.hongkiat.com/blog/css-object-model-cssom/
+ https://developer.mozilla.org/en-US/docs/Glossary/CSSOM

#### Web (First one is really good)
+ https://web.dev/articles/howbrowserswork

#### Work Flow
                +---------------------+
                |    Raw HTML (Input)  |   
                +---------------------+
                           |
                           V
            +--------------------------+
            |       DOM Construction    |
            |  (Parse HTML to DOM Tree) |
            +--------------------------+
                           |
                           V
            +--------------------------+
            |       CSSOM Construction  |
            | (Parse CSS to CSSOM Tree) |
            +--------------------------+
                           |
                           V
            +--------------------------+
            |     Render Tree Creation  |
            |  (Combine DOM + CSSOM)    |
            +--------------------------+
                           |
                           V
            +--------------------------+
            |        Layout Phase       |
            |   (Calculate Position &   |
            |   Size of Elements)       |
            +--------------------------+
                           |
                           V
            +--------------------------+
            |       Paint Phase         |
            | (Rasterize into Bitmaps)  |
            +--------------------------+
                           |
                           V
            +--------------------------+
            |   Composition Phase       |
            |  (Combine Layers into Final|
            |      Image)               |
            +--------------------------+
                           |
                           V
            +--------------------------+
            |     GUI (Interaction)     |
            |  (Handle Events, User Input|
            |   & Trigger Repainting)   |
            +--------------------------+
                           |
                           V
            +--------------------------+
            |   Final Image on Screen   |
            +--------------------------+
