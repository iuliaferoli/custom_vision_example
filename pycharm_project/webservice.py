import config
import os
import json

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

coil_ids = ['879832A', '0194131', '88125521', '87724111', '88393911', '8816251', '884045', '87877411', '8796151', '881720B', '0194684', '0194682', '0237872', '875348701', '880829A', '8827381', '8790341', '0231501', '88331011', '87953056', '87829311', '87866957', '02940156', '88307921', '883750', '8826701', '8651981', '882679211', '883887', '88268011', '877597B', '88006257', '8839641', '9122671', '8831271', '8690562', '024487A', '02941411', '0231512', '85575958', '872033211', '873884700', '88124156', '87154799', '01978112', '0233702', '0293181', '88024456', '8830661', '87324811', '8796171', '02932311', '87292960', '87633056', '877820112', '8828082', '88081657', '882941', '0231751', '88123358', '87428856', '8612621peugeot', '8766832', '883997B', '880829B', '883890', '878293562', '87487156', '0197831', '8826821', '882698111', '8827701', '8720902', '8796152', '02643656', '87586412', '02940111', '88148157', '85931812', '879861A', '8823523', '883895', '87705411', '02408811', '0291991', '88141757', '8828092', '883017112', '9122672', '883888', '8833492', '8719861', '8828151', '02246756', '883113112', '8833962', '0180832', '880231B', '02', '02933811', '88270821', '88197414', '863822701', '8815981', '87272723', '84896113', '88307011', '030109', '02575911', '87979556', '02419112', '86753856', '87020156', '88123356', '86519511', '0293412', '9122691', '02941731', '884046', '030409', '8823821', '87154603', '881020561', '882141B', '8826671', '874908700', '880830A', '883050211', '87856799', '872033212', '02472856', '87897156', '04', '05', '0253841', '024787A', '0293382', '88311021', '883997A', '879824A', '0284821', '02502056', '869391151', '029326121', '8815001', '0293481', '87936856', '87856422', '87849112', '87544057', '88331012', '8769181', '88131112', '880231A', '02469456', '0293411', '8833961', '88304511', '0198713', '881258211', '882060A', '87856756', '02760112', '8827081', '0293861', '8835771', '880199B', '02932611', '0194683', '884048', '87721621', '87772723', '88123211', '02849356', '879552B', '88301611', '00', '02941456', '883883', '02593012', '8703882', '8796142', '8651983', '8813062', '883906', '879871A', '883113111', 'ID', '8776051', '8828112', '8651984', '028109111', '018472A', '00785711', '0292821', '881723B', '883955', '86519512', '87543812', '880252A', '8754362', '8813102', '8831261', '8833911', '883882', '026870221', '87543822', '88149298', '87461058', '8787892', '02247056', '0241321', '8833491', '624476700', '88158721', '8763231', '87543811', '02823421', '87912956', '8843851', '87880211', '9121861', '866953111', '881770A', '88335821', '029921', '88261956', '8833241', '9122681', '88131556', '027432', '02500756', '8817551', '029920', '881640C', '8651985', '883834', '01909911', '0293331', '88305511', '8843831', '024272', '87912957', '880252B', '01976056', '87033521', '87891556', '88148156', '884047', '87772912', '880021111', '88123357', '87876256', '06', '8833252', '0198712', '02932812', '02246358', '024787B', '8831201', '8829361', '87668511', '87846456', '881723A', '87829313', '87986456', '9122421', '868975B', '881255111', '882141A', '877820113', '8823561', '0293862', '882917211', '8831112', '8789881', '8829362', '85530911', '875025111', '02931311', '883008211', '02932312', '9122641', '0282711', '01961111']

with open('data/all_images_predictions_19-6.json') as json_file:  
    predictions = json.load(json_file)

with open('data/stats.json') as json_file:  
    stats = json.load(json_file)

