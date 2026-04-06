from fastapi import FastAPI
from src.auth.routers import auth_router
from src.financial.routers import fin_router
from src.analysis.routers import analytic_router
from src.error import register_all_errors
version  = "v1"
    

app = FastAPI(
    title = "Zorvyn API",
    version = version,
    )


register_all_errors(app)

app.include_router(auth_router , prefix = f"/api/{version}/auth" , tags = ["Authentication"])
app.include_router(fin_router , prefix = f"/api/{version}/financial" , tags = ["Financial"])
app.include_router(analytic_router , prefix = f"/api/{version}" , tags = ["Analytics"])