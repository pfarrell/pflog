# Pflog
## A Foto Blog generator

Pflog (will build on the simple concept of using email as an input interface for a system.
Yes, I know this idea for this application is like "beating a dead horse".  That's part of
its name.

The basic idea is that pflog will exist in two parts

An agent that will:
1. monitor an email address for new messages
1. an email is parsed to extract 
  * video, photo, documents, any MIME type
  * information from the sender, subject and message body
1. information can be stored in some datastore (say SQLite or even git)

A classic website to display the uploaded info
