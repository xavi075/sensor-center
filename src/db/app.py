"""
Programa que, mitjançant els mètodes get i post, permet consultar i inserir dades en una base
de dades. Per a cada petició, s'especifica com ha de ser el format de la sol·licitud i quin
serà el format de la resposta en cas de que funcioni correctament. En cas contrari, la
resposta sempre tindrà el mateix format:

```json
{
    "success" = False,
    "error" = "descripció del error"
}   
```
"""

from flask import Flask, request, jsonify
from mariaDB import mariaDBConn



app = Flask(__name__)
# connexió a la base de dades
db = mariaDBConn('localhost', 'ferran', '3007', 'integracioSistemes')
db.conecta()

@app.route('/inserirProva', methods = ['POST'])
def inserirProva():
    """
    Endpoint de Flask per inserir dades a la taula provesDoctests.

    Mètode: POST
    Format de dades esperat: JSON

    Exemple de sol·licitud:
    ```
    POST /inserirProva
    {
        "nomProva": "nom_prova",
        "dataHoraProva": "2023-11-16 12:30:00",
        "dadaProva": 42.5
    }
    ```

    Respostes possibles:
    - 200 OK: Dades insertades correctament.   
        ```json
        {
            "success" = True
        }   
        ```
    - 400 Bad Request:
        - Si no es proporciona un JSON en la sol·licitud.
        - Si falta alguna dada necessària en el JSON. S'especifica quina dada falta.
    - 500 Internal Sever Error: 
        - Error al inserir les dades a la base de dades.
        - Error no controlat.
    """
    try: 
        try: 
            dades_json = request.json
        except Exception as e:
            return jsonify({'success': False, 'error': f"No s'ha propocionat un JSON en la sol·licitud."}), 400

        nom = dades_json.get('nomProva')
        dataHora = dades_json.get('dataHoraProva')
        dada = dades_json.get('dadaProva')

        if nom is None:
            return jsonify({'success': False, 'error': f'Camp "nomProva" no especificat en el JSON'}), 400
        elif dataHora is None:
            return jsonify({'error': f'Camp "dataHoraProva" no especificat en el JSON'}), 400
        elif dada is None:
            return jsonify({'success': False, 'error': f'Camp "dadaProva" no especificat en el JSON'}), 400
        
        else:
            db.començaTransaccio()
            try:
                db.insert('provesDoctests', {'nomProva': nom, 'dataHoraProva': dataHora, 'dadaProva': dada})
            except Exception as e:
                db.rollback()
                return jsonify({'success': False, 'error': f'Error al inserir dades: {str(e)}'}), 500
            else:
                db.commit()
                return jsonify({'success': True})
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error no controlat: {str(e)}'}), 500

# ¡¡¡¡ERROR!!!!: QUAN HI HA ALGUN ERROR INSERINT UN USUARI, S'AUGMENTA EL ID
# ex: inserir correctament -> id = 1. inserir incorrectament. inserir correctament -> ¡¡¡¡id = 3!!!!
# afegir que l'usuari passi contrasenya i es guardi hashejada
@app.route('/inserirUsuari', methods = ['POST'])
def inserirUsuari():
    """
    Endpoint de Flask per inserir dades a la taula usuaris.

    Mètode: POST
    Format de dades esperat: JSON

    Exemple de sol·licitud:
    ```
    POST /inserirUsuari
    {
        "email": "usuari@exemple.com",
        "nomUsuari": "nom_usuari",
        "contrasenya": "pwd"
    }
    ```

    Respostes possibles:
    - 200 OK: Dades insertades correctament. Especifica el id que se li ha assignat a l'usuari insertat.
        ```json
        {
            "success" = True,
            "idUsuariInsertat": id
        }   
        ```
    - 400 Bad Request:
        - Si no es proporciona un JSON en la sol·licitud.
        - Si falta alguna dada necessària en el JSON. S'especifica quina dada falta.
    - 500 Internal Sever Error: 
        - Error al inserir les dades a la base de dades.
        - Error no controlat.
    """
    try: 
        try: 
            dades_json = request.json
        except Exception as e:
            return jsonify({'success': False, 'error': f"No s'ha propocionat un JSON en la sol·licitud."}), 400

        email = dades_json.get('email')
        nomUsuari = dades_json.get('nomUsuari')

        if email is None:
            return jsonify({'success': False, 'error': f'Camp "email" no especificat en el JSON'}), 400
        elif nomUsuari is None:
            return jsonify({'error': f'Camp "nomUsuari" no especificat en el JSON'}), 400
        
        else:
            db.començaTransaccio()
            try:
                db.insert('usuaris', {'email': email, 'nomUsuari': nomUsuari})
            except Exception as e:
                db.rollback()
                return jsonify({'success': False, 'error': f'Error al inserir dades: {str(e)}'}), 500
            else:
                db.commit()
                idUsuariInsertat = db.executaQuery("SELECT id FROM usuaris WHERE email = %s", (email, ))[0][0]
                return jsonify({'success': True, 'idUsuariInsertat': idUsuariInsertat})
    
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error no controlat: {str(e)}'}), 500

