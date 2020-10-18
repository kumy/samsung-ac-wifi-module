{% args req, storage, lookup %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Elements</title>
    <link rel="stylesheet" href="css/chota.min.css" />
    <style>
      body.dark {
        --bg-color: #000;
        --bg-secondary-color: #131316;
        --font-color: #f5f5f5;
        --color-grey: #ccc;
        --color-darkGrey: #777;
      }
    </style>
  </head>

  <body>
    <div id="top" class="container" role="document">
      <header role="banner">
        <h1 class="pull-right" style="margin: 0;">
          <a href="javascript:void(0)" onclick="switchMode(this)">☀️</a>
        </h1>
        <h1>Samsung AC OSS Wifi</h1>
        <div class="clearfix"></div>
        <p>Request path: '{{req.path}}'</p>
      </header>
      <main role="main">

        <section id="Command">
          <a class="button {% if b'\x12' in storage.storage and b'\x01' in storage.storage[b'\x12'] and storage.storage[b'\x12'][b'\x01'] == b'\x0f' %}primary{% endif %}">Power On</a>
          <article id="text__headings">
          </article>
        </section>

        <section id="text">
          <header>
            <h1>Text</h1>
          </header>
          <article id="text__headings">

<table border="1">
{% for c in storage.storage.keys() %}
{% for r in storage.storage[c].keys() %}
<tr><td> {{c}}/{{r}}: {{lookup.get_register_details(r)['name']}} </td><td> {{lookup.get_value_mapping(r, storage.storage[c][r])}} </td></tr>
{% endfor %}
{% endfor %}
</table>
          </article>
        </section>

      </main>
    </div>
  </body>
</html>