html_img_base = '''
    <div style="flex: 40%; margin: 8px; position: relative;">
        <a href="image/{name}" alt="{name}"><img src="{url}" style="max-width: 100%; max-height: 100%;"></a>
            <div
                title="{damage}"
                id="word1"
                class="word"
                    style="
                    border: 3px solid {color};
                    position: absolute;
                    top: {top}%;
                    left: {left}%;
                    width: {width}%;
                    height: {height}%;"
            >
        </div>
        <div
                title="{damage}"
                id="word1"
                    style="
                    position: absolute;
                    top: 5%;
                    left: 2%;
                    width: 10%;
                    height: 10%;
                    font-size: 20px;"
            >{score}
        </div>
    </div>
'''

@app.route("/image/<coil_id>/<camera>")
def image(coil_id,camera):
    title = 'Detail of {coil_id} for camera {camera}'.format(coil_id=coil_id, camera=camera)
    try:
        info = [prediction for prediction in predictions if prediction['coil_id'] == coil_id and prediction['camera_name'] == camera][0]
        coordinates = info['coordinates']
        prediction = info['prediction']
        damage = 1 if prediction == 'damages' else 0
        bordercolor = "red" if damage else "green"
        score = '✔️' if prediction == info['label'] else '❌'
        html = html_img_base.format(
            damage=damage,
            color=bordercolor,
            top=coordinates[1]*100,
            left=coordinates[0]*100,
            width=coordinates[2]*100,
            height=coordinates[3]*100,
            url=info['url'],
            name=info['coil_id'] + '/' + info['camera_name'],
            score=score)
    except:
        return "Image not found"
    return render_template("images_overview.html", title=title, html=html)

@app.route("/coils")
def coils():
    title = 'Overview per coil'
    links = list()

    correctly_classified = [prediction for prediction in predictions if prediction['label'] == prediction['prediction']]
    not_correctly_classified = [prediction for prediction in predictions if prediction['label'] != prediction['prediction']]
    true_positive = [prediction for prediction in correctly_classified if prediction['label'] == 'damages']
    false_positive = [prediction for prediction in not_correctly_classified if prediction['label'] == 'Negative']
    false_negative = [prediction for prediction in not_correctly_classified if prediction['label'] == 'damages']

    links.append('''
        <h2 style="flex:100%; margin: 8px">Classified correctly: {correct} out of {total} ({perc}%)</h2>
    '''.format(correct=len(correctly_classified), total=len(predictions), perc='{0:.2f}'.format(len(correctly_classified)/len(predictions)*100)))
    for coil_id in coil_ids:
        links.append('''
            <h1 style="flex:100%; margin: 8px">Coil id: {title}</h1>
        '''.format(title=coil_id))
        
        for prediction in [prediction for prediction in predictions if coil_id == prediction['coil_id']]:
            coordinates = prediction['coordinates']
            classification = prediction['prediction']
            bordercolor = "red" if classification == "damages" else "green"
            score = '✔️' if classification == prediction['label'] else '❌'
            links.append(html_img_base.format(
                damage=classification,
                color=bordercolor,
                top=coordinates[1]*100,
                left=coordinates[0]*100,
                width=coordinates[2]*100,
                height=coordinates[3]*100,
                url=prediction['url'],
                name=prediction['coil_id'] + '/' + prediction['camera_name'],
                score=score))
    return render_template("images_overview.html", title=title, html="\n".join(links))