@app.route('/inserirDispositiu', methods = ['POST'])
def inserirDispositiu():
    """
    Endpoint de Flask per inserir dades a la taula dispositius.

    Mètode: POST
    Format de dades esperat: JSON

    Exemple de sol·licitud:
    ```
    POST /inserirDispositiu
    {
        "idUsuariPropietari": 1,
        "nomDispositiu": "Nom del dispositiu"
    }
    ```

    Respostes possibles:
    - 200 OK: Dades insertades correctament. Especifica el id intern que se li ha assignat al dispositiu insertat.
        ```json
        {
            "success" = True,
            "idDispositiuInsertat": id
        }   
        ```
    - 400 Bad Request:
        - Si no es proporciona un JSON en la sol·licitud.
        - Si falta alguna dada necessària en el JSON. S'especifica quina dada falta.
    - 500 Internal Sever Error: 
        - Error al inserir les dades a la base de dades.
        - Error no controlat.
    """

@app.route('/inserirDada', methods = ['POST'])
def inserirDadesDispositiu():
    """
    Endpoint de Flask per inserir dades a la taula dadesDispositius.

    Mètode: POST
    Format de dades esperat: JSON

    Exemple de sol·licitud:
    ```
    POST /inserirDada
    {
        "idDispositiu": 1,
        "dataHora": "2023-11-16 12:30:00",
        "dadaHum": 45.14,
        "dadaTemp": 16.2
    }
    ```

    Respostes possibles:
    - 200 OK: Dades insertades correctament. Especifica el id intern que se li ha assignat a la dada insertada.
        ```json
        {
            "success" = True,
            "idDadaInsertada": id
        }   
        ```
    - 400 Bad Request:
        - Si no es proporciona un JSON en la sol·licitud.
        - Si falta alguna dada necessària en el JSON. S'especifica quina dada falta.
    - 500 Internal Sever Error: 
        - Error al inserir les dades a la base de dades.
        - Error no controlat.
    """

@app.route('/obtenirUsuaris', method = ['GET'])
def obtenirUsuaris():
    """
    Endpoint de Flask per obtenir dades de la taula usuaris. Permet obtenir les dades d'un usuari
    en concret o de tots els usuaris. Cal tenir en compte que mai es poden obtenir les contrasenyes
    de forma directa.

    Mètode: GET
    Paràmetres de la URL:
    - emailUsuari [obligatori]: email de l'usuari del qual es volen obtenir les dades.

    Exemples de sol·licitud
    - Obtenir totes les dades:
      ```
      GET /obtenirUsuaris
      ```
    - Obtenir les dades d'un usuari en concret:
      ```
      GET /obtenirUsuaris?emailUsuari=usuari@exemple.com
      ```

    Respostes possibles:
    - 200 OK: Retorna les dades obtingudes segons els paràmetres proporcionats
        ```json
        {
            "success" = True,
            "dades": 
            [
                {"id": 1, "email": "usuari1@exemple.com", nomUsuari: "nom_usuari1", dataCreacioUsuari: "2023-11-16 12:30:00"},
                {"id": 2, "email": "usuari2@exemple.com", nomUsuari: "nom_usuari2", dataCreacioUsuari: "2023-11-16 12:30:00"},
                ...
            ]
        }
        ```
    - 400 Bad Request: 
        - Si no es proporciona un JSON en la sol·licitud.
        - Si falta alguna dada necessària en el JSON.
    - 500 Internal Server Error: 
        - Error al consultar la base de dades.
        - Error no controlat.
    """

