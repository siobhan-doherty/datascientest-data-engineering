#!/usr/bin/env bash
# health
curl -i http://127.0.0.1:8000/health

# unauthorised
curl -i http://127.0.0.1:8000/questions?use=MCQ\&subject=Math\&count=5

# poor count
curl -i -H "Authorization: Basic alice:wonderland" \
     "http://127.0.0.1:8000/questions?use=MCQ&subject=Math&count=3"

# fetch 5 math MCQs
curl -i -H "Authorization: Basic alice:wonderland" \
     "http://127.0.0.1:8000/questions?use=MCQ&subject=Math&count=5"

# create forbidden
curl -i -X POST -H "Authorization: Basic bob:builder" \
     -H "Content-Type: application/json" \
     -d '{"question":"Q?","subject":"Math","use":"MCQ","correct":["A"],"answerA":"A","answerB":"B","answerC":"C"}' \
     http://127.0.0.1:8000/questions

# create admin
curl -i -X POST -H "Authorization: Basic admin:4dm1N" \
     -H "Content-Type: application/json" \
     -d '{"question":"What?","subject":"Geo","use":"MCQ","correct":["C"],"answerA":"A","answerB":"B","answerC":"C"}' \
     http://127.0.0.1:8000/questions
