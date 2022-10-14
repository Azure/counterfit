import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


from counterfit import Counterfit

scans = []

def setup_routes(app):
    @app.get("/api/v1/attacks")
    def get_attacks():
        attacks = {}
        frameworks = Counterfit.get_frameworks()
        for k, v in frameworks:
            attacks[k] = v["attacks"]
        
        return JSONResponse(content=attacks)

    # curl -X POST -H "Content-Type: application/json" --data '{"target": "creditfraud", "attacks": {"attack_1": {"attack_name": "hop_skip_jump"}, "attack_2": {"attack_name": "hop_skip_jump"}}}' https://localhost:8000
    @app.post("/api/v1/scan")
    def execute_scan(scan_request: Request):
        #data = scan_request.json()
        #results = Counterfit.attack_from_config(data)
        return JSONResponse(content="{'test': 'scan'}")

if __name__ == "__main__":
    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_routes(app)
    uvicorn.run(app, host="127.0.0.1", port=8000)



