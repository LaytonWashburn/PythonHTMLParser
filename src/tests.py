
class Test:

    def __init__(self):
        pass
    
    def get_html(self):
        # Test 0
        # html = """<body></body>"""
        # # html = """<body>Test</body>"""

        # # Test 1
        # html = """<body>Test<p>Test2</p></body>"""

        # # Test 1.9
        # html = """<body id=test>Test</body>"""

        # # Test 2
        # html = """<body>
        #           <p>This is a simple web page created with HTML and displayed using Python<h1>TESTING NESTED</h1></p>
        #           <p>Here is a link</p>
        #           </body>"""

        # Test 3
        html = ""
        with open('src/html-tests/index.html', 'r', encoding='utf-8') as file:
            html = file.read()
        css = ""
        with open('src/css-tests/index.css', 'r', encoding='utf-8') as file:
            css = file.read()

        # # Test 4
        # html = """<body>
        #             <h1>Help</h1>
        #             Test
        #             <p>Test2</p>
        #         </body>"""

        # # Test 5 --> This doesn't work right now
        # html = "Hello"

        # # Test 6
        # html = """<"""

        # # Test 7
        # html =""">"""

        # # Test 8
        # html =""""""

        # # Test 9
        # html ="""<f><f<<<<"""

        # # Test 10
        # html = """<body test=test>Hello World</body>"""

        # # Test 11
        # html = """\""""

        # # Test 12
        # html = """ " """
        return html, css
