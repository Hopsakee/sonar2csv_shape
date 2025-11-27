---
trigger: manual
---

<project title="FastHTML" summary='FastHTML is a python library which brings together Starlette, Uvicorn, HTMX, and fastcore&#39;s `FT` "FastTags" into a library for creating server-rendered hypermedia applications. The `FastHTML` class itself inherits from `Starlette`, and adds decorator-based routing with many additions, Beforeware, automatic `FT` to HTML rendering, and much more.'>Things to remember when writing FastHTML apps:

- Although parts of its API are inspired by FastAPI, it is *not* compatible with FastAPI syntax and is not targeted at creating API services
- FastHTML includes support for Pico CSS and the fastlite sqlite library, although using both are optional; sqlalchemy can be used directly or via the fastsql library, and any CSS framework can be used. Support for the Surreal and css-scope-inline libraries are also included, but both are optional
- FastHTML is compatible with JS-native web components and any vanilla JS library, but not with React, Vue, or Svelte
- Use `serve()` for running uvicorn (`if __name__ == "__main__"` is not needed since it's automatic)
- When a title is needed with a response, use `Titled`; note that that already wraps children in `Container`, and already includes both the meta title as well as the H1 element.<docs><doc title="FastHTML concise guide" desc="A brief overview of idiomatic FastHTML apps"># Concise reference



## About FastHTML

``` python
from fasthtml.common import *
```

FastHTML is a python library which brings together Starlette, Uvicorn,
HTMX, and fastcore’s `FT` “FastTags” into a library for creating
server-rendered hypermedia applications. The
[`FastHTML`](https://www.fastht.ml/docs/api/core.html#fasthtml) class
itself inherits from `Starlette`, and adds decorator-based routing with
many additions, Beforeware, automatic `FT` to HTML rendering, and much
more.

Things to remember when writing FastHTML apps:

- *Not* compatible with FastAPI syntax; FastHTML is for HTML-first apps,
  not API services (although it can implement APIs too)
- FastHTML includes support for Pico CSS and the fastlite sqlite
  library, although using both are optional; sqlalchemy can be used
  directly or via the fastsql library, and any CSS framework can be
  used. MonsterUI is a richer FastHTML-first component framework with
  similar capabilities to shadcn
- FastHTML is compatible with JS-native web components and any vanilla
  JS library, but not with React, Vue, or Svelte
- Use [`serve()`](https://www.fastht.ml/docs/api/core.html#serve) for
  running uvicorn (`if __name__ == "__main__"` is not needed since it’s
  automatic)
- When a title is needed with a response, use
  [`Titled`](https://www.fastht.ml/docs/api/xtend.html#titled); note
  that that already wraps children in
  [`Container`](https://www.fastht.ml/docs/api/pico.html#container), and
  already includes both the meta title as well as the H1 element.

## Minimal App

The code examples here use fast.ai style: prefer ternary op, 1-line
docstring, minimize vertical space, etc. (Normally fast.ai style uses
few if any comments, but they’re added here as documentation.)

A minimal FastHTML app looks something like this:

``` python
# Meta-package with all key symbols from FastHTML and Starlette. Import it like this at the start of every FastHTML app.
from fasthtml.common import *
# The FastHTML app object and shortcut to `app.route`
app,rt = fast_app()

# Enums constrain the values accepted for a route parameter
name = str_enum('names', 'Alice', 'Bev', 'Charlie')

# Passing a path to `rt` is optional. If not passed (recommended), the function name is the route ('/foo')
# Both GET and POST HTTP methods are handled by default
# Type-annotated params are passed as query params (recommended) unless a path param is defined (which it isn't here)
@rt
def foo(nm: name):
    # `Title` and `P` here are FastTags: direct m-expression mappings of HTML tags to Python functions with positional and named parameters. All standard HTML tags are included in the common wildcard import.
    # When a tuple is returned, this returns concatenated HTML partials. HTMX by default will use a title HTML partial to set the current page name. HEAD tags (e.g. Meta, Link, etc) in the returned tuple are automatically placed in HEAD; everything else is placed in BODY.
    # FastHTML will automatically return a complete HTML document with appropriate headers if a normal HTTP request is received. For an HTMX request, however, just the partials are returned.
    return Title("FastHTML"), H1("My web app"), P(f"Hello, {name}!")
# By default `serve` runs uvicorn on port 5001. Never write `if __name__ == "__main__"` since `serve` checks it internally.
serve()
```

To run this web app:

``` bash
python main.py  # access via localhost:5001
```

## FastTags (aka FT Components or FTs)

FTs are m-expressions plus simple sugar. Positional params map to
children. Named parameters map to attributes. Aliases must be used for
Python reserved words.

``` python
tags = Title("FastHTML"), H1("My web app"), P(f"Let's do this!", cls="myclass")
tags
```

    (title(('FastHTML',),{}),
     h1(('My web app',),{}),
     p(("Let's do this!",),{'class': 'myclass'}))

This example shows key aspects of how FTs handle attributes:

``` python
Label(
    "Choose an option", 
    Select(
        Option("one", value="1", selected=True),  # True renders just the attribute name
        Option("two", value=2, selected=False),   # Non-string values are converted to strings. False omits the attribute entirely
        cls="selector", id="counter",             # 'cls' becomes 'class'
        **{'@click':"alert('Clicked');"},         # Dict unpacking for attributes with special chars
    ),
    _for="counter",                               # '_for' becomes 'for' (can also use 'fr')
)
```

Classes with `__ft__` defined are rendered using that method.

``` python
class FtTest:
    def __ft__(self): return P('test')
    
to_xml(FtTest())
```

    '<p>test</p>\n'

You can create new FTs by importing the new component from
`fasthtml.components`. If the FT doesn’t exist within that module,
FastHTML will create it.

``` python
from fasthtml.components import Some_never_before_used_tag

Some_never_before_used_tag()
```

``` html
<some-never-before-used-tag></some-never-before-used-tag>
```

FTs can be combined by defining them as a function.

``` python
def Hero(title, statement): return Div(H1(title),P(statement), cls="hero")
to_xml(Hero("Hello World", "This is a hero statement"))
```

    '<div class="hero">\n  <h1>Hello World</h1>\n  <p>This is a hero statement</p>\n</div>\n'

When handling a response, FastHTML will automatically render FTs using
the `to_xml` function.

``` python
to_xml(tags)
```

    '<title>FastHTML</title>\n<h1>My web app</h1>\n<p class="myclass">Let&#x27;s do this!</p>\n'

## JS

The [`Script`](https://www.fastht.ml/docs/api/xtend.html#script)
function allows you to include JavaScript. You can use Python to
generate parts of your JS or JSON like this:

``` python
# In future snippets this import will not be shown, but is required
from fasthtml.common import * 
app,rt = fast_app(hdrs=[Script(src="https://cdn.plot.ly/plotly-2.32.0.min.js")])
# `index` is a special function name which maps to the `/` route. 
@rt
def index():
    data = {'somedata':'fill me in…'}
    # `Titled` returns a title tag and an h1 tag with the 1st param, with remaining params as children in a `Main` parent.
    return Titled("Chart Demo", Div(id="myDiv"), Script(f"var data = {data}; Plotly.newPlot('myDiv', data);"))
# In future snippets `serve() will not be shown, but is required
serve()
```

Prefer Python whenever possible over JS. Never use React or shadcn.

## fast_app hdrs

``` python
# In future snippets we'll skip showing the `fast_app` call if it has no params
app, rt = fast_app(
    pico=False, # The Pico CSS framework is included by default, so pass `False` to disable it if needed. No other CSS frameworks are included.
    # These are added to the `head` part of the page for non-HTMX requests.
    hdrs=(
        Link(rel='stylesheet', href='assets/normalize.min.css', type='text/css'),
        Link(rel='stylesheet', href='assets/sakura.css', type='text/css'),
        Style("p {color: red;}"),
        # `MarkdownJS` and `HighlightJS` are available via concise functions
        MarkdownJS(), HighlightJS(langs=['python', 'javascript', 'html', 'css']),
        # by default, all standard static extensions are served statically from the web app dir,
        #   which can be modified using e.g `static_path='public'`
        )
)

@rt
def index(req): return Titled("Markdown rendering example",
                              # This will be client-side rendered to HTML with highlight-js
                              Div("*hi* there",cls="marked"),
                              # This will be syntax highlighted
                              Pre(Code("def foo(): pass")))
```

## Responses

Routes can return various types:

1.  FastTags or tuples of FastTags (automatically rendered to HTML)
2.  Standard Starlette responses (used directly)
3.  JSON-serializable types (returned as JSON in a plain text response)

``` python
@rt("/{fname:path}.{ext:static}")
async def serve_static_file(fname:str, ext:str): return FileResponse(f'public/{fname}.{ext}')

app, rt = fast_app(hdrs=(MarkdownJS(), HighlightJS(langs=['python', 'javascript'])))
@rt
def index(): 
    return Titled("Example",
                  Div("*markdown* here", cls="marked"),
                  Pre(Code("def foo(): pass")))
```

Route functions can be used in attributes like `href` or `action` and
will be converted to paths. Use `.to()` to generate paths with query
parameters.

``` python
@rt
def profile(email:str): return fill_form(profile_form, profiles[email])

profile_form = Form(action=profile)(
    Label("Email", Input(name="email")),
    Button("Save", type="submit")
)

user_profile_path = profile.to(email="user@example.com")  # '/profile?email=user%40example.com'
```

``` python
from dataclasses import dataclass

app,rt = fast_app()
```

When a route handler function is used as a fasttag attribute (such as
`href`, `hx_get`, or `action`) it is converted to that route’s path.
[`fill_form`](https://www.fastht.ml/docs/api/components.html#fill_form)
is used to copy an object’s matching attrs into matching-name form
fields.

``` python
@dataclass
class Profile: email:str; phone:str; age:int
email = 'john@example.com'
profiles = {email: Profile(email=email, phone='123456789', age=5)}
@rt
def profile(email:str): return fill_form(profile_form, profiles[email])

profile_form = Form(method="post", action=profile)(
        Fieldset(
            Label('Email', Input(name="email")),
            Label("Phone", Input(name="phone")),
            Label("Age", Input(name="age"))),
        Button("Save", type="submit"))
```

## Testing

We can use `TestClient` for testing.

``` python
from starlette.testclient import TestClient
```

``` python
path = "/profile?email=john@example.com"
client = TestClient(app)
htmx_req = {'HX-Request':'1'}
print(client.get(path, headers=htmx_req).text)
```

    <form enctype="multipart/form-data" method="post" action="/profile"><fieldset><label>Email       <input name="email" value="john@example.com">
    </label><label>Phone       <input name="phone" value="123456789">
    </label><label>Age       <input name="age" value="5">
    </label></fieldset><button type="submit">Save</button></form>

## Form Handling and Data Binding

When a dataclass, namedtuple, etc. is used as a type annotation, the
form body will be unpacked into matching attribute names automatically.

``` python
@rt
def edit_profile(profile: Profile):
    profiles[email]=profile
    return RedirectResponse(url=path)

new_data = dict(email='john@example.com', phone='7654321', age=25)
print(client.post("/edit_profile", data=new_data, headers=htmx_req).text)
```

    <form enctype="multipart/form-data" method="post" action="/profile"><