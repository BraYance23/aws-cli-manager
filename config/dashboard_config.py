"""
Configuración del dashboard: caching, estado de servicios y
funciones para mutar el estado del dashboard.
"""

dashboard_services = ["ec2", "sg", "kp"]

summary_fallback = {
    "ec2": ("N/A", "N/A"),
    "sg": "N/A",
    "kp": "N/A"
}

dashboard_dirty = {
    "ec2": {
        "needs_update": True,
        "last_summary": None
    },
    "sg": {
        "needs_update": True,
        "last_summary": None,
    },
    "kp": {
        "needs_update": True,
        "last_summary": None
    }
}

def need_update_dashboard(service:str):

    dashboard_dirty[service]["needs_update"] = True

def reset_data_dashboard():

    for service in dashboard_services:
        dashboard_dirty[service]["needs_update"] = True
        dashboard_dirty[service]["last_summary"] = None