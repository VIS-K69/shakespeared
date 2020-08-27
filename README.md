
1. Download Python 3.8 (from https://www.python.org/downloads/) and install it following the instructions contained in the official
Web site.
	
2. Install the following Python packages using the command "pip install {package_name}":
	- flask
	- connexion
	- pokebase
	- requests
	
3. Unzip the content of the archive shakespeared_server.zip.

4. Open a command prompt window and navigate to the folder where the archive was unzipped. 

5. Start the server using the following command:
	python shakespeared_server.py
	
6. In your browser type the following url (replace {pokemon name} with the name of the pokemon you are looking for):
	http://localhost:5000/pokemon/{pokemon name}
	
	