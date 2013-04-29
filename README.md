simple-task-queue-channel-api
=============================

A simple implementation of the task queue and channel api from google appengine

If you have a google app engine process that you expect to run for more than 60 seconds than you must add it to the taskqueue (or use a backend) if you want it to run to completion. This is simple implementation of the task queu and channel api. Modify the `SendMessagesHandler` function to contain your long running process and the client will be able to receive messages from the process as it executes through the channel api.
