# Chatbot_Medibuddy
Create an environment from AnaConda in your specified folder where you want to run your project
    conda create -p venv python==3.10 -y
Active the environment:
    conda activate C:\Users\washi\Langchain\venv
Install all the packages mentioned in the requirements.txt that is placed inside venv folder.
    pip install -r requirements.txt
Install poppler using Conda:
    conda install -c conda-forge poppler
Create your Google API Key from this link : https://aistudio.google.com/app/apikey
Now create a new .env file where you can place your GOOGLE_API_KEY like this:
    GOOGLE_API_KEY="XXXXXXXXXXXX"
Run your .py file that is placed under venv folder using this command(My file name is chatpdf1.py)
    streamlit run chatpdf1.py
You will see a webpage where you can upload your pdfs and click Submit and Process button; Once processing is done, you can ask your questions.

All the questions that AI not able to answer will be saved In unanswered_questions.txt file, so that someone(like admin) can track what are the questions are coming that AI is not able to answer.

All the "not related" queries will also be saved into the knowledge_base.json file where admin can change the answer, And AI will pick the answer from this file next time for the same question.

All the chats are saving in a file name query_history.txt.

And code will show the history for each new session but everything will be saved in query_history file.

