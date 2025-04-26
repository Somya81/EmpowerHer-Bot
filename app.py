from flask import Flask ,render_template,request,redirect,url_for
import json
import csv

app=Flask(__name__)

users_db = {
    "somya@gmail.com": {"password": "somya123", "name": "Somya"}
}

with open('SessionDetails.json') as f:
    session_data= json.load(f)

def load_job_listings():
    job_listings = []
    with open('job_listing_data.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        print("CSV Headers:", csv_reader.fieldnames)  # Debug: Print column headers
        for row in csv_reader:
            print("Row data:", row)  # Debug: Print each row of the CSV
            job_listings.append(row)
    return job_listings


@app.route('/')
def home():
    user_name = request.args.get('user_name')  # User's name passed after login/signup

    if not user_name:
        # Redirect to login if not logged in
        return redirect(url_for('login'))
    job_listings = load_job_listings()

    
    return render_template('index.html',jobs=job_listings,sessions=session_data)


@app.route('/chat',methods=['POST'])
def chat():
    user_input = request.form['user_input'].lower()
    response= "I'm here to help! You can ask about jobs, sessions, or mentoring opportunities."
    job_listings = load_job_listings() 
    filtered_jobs=[]
    
    if "job" in user_input:

        if 'delhi' in user_input:
            filtered_jobs = [job for job in job_listings if 'delhi' in job.get('Location', '').lower()]

            response="Here are some jobs in Delhi: Data Scientist at DataX."
        elif 'data scientist' in user_input:
            filtered_jobs= [job for job in job_listings if 'data scientist' in job['job_title'].lower()]
            response="Yes! Data Scientist role available at DataX in Delhi."
        elif 'bangalore' in user_input:
            filtered_jobs =[job for job in job_listings if 'bangalore' in job['Location'].lower()]
            response= "There’s a Product Manager job at InnoTech in Bangalore."
        elif 'mumbai' in user_input:
            filtered_jobs=[job for job in job_listings if 'mumbai' in job['Location']]
            response="There’s a Software Engineer role at TechCorp in Mumbai."
        elif 'remote' in user_input:
            filtered_jobs = [job for job in job_listings if 'remote' in job['Location'].lower()]
            response="We have remote job opportunities in various roles such as Software Engineer, Data Scientist, etc."
        elif "high salary" in user_input or "high-paying jobs" in user_input:
            filtered_jobs= [job for job in job_listings if float(job['salary'])>=100000]
            response = "We have high-paying jobs like Software Engineer at TechCorp and Data Scientist at DataX."
        else:
            response= "We have several roles like Software Engineer, Data Scientist, and Product Manager."
        if not filtered_jobs:
            filtered_jobs= job_listings

    elif "session" in user_input:
        if "mumbai" in user_input:
            response="User1 has an active session in Mumbai."
        elif "delhi" in user_input:
            response = "User2 has an active session in Delhi."
        elif "online" in user_input:
            response="We have an online session scheduled for this week on 'AI and Machine Learning'."
        else:
            response="We currently have sessions in Mumbai and Delhi."
    
    elif "mentor" in user_input or "mentorship" in user_input:
        response="Mentorship opportunities will be shared soon."
    elif "hello" in user_input or "hi" in user_input:
        response= "Hello! How can I assist you today?"     
    elif "suitable for leadership" in user_input:
        response = "Absolutely! Women have been leading across various sectors. Would you like to explore some inspirational success stories of women leaders?"
    elif "empowerment" in user_input or "women leadership" in user_input:
        response = "Women have been leading across industries! For more insights on women empowerment, you can explore leadership success stories and mentorship opportunities."
    elif "python" in user_input:
        response = "We have several roles requiring Python: Data Scientist, Software Engineer."
    elif "hola" in user_input:  # Spanish greeting
        response = "¡Hola! ¿Cómo puedo ayudarte hoy?"
    elif "bonjour" in user_input:  # French greeting
        response = "Bonjour! Comment puis-je vous aider aujourd'hui?"
    elif "bye" in user_input:
        response="Goodbye! Have a great day!"

    
    return render_template('index.html', jobs=job_listings, filtered_jobs=filtered_jobs,sessions=session_data, response=response)


@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        user_name=request.form['user_name']
        user_email=request.form['user_email']

        users_db[user_email] ={"name":user_name} 

        return redirect(url_for('home',user_name=user_name))                  
    return render_template('signup_form.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user_email=request.form['user_email']
        user_password=request.form['user_password']

        if user_email in users_db :
            user_name= users_db[user_email]["name"]
            return redirect(url_for('home',user_name=user_name))
        else:
            response ="Invalid email or password. Please try again."
            return render_template('login_form.html',response=response)
    return render_template('login_form.html')

if __name__ =='__main__':
    app.run(debug=True)


