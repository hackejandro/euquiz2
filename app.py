import os
import logging
import random
from flask import Flask, render_template, request, session, redirect, url_for, flash

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

# EU organization data
EU_DATA = [
    {"acronym": "EU", "full_name": "European Union"},
    {"acronym": "EC", "full_name": "European Commission"},
    {"acronym": "EP", "full_name": "European Parliament"},
    {"acronym": "EIB", "full_name": "European Investment Bank"},
    {"acronym": "EMA", "full_name": "European Medicines Agency"},
    {"acronym": "EFSA", "full_name": "European Food Safety Authority"},
    {"acronym": "ECDC", "full_name": "European Centre for Disease Prevention and Control"},
    {"acronym": "EMSA", "full_name": "European Maritime Safety Agency"},
    {"acronym": "EEA", "full_name": "European Environment Agency"},
    {"acronym": "EFCA", "full_name": "European Fisheries Control Agency"},
    {"acronym": "EMCDDA", "full_name": "European Monitoring Centre for Drugs and Drug Addiction"},
    {"acronym": "EASO", "full_name": "European Asylum Support Office"},
    {"acronym": "EIGE", "full_name": "European Institute for Gender Equality"},
    {"acronym": "ECHA", "full_name": "European Chemicals Agency"},
    {"acronym": "ENISA", "full_name": "European Union Agency for Cybersecurity"},
    {"acronym": "BEREC", "full_name": "Body of European Regulators for Electronic Communications"},
    {"acronym": "ESMA", "full_name": "European Securities and Markets Authority"},
    {"acronym": "EBA", "full_name": "European Banking Authority"},
    {"acronym": "ESA", "full_name": "European Space Agency"},
    {"acronym": "EUIPO", "full_name": "European Union Intellectual Property Office"},
    # Added entries from CSV file
    {"acronym": "CEV", "full_name": "Center for European Volunteeriing"},
    {"acronym": "CSE", "full_name": "Civil Society Europe"},
    {"acronym": "CESES", "full_name": "Confederation of European Senior Expert Services a.i.s.b.l."},
    {"acronym": "EAP-CSF", "full_name": "Eastern Partnership Civil Society Forum"},
    {"acronym": "ECIT", "full_name": "European citizens' rights, involvement and trust"},
    {"acronym": "FCE", "full_name": "European Civic Forum"},
    {"acronym": "TGL", "full_name": "The Good Lobby"},
    {"acronym": "AEA", "full_name": "Agroecology Europe Association"},
    {"acronym": "ECVC", "full_name": "European Coordination Via Campesina"},
    {"acronym": "EfA", "full_name": "Eurogroup for Animals"},
    {"acronym": "HSI Europe", "full_name": "Humane Society International - Europe"},
    {"acronym": "ENAR", "full_name": "European Network Against Racism"},
    {"acronym": "ERGO Network", "full_name": "European Roma Grassroots Organisations Network"},
    {"acronym": "CEC", "full_name": "CEC European Managers"},
    {"acronym": "UNITEE", "full_name": "New European Business Confederation"},
    {"acronym": "UECNA", "full_name": "Union Européenne Contre les Nuisances des Avions"},
    {"acronym": "CEACSO", "full_name": "Centre for the Advancement of Civil Society Organisations"},
    {"acronym": "ECNL", "full_name": "European Center for Non for profit law"},
    {"acronym": "CEDAG", "full_name": "European Council for Non-Profit Organisations"},
    {"acronym": "AEW", "full_name": "AgoraEnergieWende"},
    {"acronym": "Birdlife Europe", "full_name": "Birdlife International Europe and Central Asia"},
    {"acronym": "C40", "full_name": "C40 Cities"},
    {"acronym": "CMW", "full_name": "Carbon Market Watch"},
    {"acronym": "CCLE", "full_name": "Citizen' Climate Lobby Europe"},
    {"acronym": "CAN Europe", "full_name": "Climate Action Network Europe"},
    {"acronym": "CA", "full_name": "Climate Alliance"},
    {"acronym": "CI Europe", "full_name": "Conservation International Europe"},
    {"acronym": "CME", "full_name": "Covenant of Mayors Europe"},
    {"acronym": "ECOS", "full_name": "Environmental Coalition on Standards"},
    {"acronym": "EJF", "full_name": "Environmental Justice Foundation"},
    {"acronym": "EBCD", "full_name": "European Bureau for Conservation and Development"},
    {"acronym": "ECF", "full_name": "European Climate Foundation"},
    {"acronym": "ECN", "full_name": "European Compost Network"},
    {"acronym": "ECF", "full_name": "European Cyclists' Federation"},
    {"acronym": "EEB", "full_name": "European Environmental Bureau"},
    {"acronym": "EFCF", "full_name": "European Federation of City Farms"},
    {"acronym": "EGC", "full_name": "European Green Cities"},
    {"acronym": "ELSA", "full_name": "European Land and Soil Alliance"},
    {"acronym": "ESTELA", "full_name": "European Solar Thermal Electricity Association"},
    {"acronym": "ESCP", "full_name": "European Sustainable Cities Platform"},
    {"acronym": "XR", "full_name": "Extinction Rebellion"},
    {"acronym": "FFF", "full_name": "Fridays for Future"},
    {"acronym": "NF", "full_name": "Friends of Nature"},
    {"acronym": "FoE Europe", "full_name": "Friends of the Earth Europe"},
    {"acronym": "GEN", "full_name": "Global Ecovillage Network"},
    {"acronym": "GEN Europe", "full_name": "Global Ecovillage Network Europe"},
    {"acronym": "HEAL", "full_name": "Health and Environment Alliance"},
    {"acronym": "ICLEI", "full_name": "Local Governments for Sustainability"},
    {"acronym": "NCI", "full_name": "New Climate Institute"},
    {"acronym": "OCP", "full_name": "Ocean & Climate Platform"},
    {"acronym": "OZL", "full_name": "Oceano Azul Foundation"},
    {"acronym": "PN", "full_name": "Permaculture Network"},
    {"acronym": "PAN Europe", "full_name": "Pesticide Action Network Europe"},
    {"acronym": "PSF", "full_name": "Plastic Soup Foundation"},
    {"acronym": "PIK Potsdam", "full_name": "Potsdam Institute for Climate Impact Research"},
    {"acronym": "POW Europe", "full_name": "Protect Our Winters Europe"},
    {"acronym": "SDG Watch", "full_name": "SDG watch Europe"},
    {"acronym": "SAR", "full_name": "Seas At Risk"},
    {"acronym": "SEI", "full_name": "Stockholm Environment Institute"},
    {"acronym": "SRC", "full_name": "Stockholm Resilience Center"},
    {"acronym": "Surfrider", "full_name": "Surfrider Foundation Europe"},
    {"acronym": "E3G", "full_name": "Third Generation Environmentalism"},
    {"acronym": "T&E", "full_name": "Transport and Environment"},
    {"acronym": "WCMC Europe", "full_name": "WCMC Europe"},
    {"acronym": "WWF EPO", "full_name": "World Wide Fund For Nature - European Policy Office"},
    {"acronym": "WI", "full_name": "Wuppertal Institute"},
    {"acronym": "ZWE", "full_name": "Zero Waste Europe"},
    {"acronym": "BEUC", "full_name": "Bureau Europeen des Unions des consommateurs / The European Consumer Organisation"},
    {"acronym": "CAE", "full_name": "Culture Action Europe"},
    {"acronym": "EJN", "full_name": "Europe Jazz Network"},
    {"acronym": "AEC", "full_name": "European Association of Conservatoires"},
    {"acronym": "ECC", "full_name": "European Centre for Culture"},
    {"acronym": "European Choral Association", "full_name": "European Choral Association - Europa Cantat"},
    {"acronym": "ECHO", "full_name": "European Concert Hall Organisation"},
    {"acronym": "CEATL", "full_name": "European Council of Associations of Literary Translators"},
    {"acronym": "ECHN", "full_name": "European Creative Hubs Network"},
    {"acronym": "ECF", "full_name": "European Cultural Foundation"},
    {"acronym": "EDN", "full_name": "European Dancehouse Network"},
    {"acronym": "REMA", "full_name": "European Early Music Network"},
    {"acronym": "EFHA", "full_name": "European Fashion Heritage Association"},
    {"acronym": "EFNYO", "full_name": "European Federation of National Youth Orchestras"},
    {"acronym": "EFA-AEF", "full_name": "European Festival Association"},
    {"acronym": "EFAD", "full_name": "European Film Agencies"},
    {"acronym": "EFN", "full_name": "European Folk Network"},
    {"acronym": "EuFoA", "full_name": "European Friends of Armenia"},
    {"acronym": "GESAC", "full_name": "European Grouping of Societies of Authors and Composers"},
    {"acronym": "ELIA", "full_name": "European League of Institutes of the Arts"},
    {"acronym": "EMC", "full_name": "European Music Council"},
    {"acronym": "AMATEO", "full_name": "European Network for Active Participation in Cultural Activities"},
    {"acronym": "RESEO", "full_name": "European Network for Opera and Dance Education"},
    {"acronym": "ENCC", "full_name": "European Network of Cultural Centres"},
    {"acronym": "ACCR", "full_name": "European Network of Cultural Centres-Historic Monuments"},
    {"acronym": "ERC", "full_name": "European Region of Culture"},
    {"acronym": "ETC", "full_name": "European Theatre Convention"},
    {"acronym": "EEOFE", "full_name": "Eyes & Ears Europe – Association for the Design, Promotion and Marketing of Audiovisual Media"},
    {"acronym": "FEST Network", "full_name": "Federation for European Storytelling"},
    {"acronym": "IAA Europe", "full_name": "International Association of Art (IAA) Europe"},
    {"acronym": "PEARLE*", "full_name": "Live Performance Europe (Performing Arts Employers Association League Europe)"},
    {"acronym": "NEMO", "full_name": "Network of European Museum Organisations"},
    {"acronym": "RCE", "full_name": "Relais Culture Europe"},
    {"acronym": "ECV", "full_name": "European Confederation of Veterans"},
    {"acronym": "EUROMIL", "full_name": "European Organisation of Military Associations and Trade Unions"},
    {"acronym": "DI", "full_name": "Democracy International"},
    {"acronym": "DemNext", "full_name": "DemocracyNext"},
    {"acronym": "ALDA", "full_name": "European Association for Local Democracy"},
    {"acronym": "ECAS", "full_name": "European Citizen Action Service"},
    {"acronym": "EHF", "full_name": "European Humanist Federation"},
    {"acronym": "EPD", "full_name": "European Partnership for Democracy"},
    {"acronym": "FIDE", "full_name": "Federation for Innovation in Democracy - Europe"},
    {"acronym": "FoE", "full_name": "Friends of Europe"},
    {"acronym": "TI Europe", "full_name": "Transparency International Europe"},
    {"acronym": "WVI", "full_name": "World vision"},
    {"acronym": "EDRi", "full_name": "European Digital Rights"},
    {"acronym": "AE", "full_name": "Autism-Europe"},
    {"acronym": "BIFEC", "full_name": "Brain Injured and Families - European Confederation"},
    {"acronym": "CP-ECA", "full_name": "Cerebral Palsy - European Communities Association"},
    {"acronym": "EURO-CIU", "full_name": "European Association of Cochlear Implant Users"},
    {"acronym": "EASPD", "full_name": "European Association of Service Providers for Personns with Disabiliities"},
    {"acronym": "EBU", "full_name": "European Blind Union"},
    {"acronym": "EUCAP", "full_name": "European Council of Autistic People"},
    {"acronym": "EDU", "full_name": "European Deafblind Union"},
    {"acronym": "EDF", "full_name": "European Disability Forum"},
    {"acronym": "EDSA", "full_name": "European Down Syndrom Association"},
    {"acronym": "EDA", "full_name": "European Dyslexia Association"},
    {"acronym": "EFHOH", "full_name": "European Federation of Hard of Hearing"},
    {"acronym": "ENUSP", "full_name": "European Network of (ex)users and survivors of psychiatry (ENUSP)"},
    {"acronym": "ENIL", "full_name": "European Network on Independent Living"},
    {"acronym": "EUD", "full_name": "European Union of the Deaf"},
    {"acronym": "DEAL", "full_name": "Donut Economics Action Lab"},
    {"acronym": "All Digital", "full_name": "All Digital"},
    {"acronym": "ATEE", "full_name": "Association for Teacher Education in Europe"},
    {"acronym": "CIFE", "full_name": "Centre international de formation européenne"},
    {"acronym": "DARE", "full_name": "Democracy and Human Rights Education in Europe"},
    {"acronym": "Diesis Network", "full_name": "Diesis Network"},
    {"acronym": "EMDR Europe", "full_name": "EMDR Europe"},
    {"acronym": "EAN", "full_name": "European Apprentices Network"},
    {"acronym": "Euroclio", "full_name": "European Assocation of History Educators"},
    {"acronym": "EAIE", "full_name": "European Association for International Education"},
    {"acronym": "EAEA", "full_name": "European Association for the Education of Adults"},
    {"acronym": "AEDE", "full_name": "European Association of Education"}
]

