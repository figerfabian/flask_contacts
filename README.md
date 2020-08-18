# flask_contacts necesita de una virtualenv, para ejecutar siga los siguientes pasos:

    python -m venv env
  
    source env\Scripts\activate.bat ---> Windows.
  
    source env/bin/activate ---> Linux.
    
    cd flask_contacts_app
    
    pip install -r requirements.txt
  
  ejecutar flask para obtener las configuraciones de entorno:
  
          export FLASK_APP=App.py
          
          export FLASK_ENV=development
          
          flask run --> Ejecutará el server en modo debug en el puerto 5000 --> 127.0.0.1:5000
