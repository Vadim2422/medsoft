import uvicorn


def run():
    uvicorn.run('main:app', host='localhost', port=8000)
run()