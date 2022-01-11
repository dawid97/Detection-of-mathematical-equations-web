# Drawn equations solver
This project is a web service which allows users to draw on canvas simple mathematical equations using cursor.
![Alt Text](https://i.imgur.com/NdE3X8k.gif)
## Tech Stack
| Name | Website |
| ------ | ------ |
| Angular | https://angular.io/ |
| FastAPI | https://fastapi.tiangolo.com/ |
| Uvicorn | https://www.uvicorn.org/ |
| Keras | https://keras.io/ |
## How to use
- Draw equation on the canvas (left side)
- The result will be shown on the right with detected equation under it (allows you to check whether the detection is correct) 
- There should be a gap between each character (service detects contours)
## How to run
Install the dependencies and start the server. Frontend runs on port 4200 while the Backend runs on port 8000.
### Backend
```sh
cd Backend
pip install -r "requirements.txt"
uvicorn server:app
```
### Frontend
```sh
cd Frontend
npm install
ng serve
```
Visit http://localhost:4200/ to test

## License
MIT


