import parse

# Main Entry Point to the Basic HTML Parser
def main():
    # html = """<body>Test<p>Test2</p></body>"""
    
    html = """<body>
              <p>This is a simple web page created with HTML and displayed using Python<h1>TESTING NESTED</h1></p>
              <p>Here is a link</p>
              </body>"""
    
    parser = parse.Parser(html)
    parser.parse()
    tokens = parser.get_tokens()



if __name__ == "__main__":
    main()