@app.route('/verificaLogIn', method = ['GET'])
def verificaLogIn():
    """
    Endpoint de Flask per obtenir si les credencials de log in es corresponen a les credencials
    de la base de dades. 

    Mètode: GET
    Paràmetres de la URL:
    - emailUsuari [obligatori]: email indicat per l'usuari que es vol loguejar.
    - contrasenya [obligatori]: contrasenya indicada per l'usuari que es vol loguejar. Aquesta ha de ser sense hash,
        ja que el procés de controlar els hash de la contrasenya es fa en el back-end.

    Exemples de sol·licitud
      ```
      GET /verificaLogIn?emailUsuari=usuari@exemple.com&contrasenya=pwd
      ```

    Respostes possibles:
    - 200 OK: Indica si s'ha trobat una coincidència de les credencials a la base de dades
        ```json
        {
            "success" = True,
            "credencialsTrobades": True / False
        }
        ```
    - 400 Bad Request: Si es proporcionen paràmetres incorrectes.
        - Si no es proporciona un JSON en la sol·licitud.
        - Si falta alguna dada necessària en el JSON. S'especifica quina dada falta.
    - 500 Internal Server Error: 
        - Error al consultar la base de dades.
        - Error no controlat.
    """
        
@app.route('obtenirDispositius', method = ['GET'])
def obtenirDispositius():
    """
    Endpoint de Flask per obtenir dades de la taula dispositius.

    Mètode: GET
    Paràmetres de la URL:
    - emailUsuari [opcional]: email de l'usuari del qual es volen obtenir les dades dels seus dispositius assignats.
    - nomDispositiu [opcional]: nom del dispositiu del qual es volen obtenir les dades. Sempre ha d'anar acompanyat
        d'un email d'un usuari, ja que diferents usuaris volen tenir dispositius amb el mateix nom.
    - idDispositiu [opcional]: id del dispositiu del qual es poden obtenir les dades.
    
    Exemples de sol·licitud
    - Obtenir totes les dades:
      ```
      GET /obtenirDispositius
      ```
    - Obtenir les dades dels dispositius d'un usuari en concret:
      ```
      GET /obtenirDispositius?emailUsuari=usuari@exemple.com
      ```
    - Obtenir les dades d'un dispositiu en concret a partid del id:
      ```
      GET /obtenirDispositius?idDispositiu=id
      ```
    - Obtenir les dades d'un dispositiu en concret a partir del nom d'usuari i el nom de dispositiu:
      ```
      GET /obtenirDispositius?emailUsuari=usuari@exemple.com&nomDispositiu=nom_dispositiu
      ```
    
    Respostes possibles:
    - 200 OK: Retorna les dades obtingudes segons els paràmetres proporcionats
        ```json
        {
            "success" = True,
            "dades": 
            [
                {"id": 1, "idUsuariPropietari": 1, nomDispositiu: "nom_Dispositiu1"},
                {"id": 2, "idUsuariPropietari": 1, nomDispositiu: "nom_Dispositiu2"},
                ...
            ]
        }
        ```
    - 400 Bad Request: 
        - Si no es proporciona un JSON en la sol·licitud.
        - Si falta alguna dada necessària en el JSON.
    - 500 Internal Server Error: 
        - Error al consultar la base de dades.
        - Error no controlat.
    """

