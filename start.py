import uvicorn


def run():
    uvicorn.run('src.main:app', host='localhost', port=8000)


run()
