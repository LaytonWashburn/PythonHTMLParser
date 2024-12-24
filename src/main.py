import parse

# Main Entry Point to the Basic HTML Parser
def main():
    html = """<body>Test</body>"""
    
    # """<body>
    #         <p>This is a simple web page created with HTML and displayed using Python</p>
    #         <p>Here is a link</p>
    #     </body>"""
    
    parser = parse.Parser(html)
    parser.parse()
    tokens = parser.get_tokens()
    print(tokens)
    token = tokens[0]
    print(token.get_name())
    print(token.get_attribute())
    


if __name__ == "__main__":
    main()