
1.Clone Repository :

  git clone https://github.com/EbinIttira/BlogPost.git
  
  cd BlogPost

2.Create a virtual environment and activate it :

  python -m venv venv
  
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3.Install dependencies :

  pip install -r requirements.txt

4.Apply database migrations :

  python manage.py migrate

5.Run the development server :

  python manage.py runserver
