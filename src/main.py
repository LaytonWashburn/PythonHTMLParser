import parser.parse as parse

# Main Entry Point to the Basic HTML Parser
def main():
    # # Test 1
    # html = """<body>Test<p>Test2</p></body>"""
    
    # # Test 2
    # html = """<body>
    #           <p>This is a simple web page created with HTML and displayed using Python<h1>TESTING NESTED</h1></p>
    #           <p>Here is a link</p>
    #           </body>"""

    # Test 3
    html = ""
    with open('src/index.html', 'r', encoding='utf-8') as file:
        html = file.read()
  
    parser = parse.Parser(html)
    parser.parse()
    tokens = parser.get_tokens()

if __name__ == "__main__":
    main()