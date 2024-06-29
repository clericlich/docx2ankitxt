from docx2python import docx2python
import json
import os

print("Type Filename:", end=" ")
filename = str(input())
with docx2python(filename + ".docx") as docx_content:
    content = docx_content.body

    imagesPath = "images-" + filename
    try:
        os.mkdir(imagesPath)
    except:
        pass

    for name, image in docx_content.images.items():
        if "tmp" in name:
            name = name.replace("tmp", "png")

        with open(imagesPath+"/"+filename+"-"+name, 'wb') as image_destination:
            image_destination.write(image)


questions = []
for index in range(len(content)):
    for index2 in range(len(content[index])):
            if len(content[index][index2]) == 4:
                questions.append(content[index][index2])


formatted_questions = []
for question in questions:
    #Format Questions
    question_string = ""
    for part in question[1]:
        question_string = question_string + "\n" + part
    question[1] = question_string.replace("\n", "<br>")
    question[1] = question[1].strip()

    answer_string = ""
    for part in question[2]:
         answer_string = answer_string + " " + part
    question[2] = answer_string.replace("\n", "<br>")
    question[2] = question[2].strip()

    rationale_string = ""
    for part in question[3]:
        rationale_string = rationale_string + "\n" + part
    question[3] = rationale_string
    question[3] = rationale_string.replace("----media/",  "<img src=\"" + filename+"-" )
    question[3] = question[3].replace("----", "\">")
    question[3] = question[3].replace("\n", "<br>")
    question[3] = question[3].replace(".tmp", ".png")
    question[3] = question[3].strip()

    final_question = question[1]
    final_answer = question[2] + "<br>" + question[3]

    if question[0] != ["#"] :
        formatted_questions.append( [final_question, final_answer] )


file = open(filename + ".txt", "w", encoding="utf-8")

for question in formatted_questions:
    file.write(question[0] + ";" + question[1] +"\n" )

file.close()