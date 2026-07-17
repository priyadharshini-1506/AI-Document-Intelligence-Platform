from groq import Groq
import os
import json


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



def extract_information(
        text,
        document_type
):


    prompt = f"""

You are an AI document information extraction system.

Document Type:
{document_type}


Extract important information from the document.

Return ONLY valid JSON.
Do not add explanation.



Rules:


If document is Resume:

Extract:

candidate_name
email
phone
skills
education
projects
experience
certifications



If document is Certificate:

Extract:

candidate_name
organization
course
title
date



If document is Invoice:

Extract:

invoice_number
company
customer
amount
date



Document:

{text}


Return JSON:

"""


    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role":"user",
                "content":prompt
            }

        ],

        temperature=0

    )


    output = response.choices[0].message.content



    try:

        data=json.loads(output)

        return data



    except:


        return {

            "error":
            "JSON parsing failed",

            "raw_output":
            output

        }