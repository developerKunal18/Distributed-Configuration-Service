import os,time
from threading import Lock
from flask import Flask,jsonify,request

app=Flask(__name__)
DEFAULT_ENV=os.getenv("APP_ENV","development")
_lock=Lock()
_configs={}
_history={}

def validate(p):
    if not isinstance(p,dict): return None,"invalid_json"
    env=p.get("environment",DEFAULT_ENV); cfg=p.get("config")
    if not isinstance(env,str) or not env.strip(): return None,"environment_required"
    if not isinstance(cfg,dict): return None,"config_object_required"
    return {"environment":env,"config":cfg},None

@app.get("/health")
def health(): return jsonify({"status":"ok"})

@app.get("/api/config/<service>")
def get_config(service):
    env=request.args.get("environment",DEFAULT_ENV)
    with _lock:
        record=_configs.get(service,{}).get(env)
        if not record: return jsonify({"error":"configuration_not_found","service":service,"environment":env}),404
        return jsonify({"service":service,"environment":env,**record})

@app.put("/api/config/<service>")
def update_config(service):
    payload,error=validate(request.get_json(silent=True))
    if error: return jsonify({"error":error}),400
    env,cfg=payload["environment"],payload["config"]
    with _lock:
        service_cfg=_configs.setdefault(service,{})
        previous=service_cfg.get(env)
        version=previous["version"]+1 if previous else 1
        record={"version":version,"config":cfg,"updated_at":int(time.time())}
        service_cfg[env]=record
        _history.setdefault(service,{}).setdefault(env,[]).append(record.copy())
    return jsonify({"service":service,"environment":env,**record}),200 if previous else 201

@app.get("/api/config/<service>/history")
def history(service):
    env=request.args.get("environment",DEFAULT_ENV)
    with _lock:
        versions=_history.get(service,{}).get(env,[])
        return jsonify({"service":service,"environment":env,"versions":versions,"count":len(versions)})

@app.errorhandler(404)
def not_found(_): return jsonify({"error":"resource_not_found"}),404

if __name__=="__main__": app.run(host="0.0.0.0",port=5000,debug=True)