@app.route("/errors")
def errors():
    title = 'Classification errors'
    links = list()

    correctly_classified = [prediction for prediction in predictions if prediction['label'] == prediction['prediction']]
    not_correctly_classified = [prediction for prediction in predictions if prediction['label'] != prediction['prediction']]
    false_positive = [prediction for prediction in not_correctly_classified if prediction['label'] == 'Negative']
    false_negative = [prediction for prediction in not_correctly_classified if prediction['label'] == 'damages']
    errors = {'false_positive': false_positive, 'false_negative': false_negative}

    links.append('''
        <h2 style="flex:100%; margin: 8px">Classified correctly: {correct} out of {total} ({perc}%)</h2>
    '''.format(correct=len(correctly_classified), total=len(predictions), perc='{0:.2f}'.format(len(correctly_classified)/len(predictions)*100)))
    for error in ['false_positive', 'false_negative']:
        links.append('''
            <h1 style="flex:100%; margin: 8px">{title}</h1>
        '''.format(title=error))
        
        for prediction in errors[error]:
            coordinates = prediction['coordinates']
            classification = prediction['prediction']
            bordercolor = "red" if classification == "damages" else "green"
            score = '✔️' if classification == prediction['label'] else '❌'
            links.append(html_img_base.format(
                damage=classification,
                color=bordercolor,
                top=coordinates[1]*100,
                left=coordinates[0]*100,
                width=coordinates[2]*100,
                height=coordinates[3]*100,
                url=prediction['url'],
                name=prediction['coil_id'] + '/' + prediction['camera_name'],
                score=score))
    return render_template("images_overview.html", title=title, html="\n".join(links))


@app.route("/cameras")
def cameras():
    title='Overview per camera'
    camera_names = ['A3_West', 'A4_Noord', 'A6_Oost', 'A6_Zuid']

    links = list()
    correctly_classified = len([prediction for prediction in predictions if prediction['label'] == prediction['prediction']])
    links.append('''
        <h2 style="flex:100%; margin: 8px">Classified correctly: {correct} out of {total} ({perc}%)</h2>
    '''.format(correct=correctly_classified, total=len(predictions), perc='{0:.2f}'.format(correctly_classified/len(predictions)*100)))

    for camera in camera_names:
        correct_camera = len([prediction for prediction in predictions if prediction['label'] == prediction['prediction'] if camera == prediction['camera_name']])
        links.append('''
            <h1 style="flex:100%; margin: 8px">Camera name: {title} ({correct}%)</h1>
        '''.format(title=camera, correct='{0:.2f}'.format(correct_camera/len([prediction for prediction in predictions if camera == prediction['camera_name']])*100)))

        
        for prediction in [prediction for prediction in predictions if camera == prediction['camera_name']]:
            coordinates = prediction['coordinates']
            classification = prediction['prediction']
            bordercolor = "red" if classification == "damages" else "green"
            score = '✔️' if classification == prediction['label'] else '❌'
            links.append(html_img_base.format(
                damage=classification,
                color=bordercolor,
                top=coordinates[1]*100,
                left=coordinates[0]*100,
                width=coordinates[2]*100,
                height=coordinates[3]*100,
                url=prediction['url'],
                name=prediction['coil_id'] + '/' + prediction['camera_name'],
                score=score))
    return render_template("images_overview.html", title=title, html="\n".join(links))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@app.route('/statistics')
def statistics():
    html = list()
    html.append('''
    <table style="flex:40%; flex-grow:1">
  <tr>
    <th>Camera</th>
    <th>Precision</th>
    <th>Recall</th>
    <th>Accuracy</th>
    <th>Tp</th>
    <th>Tn</th>
    <th>Fp</th>
    <th>Fn</th>
  </tr>
  ''')
    for camera_name in ['all', 'A3_West', 'A4_Noord', 'A6_Oost', 'A6_Zuid']:
        print(stats[camera_name])
        html.append(
        '''
        <tr>
            <td>{camera_name}</td>
            <td>{precision}</td>
            <td>{recall}</td>
            <td>{accuracy}</td>
            <td>{tp}</td>
            <td>{tn}</td>
            <td>{fp}</td>
            <td>{fn}</td>

        </tr>
    '''.format(camera_name=camera_name, precision=stats[camera_name][0], recall=stats[camera_name][1], accuracy=stats[camera_name][2], tp=stats[camera_name][3], tn=stats[camera_name][4], fp=stats[camera_name][5], fn=stats[camera_name][6]))
    html.append('''</table>''')
    return render_template("images_overview.html", title="Statistics", html="\n".join(html))