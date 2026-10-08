# deployment checklist



- [x] `/health/` returns HTTP 200 and `OK`.
- [x] `/ready/` returns HTTP 200 and `OK`; the database query succeeds.
- [x] HTTPS works and HTTP login requests redirect to HTTPS.
- [x] Static CSS loads successfully from its hashed URL.
- [x] Registration, login, dashboard, and logout work.
- [x] Applications can be created, viewed, edited, and deleted.
- [x] Company search and status filtering work.
- [x] Other users cannot list, view, edit, or delete another user's application.
      Unauthorized detail/edit/delete requests return 404.
- [x] Session and CSRF cookies are secure; a form POST without a CSRF token
      returns 403. Logged-out visitors are redirected to login.
- [x] The login page looks correct on desktop and a 390 px mobile viewport;
      the mobile page has no horizontal overflow.
- [x] An unknown URL shows a generic 404 without a debug traceback.