def prepare_quiz_questions(num_questions=15):
    """Prepare quiz questions from the data"""
    # If we have fewer items than requested questions, use all available
    num_questions = min(num_questions, len(EU_DATA))
    
    # Randomly select questions
    selected_questions = random.sample(EU_DATA, num_questions)
    quiz_questions = []
    
    for item in selected_questions:
        quiz_questions.append({
            'acronym': item['acronym'],
            'correct': item['full_name']
        })
    
    return quiz_questions

@app.route('/')
def index():
    """Render the welcome page"""
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_quiz():
    """Start the quiz"""
    # Prepare quiz questions
    quiz_questions = prepare_quiz_questions()
    
    # Store quiz data in session
    session['quiz_questions'] = quiz_questions
    session['current_question'] = 0
    session['score'] = 0
    session['user_answers'] = []
    
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    """Render the quiz page"""
    if 'quiz_questions' not in session:
        flash('Please start the quiz first', 'warning')
        return redirect(url_for('index'))
    
    current_q = session.get('current_question', 0)
    total_q = len(session['quiz_questions'])
    
    if current_q >= total_q:
        return redirect(url_for('results'))
    
    question = session['quiz_questions'][current_q]
    
    return render_template('quiz.html', 
                           question=question, 
                           question_number=current_q + 1, 
                           total_questions=total_q)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Process the submitted answer"""
    if 'quiz_questions' not in session:
        flash('No quiz in progress', 'danger')
        return redirect(url_for('index'))
    
    answer = request.form.get('answer', '').strip()
    
    current_q = session.get('current_question', 0)
    total_q = len(session['quiz_questions'])
    
    if current_q >= total_q:
        return redirect(url_for('results'))
    
    question = session['quiz_questions'][current_q]
    correct = question['correct']
    is_correct = answer.lower() == correct.lower()
    
    # Store user's answer for results page
    session['user_answers'].append({
        'acronym': question['acronym'],
        'user_answer': answer,
        'correct_answer': correct,
        'is_correct': is_correct
    })
    
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    
    # Move to the next question
    session['current_question'] = current_q + 1
    
    if current_q + 1 >= total_q:
        return redirect(url_for('results'))
    else:
        return redirect(url_for('quiz'))

@app.route('/results')
def results():
    """Show the quiz results"""
    if 'quiz_questions' not in session or 'score' not in session:
        flash('No quiz results available', 'danger')
        return redirect(url_for('index'))
    
    score = session.get('score', 0)
    total = len(session['quiz_questions'])
    user_answers = session.get('user_answers', [])
    
    # Get only incorrect answers for display
    incorrect_answers = [ans for ans in user_answers if not ans['is_correct']]
    
    return render_template('results.html', 
                           score=score, 
                           total=total, 
                           incorrect_answers=incorrect_answers)

@app.route('/reset', methods=['POST'])
def reset_quiz():
    """Reset the quiz"""
    if 'quiz_questions' in session:
        session.pop('quiz_questions')
    if 'current_question' in session:
        session.pop('current_question')
    if 'score' in session:
        session.pop('score')
    if 'user_answers' in session:
        session.pop('user_answers')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