@app.route('obtenirDadesDispositius', method = ['GET'])
def obtenirDadesDispositius():
    """
    Endpoint de Flask per obtenir dades de la taula dadesDispositius.

    Mètode: GET
    Paràmetres de la URL:
    - emailUsuari [opcional]: email de l'usuari del qual es volen obtenir les dades dels seus dispositius assignats.
    - idDispositiu [opcional]: id del dispositiu del qual es volen obtenir les dades.
    - dataInici [opcional]: data a partir de la qual es volen obtenir dades.
    - dataFi [opcional]: data fins a la qual es volen obtenir dades.
    
    Exemples de sol·licitud
    - Obtenir totes les dades:
      ```
      GET /obtenirDadesDispositius
      ```
    - Obtenir totes les dades d'un usuari:
      ```
      GET /obtenirDadesDispositius?emailUsuari=usuari@exemple.com
      ```
    - Obtenir totes les dades d'un dispositiu a partir del id:
      ```
      GET /obtenirDadesDispositius?idDispositiu=id
      ```
    - Obtenir totes les dades d'un usuari indicant data inici i data fi
      ```
      GET /obtenirDadesDispositius?emailUsuari=usuari@exemple.com&dataInici=2023-11-16 00:01:00&dataFi=31-12-2023 23:59:00
      ```
    - Obtenir totes les dades d'un dispositiu indicant data inici i data fi
      ```
      GET /obtenirDadesDispositius?idDispositiu=id&dataInici=01-01-2023 00:01:00&dataFi=31-12-2023 23:59:00
      ```

    Respostes possibles:
    - 200 OK: Retorna les dades obtingudes segons els paràmetres proporcionats
        ```json
        {
            "success" = True,
            "dades": 
            [
                {"idDispositiu": 1, "dataHora": "2023-11-16 12:30:00", dadaHum: 45.12, dataTemp: 13.7},
                {"idDispositiu": 1, "dataHora": "2023-11-16 12:31:00", dadaHum: 15, dadaTemp: 14},
                {"idDispositiu": 2, "dataHora": "2023-11-16 12:31:00", dadaHum: 7.9, dadaTemp: 2},
                ...
            ]
        }
        ```
    - 400 Bad Request: 
        - Si no es proporciona un JSON en la sol·licitud.
        - Si falta alguna dada necessària en el JSON.
    - 500 Internal Server Error: 
        - Error al consultar la base de dades.
        - Error no controlat.
    """

@app.route('obtenirUltimaDadaDispositiu', method = ['GET'])
def obtenirUltimaDadaDispositiu():
    """
    Endpoint de Flask per obtenir les últimes dades de la taula dadesDispositius.

    Mètode: GET
    Paràmetres de la URL:
    - emailUsuari [opcional]: email de l'usuari del qual es vol obtenir les dades dels seus dispositius assignats.
    - idDispositiu [opcional]: id del dispositiu del qual es vol obtenir la dada.

    - Obtenir la última dada de tots els dispositius d'un usuari:
      ```
      GET /obtenirUltimaDadaDispositiu?emailUsuari=usuari@exemple.com
      ```
    - Obtenir la última dada d'un dispositiu en concret:
      ```
      GET /obtenirUltimaDadaDispositiu?idDispositiu=id
      ```

     Respostes possibles:
    - 200 OK: Retorna les dades obtingudes segons els paràmetres proporcionats
        ```json
        {
            "success" = True,
            "dades": 
            [
                {"idDispositiu": 1, "dataHora": "2023-11-16 12:31:00", dadaHum: 15, dadaTemp: 14},
                {"idDispositiu": 2, "dataHora": "2023-11-16 12:31:00", dadaHum: 7.9, dadaTemp: 2},
                ...
            ]
        }
        ```
    - 400 Bad Request: 
        - Si no es proporciona un JSON en la sol·licitud.
        - Si falta alguna dada necessària en el JSON.
    - 500 Internal Server Error: 
        - Error al consultar la base de dades.
        - Error no controlat.
    """

if __name__ == '__main__':
    app.run(debug=True)