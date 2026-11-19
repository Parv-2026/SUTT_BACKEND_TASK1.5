
# SUTT_BACKEND_TASK1.5

## Web fundamentals — answers for the nine Task 1.5 questions

### 1. What happens when I type a URL and press Enter?

The browser parses the URL to identify the scheme (usually HTTPS), host, and path. It looks up the host's IP address using DNS (possibly from a cache). It establishes a network connection and, for HTTPS, negotiates an encrypted TLS connection. It sends an HTTP request identifying the page it wants. A server processes the request and replies with an HTTP response. The browser parses the HTML and requests additional files such as CSS, images, and JavaScript. It lays out and paints the page, then runs scripts as required. Caching and connection reuse can change some details.

### 2. What are the client and server, and how do they communicate?

The **client** is usually my browser. It makes requests for information or actions. The **server** is a program running elsewhere (or on my own laptop during development) that handles those requests. They communicate by sending HTTP messages across a network. In this project, the browser is the client and Django's development server responds to requests.

### 3. What is HTTP? What's inside a request and response?

HTTP is an application-level protocol for exchanging messages between clients and servers. A **request** has a method (`GET` or `POST`), a target path, headers, and sometimes a body (such as submitted form data). A **response** contains a status code, headers, and possibly a body (such as HTML). For example, requesting `/polls/` produces HTML for the questions list.

### 4. GET versus POST?

`GET` is used to retrieve information and should not change server-side state. `POST` submits data that may cause a change, such as casting a vote. The polls index and detail pages use `GET`, whereas the voting form sends a `POST` to increment the vote count. After a successful vote, Django redirects to a results page to avoid accidental form resubmission on refresh.

### 5. What do 200, 302, 404 and 500 mean?

- **200 OK**: the request succeeded and the server returned the page.
- **302 Found**: a temporary redirect; the browser is told to request another URL.
- **404 Not Found**: the requested resource does not exist or is not accessible at that URL.
- **500 Internal Server Error**: the server encountered an unexpected error while handling the request.

In this app, loading a question normally returns 200, voting successfully leads to a 302 redirect, and requesting an unknown question returns 404.

### 6. What do HTML, CSS, and JavaScript do?

**HTML** defines the page's structure and content (headings, links, forms). **CSS** controls presentation (layout, colors, spacing, typography). **JavaScript** adds browser-side logic and interactions. This polls app uses HTML and CSS; its essential voting behavior works without JavaScript because Django processes the submitted form on the server.

### 7. How does a website remember someone between pages?

HTTP requests are stateless by themselves, so websites typically use **cookies** and **sessions**. A cookie is a small value the browser stores and sends back on later requests. A session allows the server to associate multiple requests with a common session identifier. Django's session middleware can track such state. This tutorial app does not require login, so visitors can vote without being identified; the same visitor can vote repeatedly. Real polls might need additional vote limits and authentication.

### 8. How does a request travel through URLs, views, models and templates in Django?

The browser sends a request, and Django uses `mysite/urls.py`, then `polls/urls.py`, to select the matching **view**. The view can query **models**, which represent database tables, to retrieve questions and choices. It then renders an HTML **template** using that data and returns an HTTP response. For voting, the view instead validates the POST form, updates a Choice row, and redirects to the results URL.

### 9. Why does the vote form use `{% csrf_token %}`?

CSRF stands for **Cross-Site Request Forgery**. An attacker might try to trick a browser into submitting an unwanted state-changing request to another site. Django's CSRF middleware checks a token submitted with protected forms to help ensure the POST came through an authorized form flow. `{% csrf_token %}` inserts the necessary hidden field into the voting form. It helps protect POST requests, but it is not a replacement for user authentication or other authorization checks.

