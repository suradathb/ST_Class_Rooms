# ST_Class_Rooms Step install

clone project to PC Dev 
``` git clone https://github.com/suradathb/ST_Class_Rooms.git ```

## Require PIP install python v3.10
``` https://www.python.org/downloads/release/python-3100/ ```

## Setup to project 
``` cd ST_Class_Rooms/app ```
# Dev install from requirement.txt manual
``` pip install <name> version ```
``` pip3 install <name> version ```

## Or create Docker 
Teknik : Solution Setup Docker Step by Step
#1.For example, your requirements.txt could look like: วิธีการ pip install -r requirements.txt หรือ สร้างไฟล์เองก็ได้
fastapi>=0.68.0,<0.69.0
pydantic>=1.8.0,<2.0.0
uvicorn>=0.15.0,<0.16.0
python-multipart
et-xmlfile
pandas
openpyxl
	
#2. Create the FastAPI Code
• Create an app directory and enter it.
• Create an empty file __init__.py.
• Create a main.py file with:

from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
		
#3. Dockerfile Now in the same project directory create a file Dockerfile with:
# ระบุ Version python
FROM python:3.10
    
# ไฟล์จะถูกสร้างที่ Code ใน docker
WORKDIR /code
    
# สั่ง Copy lbl  ไปที่ code
COPY ./requirements.txt /code/requirements.txt

# ให้ install lbl ตาม requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# ให้ Copy App ไปใส่ที่ code
COPY ./app /code/app
    
# สั่งให้เริ่ม Start Job
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

Note : 
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
		
	
#4. สร้าง Image Docker Teamplate
CMD : ``` docker build -t <ตั่งชื่อว่าอะไรก็ได้> . ```
CMD: ``` docker build -t <ตั่งชื่อว่าอะไรก็ได้>:lastest .   หรือ docker buildx  build . ```
#5. Start the Docker Container
CMD : ``` docker run -d --name mycontainer -p 80:80 <ชื่อตาม Image ที่ต้องการ> ```
	
Teknik : Solution Setup Docker Step by Step END


## Run on part maketrep/app
``` uvicorn main:app --reload ```
OR
``` uvicorn main:app --reload  --port 8001 ```
