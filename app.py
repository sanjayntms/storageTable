from flask import Flask, render_template, request, redirect, url_for
from azure_storage_service import create_user_profile, get_user_profile, query_profiles_by_name, get_all_profiles

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    all_profiles = get_all_profiles()
    return render_template('profile.html', all_profiles=all_profiles)

@app.route('/create_profile', methods=['POST'])
def create_profile():
    name = request.form.get('name')
    website = request.form.get('website')
    twitter = request.form.get('twitter')
    bio = request.form.get('bio')

    if name:
        # Sanitize the name to be a valid RowKey (replace spaces, etc.)
        row_key = name.replace(" ", "_").lower()
        create_user_profile(row_key, website=website, twitter=twitter, bio=bio)
        return redirect(url_for('index'))
    else:
        return "Name is required to create a profile."

@app.route('/search_profiles', methods=['GET'])
def search_profiles():
    search_name = request.args.get('name')
    profiles = []
    search_performed = False
    if search_name:
        profiles = query_profiles_by_name(search_name)
        search_performed = True
    return render_template('profile.html', profiles=profiles, search_performed=search_performed)

if __name__ == '__main__':
    app.run(debug=True, port=3000, ssl_context='adhoc', host='0.0.0.0')
