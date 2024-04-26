from flask import Flask, render_template, request, redirect, url_for
from models.species import Species
from models.taxon import Taxon
import db

app = Flask(__name__)
db.init_app(app)

@app.route('/')
def index():
    conn = db.get_db()
    lst = Species.getList(conn)
    return render_template('index.html', species=lst, title="Voles Database")


@app.route('/species/<id>')
def species(id):
    sp = Species.getById(db.get_db(), id)
    return render_template('species.html', species=sp)


@app.route('/update/species/<id>', methods=['GET', 'POST'])
def update_species(id):
    sp = Species.getById(db.get_db(), id)
    if request.method == 'POST':
        sp.speciesName = request.form['sname']
        sp.genusName = request.form['gname']
        sp.description = request.form['description']
        sp.save(db.get_db())
        return redirect(url_for('species', id=sp.id))
    genera = Taxon.getListByRank(db.get_db(), 'genus')
    return render_template('update_species.html', species=sp, genera=genera)

@app.route('/create/species/', methods=['GET', 'POST'])
def create_species():
    sp = Species('', '', '')
    if request.method == 'POST':
        sp.speciesName = request.form['sname']
        sp.genusName = request.form['gname']
        sp.description = request.form['description']
        sp.save(db.get_db())
        return redirect(url_for('species', id=sp.id))
