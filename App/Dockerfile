FROM continuumio/miniconda3:latest

# remember to expose the port your app'll be exposed on.
EXPOSE 8080

RUN pip install -U pip

RUN pip install argon2_cffi==21.1.0 
RUN pip install geos
RUN pip install numpy==1.21.2
RUN pip install geopandas==0.9.0
RUN pip install streamlit
RUN pip install streamlit-folium
RUN pip install shapely --no-binary shapely

COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

# copy into a directory of its own (so it isn't in the toplevel dir)
COPY . /app
WORKDIR /app

# run it!
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
