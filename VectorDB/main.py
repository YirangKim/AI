from fastapi import FastAPI
# from upload import upload_router
from upload_v2 import upload_router_v2
#from upload_json import upload_json_router
# from query import query_router
from query_v2 import query_router_v2
from query_v3 import query_router_v3
#from query_lang import query_router_langch

app = FastAPI()

#app.include_router(upload_router, prefix="/api") # VDB저장
app.include_router(upload_router_v2, prefix="/api") # chunck VDB저장
#app.include_router(query_router, prefix="/api") # RAG
app.include_router(query_router_v2, prefix="/api") # RAG
app.include_router(query_router_v3, prefix="/api") # RAG
#app.include_router(query_router_langch, prefix="/api") # query_router_langch
#app.include_router(upload_json_router, prefix="/api") # json

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)